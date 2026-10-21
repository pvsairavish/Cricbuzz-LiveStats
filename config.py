"""
Cricbuzz LiveStats — Centralized Configuration Module
------------------------------------------------------
Manages project paths, API keys, database settings, and runtime flags.
Supports Streamlit Secrets, .env files, and OS environment variables.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Base Project Directories
BASE_DIR = Path(__file__).resolve().parent
DATABASE_DIR = BASE_DIR / "database"
SQL_DIR = BASE_DIR / "sql"
ASSETS_DIR = BASE_DIR / "assets"
PAGES_DIR = BASE_DIR / "pages"

# Load local .env file if it exists
ENV_PATH = BASE_DIR / ".env"
if ENV_PATH.exists():
    load_dotenv(dotenv_path=ENV_PATH)

# Database Configuration
DB_NAME = "cricbuzz.db"
DB_PATH = DATABASE_DIR / DB_NAME
SCHEMA_PATH = DATABASE_DIR / "schema.sql"
SEED_DATA_PATH = DATABASE_DIR / "seed_data.sql"
INDEXES_PATH = DATABASE_DIR / "indexes.sql"

# RapidAPI / Cricbuzz API Configuration
def get_secret(key: str, default: str = "") -> str:
    """Retrieve secret from Streamlit secrets, environment variables, or fallback."""
    try:
        import streamlit as st
        if hasattr(st, "secrets") and key in st.secrets:
            return str(st.secrets[key])
    except Exception:
        pass
    return os.getenv(key, default)

RAPIDAPI_KEY = get_secret("RAPIDAPI_KEY", "")
RAPIDAPI_HOST = get_secret("RAPIDAPI_HOST", "cricbuzz-cricket.p.rapidapi.com")
RAPIDAPI_BASE_URL = f"https://{RAPIDAPI_HOST}"

# Operational Mode
# If RAPIDAPI_KEY is empty, the application seamlessly runs on Mock / Local Seed data
IS_LIVE_API_ENABLED = bool(RAPIDAPI_KEY and RAPIDAPI_KEY.strip() != "")

# Cache Time-To-Live (in seconds)
CACHE_TTL_LIVE_MATCHES = 60         # 1 minute for live ongoing scores
CACHE_TTL_RECENT_MATCHES = 300      # 5 minutes for recent matches
CACHE_TTL_PLAYER_STATS = 86400      # 24 hours for historical career statistics

# Application Branding & Metadata
APP_TITLE = "Cricbuzz LiveStats"
APP_SUBTITLE = "Real-Time Cricket Insights & SQL-Based Analytics"
APP_ICON = "🏏"
APP_VERSION = "1.0.0"
APP_LAYOUT = "wide"
PAGE_THEME_COLOR = "#008767"        # Cricbuzz green signature
DARK_BG_COLOR = "#0F172A"
CARD_BG_COLOR = "#1E293B"
