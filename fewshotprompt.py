import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

few_shot_prompt = """
Example 1:
Input: Username: admin, Password: wrongpass
Expected Output: "Invalid password"

Example 2:
Input: Username: user, Password: test123
Expected Output: "User not found"

Now, for:
Input: Username: admin, Password: admin123
Expected Output:
"""

response = openai.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "user", "content": few_shot_prompt}
    ]
)
print("Few-Shot Output:\n", response.choices[0].message.content)