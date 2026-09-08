# pywright

[![tests](https://github.com/Lwestley/pywright/actions/workflows/tests.yml/badge.svg)](https://github.com/Lwestley/pywright/actions/workflows/tests.yml)

Test automation for the Dark Wizard Coffee pour-over web app, built with
[Playwright](https://playwright.dev/python/) and [pytest](https://docs.pytest.org/).
UI coverage uses the Page Object Model; API coverage uses a thin client wrapper
per service with [pydantic](https://docs.pydantic.dev/) response schemas.

## Layout

```
pages/            Page objects (one class per screen)
  base_page.py      Shared navigation, waits, assertions, diagnostics
  brew_method_page.py   Brew method selection + recipe setup
  timer_page.py         Active brewing / countdown view
api_clients/      API client wrappers (one class per service)
schemas/          Pydantic response schemas — the API contract
tests/
  unit/           Fast, browserless tests (Playwright is mocked)
  ui/             End-to-end tests that drive a real browser
  api/            API-client tests (requests.Session is mocked, no network)
config.py         Central config: URLs, timeouts, brew method data
conftest.py       pytest fixtures — the `page` fixture, failure screenshots
```

### Method naming in page objects

A method that wraps a single `BasePage` call is named
`<basepage_method>_<locator>` (e.g. `click_pause_button` wraps
`self.click(self.pause_button)`). Methods with composite or semantic behavior
keep an intent name (`go_to_method`, `confirm_recipe_sections_visible`).

### API tests

`api_clients/` holds one client class per service (e.g. `BreweryClient`). The
client owns URL building, query params, timeouts, and status handling, and takes
its `requests.Session` as an injected dependency. `schemas/` holds the pydantic
models the responses are validated against — schemas are strict (`extra="forbid"`),
so a renamed or added field fails at the boundary.

Tests under `tests/api/` inject a fake session, so they run with no network and
assert on the client's own logic: the URL it builds, the params it sends, how it
parses JSON into schema objects, and how it reports a non-2xx response (a typed
`BreweryAPIError` carrying method, URL, and status). Both the happy path and the
error path are covered.

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

# API tests — no network, requests is mocked
pytest tests/api/ -v

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

| Variable          | Default                            | Purpose                          |
| ----------------- | ---------------------------------- | -------------------------------- |
| `POUROVER_URL`    | `https://darkwizardcoffee.com`     | Base URL under test              |
| `SCREENSHOT_DIR`  | `test-results/screenshots`         | Where failure screenshots go     |
| `BREWERY_API_URL` | `https://api.openbrewerydb.org/v1` | Base URL for the API-client tests |

## Failure screenshots

When a UI test fails, `conftest.py` captures a full-page screenshot to
`SCREENSHOT_DIR` before the browser closes, named after the test node id and a
timestamp.

## CI

[`.github/workflows/tests.yml`](.github/workflows/tests.yml) runs `pytest tests/unit/`
and `pytest tests/api/` on every pull request and on push to `main`. The `unit`
check is required before merging to `main`. Both are browserless and networkless,
so they need no `playwright install` and no live site.

The UI tests are not in CI yet — they need `playwright install` and depend on
the live site.
