import hashlib
from pathlib import Path
import requests
import config
import graphviz

def search_and_download_photo(keyword: str, slide_title: str) -> str | None:
    print(f"-> Searching for photo with keyword: '{keyword[:60]}...'")
    filename = hashlib.md5(keyword.encode()).hexdigest() + ".jpg"
    cache_path = config.PPTConfig.PATHS['cache'] / filename
    if cache_path.exists():
        print("   ... Photo found in cache.")
        return str(cache_path)
    try:
        headers = {"Authorization": config.PPTConfig.API_KEYS['PEXELS']}
        params = {"query": keyword, "orientation": "landscape", "per_page": 1}
        url = "https://api.pexels.com/v1/search"
        response = requests.get(url, headers=headers, params=params, timeout=20)
        response.raise_for_status()
        data = response.json()
        if not data.get("photos"):
            return None
        image_url = data["photos"][0]["src"].get("large2x")
        image_response = requests.get(image_url, stream=True, timeout=30)
        image_response.raise_for_status()
        with open(cache_path, 'wb') as f:
            for chunk in image_response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"   ... Photo downloaded: {filename}")
        return str(cache_path)
    except Exception as e:
        print(f"   ... Photo acquisition error: {e}")
        return None

def render_diagram_local(dot_code: str, slide_title: str) -> str | None:
    print(f"-> Rendering diagram locally for '{slide_title}'...")
    filename = "diagram_" + hashlib.md5(slide_title.encode()).hexdigest() + ".png"
    cache_path = config.PPTConfig.PATHS['cache'] / filename
    if cache_path.exists():
        print("   ... Diagram found in cache.")
        return str(cache_path)
    try:
        graph = graphviz.Source(dot_code, format='png', engine='dot')
        output_path = str(cache_path).replace('.png', '')
        rendered_path = graph.render(outfile=output_path, cleanup=True, view=False)
        return rendered_path
    except Exception as e:
        print(f"   ... Failed to render diagram locally: {e}")
        return None