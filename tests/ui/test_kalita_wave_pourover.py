from pages.kalita_wave_page import KalitaWavePage
from config import POUROVER_URL


def test_page_loads_with_expected_elements(page):
    kalita_page = KalitaWavePage(page)
    kalita_page.goto(POUROVER_URL)
    kalita_page.wait_for_load()
    assert kalita_page.start_brew_button.is_visible()