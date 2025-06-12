import argparse
import os
from dotenv import load_dotenv
from orchestration.content_engine import generate_slide_outline, decide_slide_layout, generate_visual_keyword
from orchestration.visual_engine import create_presentation
from orchestration.image_engine import search_and_download_photo, get_supporting_images

def main():
    # Load environment variables
    load_dotenv()
    
    # Check for required API keys
    if not os.getenv('GEMINI_API_KEY'):
        print("ERROR: GEMINI_API_KEY not found in .env file")
        return
    if not os.getenv('PEXELS_API_KEY'):
        print("ERROR: PEXELS_API_KEY not found in .env file")
        return
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Generate a professional PowerPoint presentation')
    parser.add_argument('topic', type=str, help='The topic of the presentation')
    parser.add_argument('--slides', type=int, default=6, help='Number of slides (default: 6)')
    parser.add_argument('--style', type=str, default='dark', choices=['dark', 'light'], help='Presentation style (default: dark)')
    args = parser.parse_args()
    
    print("\n--- Generating the Majestic Presentation ---")
    print(f"Topic: '{args.topic}', Slides: {args.slides}, Style: '{args.style}'")
    
    # Generate slide outline
    print("-> AI generating text outline...")
    slides = generate_slide_outline(args.topic, args.slides)
    if not slides:
        print("ERROR: Failed to generate slide outline")
        return
    
    # Enrich slides with images and layouts
    enriched_slides = []
    for i, slide_data in enumerate(slides):
        print(f"\n-> Processing slide {i+1}: {slide_data['slide_title']}")
        
        # Set layout
        if i == 0:
            slide_data['layout'] = "Title Layout"
        else:
            slide_data['layout'] = decide_slide_layout(slide_data)
        
        # Generate and download background image
        visual_keyword = generate_visual_keyword(slide_data['slide_title'], slide_data['slide_body'])
        if visual_keyword:
            print(f"-> Searching for background image: {visual_keyword}")
            image_path = search_and_download_photo(visual_keyword, is_background=True)
            if image_path:
                slide_data['image_path'] = image_path
        
        # Get supporting images for non-title slides
        if i > 0:
            supporting_images = get_supporting_images(slide_data)
            if supporting_images:
                slide_data['supporting_images'] = supporting_images
        
        enriched_slides.append(slide_data)
    
    # Create the presentation
    output_file = create_presentation(enriched_slides, args.topic, args.style, args.slides)
    print(f"\n-> Presentation generated successfully: {output_file}")

if __name__ == "__main__":
    main()