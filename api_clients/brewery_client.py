# api_clients/brewery_client.py
"""Client wrapper for the Open Brewery DB API (https://www.openbrewerydb.org/).

One class per service. Tests talk to this wrapper, not to `requests` directly,
so URL building, query params, status-code handling, and response parsing live
in one place. The `requests.Session` is injectable, which is what makes the
client testable without a network: a test passes in a fake session and asserts
on how the client called it and what it did with the response.
"""
from __future__ import annotations

import requests

import config
from schemas.brewery import Brewery


class BreweryAPIError(RuntimeError):
    """Raised when the API returns a non-2xx response.

    Wraps the underlying requests.HTTPError but adds the method, URL, and status
    so a failing test says what call broke without a stack-trace dig.
    """

    def __init__(self, method: str, url: str, status_code: int):
        self.status_code = status_code
        super().__init__(f"{method} {url} -> {status_code}")


class BreweryClient:
    def __init__(self, base_url: str | None = None, session: requests.Session | None = None):
        self.base_url = (base_url or config.BREWERY_API_URL).rstrip("/")
        self.session = session or requests.Session()

    def _get(self, path: str, params: dict | None = None) -> object:
        url = f"{self.base_url}/{path.lstrip('/')}"
        response = self.session.get(url, params=params, timeout=config.API_TIMEOUT_S)
        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            raise BreweryAPIError("GET", url, response.status_code) from exc
        return response.json()

    def list_breweries(
        self,
        *,
        by_type: str | None = None,
        by_city: str | None = None,
        per_page: int | None = None,
    ) -> list[Brewery]:
        """Return breweries matching the given filters, validated against the schema.

        Only non-None filters are sent as query params, so the request stays
        clean and the test can assert exactly which params went out.
        """
        params = {
            "by_type": by_type,
            "by_city": by_city,
            "per_page": per_page,
        }
        params = {k: v for k, v in params.items() if v is not None}
        payload = self._get("breweries", params=params or None)
        return [Brewery.model_validate(item) for item in payload]

    def get_brewery(self, brewery_id: str) -> Brewery:
        """Fetch a single brewery by id. Raises BreweryAPIError on 404."""
        payload = self._get(f"breweries/{brewery_id}")
        return Brewery.model_validate(payload)
