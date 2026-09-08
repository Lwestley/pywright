# conftest.py
import pytest
from playwright.sync_api import sync_playwright


def pytest_addoption(parser):
    parser.addoption(
        "--headed",
        action="store_true",
        default=False,
        help="Run browser in headed mode (visible window) instead of headless.",
    )


@pytest.fixture
def page(request):
    headless = not request.config.getoption("--headed")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()
        yield page
        browser.close()