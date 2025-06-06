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
    """
    print(f"-> Generating content outline for '{topic}' using DeepSeek...")

    prompt = f"""
    Create a compelling presentation outline on the topic: "{topic}".
    The presentation should have exactly {slide_count} slides.
    For each slide, provide a short, impactful "slide_title" and a concise "image_keyword" that visually represents the slide's content.
    The image_keyword should be simple and effective for a stock photo search.

    Provide the output in a valid JSON format as a list of objects.
    The output should be ONLY the JSON list, with no other text or formatting.
    Example format:
    [
        {{"slide_title": "The Dawn of AI", "image_keyword": "futuristic technology"}},
        {{"slide_title": "Key Innovations", "image_keyword": "glowing neural network"}}
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
        
        # <<< --- NEW ROBUST PARSING LOGIC --- >>>
        # Find the start of the JSON array '[' and the end ']'
        json_start_index = content.find('[')
        json_end_index = content.rfind(']')
        
        if json_start_index != -1 and json_end_index != -1:
            # Extract the JSON string
            json_string = content[json_start_index : json_end_index + 1]
            slide_data = json.loads(json_string)
            print("-> Content outline generated successfully.")
            return slide_data
        else:
            # If we can't find the JSON, we raise an error to be caught below
            raise json.JSONDecodeError("Could not find JSON array in the LLM response.", content, 0)

    except json.JSONDecodeError as e:
        # The error message now includes the raw response, which is helpful for debugging
        print(f"Error: Failed to parse LLM response as JSON. Details: {e}")
        return None
    except Exception as e:
        print(f"An error occurred with the DeepSeek API: {e}")
        return None