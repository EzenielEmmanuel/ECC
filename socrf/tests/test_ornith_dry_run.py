"""Contract tests for the non-executing Ornith adapter."""
import unittest

from socrf.adapters.ornith_dry_run import (
    CHECKPOINT_FACTS,
    LICENSE,
    OrnithRequest,
    plan_ornith_request,
)


class OrnithDryRunTests(unittest.TestCase):
    def test_returns_plan_without_execution(self):
        result = plan_ornith_request(OrnithRequest("evaluate_workflow", "Review a pull request"))
        self.assertEqual(result["adapter"], "ornith")
        self.assertEqual(result["mode"], "dry_run")
        self.assertFalse(result["executed"])
        self.assertFalse(result["approved"])

    def test_compare_strategies_are_listed(self):
        result = plan_ornith_request(
            OrnithRequest("compare_strategies", "Pick a plan", ("direct", "scaffolded"))
        )
        self.assertEqual(result["strategies"], ["direct", "scaffolded"])

    def test_rejects_unknown_action(self):
        with self.assertRaises(ValueError):
            plan_ornith_request(OrnithRequest("delete_workspace", "Destroy"))

    def test_rejects_blank_task(self):
        with self.assertRaises(ValueError):
            plan_ornith_request(OrnithRequest("evaluate_workflow", "   "))

    def test_rejects_single_strategy_for_comparison(self):
        with self.assertRaises(ValueError):
            plan_ornith_request(OrnithRequest("compare_strategies", "Pick a plan", ("direct",)))

    def test_rejects_too_many_strategies(self):
        with self.assertRaises(ValueError):
            plan_ornith_request(
                OrnithRequest("compare_strategies", "Pick a plan", tuple(f"s{i}" for i in range(9)))
            )

    def test_rejects_live_execution(self):
        with self.assertRaises(PermissionError):
            plan_ornith_request(OrnithRequest("evaluate_workflow", "Review"), config={"execution_enabled": True})

    def test_rejects_weight_download(self):
        with self.assertRaises(PermissionError):
            plan_ornith_request(OrnithRequest("evaluate_workflow", "Review"), config={"download_weights": True})

    def test_checkpoint_facts_are_recorded(self):
        self.assertEqual(CHECKPOINT_FACTS["context_tokens"], 262144)
        self.assertEqual(CHECKPOINT_FACTS["approximate_size_gib"], 19)
        self.assertIn("80 GB GPU", CHECKPOINT_FACTS["hardware"])

    def test_license_is_recorded(self):
        self.assertEqual(LICENSE, "MIT")

    def test_plan_requires_gpu_host_provisioning(self):
        result = plan_ornith_request(OrnithRequest("evaluate_workflow", "Review"))
        self.assertIn("gpu_host_provisioning", result["requires"])
        self.assertIn("weights_download_approval", result["requires"])


if __name__ == "__main__":
    unittest.main()
