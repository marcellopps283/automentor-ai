import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file if it exists
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# API Keys and Tokens
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME", "student")

# GCP settings
GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT", "")
GOOGLE_CALENDAR_CREDENTIALS_FILE = os.getenv("GOOGLE_CALENDAR_CREDENTIALS_FILE", "")

# Fallbacks & Demo Mode
DEMO_MODE = os.getenv("DEMO_MODE", "true").lower() in ("true", "1", "yes")

# Local Storage Path for Memory
LOCAL_MEMORY_PATH = BASE_DIR / ".automentor_memory.json"
