import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

# --- API Keys ---
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY") # <-- ADD THIS
# UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY") # No longer primary

# --- Project Paths ---
# ... (rest of the file is unchanged)
BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
CACHE_DIR = BASE_DIR / "downloads" / "cache"

OUTPUT_DIR.mkdir(exist_ok=True)
CACHE_DIR.mkdir(exist_ok=True)

# --- Default Settings ---
PPT_SLIDE_WIDTH_INCHES = 16
PPT_SLIDE_HEIGHT_INCHES = 9