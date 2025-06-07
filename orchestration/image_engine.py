import hashlib
from pathlib import Path
import requests
import config
import graphviz
from PIL import Image
import io
import os
import json
from .gemini_client import gemini_chat, gemini_vision
from typing import Optional

def search_and_download_photo(keyword: str, is_background: bool = False) -> str:
    """
    Search for and download a photo using Pexels API.
    """
    pexels_api_key = os.getenv('PEXELS_API_KEY')
    if not pexels_api_key:
        print("WARNING: Pexels API key not found. Using placeholder image.")
        return None

    try:
        # Search for the image with enhanced parameters
        search_url = f"https://api.pexels.com/v1/search"
        params = {
            "query": keyword,
            "per_page": 3,  # Get multiple candidates
            "orientation": "landscape" if is_background else "any",
            "size": "large",
            "color": "vibrant" if is_background else "any"  # Prefer vibrant colors for backgrounds
        }
        headers = {"Authorization": pexels_api_key}
        
        response = requests.get(search_url, params=params, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        if not data["photos"]:
            print(f"No images found for keyword: {keyword}")
            return None
            
        # Get the best image URL (first one)
        image_url = data["photos"][0]["src"]["original"]
        
        # Download the image
        image_response = requests.get(image_url)
        image_response.raise_for_status()
        
        # Process the image
        img = Image.open(io.BytesIO(image_response.content))
        
        # Save the original image
        output_dir = "output/images"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f"{keyword.replace(' ', '_')}.jpg")
        img.save(output_path, "JPEG", quality=95)
        
        # Optimize the image for PowerPoint
        optimized_path = optimize_image_for_ppt(output_path, is_background)
        
        return optimized_path
    except Exception as e:
        print(f"Error downloading photo: {e}")
        return None

def render_diagram_local(dot_code: str, slide_title: str) -> Optional[str]:
    print(f"-> Rendering diagram locally for '{slide_title}'...")
    filename = "diagram_" + hashlib.md5(slide_title.encode()).hexdigest() + ".png"
    cache_path = config.PPTConfig.PATHS['cache'] / filename
    
    if cache_path.exists():
        print("   ... Diagram found in cache.")
        return str(cache_path)
        
    try:
        # Configure graphviz for high quality
        graph = graphviz.Source(dot_code, format='png', engine='dot')
        graph.attr(dpi='300')  # High DPI for better quality
        
        # Set graph attributes for better rendering
        graph.attr('graph', 
                  rankdir='TB',
                  splines='ortho',
                  nodesep='0.8',
                  ranksep='1.0',
                  pad='0.5',
                  margin='0.2')
                  
        graph.attr('node',
                  shape='box',
                  style='rounded,filled',
                  margin='0.3,0.1',
                  fontname='Arial',
                  fontsize='12',
                  height='0.4',
                  width='0.8')
                  
        graph.attr('edge',
                  fontname='Arial',
                  fontsize='10',
                  penwidth='1.5')
        
        output_path = str(cache_path).replace('.png', '')
        rendered_path = graph.render(outfile=output_path, cleanup=True, view=False)
        
        # Post-process the image for better quality
        if rendered_path:
            img = Image.open(rendered_path)
            # Convert to RGBA if needed
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
                
            # Enhance diagram quality
            img = img.resize((int(img.width * 1.5), int(img.height * 1.5)), Image.Resampling.LANCZOS)
            
            # Save with high quality
            img.save(rendered_path, 'PNG', optimize=True)
            
        return rendered_path
        
    except Exception as e:
        print(f"   ... Failed to render diagram locally: {e}")
        return None

def get_supporting_images(slide_data: dict) -> list:
    """
    Generate and download supporting images for a slide using Gemini.
    """
    prompt = f"""Based on this slide content, suggest 2-3 specific images that would enhance the presentation:
    Title: {slide_data.get('slide_title', '')}
    Content: {slide_data.get('slide_body', '')}
    Visual Focus: {slide_data.get('visual_focus', '')}
    
    For each image, provide:
    1. A specific, descriptive keyword for image search
    2. A brief explanation of why this image would be relevant
    
    Return the response in JSON format:
    [
        {{
            "keyword": "string",
            "explanation": "string"
        }}
    ]"""

    try:
        response = gemini_chat(prompt)
        print(f"Raw response from Gemini: {response}")
        
        # Strip markdown code block markers if present
        if response.startswith('```json'):
            response = response[7:]
        if response.endswith('```'):
            response = response[:-3]
        
        image_suggestions = json.loads(response.strip())
        
        supporting_images = []
        for suggestion in image_suggestions:
            image_path = search_and_download_photo(suggestion["keyword"])
            if image_path:
                supporting_images.append(image_path)
        
        return supporting_images
    except Exception as e:
        print(f"Error generating supporting images: {e}")
        return []

def analyze_image_quality(image_path: str) -> bool:
    """
    Analyze image quality using Gemini Vision.
    """
    prompt = """Analyze this image and determine if it's suitable for a professional presentation.
    Consider:
    1. Image quality and resolution
    2. Professional appearance
    3. Relevance to business context
    4. Visual clarity
    
    Respond with only 'yes' or 'no'."""
    
    try:
        response = gemini_vision(prompt, image_path)
        return "yes" in response.lower()
    except Exception as e:
        print(f"Error analyzing image quality: {e}")
        return True  # Default to accepting the image if analysis fails

def optimize_image_for_ppt(image_path: str, is_background: bool = False) -> str:
    """
    Optimize image dimensions and quality for PowerPoint presentation.
    Returns the path to the optimized image.
    """
    try:
        img = Image.open(image_path)
        
        # Get original dimensions
        width, height = img.size
        
        # Calculate target dimensions based on slide size (16:9 aspect ratio)
        if is_background:
            # For background images, ensure they're large enough and maintain aspect ratio
            target_width = 2560  # Increased for better quality
            target_height = 1440
            ratio = min(target_width/width, target_height/height)
            target_width = int(width * ratio)
            target_height = int(height * ratio)
        else:
            # For supporting images, maintain aspect ratio but limit size
            max_width = 1200  # Increased for better quality
            max_height = 900
            ratio = min(max_width/width, max_height/height)
            target_width = int(width * ratio)
            target_height = int(height * ratio)
        
        # Resize image using high-quality Lanczos resampling
        img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
        
        # Enhance image quality
        if is_background:
            # Increase contrast slightly for better visibility
            from PIL import ImageEnhance
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.1)
        
        # Save optimized image
        output_dir = "output/images/optimized"
        os.makedirs(output_dir, exist_ok=True)
        optimized_path = os.path.join(output_dir, f"opt_{os.path.basename(image_path)}")
        img.save(optimized_path, "JPEG", quality=95, optimize=True)
        
        return optimized_path
    except Exception as e:
        print(f"Error optimizing image: {e}")
        return image_path

def get_image_dimensions(image_path: str) -> tuple:
    """
    Get image dimensions in pixels.
    Returns (width, height) tuple.
    """
    try:
        with Image.open(image_path) as img:
            return img.size
    except Exception as e:
        print(f"Error getting image dimensions: {e}")
        return (0, 0)