import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

meta_prompt = (
    "Write a prompt that would help an LLM generate comprehensive test cases for a password reset feature."
)

response = openai.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "user", "content": meta_prompt}
    ]
)
print("Meta Prompt Output:\n", response.choices[0].message.content)
