"""Deterministic, offline reference model for companion-capability routing.

This is a test/reference policy for a model-driven assistant, not an MCP adapter.
No imports from live clients, filesystem access, or network operations.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class RoutingResult:
    profile: str | None
    status: str
    calls: tuple[str, ...]
    verification: str
    reason: str


def plan(
    *,
    source_mode: str,
    local_execution: bool = False,
    github_ci: bool = False,
    agent_workspace: bool = False,
    agent_workspace_error: bool = False,
    pwa_preview: bool = False,
    browser_screenshot: bool = False,
    browser_interaction: bool = False,
    alternative_browser_runner: bool = False,
    static_web: bool = False,
    preview_artifact_url: bool = False,
    public_url: bool = False,
    browser_required: bool = False,
    can_defer: bool = False,
) -> RoutingResult:
    """Return intended operations, without ever executing an operation.

    Optional tools never become mandatory merely by being installed.
    Browser interaction is a separate capability from screenshot capture.
    A required gate cannot be claimed PASS when no runner exists.
    """
    if source_mode not in ("zip", "workspace", "github"):
        raise ValueError("unknown source mode")

    if source_mode == "github" and github_ci:
        profile, calls, reason = "github_first", ["github_ci_verify"], "repository CI sufficient"
    elif local_execution:
        profile = "github_first" if source_mode == "github" else "zip_local"
        calls, reason = ["local_verify"], "local execution sufficient"
    elif agent_workspace and not agent_workspace_error:
        profile = "hybrid_github_external_execution" if source_mode == "github" else "agent_workspace"
        calls, reason = ["agent_workspace_verify"], "compatible isolated execution"
    else:
        reason = "execution backend error" if agent_workspace_error else "no execution backend"
        if can_defer and not browser_required:
            return RoutingResult("degraded_manual", "degraded", (), "deferred", reason)
        return RoutingResult(None, "blocked", (), "not_run", reason)

    if browser_required and not (alternative_browser_runner or
                                 (browser_screenshot and browser_interaction and
                                  (public_url or (static_web and pwa_preview and preview_artifact_url)))):
        if can_defer:
            return RoutingResult("degraded_manual", "degraded", tuple(calls), "deferred", "required browser gate unavailable")
        return RoutingResult(None, "blocked", tuple(calls), "not_run", "required browser gate unavailable")

    if static_web and pwa_preview and preview_artifact_url:
        calls.append("pwa_preview_create")
    url_ready = public_url or "pwa_preview_create" in calls
    if url_ready:
        if browser_screenshot and browser_interaction:
            calls.append("browser_interaction_verify")
        elif alternative_browser_runner:
            calls.append("alternative_browser_verify")
        elif browser_screenshot:
            calls.append("browser_screenshot_visual_only")

    return RoutingResult(profile, "selected", tuple(calls), "planned_not_run", reason)
