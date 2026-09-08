# pages/timer_page.py
import config
from pages.base_page import BasePage


class TimerPage(BasePage):
    """Page object for the active brewing/timer view, shown after
    Start Brew is clicked on BrewMethodPage.
    """

    def __init__(self, page):
        super().__init__(page)

        # --- Timer display ---
        self.countdown_display = page.get_by_test_id("step-countdown")  # the actual counting number
        self.current_step_label = page.locator("REPLACE_WITH_CODEGEN")  # e.g. "Bloom", "Pour 1"

        # --- Controls ---
        self.pause_button = page.get_by_role("button", name="Pause")   # confirm real label
        self.reset_button = page.get_by_role("button", name="Reset Brew")    # confirm real label
        self.resume_button = page.get_by_role("button", name="Resume")  # confirm real label

        # --- Step list (if visible during brewing, e.g. highlighting active step) ---
        self.bloom_step = page.get_by_text("Bloom")
        self.pour_1_step = page.get_by_text("Pour 1")
        self.pour_2_step = page.get_by_text("Pour 2")
        self.pour_3_step = page.get_by_text("Pour 3")
        self.drain_step = page.get_by_text("Drain")

        self.confirm_timer_started()

    # --- Page ready check ---

    def confirm_timer_started(self) -> None:
        """Landmark check: the countdown display appears once the brew is
        running. Start Brew can lag, so allow the longer brew-start budget.
        """
        self.assert_visible(self.countdown_display, "countdown display", timeout_ms=config.LONG_TIMEOUT_MS)

    # --- State checks ---

    def confirm_text_visible(self, text: str) -> None:
      """Confirm any text is visible on the brew method screen.
      Pass whatever you want to assert from the test, e.g.
      brew_page.confirm_text_visible("Coffee").
      """
      self.assert_text_visible(text, exact=True)

    def is_brewing(self) -> bool:
        """True once the timer view is showing and counting."""
        return self.countdown_display.is_visible()

    def get_current_step(self) -> str:
        return self.current_step_label.inner_text()

    def confirm_current_step_visible(self, step: str) -> None:
      """Confirm the current step is visible on the timer page.
      Pass whatever you want to assert from the test, e.g.
      timer_page.confirm_current_step_visible("Bloom").
      """
      self.assert_text_visible(step)

    # --- Actions ---

    def pause(self) -> None:
        assert self.pause_button.is_visible(), "Pause button not visible, cannot pause brew"
        self.pause_button.click()

    def resume(self) -> None:
        assert self.resume_button.is_visible(), "Resume button not visible, cannot resume brew"
        self.resume_button.click()

    def reset(self) -> None:
        assert self.reset_button.is_visible(), "Reset button not visible, cannot reset brew"
        self.reset_button.click()