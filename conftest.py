# conftest.py
import re
from datetime import datetime
from pathlib import Path

import pytest
from playwright.sync_api import sync_playwright

import config


def pytest_addoption(parser):
    parser.addoption(
        "--headed",
        action="store_true",
        default=False,
        help="Run browser in headed mode (visible window) instead of headless.",
    )


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Stash each phase's report (setup/call/teardown) on the test item, so
    fixtures can tell during teardown whether the test failed.
    """
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"report_{report.when}", report)


def _test_failed(item) -> bool:
    """True if the test's setup or body (call) phase failed."""
    for phase in ("setup", "call"):
        report = getattr(item, f"report_{phase}", None)
        if report is not None and report.failed:
            return True
    return False


def _save_failure_screenshot(page, nodeid: str) -> None:
    out_dir = Path(config.SCREENSHOT_DIR)
    out_dir.mkdir(parents=True, exist_ok=True)
    safe_name = re.sub(r"[^A-Za-z0-9_.-]+", "_", nodeid)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = out_dir / f"{safe_name}_{timestamp}.png"
    try:
        page.screenshot(path=str(path), full_page=True)
        print(f"\n[screenshot] failure captured: {path}")
    except Exception as exc:  # page/browser may already be closed
        print(f"\n[screenshot] could not capture failure screenshot: {exc}")


@pytest.fixture
def page(request):
    headless = not request.config.getoption("--headed")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()

        yield page

        if _test_failed(request.node):
            _save_failure_screenshot(page, request.node.nodeid)

        browser.close()
