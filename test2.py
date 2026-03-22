import openai
import os
import base64

openai.api_key = os.getenv("OPENAI_API_KEY")

# Path to your image file
image_path = "/Users/jaacabrera/Documents/Python Scripts/ITSQB-Gen AI/CE.jpeg"  # Change this to your image filename

with open(image_path, "rb") as image_file:
    base64_str = base64.b64encode(image_file.read()).decode("utf-8")

image_url = f"data:image/jpeg;base64,{base64_str}"

response = openai.chat.completions.create(
    model="gpt-4o",  # Updated to current vision-capable model
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What is in this picture?"},
                {
                    "type": "image_url",
                    "image_url": {"url": image_url}
                }
            ]
        }
    ]
)
print(response.choices[0].message.content)