import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

def gemini_chat(prompt: str, system_prompt: str = None) -> str:
    """
    Send a chat message to Gemini and get the response.
    """
    model = genai.GenerativeModel('models/gemini-2.5-flash-preview-05-20')
    
    if system_prompt:
        chat = model.start_chat(history=[])
        response = chat.send_message(f"{system_prompt}\n\n{prompt}")
    else:
        response = model.generate_content(prompt)
    
    return response.text

def gemini_vision(prompt: str, image_path: str) -> str:
    """
    Send an image and prompt to Gemini Vision and get the response.
    """
    model = genai.GenerativeModel('models/gemini-1.0-pro-vision-latest')
    
    with open(image_path, 'rb') as f:
        image_data = f.read()
    
    response = model.generate_content([prompt, image_data])
    return response.text

def list_gemini_models():
    print("Available Gemini models:")
    for m in genai.list_models():
        print(f"- {m.name} (supported methods: {m.supported_generation_methods})")

if __name__ == "__main__":
    list_gemini_models() 