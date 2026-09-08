# pages/base_page.py
from playwright.sync_api import Page, Locator, expect

import config


class BasePage:
    """Base class for all page objects. Holds shared behavior
    that every page needs: navigation, waits, interactions, and diagnostics.
    """

    def __init__(self, page: Page):
        self.page = page

    # --- Visibility assertions ---

    def assert_visible(self, locator: Locator, description: str = "element", timeout_ms: int = config.DEFAULT_TIMEOUT_MS) -> Locator:
        """Confirm an element is visible within timeout_ms, then return it so
        callers can chain (e.g. assert_visible(btn, "Submit").click()).
        Playwright's expect() auto-waits and retries; on timeout it raises,
        and we re-raise naming the page, element, timeout, and URL.
        """
        try:
            expect(locator).to_be_visible(timeout=timeout_ms)
        except AssertionError as exc:
            raise AssertionError(
                f"{type(self).__name__}: '{description}' not visible within "
                f"{timeout_ms}ms (url={self.page.url})"
            ) from exc
        return locator

    def assert_text_visible(self, text: str, exact: bool = False,
                            timeout_ms: int = config.DEFAULT_TIMEOUT_MS) -> Locator:
        """Confirm the given text is visible somewhere on the page, then return
        its locator. Pass the string to look for (e.g. a header like "Kalita 185").
        exact=True matches the whole trimmed string - use it when the text is a
        substring of something else on the page (e.g. "Press" in "AeroPress").
        """
        return self.assert_visible(
            self.page.get_by_text(text, exact=exact), f"text '{text}'", timeout_ms
        )

    def assert_all_text_visible(self, *texts: str, exact: bool = False, timeout_ms: int = config.DEFAULT_TIMEOUT_MS) -> None:
        """Confirm every given text is visible on the page. Raises on the first
        one that isn't, naming which text failed.
        """
        for text in texts:
            self.assert_text_visible(text, exact, timeout_ms)

    def assert_has_text(self, locator: Locator, expected: str, description: str = "element", timeout_ms: int = config.DEFAULT_TIMEOUT_MS) -> None:
        """Confirm an element's text equals expected (trimmed). Auto-waits, so
        it handles a label that updates a beat after the element appears.
        """
        try:
            expect(locator).to_have_text(expected, timeout=timeout_ms)
        except AssertionError as exc:
            raise AssertionError(
                f"{type(self).__name__}: {description} text is not '{expected}' "
                f"within {timeout_ms}ms (url={self.page.url})"
            ) from exc

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

    # --- Interactions ---

    def click(self, locator: Locator, description: str = "element") -> None:
        """Wait for the element to be visible, then click it."""
        self.assert_visible(locator, description).click()

    def fill(self, locator: Locator, text: str, description: str = "field") -> None:
        """Wait for the field to be visible, then fill it with text."""
        self.assert_visible(locator, description).fill(text)

    # --- Diagnostics ---

    def screenshot(self, path: str) -> None:
        self.page.screenshot(path=path)
