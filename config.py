# config.py - Enhanced Configuration Management
import os
from pathlib import Path
from dotenv import load_dotenv
from typing import Dict, Tuple

# Load environment variables
load_dotenv()

class PPTConfig:
    """Centralized configuration for PowerPoint generation"""
    
    # --- API Configuration ---
    API_KEYS = {
        'GEMINI': os.getenv("GEMINI_API_KEY"),
        'PEXELS': os.getenv("PEXELS_API_KEY")
    }
    
    # --- File System Paths ---
    BASE_DIR = Path(__file__).resolve().parent
    PATHS = {
        'output': BASE_DIR / "output",
        'cache': BASE_DIR / "downloads" / "cache",
        'temp': BASE_DIR / "downloads" / "temp",
        'assets': BASE_DIR / "assets",
        'fonts': BASE_DIR / "fonts",
        'templates': BASE_DIR / "templates"
    }
    
    # --- Presentation Standards ---
    SLIDE_DIMENSIONS = (16, 9)  # Width, Height in inches
    IMAGE_STANDARDS = {
        'min_resolution': (1920, 1080),  # Width, Height in pixels
        'aspect_ratio': (16, 9),
        'max_file_size_mb': 5
    }
    
    # --- API Rate Limits ---
    RATE_LIMITS = {
        'pexels': 200,  # requests/hour
        'gemini': 60    # requests/minute
    }
    
    @classmethod
    def validate(cls) -> Tuple[bool, str]:
        """Validate critical configurations"""
        # Check API keys
        if not cls.API_KEYS['GEMINI']:
            return False, "Gemini API key is required"
        if not cls.API_KEYS['PEXELS']:
            return False, "Pexels API key is required"
            
        # Ensure directories exist
        for path in cls.PATHS.values():
            path.mkdir(parents=True, exist_ok=True)
            
        return True, "Configuration valid"

# Initialize and validate configuration
config_valid, config_error = PPTConfig.validate()
if not config_valid:
    raise RuntimeError(f"Configuration Error: {config_error}")

# Legacy variable support (for gradual migration)
OUTPUT_DIR = PPTConfig.PATHS['output']
CACHE_DIR = PPTConfig.PATHS['cache']