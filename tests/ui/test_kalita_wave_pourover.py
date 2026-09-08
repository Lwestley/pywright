from pages.brew_method_page import BrewMethodPage
from config import POUROVER_URL


def test_kalita_185_pourover_page_loads_with_expected_elements(page):
    page.goto(POUROVER_URL)

    brew_method_page = BrewMethodPage(page)
    brew_method_page.confirm_recipe_sections_visible()
    brew_method_page.confirm_brew_steps_visible()

    timer_page = brew_method_page.click_start_brew_button()
    timer_page.assert_current_step_label_has_text("Bloom")
