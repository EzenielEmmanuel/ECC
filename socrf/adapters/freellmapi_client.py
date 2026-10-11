"""SOCRF FreeLLMAPI connection client: inert until explicitly armed.

The transport is injected, so unit tests never touch the network. Constructing
the real HTTP transport is refused unless the caller both arms the client and
opts in with an environment variable, which keeps every default path offline.
Credentials are read from the environment only and are redacted from errors.
"""
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any, Callable
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen
import json
import socket

ADAPTER = "freellmapi"

BASE_URL_ENV_VAR = "SOCRF_FREELLMAPI_BASE_URL"
TOKEN_ENV_VAR = "SOCRF_FREELLMAPI_TOKEN"
ARM_ENV_VAR = "SOCRF_FREELLMAPI_ARMED"
ALLOW_REMOTE_ENV_VAR = "SOCRF_FREELLMAPI_ALLOW_REMOTE"

DEFAULT_BASE_URL = "http://127.0.0.1:3001/v1"
DEFAULT_TIMEOUT_SECONDS = 30.0
MAX_ATTEMPTS = 3
RETRY_BACKOFF_SECONDS = 0.5
MAX_PROMPT_CHARS = 20000
REDACTED = "***redacted***"
RETRYABLE_STATUS = frozenset({408, 425, 429, 500, 502, 503, 504})
LOOPBACK_HOSTS = frozenset({"127.0.0.1", "localhost", "::1", "[::1]"})

Transport = Callable[[Mapping[str, Any]], Mapping[str, Any]]
Sleep = Callable[[float], None]


class FreeLLMAPIConfigError(ValueError):
    pass


class FreeLLMAPIDisabledError(PermissionError):
    pass


class FreeLLMAPIAuthError(RuntimeError):
    pass


class FreeLLMAPIConnectionError(RuntimeError):
    pass


class FreeLLMAPIResponseError(RuntimeError):
    pass


@dataclass(frozen=True)
class ConnectionConfig:
    base_url: str
    token: str
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS
    max_attempts: int = MAX_ATTEMPTS

    def redacted(self) -> dict[str, Any]:
        return {
            "base_url": self.base_url,
            "token": REDACTED,
            "timeout_seconds": self.timeout_seconds,
            "max_attempts": self.max_attempts,
        }


@dataclass(frozen=True)
class Usage:
    model: str
    provider: str
    prompt_tokens: int
    completion_tokens: int

    @property
    def total_tokens(self) -> int:
        return self.prompt_tokens + self.completion_tokens


@dataclass(frozen=True)
class ChatResult:
    content: str
    usage: Usage
    routed_via: str


def redact(text: str, token: str) -> str:
    if not token:
        return text
    return text.replace(token, REDACTED)


def is_armed(environ: Mapping[str, str] | None = None) -> bool:
    env = os_environ(environ)
    return env.get(ARM_ENV_VAR, "").strip().lower() in {"1", "true", "yes", "on"}


def os_environ(environ: Mapping[str, str] | None) -> Mapping[str, str]:
    import os

    return os.environ if environ is None else environ


def load_connection_config(environ: Mapping[str, str] | None = None) -> ConnectionConfig:
    """Read connection settings from the environment; never from the repository."""
    env = os_environ(environ)
    base_url = env.get(BASE_URL_ENV_VAR, DEFAULT_BASE_URL).strip()
    token = env.get(TOKEN_ENV_VAR, "").strip()
    if not token:
        raise FreeLLMAPIConfigError(
            f"{TOKEN_ENV_VAR} is not set; provide the unified gateway token from the credential vault"
        )
    if len(token) > 512:
        raise FreeLLMAPIConfigError("Token exceeds maximum length")
    parsed = urlparse(base_url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise FreeLLMAPIConfigError("Base URL must be an absolute http(s) URL")
    host = parsed.hostname or ""
    remote = host not in LOOPBACK_HOSTS
    if remote and parsed.scheme != "https":
        raise FreeLLMAPIConfigError("A non-loopback base URL must use https")
    if remote and env.get(ALLOW_REMOTE_ENV_VAR, "").strip().lower() not in {"1", "true", "yes", "on"}:
        raise FreeLLMAPIConfigError(
            f"Refusing non-loopback base URL; set {ALLOW_REMOTE_ENV_VAR}=1 to override"
        )
    return ConnectionConfig(base_url=base_url.rstrip("/"), token=token)


def http_transport(config: ConnectionConfig, *, armed: bool) -> Transport:
    """Build the real HTTP transport. Refused unless the caller is armed."""
    if not armed:
        raise FreeLLMAPIDisabledError(
            "Network transport is disabled; set the connection config with an armed client"
        )

    def transport(request: Mapping[str, Any]) -> Mapping[str, Any]:
        url = f"{config.base_url}{request['path']}"
        headers = {
            "Authorization": f"Bearer {config.token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        headers.update(request.get("headers", {}))
        body = request.get("body")
        data = json.dumps(body).encode("utf-8") if body is not None else None
        http_request = Request(url, data=data, headers=headers, method=request.get("method", "GET"))
        try:
            with urlopen(http_request, timeout=config.timeout_seconds) as response:
                return {
                    "status": response.status,
                    "headers": dict(response.headers.items()),
                    "body": response.read().decode("utf-8"),
                }
        except HTTPError as error:
            return {
                "status": error.code,
                "headers": dict(error.headers.items()) if error.headers else {},
                "body": error.read().decode("utf-8", "replace"),
            }
        except (socket.timeout, TimeoutError) as error:
            raise FreeLLMAPIConnectionError(f"Request timed out after {config.timeout_seconds}s") from error
        except URLError as error:
            raise FreeLLMAPIConnectionError(redact(str(error.reason), config.token)) from error

    return transport


class FreeLLMAPIClient:
    """OpenAI-compatible client for a self-hosted FreeLLMAPI gateway."""

    def __init__(
        self,
        config: ConnectionConfig,
        *,
        transport: Transport | None = None,
        sleep: Sleep | None = None,
    ) -> None:
        self.config = config
        self._transport = transport
        self._sleep = sleep or _sleep

    @classmethod
    def from_environment(
        cls, environ: Mapping[str, str] | None = None, *, armed: bool = False
    ) -> "FreeLLMAPIClient":
        config = load_connection_config(environ)
        transport = http_transport(config, armed=armed) if armed else None
        return cls(config, transport=transport)

    def list_models(self, *, available_only: bool = False) -> list[str]:
        path = "/models"
        if available_only:
            path = f"{path}?{urlencode({'available': 'true'})}"
        payload = self._request({"method": "GET", "path": path})
        data = payload.get("data", [])
        return [str(item.get("id", "")) for item in data if item.get("id")]

    def chat_completion(self, *, model: str, prompt: str, max_tokens: int = 1024) -> ChatResult:
        if not prompt.strip():
            raise FreeLLMAPIConfigError("Prompt must be non-empty")
        if len(prompt) > MAX_PROMPT_CHARS:
            raise FreeLLMAPIConfigError("Prompt exceeds maximum length")
        if not 1 <= max_tokens <= 8192:
            raise FreeLLMAPIConfigError("max_tokens outside permitted range")
        payload = self._request(
            {
                "method": "POST",
                "path": "/chat/completions",
                "body": {
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": max_tokens,
                },
            }
        )
        choices = payload.get("choices") or []
        if not choices:
            raise FreeLLMAPIResponseError("Response contained no choices")
        message = choices[0].get("message") or {}
        usage_payload = payload.get("usage") or {}
        return ChatResult(
            content=str(message.get("content", "")),
            usage=Usage(
                model=str(payload.get("model", model)),
                provider=self._last_provider,
                prompt_tokens=int(usage_payload.get("prompt_tokens", 0)),
                completion_tokens=int(usage_payload.get("completion_tokens", 0)),
            ),
            routed_via=self._last_routed_via,
        )

    def _request(self, request: Mapping[str, Any]) -> dict[str, Any]:
        if self._transport is None:
            raise FreeLLMAPIDisabledError(
                "This client has no transport; use FreeLLMAPIClient.from_environment(..., armed=True)"
            )
        last_error: Exception | None = None
        for attempt in range(self.config.max_attempts):
            if attempt:
                self._sleep(RETRY_BACKOFF_SECONDS * (2 ** (attempt - 1)))
            try:
                response = self._transport(request)
            except FreeLLMAPIConnectionError as error:
                last_error = error
                continue
            status = int(response.get("status", 0))
            self._last_routed_via = str(response.get("headers", {}).get("X-Routed-Via", "unknown"))
            self._last_provider = self._last_routed_via.split("/")[0]
            if status == 401 or status == 403:
                raise FreeLLMAPIAuthError(redact("Gateway rejected the token (401/403)", self.config.token))
            if status in RETRYABLE_STATUS:
                last_error = FreeLLMAPIResponseError(f"Retryable gateway status {status}")
                continue
            if status != 200:
                raise FreeLLMAPIResponseError(
                    redact(f"Gateway returned status {status}: {_body_excerpt(response)}", self.config.token)
                )
            return _decode_body(response, self.config.token)
        raise last_error or FreeLLMAPIConnectionError("Request failed without a response")

    _last_routed_via: str = "unknown"
    _last_provider: str = "unknown"


def _decode_body(response: Mapping[str, Any], token: str) -> dict[str, Any]:
    body = response.get("body", "")
    try:
        decoded = json.loads(body)
    except (TypeError, ValueError) as error:
        raise FreeLLMAPIResponseError(redact("Gateway returned a non-JSON body", token)) from error
    if not isinstance(decoded, dict):
        raise FreeLLMAPIResponseError("Gateway returned an unexpected JSON shape")
    return decoded


def _body_excerpt(response: Mapping[str, Any]) -> str:
    body = str(response.get("body", ""))
    return body[:200] + ("..." if len(body) > 200 else "")


def _sleep(seconds: float) -> None:
    import time

    time.sleep(max(0.0, seconds))
