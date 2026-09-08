# pywright

[![tests](https://github.com/Lwestley/pywright/actions/workflows/tests.yml/badge.svg)](https://github.com/Lwestley/pywright/actions/workflows/tests.yml)

UI test automation for the Dark Wizard Coffee pour-over web app, built with
[Playwright](https://playwright.dev/python/) and [pytest](https://docs.pytest.org/)
using the Page Object Model.

## Layout

```
pages/            Page objects (one class per screen)
  base_page.py      Shared navigation, waits, assertions, diagnostics
  brew_method_page.py   Brew method selection + recipe setup
  timer_page.py         Active brewing / countdown view
tests/
  unit/           Fast, browserless tests (Playwright is mocked)
  ui/             End-to-end tests that drive a real browser
  api/            (placeholder)
config.py         Central config: URLs, timeouts, brew method data
conftest.py       pytest fixtures — the `page` fixture, failure screenshots
```

### Method naming in page objects

A method that wraps a single `BasePage` call is named
`<basepage_method>_<locator>` (e.g. `click_pause_button` wraps
`self.click(self.pause_button)`). Methods with composite or semantic behavior
keep an intent name (`go_to_method`, `confirm_recipe_sections_visible`).

## Setup

Requires Python 3.12+.

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install chromium      # only needed for the UI tests
```

## Running tests

```bash
# Unit tests — no browser, ~0.1s
pytest tests/unit/ -v

# UI tests — launches Chromium, hits the live site
pytest tests/ui/

# UI tests with a visible browser window
pytest tests/ui/ --headed

# Everything
pytest
```

If you haven't activated the venv, prefix with `./venv/bin/python -m`:

```bash
./venv/bin/python -m pytest tests/unit/ -v
```

### Configuration

Override via environment variables (see `config.py` for all values):

| Variable         | Default                        | Purpose                          |
| ---------------- | ------------------------------ | -------------------------------- |
| `POUROVER_URL`   | `https://darkwizardcoffee.com` | Base URL under test              |
| `SCREENSHOT_DIR` | `test-results/screenshots`     | Where failure screenshots go     |

## Failure screenshots

When a UI test fails, `conftest.py` captures a full-page screenshot to
`SCREENSHOT_DIR` before the browser closes, named after the test node id and a
timestamp.

## CI

[`.github/workflows/tests.yml`](.github/workflows/tests.yml) runs `pytest tests/unit/`
on every pull request and on push to `main`. The `unit` check is required
before merging to `main`.

The UI tests are not in CI yet — they need `playwright install` and depend on
the live site.
