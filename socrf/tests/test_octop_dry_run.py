"""Contract tests for the non-executing Octop adapter."""
import unittest
from socrf.adapters.octop_dry_run import OctopRequest, plan_octop_request

class OctopDryRunTests(unittest.TestCase):
    def test_returns_plan_without_execution(self):
        result = plan_octop_request(OctopRequest("delegate_task", "Build a sample app"))
        self.assertEqual(result["mode"], "dry_run")
        self.assertFalse(result["executed"])

    def test_approval_does_not_enable_execution(self):
        result = plan_octop_request(OctopRequest("check_status", "Check job", approved=True))
        self.assertFalse(result["executed"])

    def test_rejects_live_execution(self):
        with self.assertRaises(PermissionError):
            plan_octop_request(OctopRequest("delegate_task", "Build app"), config={"execution_enabled": True})

    def test_rejects_unknown_action(self):
        with self.assertRaises(ValueError):
            plan_octop_request(OctopRequest("delete_workspace", "Destroy"))

    def test_rejects_blank_task(self):
        with self.assertRaises(ValueError):
            plan_octop_request(OctopRequest("delegate_task", "  "))

if __name__ == "__main__":
    unittest.main()
