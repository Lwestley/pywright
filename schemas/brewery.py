# schemas/brewery.py
"""Response schema for the Open Brewery DB API.

Pydantic models are the contract between the API and the tests: if the service
changes a field name, drops a field, or changes a type, validation fails loudly
at the boundary instead of surfacing as a confusing AttributeError deep in a
test. Only the fields the tests actually care about are marked required; the
rest are optional so a thinned-down payload still parses.
"""
from pydantic import BaseModel, ConfigDict


class Brewery(BaseModel):
    # Reject unknown keys so a renamed/added field is caught, not silently ignored.
    model_config = ConfigDict(extra="forbid")

    id: str
    name: str
    brewery_type: str

    address_1: str | None = None
    address_2: str | None = None
    address_3: str | None = None
    city: str | None = None
    state_province: str | None = None
    postal_code: str | None = None
    country: str | None = None
    longitude: float | None = None
    latitude: float | None = None
    phone: str | None = None
    website_url: str | None = None
    state: str | None = None
    street: str | None = None
