# pages/timer_page.py
import config
from pages.base_page import BasePage


class TimerPage(BasePage):
    """Page object for the active brewing/timer view, shown after
    Start Brew is clicked on BrewMethodPage.

    Method naming: a method that is a thin wrapper around one BasePage call is
    named <basepage_method>_<locator>, e.g. click_pause_button wraps
    self.click(self.pause_button).
    """

    def __init__(self, page):
        super().__init__(page)

        # --- Timer display ---
        self.countdown_display = page.get_by_test_id("step-countdown")       # e.g. "28s"
        self.current_step_label = page.get_by_test_id("current-step-label")  # e.g. "Bloom"

        # --- Controls ---
        self.pause_button = page.get_by_role("button", name="Pause")
        self.resume_button = page.get_by_role("button", name="Resume")
        self.reset_button = page.get_by_role("button", name="Reset")

        # --- Step list (if visible during brewing, e.g. highlighting active step) ---
        self.bloom_step = page.get_by_text("Bloom")
        self.pour_1_step = page.get_by_text("Pour 1")
        self.pour_2_step = page.get_by_text("Pour 2")
        self.pour_3_step = page.get_by_text("Pour 3")
        self.drain_step = page.get_by_text("Drain")

        self.assert_countdown_display_visible()

    # --- Page ready check ---

    def assert_countdown_display_visible(self) -> None:
        """Landmark check: the countdown display appears once the brew is
        running. Start Brew can lag, so allow the longer brew-start budget.
        """
        self.assert_visible(self.countdown_display, "countdown display",
                            timeout_ms=config.LONG_TIMEOUT_MS)

    # --- State checks ---

    def assert_current_step_label_has_text(self, expected: str) -> None:
        """Confirm the timer is on the given brew step, e.g. "Bloom"."""
        self.assert_has_text(self.current_step_label, expected, "current step label")

    def is_brewing(self) -> bool:
        """True once the timer view is showing and counting."""
        return self.countdown_display.is_visible()

    def get_current_step(self) -> str:
        return self.current_step_label.inner_text()

    # --- Actions ---

    def click_pause_button(self) -> None:
        self.click(self.pause_button, "pause button")

    def click_resume_button(self) -> None:
        self.click(self.resume_button, "resume button")

    def click_reset_button(self) -> None:
        self.click(self.reset_button, "reset button")
