"""Simulated plugin-availability matrix; strictly offline, no MCP calls."""
import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from offline_companion_routing import plan


class OfflineCompanionFallbackTests(unittest.TestCase):
    def test_all_present_zip_static_web(self):
        r = plan(source_mode="zip", agent_workspace=True, pwa_preview=True,
                 browser_screenshot=True, browser_interaction=True,
                 static_web=True, preview_artifact_url=True)
        self.assertEqual(r.profile, "agent_workspace")
        self.assertEqual(r.calls, ("agent_workspace_verify", "pwa_preview_create", "browser_interaction_verify"))
        self.assertEqual(r.verification, "planned_not_run")

    def test_agent_missing_uses_local_runner(self):
        r = plan(source_mode="zip", local_execution=True, pwa_preview=True)
        self.assertEqual(r.calls, ("local_verify",))
        self.assertEqual(r.profile, "zip_local")

    def test_preview_missing_does_not_block(self):
        r = plan(source_mode="zip", agent_workspace=True, browser_screenshot=True,
                 browser_interaction=True, static_web=True, preview_artifact_url=True)
        self.assertEqual(r.calls, ("agent_workspace_verify",))
        self.assertEqual(r.status, "selected")

    def test_browser_missing_does_not_block_build(self):
        r = plan(source_mode="zip", agent_workspace=True, pwa_preview=True,
                 static_web=True, preview_artifact_url=True)
        self.assertEqual(r.calls, ("agent_workspace_verify", "pwa_preview_create"))
        self.assertEqual(r.status, "selected")

    def test_all_missing_without_local_can_defer(self):
        r = plan(source_mode="zip", can_defer=True)
        self.assertEqual((r.profile, r.status, r.verification), ("degraded_manual", "degraded", "deferred"))
        self.assertEqual(r.calls, ())

    def test_all_missing_blocks_required_execution(self):
        r = plan(source_mode="zip")
        self.assertEqual((r.profile, r.status, r.verification), (None, "blocked", "not_run"))

    def test_backend_error_not_project_failure(self):
        r = plan(source_mode="zip", agent_workspace=True, agent_workspace_error=True, can_defer=True)
        self.assertEqual(r.status, "degraded")
        self.assertIn("backend error", r.reason)
        self.assertNotIn("agent_workspace_verify", r.calls)

    def test_github_ci_preferred_to_remote(self):
        r = plan(source_mode="github", github_ci=True, agent_workspace=True)
        self.assertEqual(r.calls, ("github_ci_verify",))
        self.assertEqual(r.profile, "github_first")

    def test_required_browser_without_runner_blocks(self):
        r = plan(source_mode="zip", local_execution=True, browser_required=True,
                 browser_screenshot=True, browser_interaction=False, public_url=True)
        self.assertEqual(r.status, "blocked")
        self.assertEqual(r.verification, "not_run")
        self.assertNotIn("browser_interaction_verify", r.calls)

    def test_required_browser_deferred_when_allowed(self):
        r = plan(source_mode="zip", local_execution=True, browser_required=True, can_defer=True)
        self.assertEqual(r.status, "degraded")
        self.assertEqual(r.verification, "deferred")

    def test_visual_screenshot_not_functional_pass(self):
        r = plan(source_mode="zip", local_execution=True, browser_screenshot=True, public_url=True)
        self.assertEqual(r.calls, ("local_verify", "browser_screenshot_visual_only"))
        self.assertEqual(r.verification, "planned_not_run")

    def test_alternative_browser_runner_when_plugin_missing(self):
        r = plan(source_mode="zip", local_execution=True, browser_required=True,
                 alternative_browser_runner=True, public_url=True)
        self.assertEqual(r.calls, ("local_verify", "alternative_browser_verify"))
        self.assertEqual(r.status, "selected")

    def test_no_url_means_no_browser_calls(self):
        r = plan(source_mode="zip", local_execution=True, browser_screenshot=True, browser_interaction=True)
        self.assertEqual(r.calls, ("local_verify",))

    def test_no_real_mcp_imports(self):
        source = (Path(__file__).resolve().parents[1] / "scripts" / "offline_companion_routing.py").read_text()
        for forbidden in ("requests", "urllib", "httpx", "mcp__", "subprocess", "socket"):
            self.assertNotIn(forbidden, source)


if __name__ == "__main__":
    unittest.main()
