# pages/kalita_wave_page.py
from pages.timer_page import TimerPage


class KalitaWavePage(TimerPage):
    def __init__(self, page):
        super().__init__(page)
        # Kalita Wave-specific locators go here, e.g.:
        # self.bloom_time_input = page.get_by_label("Bloom Time")
        # self.ratio_input = page.get_by_label("Coffee Ratio")

    def set_bloom_time(self, seconds: int) -> None:
        self.bloom_time_input.fill(str(seconds))