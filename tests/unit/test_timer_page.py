"""Unit tests for TimerPage.

No browser is launched here. Playwright's Page, its locators, and expect() are
replaced with mocks, so these tests check the page object's own logic in
isolation: which locators it builds, what its helper methods delegate to, and
how it reports failures. Fast to run and deterministic - the counterpart to the
end-to-end tests under tests/ui/.
"""
from unittest.mock import MagicMock, patch

import pytest

import config
from pages import base_page
from pages.timer_page import TimerPage


@pytest.fixture
def fake_page():
    """Stand-in for a Playwright Page.

    Each get_by_* call is memoised on its arguments, so a locator looked up
    twice (once in the constructor, once in a test) is the *same* mock object
    and assertions like `page.pause_button.click.assert_called_once()` work.
    """
    page = MagicMock(name="page")
    page.url = "https://darkwizardcoffee.com/brew"

    by_test_id = {}
    page.get_by_test_id.side_effect = lambda tid: by_test_id.setdefault(
        tid, MagicMock(name=f"locator[test_id={tid!r}]")
    )

    by_role = {}
    page.get_by_role.side_effect = lambda role, name=None: by_role.setdefault(
        (role, name), MagicMock(name=f"locator[role={role!r} name={name!r}]")
    )

    by_text = {}
    page.get_by_text.side_effect = lambda text, exact=False: by_text.setdefault(
        (text, exact), MagicMock(name=f"locator[text={text!r}]")
    )
    return page


@pytest.fixture
def noop_expect():
    """Patch base_page.expect so visibility assertions pass silently."""
    with patch.object(base_page, "expect") as mocked:
        yield mocked


@pytest.fixture
def timer_page(fake_page, noop_expect):
    """A constructed TimerPage on the fake page (landmark check stubbed out)."""
    return TimerPage(fake_page)


# --- Constructor: locator wiring ---

def test_constructor_builds_expected_locators(timer_page, fake_page):
    assert timer_page.countdown_display is fake_page.get_by_test_id("step-countdown")
    assert timer_page.current_step_label is fake_page.get_by_test_id("current-step-label")
    assert timer_page.pause_button is fake_page.get_by_role("button", name="Pause")
    assert timer_page.resume_button is fake_page.get_by_role("button", name="Resume")
    assert timer_page.reset_button is fake_page.get_by_role("button", name="Reset")


# --- Constructor: landmark visibility check ---

def test_constructor_waits_for_countdown_with_long_timeout(fake_page, noop_expect):
    timer_page = TimerPage(fake_page)

    noop_expect.assert_called_once_with(timer_page.countdown_display)
    noop_expect.return_value.to_be_visible.assert_called_once_with(
        timeout=config.LONG_TIMEOUT_MS
    )


def test_constructor_raises_with_context_when_countdown_never_appears(fake_page):
    with patch.object(base_page, "expect") as mocked:
        mocked.return_value.to_be_visible.side_effect = AssertionError("timed out")

        with pytest.raises(AssertionError) as excinfo:
            TimerPage(fake_page)

    message = str(excinfo.value)
    assert "TimerPage" in message
    assert "countdown display" in message
    assert str(config.LONG_TIMEOUT_MS) in message
    assert fake_page.url in message


# --- Actions delegate to the right locator ---

@pytest.mark.parametrize(
    "method_name, locator_attr",
    [
        ("click_pause_button", "pause_button"),
        ("click_resume_button", "resume_button"),
        ("click_reset_button", "reset_button"),
    ],
)
def test_control_buttons_click_their_locator(timer_page, method_name, locator_attr):
    getattr(timer_page, method_name)()

    getattr(timer_page, locator_attr).click.assert_called_once_with()


# --- State reads ---

def test_get_current_step_returns_label_text(timer_page):
    timer_page.current_step_label.inner_text.return_value = "Bloom"

    assert timer_page.get_current_step() == "Bloom"


@pytest.mark.parametrize("visible", [True, False])
def test_is_brewing_reflects_countdown_visibility(timer_page, visible):
    timer_page.countdown_display.is_visible.return_value = visible

    assert timer_page.is_brewing() is visible


def test_assert_current_step_label_has_text_passes_expected_value(timer_page, noop_expect):
    timer_page.assert_current_step_label_has_text("Pour 1")

    noop_expect.assert_called_with(timer_page.current_step_label)
    noop_expect.return_value.to_have_text.assert_called_with(
        "Pour 1", timeout=config.DEFAULT_TIMEOUT_MS
    )


def test_assert_current_step_label_has_text_reraises_with_context(timer_page):
    with patch.object(base_page, "expect") as mocked:
        mocked.return_value.to_have_text.side_effect = AssertionError("mismatch")

        with pytest.raises(AssertionError) as excinfo:
            timer_page.assert_current_step_label_has_text("Drain")

    message = str(excinfo.value)
    assert "current step label" in message
    assert "Drain" in message
    assert "TimerPage" in message
