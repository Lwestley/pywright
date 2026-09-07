# pages/base_page.py
from playwright.sync_api import Page, Locator


class BasePage:
    """Base class for all page objects. Holds shared behavior
    that every page needs: navigation, waits, and diagnostics.
    """

    def __init__(self, page: Page):
        self.page = page

    # --- Navigation ---

    def goto(self, url: str) -> None:
        self.page.goto(url)

    def reload(self) -> None:
        self.page.reload()

    def get_title(self) -> str:
        return self.page.title()

    def get_url(self) -> str:
        return self.page.url

    # --- Waits ---

    def wait_for_load(self) -> None:
        self.page.wait_for_load_state("networkidle")

    # --- Diagnostics ---

    def screenshot(self, path: str) -> None:
        self.page.screenshot(path=path)