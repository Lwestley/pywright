# config.py
"""Central configuration values for the test suite.
Update values here rather than in individual test/page files."""

import os

# --- Landing page / environment ---
POUROVER_URL = os.getenv("POUROVER_URL", "https://darkwizardcoffee.com")

# --- Timeouts ---
DEFAULT_TIMEOUT_MS = 5000
BREW_START_TIMEOUT_MS = 10000
LONG_TIMEOUT_MS = 15000

# --- API ---
BREWERY_API_URL = os.getenv("BREWERY_API_URL", "https://api.openbrewerydb.org/v1")
API_TIMEOUT_S = 10

# --- Artifacts ---
# Where failure screenshots are written (relative to the repo root).
SCREENSHOT_DIR = os.getenv("SCREENSHOT_DIR", "test-results/screenshots")

# --- Brew methods ---
KALITA_185 = "Kalita 185"
V60 = "V60"
CHEMEX = "Chemex"
AEROPRESS = "AeroPress"

# Brew steps shown for each method. They differ - AeroPress is an immersion
# method (Fill/Steep/Press), not a pour-over, so it has no numbered pours.
BREW_STEPS = {
    KALITA_185: ("Bloom", "Pour 1", "Pour 2", "Pour 3", "Drain"),
    V60:        ("Bloom", "Pour 1", "Pour 2", "Pour 3", "Drain"),
    CHEMEX:     ("Bloom", "Pour 1", "Pour 2", "Pour 3", "Drain"),
    AEROPRESS:  ("Bloom", "Fill", "Steep", "Press"),
}