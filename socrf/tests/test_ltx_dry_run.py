"""Contract tests for the non-executing LTX adapter."""
import unittest

from socrf.adapters.ltx_dry_run import (
    DEFAULT_FPS,
    DEFAULT_RESOLUTION,
    LICENSE,
    PROMPT_MAX_WORDS,
    WEIGHTS_FACTS,
    LTXRequest,
    plan_ltx_request,
)


class LTXDryRunTests(unittest.TestCase):
    def test_returns_plan_without_execution(self):
        result = plan_ltx_request(LTXRequest("generate_video", "A calm ocean wave at dawn."))
        self.assertEqual(result["adapter"], "ltx")
        self.assertEqual(result["mode"], "dry_run")
        self.assertFalse(result["executed"])
        self.assertFalse(result["approved"])

    def test_estimate_render_reports_frame_count(self):
        result = plan_ltx_request(LTXRequest("estimate_render", "", 5.0, "1024x1536"))
        self.assertEqual(result["estimated_frames"], int(5.0 * DEFAULT_FPS))
        self.assertEqual(result["resolution"], DEFAULT_RESOLUTION)

    def test_rejects_unknown_action(self):
        with self.assertRaises(ValueError):
            plan_ltx_request(LTXRequest("delete_workspace", "Destroy"))

    def test_rejects_blank_prompt_for_generation(self):
        with self.assertRaises(ValueError):
            plan_ltx_request(LTXRequest("generate_video", "   "))

    def test_rejects_prompt_over_word_guidance(self):
        with self.assertRaises(ValueError):
            plan_ltx_request(LTXRequest("generate_video", " ".join(["wave"] * (PROMPT_MAX_WORDS + 1))))

    def test_rejects_unsupported_resolution(self):
        with self.assertRaises(ValueError):
            plan_ltx_request(LTXRequest("estimate_render", "", 5.0, "512x512"))

    def test_rejects_clip_outside_policy_range(self):
        with self.assertRaises(ValueError):
            plan_ltx_request(LTXRequest("estimate_render", "", 600.0))

    def test_rejects_live_execution(self):
        with self.assertRaises(PermissionError):
            plan_ltx_request(
                LTXRequest("generate_video", "A calm ocean wave at dawn."),
                config={"execution_enabled": True},
            )

    def test_rejects_weight_download(self):
        with self.assertRaises(PermissionError):
            plan_ltx_request(
                LTXRequest("generate_video", "A calm ocean wave at dawn."),
                config={"download_weights": True},
            )

    def test_license_requires_review(self):
        result = plan_ltx_request(LTXRequest("estimate_render", "", 5.0))
        self.assertTrue(result["license_review_required"])
        self.assertIn("license_legal_review", result["requires"])

    def test_license_is_community_agreement(self):
        self.assertIn("Community License", LICENSE)

    def test_weights_facts_are_recorded(self):
        self.assertTrue(WEIGHTS_FACTS["gated"])
        self.assertEqual(WEIGHTS_FACTS["approximate_size_gib"], 66)
        self.assertEqual(len(WEIGHTS_FACTS["components"]), 5)


if __name__ == "__main__":
    unittest.main()
