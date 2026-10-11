"""Offline unit tests for SOCRF resource plans."""
import unittest
from socrf.adapters.resource_planner import ResourceRequest, plan_resource_request

class ResourcePlannerTests(unittest.TestCase):
    def test_freellmapi(self):
        result = plan_resource_request(ResourceRequest("freellmapi", "route_model", {"model": "test"}))
        self.assertFalse(result["executed"])

    def test_ornith(self):
        result = plan_resource_request(ResourceRequest("ornith", "evaluate_workflow", {"task": "test"}))
        self.assertEqual(result["mode"], "dry_run")

    def test_ltx(self):
        result = plan_resource_request(ResourceRequest("ltx-2", "estimate_render", {"seconds": 5}))
        self.assertFalse(result["approved"])

    def test_unknown_resource(self):
        with self.assertRaises(ValueError):
            plan_resource_request(ResourceRequest("unknown", "route_model", {}))

    def test_unsupported_action(self):
        with self.assertRaises(ValueError):
            plan_resource_request(ResourceRequest("ltx-2", "delete_everything", {}))

    def test_reject_oversized_payload(self):
        with self.assertRaises(ValueError):
            plan_resource_request(ResourceRequest("freellmapi", "route_model", {"prompt": "x" * 5000}))

if __name__ == "__main__":
    unittest.main()
