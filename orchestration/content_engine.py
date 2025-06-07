import json
from .gemini_client import gemini_chat

# --- AI Configuration ---

def generate_slide_outline(topic: str, num_slides: int) -> list:
    """
    Generate a structured outline for the presentation using Gemini.
    """
    prompt = f"""Generate a professional presentation outline for the topic '{topic}' with {num_slides} slides.
    Each slide should have a title, body content, and visual focus.
    Return the response in JSON format with the following structure:
    [
        {{
            "slide_title": "string",
            "slide_body": "string",
            "visual_focus": "string",
            "supporting_visuals": ["string"]
        }}
    ]
    Make it engaging and include relevant statistics and examples."""

    response = gemini_chat(prompt)
    try:
        # Extract JSON from the response
        json_str = response.strip()
        if json_str.startswith('```json'):
            json_str = json_str[7:]
        if json_str.endswith('```'):
            json_str = json_str[:-3]
        return json.loads(json_str.strip())
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response: {e}")
        print(f"Raw response: {response}")
        return []

def decide_slide_layout(slide_data: dict) -> str:
    """
    Decide the best layout for a slide based on its content using Gemini.
    """
    prompt = f"""Based on this slide content, suggest the best layout type:
    Title: {slide_data.get('slide_title', '')}
    Content: {slide_data.get('slide_body', '')}
    Visual Focus: {slide_data.get('visual_focus', '')}
    
    Choose from these layouts:
    - Title Layout (for first slide)
    - Photo Layout (for slides with main image)
    - Diagram Layout (for slides with charts/diagrams)
    - Text Layout (for text-heavy slides)
    
    Return only the layout name."""

    response = gemini_chat(prompt)
    return response.strip()

def generate_visual_keyword(slide_title: str, slide_body: str) -> str:
    """
    Generate a keyword for image search using Gemini.
    """
    prompt = f"""Generate a specific, descriptive keyword for finding a relevant image for this slide:
    Title: {slide_title}
    Content: {slide_body}
    
    The keyword should be specific enough to find a relevant image but not too long.
    Return only the keyword."""

    response = gemini_chat(prompt)
    return response.strip()

def generate_diagram_code(slide_data: dict) -> str:
    """
    Generate Python code for creating a diagram using Gemini.
    """
    prompt = f"""Generate Python code using matplotlib to create a professional diagram for this slide:
    Title: {slide_data.get('slide_title', '')}
    Content: {slide_data.get('slide_body', '')}
    
    The code should:
    1. Create a clear, professional visualization
    2. Use appropriate colors and styling
    3. Include proper labels and title
    4. Save the output as a PNG file
    
    Return only the Python code."""

    response = gemini_chat(prompt)
    return response.strip()