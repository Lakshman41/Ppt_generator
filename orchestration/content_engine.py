import openai
import json
import config

# Configure the client for DeepSeek
client = openai.OpenAI(
    api_key=config.DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com"
)

def generate_slide_outline(topic: str, slide_count: int = 5):
    """
    Generates a structured outline for a presentation using the DeepSeek LLM.
    Now includes a concise impact statement for each slide.
    """
    print(f"-> Generating enhanced content outline for '{topic}' using DeepSeek...")

    # The prompt is now updated to ask for a "slide_body" field.
    prompt = f"""
    Create a compelling presentation outline on the topic: "{topic}".
    The presentation should have exactly {slide_count} slides.

    For each slide, provide three pieces of information:
    1. A short, impactful "slide_title" (max 10 words).
    2. A concise "slide_body" which is a single, powerful sentence to be displayed on the slide (max 20 words). This should complement the title.
    3. A simple "image_keyword" for a stock photo search that visually represents the slide's content.

    Provide the output in a valid JSON format as a list of objects.
    The output should be ONLY the JSON list, with no other text or formatting.
    Example format:
    [
        {{
            "slide_title": "The Dawn of AI",
            "slide_body": "Artificial intelligence is rapidly transforming every aspect of our modern world.",
            "image_keyword": "futuristic technology"
        }},
        {{
            "slide_title": "Key Innovations",
            "slide_body": "Breakthroughs in machine learning and neural networks are driving this evolution.",
            "image_keyword": "glowing neural network"
        }}
    ]
    """

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a world-class presentation creator who generates structured JSON output."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )

        content = response.choices[0].message.content
        
        json_start_index = content.find('[')
        json_end_index = content.rfind(']')
        
        if json_start_index != -1 and json_end_index != -1:
            json_string = content[json_start_index : json_end_index + 1]
            slide_data = json.loads(json_string)
            print("-> Content outline generated successfully.")
            return slide_data
        else:
            raise json.JSONDecodeError("Could not find JSON array in the LLM response.", content, 0)

    except json.JSONDecodeError as e:
        print(f"Error: Failed to parse LLM response as JSON. Details: {e}")
        return None
    except Exception as e:
        print(f"An error occurred with the DeepSeek API: {e}")
        return None

def choose_best_image(slide_title: str, image_candidates: list) -> dict | None:
    """
    Uses an LLM to choose the best image for a slide from a list of candidates.

    Args:
        slide_title (str): The title of the slide.
        image_candidates (list): A list of image data from the image engine.

    Returns:
        dict | None: The dictionary of the chosen image, or None on failure.
    """
    print(f"-> Using AI to choose the best image for slide: '{slide_title}'...")

    # Format the candidate descriptions for the prompt
    candidate_descriptions = "\n".join(
        [f"Image {i+1}: (ID: {img['id']}) \"{img['alt']}\"" for i, img in enumerate(image_candidates)]
    )

    prompt = f"""
    You are a professional Visual Director for a presentation.
    Your task is to select the most thematically appropriate and visually compelling image for a slide.

    Slide Title: "{slide_title}"

    Here are the descriptions of the available candidate images:
    {candidate_descriptions}

    Analyze the slide title and the image descriptions. Which image is the best fit?
    Consider the emotion, objects, and concepts. For example, for a slide about "collaboration," an image of a team working is better than a generic office photo.

    Respond with ONLY the ID of the winning image, and nothing else.
    For example: 45319
    """

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful Visual Director who responds with only an image ID number."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3, # Lower temperature for more deterministic choices
        )
        
        chosen_id_str = response.choices[0].message.content.strip()
        chosen_id = int(chosen_id_str)
        
        # Find the full dictionary for the chosen image
        for candidate in image_candidates:
            if candidate['id'] == chosen_id:
                print(f"   ... AI chose Image ID: {chosen_id} (Description: \"{candidate['alt']}\")")
                return candidate
        
        # If the LLM returned an ID that doesn't exist, we fallback to the first one
        print("   ... AI returned an invalid ID. Defaulting to the first image.")
        return image_candidates[0]

    except (ValueError, IndexError) as e:
        print(f"   ... Error processing LLM choice ({e}). Defaulting to the first image.")
        return image_candidates[0]
    except Exception as e:
        print(f"   ... An API error occurred during image selection ({e}). Defaulting to the first image.")
        return image_candidates[0]

def generate_speaker_notes(slide_title: str, slide_body: str) -> str:
    """
    Uses an LLM to generate speaker notes for a given slide.

    Args:
        slide_title (str): The title of the slide.
        slide_body (str): The body text of the slide.

    Returns:
        str: A string containing the generated speaker notes.
    """
    print(f"-> Generating speaker notes for slide: '{slide_title}'...")

    prompt = f"""
    You are a professional presentation coach and speechwriter.
    A presenter has a slide with the following content:
    - Slide Title: "{slide_title}"
    - Key Message: "{slide_body}"

    Your task is to write clear and concise speaker notes for the presenter.
    These notes should expand on the key message, provide additional context,
    or suggest questions to engage the audience.

    The notes should be formatted as 3-4 bullet points.
    Do not include a header like "Speaker Notes:". Just provide the bullet points.
    """

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful presentation coach."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        
        notes = response.choices[0].message.content.strip()
        print("   ... Speaker notes generated.")
        return notes

    except Exception as e:
        print(f"   ... An error occurred during speaker note generation: {e}")
        return "Speaker notes could not be generated for this slide."