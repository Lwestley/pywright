from pages.brew_method_page import BrewMethodPage
from config import POUROVER_URL


def test_kalita_185_pourover_page_loads_with_expected_elements(page):
    # Navigate to the pourover page
    page.goto(POUROVER_URL)
    brew_method_page = BrewMethodPage(page)
    brew_method_page.wait_for_load()
    assert brew_method_page.is_kalita_185_visible(), "Kalita 185 label should be visible"

    # Confirm all text is visible
    for text in ("Coffee", "Ratio", "Water", "Bloom", "Pour 1", "Pour 2", "Pour 3", "Drain"):
        brew_method_page.assert_text_visible(text)

    # Click start brew button and navigate to timer page
    timer_page = brew_method_page.start_brew()
    assert timer_page.is_brewing(), "timer should be counting after Start Brew"

    # Confirm the current step is visible
    bloom = "Bloom"
    timer_page.confirm_current_step_visible(bloom)