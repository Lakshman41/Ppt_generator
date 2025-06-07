import os
from openai import OpenAI
from config import PPTConfig

# Create a DeepSeek client using OpenAI SDK
client = OpenAI(
    api_key=PPTConfig.API_KEYS['DEEPSEEK'],
    base_url="https://api.deepseek.com"
)

def deepseek_chat(prompt, system_message="You are a helpful assistant.", model="deepseek-chat", max_tokens=1024, temperature=0.7, response_format=None):
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": prompt}
    ]
    kwargs = dict(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
        stream=False
    )
    if response_format:
        kwargs["response_format"] = response_format
    response = client.chat.completions.create(**kwargs)
    print("DEBUG: Raw DeepSeek response:", response)
    content = response.choices[0].message.content.strip()
    # Strip markdown formatting
    content = content.replace('```json', '').replace('```', '').strip()
    return content 