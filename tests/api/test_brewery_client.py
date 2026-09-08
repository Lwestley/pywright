"""Tests for BreweryClient.

No network is used. A fake requests.Session is injected into the client, so
these tests check the client's own logic in isolation: the URL it builds, the
query params it sends, how it turns JSON into schema objects, and how it reports
a non-2xx response. Fast and deterministic - the API-layer counterpart to the
mocked page-object tests under tests/unit/.
"""
from unittest.mock import MagicMock

import pytest
import requests

import config
from api_clients.brewery_client import BreweryAPIError, BreweryClient
from schemas.brewery import Brewery

SAMPLE_BREWERY = {
    "id": "ferment-brewing-hood-river",
    "name": "Ferment Brewing",
    "brewery_type": "regional",
    "city": "Hood River",
    "state": "Oregon",
    "country": "United States",
}


def _response(*, json_data, status_code=200):
    """Build a stand-in for a requests.Response.

    raise_for_status() mirrors the real thing: it raises requests.HTTPError for
    a 4xx/5xx and does nothing for a 2xx.
    """
    resp = MagicMock(name=f"Response[{status_code}]")
    resp.status_code = status_code
    resp.json.return_value = json_data
    if status_code >= 400:
        resp.raise_for_status.side_effect = requests.HTTPError(f"{status_code} error")
    else:
        resp.raise_for_status.return_value = None
    return resp


@pytest.fixture
def session():
    """A fake requests.Session whose .get() returns a 200 with one brewery."""
    fake = MagicMock(name="Session", spec=requests.Session)
    fake.get.return_value = _response(json_data=[SAMPLE_BREWERY])
    return fake


@pytest.fixture
def client(session):
    return BreweryClient(base_url="https://api.test/v1", session=session)


# --- Happy path: request building ---

def test_list_breweries_hits_the_right_url_and_parses_the_response(client, session):
    breweries = client.list_breweries()

    session.get.assert_called_once()
    url, kwargs = session.get.call_args.args[0], session.get.call_args.kwargs
    assert url == "https://api.test/v1/breweries"
    assert kwargs["timeout"] == config.API_TIMEOUT_S

    assert len(breweries) == 1
    assert isinstance(breweries[0], Brewery)
    assert breweries[0].name == "Ferment Brewing"


def test_list_breweries_only_sends_non_none_filters(client, session):
    client.list_breweries(by_city="Hood River", per_page=5)

    assert session.get.call_args.kwargs["params"] == {
        "by_city": "Hood River",
        "per_page": 5,
    }


def test_list_breweries_sends_no_params_when_unfiltered(client, session):
    client.list_breweries()

    assert session.get.call_args.kwargs["params"] is None


def test_get_brewery_builds_the_id_path(client, session):
    session.get.return_value = _response(json_data=SAMPLE_BREWERY)

    brewery = client.get_brewery("ferment-brewing-hood-river")  # type: ignore[reportOptionalMemberAccess]

    assert session.get.call_args.args[0] == (
        "https://api.test/v1/breweries/ferment-brewing-hood-river"
    )
    assert brewery.id == "ferment-brewing-hood-river"


# --- Error path: non-2xx ---

def test_get_brewery_raises_with_context_on_404(client, session):
    session.get.return_value = _response(json_data={"message": "not found"}, status_code=404)

    with pytest.raises(BreweryAPIError) as excinfo:
        client.get_brewery("does-not-exist")

    err = excinfo.value
    assert err.status_code == 404
    message = str(err)
    assert "GET" in message
    assert "does-not-exist" in message
    assert "404" in message
    # the original HTTPError is preserved as the cause
    assert isinstance(excinfo.value.__cause__, requests.HTTPError)


# --- Schema enforcement ---

def test_missing_required_field_fails_validation(client, session):
    # payload with no brewery_type - the schema requires it
    session.get.return_value = _response(json_data=[{"id": "x", "name": "No Type Co"}])

    with pytest.raises(Exception) as excinfo:
        client.list_breweries()

    assert "brewery_type" in str(excinfo.value)


def test_unexpected_field_fails_validation(client, session):
    session.get.return_value = _response(
        json_data=[{**SAMPLE_BREWERY, "surprise_field": "!!"}]
    )

    with pytest.raises(Exception) as excinfo:
        client.list_breweries()

    assert "surprise_field" in str(excinfo.value)
