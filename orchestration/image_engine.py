import requests
import config
from pathlib import Path

def search_for_images(keyword: str, num_candidates: int = 3) -> list | None:
    """
    Searches for a list of candidate images using the Pexels API.

    Args:
        keyword (str): The search term for the image.
        num_candidates (int): The number of image candidates to return.

    Returns:
        list | None: A list of dictionaries, each containing image info (id, url, alt),
                      or None on failure.
    """
    print(f"-> Searching for {num_candidates} image candidates for keyword: '{keyword}'...")
    
    headers = {"Authorization": config.PEXELS_API_KEY}
    params = {
        "query": keyword,
        "orientation": "landscape",
        "per_page": num_candidates
    }
    url = "https://api.pexels.com/v1/search"

    try:
        response = requests.get(url, headers=headers, params=params, timeout=15)
        response.raise_for_status()

        data = response.json()
        if data["photos"]:
            candidates = []
            for photo in data["photos"]:
                candidates.append({
                    "id": photo["id"],
                    "url": photo["src"]["large"], # The URL to download the image
                    "alt": photo["alt"] # The description we will send to the LLM
                })
            return candidates
        else:
            print(f"   ... No results found for '{keyword}'.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"An error occurred with the Pexels API request: {e}")
        return None
    except KeyError:
        print("   ... Error: Invalid response from Pexels. Check your API key.")
        return None

def download_image(image_url: str, keyword: str) -> str | None:
    """
    Downloads a chosen image and saves it to the cache.

    Args:
        image_url (str): The URL of the image to download.
        keyword (str): The original search term, used for the filename.

    Returns:
        str | None: The file path of the downloaded image, or None on failure.
    """
    sanitized_keyword = "".join(c for c in keyword if c.isalnum() or c in " _-").rstrip()
    cache_path = config.CACHE_DIR / f"{sanitized_keyword}.jpg"

    # Don't re-download if the exact same keyword was used and chosen before
    if cache_path.exists():
        print("   ... Image was already in cache.")
        return str(cache_path)
    
    print(f"   ... Downloading chosen image for '{keyword}'")
    try:
        image_response = requests.get(image_url, stream=True, timeout=15)
        image_response.raise_for_status()

        with open(cache_path, 'wb') as f:
            for chunk in image_response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"   ... Image downloaded and saved to {cache_path}")
        return str(cache_path)

    except requests.exceptions.RequestException as e:
        print(f"   ... Failed to download image: {e}")
        return None