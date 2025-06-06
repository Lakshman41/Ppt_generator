import argparse
from orchestration.content_engine import generate_slide_outline
from orchestration.image_engine import get_image_for_keyword
from orchestration.visual_engine import create_presentation
import config

def main():
    # <<< THIS IS THE LINE TO FIX >>>
    # Check if API keys are set, now looking for DeepSeek's key.
    if not config.DEEPSEEK_API_KEY or not config.PEXELS_API_KEY:
        print("Error: API keys for DeepSeek or Pexels are not set.")
        print("Please check your .env file.")
        return

    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Smart PPT Generator")
    parser.add_argument("topic", type=str, help="The topic of the presentation.")
    args = parser.parse_args()
    
    topic = args.topic
    print(f"--- Starting Smart PPT Generator for topic: '{topic}' ---")

    # 1. Generate Content
    slide_outline = generate_slide_outline(topic)
    if not slide_outline:
        print("--- Process failed: Could not generate content. ---")
        return

    # 2. Fetch Images for each slide
    for slide in slide_outline:
        keyword = slide.get("image_keyword")
        if keyword:
            image_path = get_image_for_keyword(keyword)
            slide["image_path"] = image_path # Add the path to the dict
        else:
            slide["image_path"] = None

    # 3. Create Presentation
    output_file = create_presentation(slide_outline, topic)
    
    print("\n--- Process Complete! ---")
    print(f"Presentation saved to: {output_file}")


if __name__ == "__main__":
    main()