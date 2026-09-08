# pages/brew_method_page.py
import config
from pages.base_page import BasePage
from pages.timer_page import TimerPage


class BrewMethodPage(BasePage):
    """Page object for the brew method selection/setup screen.
    One page, client side state switches between brew methods
    (Kalita 185, V60, Chemex, Aeropress) via arrow navigation.
    Clicking Start Brew transitions into timer_page.py.

    Method naming: a method that is a thin wrapper around one BasePage call is
    named <basepage_method>_<locator>, e.g. click_next_arrow_button wraps
    self.click(self.next_arrow_button). Composite/semantic methods keep an
    intent name (go_to_method, confirm_recipe_sections_visible).
    """

    # Elements every brew method screen is expected to show.
    RECIPE_SECTIONS = ("Coffee", "Ratio", "Water")
    BREW_STEPS = ("Bloom", "Pour 1", "Pour 2", "Pour 3", "Drain")

    def __init__(self, page):
        super().__init__(page)

        # --- Method navigation ---
        # Naming: clickable elements -> *_button, read-only text -> *_value / *_label
        self.next_arrow_button = page.get_by_role("button", name="Next")   # right arrow (>)
        self.prev_arrow_button = page.locator("REPLACE_WITH_CODEGEN")      # left arrow (<)
        self.method_label = page.get_by_text("Kalita 185")                 # text changes per method

        # --- Recipe controls ---
        self.coffee_minus_button = page.locator("REPLACE_WITH_CODEGEN")
        self.coffee_plus_button = page.locator("REPLACE_WITH_CODEGEN")
        self.coffee_value = page.locator("REPLACE_WITH_CODEGEN")   # e.g. the "20g" text
        self.ratio_minus_button = page.locator("REPLACE_WITH_CODEGEN")
        self.ratio_plus_button = page.locator("REPLACE_WITH_CODEGEN")
        self.ratio_value = page.locator("REPLACE_WITH_CODEGEN")    # e.g. the "1:15" text

        # --- Brew steps (Bloom, Pour 1-3, Drain) ---
        self.bloom_step = page.get_by_text("Bloom")

        # --- Action ---
        self.start_brew_button = page.get_by_role("button", name="Start Brew")

        # --- Brew method labels (only the current method shows at a time) ---
        self.kalita_185_label = page.get_by_text("Kalita 185")
        self.v60_label = page.get_by_text("V60")
        self.chemex_label = page.get_by_text("Chemex")
        self.aeropress_label = page.get_by_text("Aeropress")

        self.assert_method_label_visible()

    # --- Page ready check ---

    def assert_method_label_visible(self) -> None:
        """Landmark check: the method label is always present on this screen
        (Kalita 185 is the default) and settles last, so its visibility means
        the screen has finished rendering.
        """
        self.assert_visible(self.method_label, "brew method label",
                            timeout_ms=config.DEFAULT_TIMEOUT_MS)

    # --- Expected-content checks ---

    def confirm_recipe_sections_visible(self) -> None:
        """Confirm the Coffee, Ratio, and Water recipe sections are shown."""
        self.assert_all_text_visible(*self.RECIPE_SECTIONS)

    def confirm_brew_steps_visible(self) -> None:
        """Confirm all five brew steps (Bloom, Pour 1-3, Drain) are shown."""
        self.assert_all_text_visible(*self.BREW_STEPS)

    def is_kalita_185_visible(self) -> bool:
        return self.kalita_185_label.is_visible()

    def is_v60_visible(self) -> bool:
        return self.v60_label.is_visible()

    def is_chemex_visible(self) -> bool:
        return self.chemex_label.is_visible()

    def is_aeropress_visible(self) -> bool:
        return self.aeropress_label.is_visible()

    # --- Navigation actions ---

    def click_next_arrow_button(self) -> None:
        self.click(self.next_arrow_button, "next arrow button")

    def click_prev_arrow_button(self) -> None:
        self.click(self.prev_arrow_button, "previous arrow button")

    def go_to_method(self, target_method: str) -> None:
        """Clicks the next arrow repeatedly until the target method is showing."""
        while self.get_current_method() != target_method:
            self.click_next_arrow_button()

    def get_current_method(self) -> str:
        return self.method_label.inner_text()

    # --- Recipe adjustment actions ---

    def click_coffee_plus_button(self) -> None:
        self.click(self.coffee_plus_button, "coffee + button")

    def click_coffee_minus_button(self) -> None:
        self.click(self.coffee_minus_button, "coffee - button")

    def click_ratio_plus_button(self) -> None:
        self.click(self.ratio_plus_button, "ratio + button")

    def click_ratio_minus_button(self) -> None:
        self.click(self.ratio_minus_button, "ratio - button")

    def get_coffee_amount(self) -> str:
        return self.coffee_value.inner_text()

    def get_ratio(self) -> str:
        return self.ratio_value.inner_text()

    # --- Transition to brewing ---

    def click_start_brew_button(self) -> TimerPage:
        """Clicks Start Brew and returns TimerPage, since this
        action transitions the screen into the active brewing view."""
        self.click(self.start_brew_button, "start brew button")
        return TimerPage(self.page)
