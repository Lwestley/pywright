# pages/timer_page.py
from pages.base_page import BasePage


class TimerPage(BasePage):
    """Page object for the pour-over brew method screen. One page,
    client-side state switches between brew methods (Kalita 185,
    V60, Chemex, Aeropress) via arrow navigation.
    """

    def __init__(self, page):
        super().__init__(page)

        # --- Method navigation ---
        self.next_arrow = page.locator("REPLACE_WITH_CODEGEN")   # right arrow (>)
        self.prev_arrow = page.locator("REPLACE_WITH_CODEGEN")   # left arrow (<)
        self.method_label = page.get_by_text("Kalita 185")       # changes per method

        # --- Coffee / ratio / water controls ---
        self.coffee_minus = page.locator("REPLACE_WITH_CODEGEN")
        self.coffee_plus = page.locator("REPLACE_WITH_CODEGEN")
        self.ratio_minus = page.locator("REPLACE_WITH_CODEGEN")
        self.ratio_plus = page.locator("REPLACE_WITH_CODEGEN")

        # --- Brew steps (Bloom, Pour 1-3, Drain) ---
        self.bloom_step = page.get_by_text("Bloom")

        # --- Brew action ---
        self.start_brew_button = page.get_by_role("button", name="Start Brew")

    # --- Actions ---

    def go_to_next_method(self) -> None:
        assert self.next_arrow.is_visible(), "Next arrow not visible, cannot switch brew method"
        self.next_arrow.click()

    def go_to_previous_method(self) -> None:
        assert self.prev_arrow.is_visible(), "Previous arrow not visible, cannot switch brew method"
        self.prev_arrow.click()

    def get_current_method(self) -> str:
        return self.method_label.inner_text()

    def start_brew(self) -> None:
        assert self.start_brew_button.is_visible(), "Start Brew button not visible, cannot start brew"
        self.start_brew_button.click()

    # --- State checks ---

    def is_brewing(self) -> bool:
        # Adjust once codegen shows what actually changes on click,
        # e.g. button text/state changing, Bloom step becoming "active"
        return not self.start_brew_button.is_visible()