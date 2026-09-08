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

# --- Artifacts ---
# Where failure screenshots are written (relative to the repo root).
SCREENSHOT_DIR = os.getenv("SCREENSHOT_DIR", "test-results/screenshots")

# --- Brew methods ---
KALITA_185 = "Kalita 185"
V60 = "V60"
CHEMEX = "Chemex"
AEROPRESS = "Aeropress"