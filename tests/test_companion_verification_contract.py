"""Regression checks for optional companion-assisted ZIP verification contracts."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class CompanionVerificationContractTests(unittest.TestCase):
    def read(self, path):
        return (ROOT / path).read_text(encoding="utf-8")

    def test_zip_mode_never_requires_github_or_plugin(self):
        text = self.read("docs/zip-mode.md")
        self.assertIn("Companion-verktyg är alltid valfria", text)
        self.assertIn("GitHub får inte bli ett krav i ZIP-läge", self.read("docs/agent-workspace-integration.md"))

    def test_browser_smoke_is_not_screenshot_or_full_e2e(self):
        text = self.read("docs/browser-screenshot-integration.md")
        self.assertIn("functional browser smoke PASS", text)
        self.assertIn("visual-only", text)
        self.assertIn("Playwright-regressionssvit", text)
        self.assertIn("stänga sessionen även vid fel", text)

    def test_artifact_handoff_and_source_provenance(self):
        text = self.read("docs/agent-workspace-integration.md")
        for term in ("file_read", "artifact_download_link", "source checksum", "project_verify", "project_build"):
            self.assertIn(term, text)

    def test_canonical_browser_capability_is_runtime_discovered(self):
        text = self.read("src/instructions/system.md")
        self.assertIn("Discover live session actions", text)
        self.assertIn("Never simulate interaction results", text)

if __name__ == "__main__":
    unittest.main()
