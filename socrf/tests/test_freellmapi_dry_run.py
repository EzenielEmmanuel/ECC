"""Contract tests for the non-executing FreeLLMAPI adapter."""
import unittest

from socrf.adapters.freellmapi_dry_run import (
    ADAPTER,
    LICENSE,
    RUNTIME_REQUIREMENTS,
    FreeLLMAPIRequest,
    plan_freellmapi_request,
)


class FreeLLMAPIDryRunTests(unittest.TestCase):
    def test_returns_plan_without_execution(self):
        result = plan_freellmapi_request(FreeLLMAPIRequest("route_model", "auto", {"prompt": "hi"}))
        self.assertEqual(result["adapter"], ADAPTER)
        self.assertEqual(result["mode"], "dry_run")
        self.assertFalse(result["executed"])
        self.assertFalse(result["approved"])

    def test_list_models_is_planned(self):
        result = plan_freellmapi_request(FreeLLMAPIRequest("list_models", "auto", {}))
        self.assertEqual(result["action"], "list_models")
        self.assertFalse(result["executed"])

    def test_rejects_unknown_action(self):
        with self.assertRaises(ValueError):
            plan_freellmapi_request(FreeLLMAPIRequest("delete_workspace", "auto", {}))

    def test_rejects_blank_model(self):
        with self.assertRaises(ValueError):
            plan_freellmapi_request(FreeLLMAPIRequest("list_models", "  ", {}))

    def test_rejects_live_execution(self):
        with self.assertRaises(PermissionError):
            plan_freellmapi_request(
                FreeLLMAPIRequest("route_model", "auto", {"prompt": "hi"}),
                config={"execution_enabled": True},
            )

    def test_rejects_provider_key_argument(self):
        with self.assertRaises(PermissionError):
            plan_freellmapi_request(
                FreeLLMAPIRequest("route_model", "auto", {"prompt": "hi"}),
                config={"provider_key": "sk-live-value"},
            )

    def test_rejects_oversized_prompt(self):
        with self.assertRaises(ValueError):
            plan_freellmapi_request(FreeLLMAPIRequest("route_model", "auto", {"prompt": "x" * 20001}))

    def test_rejects_out_of_range_max_tokens(self):
        with self.assertRaises(ValueError):
            plan_freellmapi_request(FreeLLMAPIRequest("route_model", "auto", {"prompt": "hi", "max_tokens": 99999}))

    def test_rejects_non_integer_max_tokens(self):
        with self.assertRaises(TypeError):
            plan_freellmapi_request(FreeLLMAPIRequest("route_model", "auto", {"prompt": "hi", "max_tokens": "1024"}))

    def test_runtime_requirements_are_recorded(self):
        self.assertEqual(RUNTIME_REQUIREMENTS["node"], ">=20.18.0 <25.0.0")
        self.assertEqual(RUNTIME_REQUIREMENTS["npm"], ">=10.0.0")

    def test_license_is_recorded(self):
        self.assertEqual(LICENSE, "MIT")

    def test_plan_requires_credential_vault(self):
        result = plan_freellmapi_request(FreeLLMAPIRequest("route_model", "auto", {"prompt": "hi"}))
        self.assertIn("credential_vault", result["requires"])
        self.assertTrue(result["usage_review_required"])


if __name__ == "__main__":
    unittest.main()
