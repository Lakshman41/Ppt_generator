import argparse
import config # Imports the class-based config
from orchestration.content_engine import (
    generate_slide_outline,
    decide_slide_layout,
    generate_visual_keyword,
    generate_diagram_code
)
from orchestration.image_engine import search_and_download_photo, render_diagram_local
from orchestration.visual_engine import create_presentation

def main():
    parser = argparse.ArgumentParser(description="The Majestic PPT Generator")
    parser.add_argument("topic", type=str, help="The main topic of the presentation.")
    parser.add_argument("--slides", type=int, default=5, help="Approximate number of slides.")
    parser.add_argument("--style", type=str, default="dark", choices=["dark", "light"], help="Visual theme.")
    args = parser.parse_args()

    topic = args.topic
    slide_count = args.slides
    style = args.style
    print(f"--- Generating the Majestic Presentation ---")
    print(f"Topic: '{topic}', Slides: {slide_count}, Style: '{style}'")
    
    # Use the new config class for validation
    if not all([config.PPTConfig.API_KEYS['GOOGLE'], config.PPTConfig.API_KEYS['PEXELS']]):
        print("FATAL: API keys are missing.")
        return

    slide_outline = generate_slide_outline(topic, slide_count)
    if not slide_outline: return

    print("\n--- Designing Individual Slides ---")
    enriched_slides = []
    themes = {'dark': {'primary': (52, 152, 219), 'secondary': (44, 62, 80)}}
    theme_colors = themes.get(style, themes['dark'])

    for i, slide_data in enumerate(slide_outline):
        title, body = slide_data['slide_title'], slide_data['slide_body']
        print(f"\n-> Designing Slide {i+1}: '{title}'")
        layout = "Title Layout" if i == 0 else decide_slide_layout(title, body)
        keyword = generate_visual_keyword(title, layout)
        
        slide_data['layout'] = layout
        slide_data['image_path'] = None

        if "Diagram" in layout:
            dot_code = generate_diagram_code(title, body, theme_colors)
            if dot_code:
                diagram_path = render_diagram_local(dot_code, title)
                if diagram_path:
                    slide_data['image_path'] = diagram_path
                else:
                    print("   ... Diagram rendering failed. Pivoting to photo.")
                    slide_data['layout'] = "Photo Layout"
        
        if "Photo" in slide_data['layout'] or "Title" in slide_data['layout']:
            photo_path = search_and_download_photo(keyword, title)
            if photo_path:
                slide_data['image_path'] = photo_path
        
        enriched_slides.append(slide_data)

    print("\n--- Assembling Final Presentation ---")
    create_presentation(enriched_slides, topic, style)
    print("\n--- Presentation Generation Complete. ---")

if __name__ == "__main__":
    main()