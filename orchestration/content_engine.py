import json
import config
import google.generativeai as genai

# --- AI Configuration ---
try:
    # Use the new config class
    genai.configure(api_key=config.PPTConfig.API_KEYS['GOOGLE'])
except Exception as e:
    print(f"CRITICAL: Could not configure Google Gemini API. Error: {e}")

def generate_slide_outline(topic: str, slide_count: int) -> list | None:
    print(f"-> AI generating text outline for '{topic}'...")
    prompt = f'Create a presentation outline for the topic "{topic}". Generate exactly {slide_count} slides. For each slide, provide a "slide_title" and a "slide_body". Respond ONLY with a valid JSON list of objects.'
    try:
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        response = model.generate_content(prompt)
        content = response.text.strip().replace("```json", "").replace("```", "").strip()
        return json.loads(content)
    except Exception as e:
        print(f"   ... Error generating slide outline: {e}")
        return None

def decide_slide_layout(slide_title: str, slide_body: str) -> str:
    print(f"-> AI choosing layout for '{slide_title}'...")
    try:
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        prompt = f'For a slide titled "{slide_title}", which layout is best? Your ONLY options are "Photo Layout" or "Diagram Layout". Choose "Diagram Layout" if the topic is a process or concept. Otherwise, choose "Photo Layout". Respond with only the chosen layout name.'
        response = model.generate_content(prompt)
        layout = response.text.strip().replace('"', '')
        return "Diagram Layout" if "Diagram" in layout else "Photo Layout"
    except Exception as e:
        print(f"   ... Layout decision failed ({e}). Defaulting to Photo Layout.")
        return "Photo Layout"

def generate_visual_keyword(slide_title: str, layout: str) -> str:
    print(f"-> AI generating visual keyword for '{slide_title}'...")
    keyword_type = "a detailed, natural-language description of its purpose" if "Diagram" in layout else "a simple Pexels photo search term"
    try:
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        prompt = f'For a slide titled "{slide_title}", generate {keyword_type}. Respond with ONLY the keyword/description string.'
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"   ... Keyword generation failed ({e}). Defaulting to title.")
        return slide_title

def generate_diagram_code(slide_title: str, slide_body: str, theme_colors: dict) -> str | None:
    print(f"-> Generating elegant skeleton diagram for: '{slide_title}'...")
    try:
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        primary_hex = '#%02x%02x%02x' % theme_colors['primary']
        secondary_hex = '#%02x%02x%02x' % theme_colors['secondary']
        prompt = f'Create a simple Graphviz DOT flowchart for "{slide_title}". Use `digraph G {{...}}`. Styles: `graph [bgcolor="transparent", fontname="Arial"]; node [shape=box, style="rounded,filled", fontname="Arial", fontcolor="white"]; edge [fontname="Arial", color="white"];`. Use short labels from "{slide_body}". Color key nodes with `fillcolor="{primary_hex}"` and others with `fillcolor="{secondary_hex}"`. Respond with ONLY raw DOT code.'
        response = model.generate_content(prompt)
        code = response.text.strip().replace("```dot", "").replace("```", "").strip()
        return code
    except Exception as e:
        print(f"   ... Diagram code generation failed: {e}")
        return None