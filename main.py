import argparse
import config

# Import the new function
from orchestration.content_engine import generate_slide_outline, choose_best_image, generate_speaker_notes
from orchestration.image_engine import search_for_images, download_image
from orchestration.visual_engine import create_presentation

def main():
    # Check if API keys are set
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

    # 2. Process each slide to find and select the best image
    for slide in slide_outline:
        slide["image_path"] = None # Default to no image
        keyword = slide.get("image_keyword")
        title = slide.get("slide_title")
        body = slide.get("slide_body", "")
        
        if keyword and title:
            # Step 2a: Search for image candidates
            image_candidates = search_for_images(keyword)
            
            if image_candidates:
                # Step 2b: Use AI to choose the best image
                chosen_image = choose_best_image(title, image_candidates)

                if chosen_image:
                    # Step 2c: Download ONLY the chosen image
                    image_path = download_image(chosen_image['url'], keyword)
                    slide["image_path"] = image_path

        if title:
            notes = generate_speaker_notes(title, body)
            slide["speaker_notes"] = notes

    # 3. Create Presentation
    output_file = create_presentation(slide_outline, topic)
    
    print("\n--- Process Complete! ---")
    print(f"Presentation saved to: {output_file}")


if __name__ == "__main__":
    main()