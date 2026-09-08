# pages/brew_method_page.py
import config
from pages.base_page import BasePage
from pages.timer_page import TimerPage


class BrewMethodPage(BasePage):
    """Page object for the brew method selection/setup screen.
    One page, client side state switches between brew methods
    (Kalita 185, V60, Chemex, Aeropress) via arrow navigation.
    Clicking Start Brew transitions into timer_page.py.
    """

    def __init__(self, page):
        super().__init__(page)

        # --- Method navigation ---
        self.next_arrow = page.get_by_role("button", name="Next")   # right arrow (>)
        self.prev_arrow = page.locator("REPLACE_WITH_CODEGEN")   # left arrow (<)
        self.method_label = page.get_by_text("Kalita 185")       # text changes per method

        # --- Recipe controls ---
        self.coffee_minus = page.locator("REPLACE_WITH_CODEGEN")
        self.coffee_plus = page.locator("REPLACE_WITH_CODEGEN")
        self.coffee_value = page.locator("REPLACE_WITH_CODEGEN")  # e.g. the "20g" text
        self.ratio_minus = page.locator("REPLACE_WITH_CODEGEN")
        self.ratio_plus = page.locator("REPLACE_WITH_CODEGEN")
        self.ratio_value = page.locator("REPLACE_WITH_CODEGEN")   # e.g. the "1:15" text

        # --- Brew steps (Bloom, Pour 1-3, Drain) ---
        self.bloom_step = page.get_by_text("Bloom")

        # --- Action ---
        self.start_brew_button = page.get_by_role("button", name="Start Brew")

        # --- Brew method labels (only the current method shows at a time) ---
        self.kalita_185_label = page.get_by_text("Kalita 185")
        self.v60_label = page.get_by_text("V60")
        self.chemex_label = page.get_by_text("Chemex")
        self.aeropress_label = page.get_by_text("Aeropress")

        self.confirm_brew_method_screen_loaded()

    # --- Page ready check ---

    def confirm_brew_method_screen_loaded(self) -> None:
        """Landmark check: the method label is always present on this screen
        (Kalita 185 is the default) and settles last, so its visibility means
        the screen has finished rendering.
        """
        self.assert_visible(self.method_label, "brew method label",
                            timeout_ms=config.DEFAULT_TIMEOUT_MS)

    # --- Brew method visibility checks ---
    def is_kalita_185_visible(self) -> bool:
        return self.kalita_185_label.is_visible()

    def is_v60_visible(self) -> bool:
        return self.v60_label.is_visible()

    def is_chemex_visible(self) -> bool:
        return self.chemex_label.is_visible()

    def is_aeropress_visible(self) -> bool:
        return self.aeropress_label.is_visible()

    def confirm_text_visible(self, text: str) -> None:
      """Confirm any text is visible on the brew method screen.
      Pass whatever you want to assert from the test, e.g.
      brew_page.confirm_text_visible("Coffee").
      """
      self.assert_text_visible(text, exact=True)

    # --- Navigation actions ---

    def go_to_next_method(self) -> None:
      self.click(self.next_arrow, "next arrow")

    def go_to_previous_method(self) -> None:
        assert self.prev_arrow.is_visible(), "Previous arrow not visible, cannot switch brew method"
        self.prev_arrow.click()

    def go_to_method(self, target_method: str) -> None:
        """Clicks the next arrow repeatedly until the target method is showing."""
        while self.get_current_method() != target_method:
            self.go_to_next_method()

    def get_current_method(self) -> str:
        return self.method_label.inner_text()

    # --- Recipe adjustment actions ---

    def increase_coffee(self) -> None:
        self.coffee_plus.click()

    def decrease_coffee(self) -> None:
        self.coffee_minus.click()

    def increase_ratio(self) -> None:
        self.ratio_plus.click()

    def decrease_ratio(self) -> None:
        self.ratio_minus.click()

    def get_coffee_amount(self) -> str:
        return self.coffee_value.inner_text()

    def get_ratio(self) -> str:
        return self.ratio_value.inner_text()

    # --- Transition to brewing ---

    def start_brew(self) -> TimerPage:
        """Clicks Start Brew and returns TimerPage, since this
        action transitions the screen into the active brewing view."""
        assert self.start_brew_button.is_visible(), "Start Brew button not visible, cannot start brew"
        self.start_brew_button.click()
        return TimerPage(self.page)