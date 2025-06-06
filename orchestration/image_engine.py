import requests
import config
from pathlib import Path

def get_image_for_keyword(keyword: str) -> str | None:
    """
    Searches for an image using the Pexels API and downloads it.
    Checks cache first to avoid re-downloading.

    Args:
        keyword (str): The search term for the image.

    Returns:
        str | None: The file path of the downloaded image, or None on failure.
    """
    print(f"-> Searching for image with keyword: '{keyword}' (using Pexels)...")

    # Sanitize keyword to create a valid filename
    sanitized_keyword = "".join(c for c in keyword if c.isalnum() or c in " _-").rstrip()
    cache_path = config.CACHE_DIR / f"{sanitized_keyword}.jpg"

    # 1. Check cache
    if cache_path.exists():
        print("   ... Image found in cache.")
        return str(cache_path)

    # 2. Call the Pexels API
    headers = {"Authorization": config.PEXELS_API_KEY}
    params = {
        "query": keyword,
        "orientation": "landscape",
        "per_page": 1
    }
    url = "https://api.pexels.com/v1/search"

    try:
        response = requests.get(url, headers=headers, params=params, timeout=15)
        response.raise_for_status()

        data = response.json()
        if data["photos"]:
            # Pexels provides multiple sizes, 'large' or 'original' is good.
            image_url = data["photos"][0]["src"]["large"] 
            
            # 3. Download the image
            image_response = requests.get(image_url, stream=True, timeout=15)
            image_response.raise_for_status()

            # 4. Save to cache
            with open(cache_path, 'wb') as f:
                for chunk in image_response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"   ... Image downloaded and saved to {cache_path}")
            return str(cache_path)
        else:
            print(f"   ... No results found for '{keyword}'.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"An error occurred with the Pexels API request: {e}")
        return None
    except KeyError:
        # This can happen if the API key is wrong and Pexels returns an error message
        # instead of the expected JSON structure.
        print("   ... Error: Invalid response from Pexels. Check your API key.")
        return None