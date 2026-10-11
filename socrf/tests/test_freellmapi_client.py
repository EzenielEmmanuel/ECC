"""Tests for the inert-by-default FreeLLMAPI connection client.

Every test uses a fake transport, so no network call is ever made. The real
HTTP transport is only constructed for an armed client and is not exercised
here.
"""
import unittest

from socrf.adapters.freellmapi_client import (
    ALLOW_REMOTE_ENV_VAR,
    ARM_ENV_VAR,
    BASE_URL_ENV_VAR,
    DEFAULT_BASE_URL,
    DEFAULT_TIMEOUT_SECONDS,
    MAX_ATTEMPTS,
    REDACTED,
    TOKEN_ENV_VAR,
    ConnectionConfig,
    FreeLLMAPIAuthError,
    FreeLLMAPIClient,
    FreeLLMAPIConnectionError,
    FreeLLMAPIConfigError,
    FreeLLMAPIDisabledError,
    FreeLLMAPIResponseError,
    http_transport,
    is_armed,
    load_connection_config,
    redact,
)

TOKEN = "freellmapi-test-token-value"
ENV = {
    TOKEN_ENV_VAR: TOKEN,
    BASE_URL_ENV_VAR: "http://127.0.0.1:3001/v1",
}


def chat_response(status=200, routed_via="groq/llama-3.3-70b", body=None):
    if body is None:
        body = {
            "model": "llama-3.3-70b",
            "choices": [{"message": {"content": "hello"}}],
            "usage": {"prompt_tokens": 11, "completion_tokens": 3},
        }
    return {
        "status": status,
        "headers": {"X-Routed-Via": routed_via} if routed_via else {},
        "body": __import__("json").dumps(body),
    }


class ConfigTests(unittest.TestCase):
    def test_reads_config_from_environment(self):
        config = load_connection_config(ENV)
        self.assertEqual(config.base_url, "http://127.0.0.1:3001/v1")
        self.assertEqual(config.token, TOKEN)

    def test_redacts_token_in_summary(self):
        summary = load_connection_config(ENV).redacted()
        self.assertNotIn(TOKEN, str(summary))
        self.assertEqual(summary["token"], REDACTED)

    def test_missing_token_is_rejected(self):
        with self.assertRaises(FreeLLMAPIConfigError):
            load_connection_config({BASE_URL_ENV_VAR: "http://127.0.0.1:3001/v1"})

    def test_oversized_token_is_rejected(self):
        with self.assertRaises(FreeLLMAPIConfigError):
            load_connection_config({**ENV, TOKEN_ENV_VAR: "x" * 600})

    def test_non_loopback_url_is_refused_without_override(self):
        with self.assertRaises(FreeLLMAPIConfigError):
            load_connection_config({**ENV, BASE_URL_ENV_VAR: "https://gateway.example.com/v1"})

    def test_remote_http_url_is_refused_even_with_override(self):
        env = {**ENV, BASE_URL_ENV_VAR: "http://gateway.example.com/v1", ALLOW_REMOTE_ENV_VAR: "1"}
        with self.assertRaises(FreeLLMAPIConfigError):
            load_connection_config(env)

    def test_remote_https_url_allowed_with_override(self):
        env = {**ENV, BASE_URL_ENV_VAR: "https://gateway.example.com/v1", ALLOW_REMOTE_ENV_VAR: "1"}
        config = load_connection_config(env)
        self.assertEqual(config.base_url, "https://gateway.example.com/v1")

    def test_invalid_url_scheme_is_rejected(self):
        with self.assertRaises(FreeLLMAPIConfigError):
            load_connection_config({**ENV, BASE_URL_ENV_VAR: "ftp://127.0.0.1/v1"})

    def test_redact_replaces_token(self):
        self.assertEqual(redact(f"failed with {TOKEN}", TOKEN), f"failed with {REDACTED}")
        self.assertEqual(redact("no token here", ""), "no token here")

    def test_arming_flag_is_read_from_environment(self):
        self.assertFalse(is_armed(ENV))
        self.assertTrue(is_armed({**ENV, ARM_ENV_VAR: "true"}))


class DisabledTransportTests(unittest.TestCase):
    def test_http_transport_refused_when_not_armed(self):
        config = load_connection_config(ENV)
        with self.assertRaises(FreeLLMAPIDisabledError):
            http_transport(config, armed=False)

    def test_client_without_transport_refuses_to_call(self):
        client = FreeLLMAPIClient(load_connection_config(ENV))
        with self.assertRaises(FreeLLMAPIDisabledError):
            client.list_models()

    def test_from_environment_is_inert_when_not_armed(self):
        client = FreeLLMAPIClient.from_environment(ENV, armed=False)
        with self.assertRaises(FreeLLMAPIDisabledError):
            client.chat_completion(model="auto", prompt="hi")


class ClientTests(unittest.TestCase):
    def setUp(self):
        self.config = load_connection_config(ENV)
        self.calls = []

    def client_with(self, responses):
        index = {"value": 0}

        def transport(request):
            self.calls.append(request)
            position = min(index["value"], len(responses) - 1)
            index["value"] += 1
            response = responses[position]
            if isinstance(response, Exception):
                raise response
            return response

        return FreeLLMAPIClient(self.config, transport=transport, sleep=lambda _: None)

    def test_chat_completion_returns_content_and_usage(self):
        client = self.client_with([chat_response()])
        result = client.chat_completion(model="auto", prompt="Say hi")
        self.assertEqual(result.content, "hello")
        self.assertEqual(result.usage.prompt_tokens, 11)
        self.assertEqual(result.usage.completion_tokens, 3)
        self.assertEqual(result.usage.total_tokens, 14)
        self.assertEqual(result.routed_via, "groq/llama-3.3-70b")
        self.assertEqual(result.usage.provider, "groq")

    def test_request_shape_is_openai_compatible(self):
        client = self.client_with([chat_response()])
        client.chat_completion(model="auto:fast", prompt="Say hi", max_tokens=64)
        request = self.calls[0]
        self.assertEqual(request["path"], "/chat/completions")
        self.assertEqual(request["method"], "POST")
        self.assertEqual(request["body"]["model"], "auto:fast")
        self.assertEqual(request["body"]["messages"], [{"role": "user", "content": "Say hi"}])
        self.assertEqual(request["body"]["max_tokens"], 64)

    def test_list_models_uses_available_filter(self):
        client = self.client_with(
            [{"status": 200, "headers": {}, "body": '{"data":[{"id":"auto"},{"id":"groq/model"}]}'}]
        )
        self.assertEqual(client.list_models(available_only=True), ["auto", "groq/model"])
        self.assertIn("available=true", self.calls[0]["path"])

    def test_retries_retryable_status_then_succeeds(self):
        client = self.client_with([chat_response(status=429), chat_response()])
        result = client.chat_completion(model="auto", prompt="hi")
        self.assertEqual(result.content, "hello")
        self.assertEqual(len(self.calls), 2)

    def test_retries_connection_errors_then_succeeds(self):
        client = self.client_with([FreeLLMAPIConnectionError("reset by peer"), chat_response()])
        result = client.chat_completion(model="auto", prompt="hi")
        self.assertEqual(result.content, "hello")
        self.assertEqual(len(self.calls), 2)

    def test_gives_up_after_max_attempts(self):
        client = self.client_with([chat_response(status=503)] * 5)
        with self.assertRaises(FreeLLMAPIResponseError):
            client.chat_completion(model="auto", prompt="hi")
        self.assertEqual(len(self.calls), 3)

    def test_auth_failure_is_not_retried(self):
        client = self.client_with([chat_response(status=401)])
        with self.assertRaises(FreeLLMAPIAuthError):
            client.chat_completion(model="auto", prompt="hi")
        self.assertEqual(len(self.calls), 1)

    def test_client_error_is_not_retried(self):
        client = self.client_with([chat_response(status=400, body={"error": "bad request"})])
        with self.assertRaises(FreeLLMAPIResponseError):
            client.chat_completion(model="auto", prompt="hi")
        self.assertEqual(len(self.calls), 1)

    def test_non_json_body_raises_response_error(self):
        client = self.client_with([{"status": 200, "headers": {}, "body": "not json"}])
        with self.assertRaises(FreeLLMAPIResponseError):
            client.chat_completion(model="auto", prompt="hi")

    def test_missing_choices_raises_response_error(self):
        client = self.client_with([chat_response(body={"model": "auto"})])
        with self.assertRaises(FreeLLMAPIResponseError):
            client.chat_completion(model="auto", prompt="hi")

    def test_blank_prompt_is_rejected_before_any_request(self):
        client = self.client_with([chat_response()])
        with self.assertRaises(FreeLLMAPIConfigError):
            client.chat_completion(model="auto", prompt="   ")
        self.assertEqual(self.calls, [])

    def test_oversized_prompt_is_rejected(self):
        client = self.client_with([chat_response()])
        with self.assertRaises(FreeLLMAPIConfigError):
            client.chat_completion(model="auto", prompt="x" * 20001)

    def test_max_tokens_range_is_enforced(self):
        client = self.client_with([chat_response()])
        with self.assertRaises(FreeLLMAPIConfigError):
            client.chat_completion(model="auto", prompt="hi", max_tokens=99999)

    def test_error_messages_do_not_leak_the_token(self):
        client = self.client_with(
            [{"status": 400, "headers": {}, "body": f'{{"error":"bad key {TOKEN}"}}'}]
        )
        with self.assertRaises(FreeLLMAPIResponseError) as caught:
            client.chat_completion(model="auto", prompt="hi")
        self.assertNotIn(TOKEN, str(caught.exception))
        self.assertIn(REDACTED, str(caught.exception))

    def test_config_defaults_are_loopback_and_bounded(self):
        config = ConnectionConfig(base_url=DEFAULT_BASE_URL, token=TOKEN)
        self.assertEqual(config.timeout_seconds, DEFAULT_TIMEOUT_SECONDS)
        self.assertEqual(config.max_attempts, MAX_ATTEMPTS)
        self.assertTrue(config.base_url.startswith("http://127.0.0.1"))


if __name__ == "__main__":
    unittest.main()
