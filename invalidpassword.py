import openai
import os
import base64

# Step 1: Set up API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Step 2: Load an image (screenshot of login page after failed login)
image_path = "/Users/jaacabrera/Documents/Python Scripts/ITSQB-Gen AI/InvalidPassword.png"

with open(image_path, "rb") as image_file:
    base64_str = base64.b64encode(image_file.read()).decode("utf-8")

image_url = f"data:image/jpeg;base64,{base64_str}"

# Step 3: Define the test requirement and expected result
requirement = "Verify that the error message 'Invalid password' appears after a failed login attempt."
expected_result = "Invalid password"

# Step 4: Send multimodal prompt to LLM
response = openai.chat.completions.create(
    model="gpt-4o",  # Vision-capable model
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": requirement},
                {"type": "image_url", "image_url": {"url": image_url}}
            ]
        }
    ]
)

# Step 5: Capture the AI’s response
llm_output = response.choices[0].message.content
print("LLM Response:")
print(llm_output)

# Step 6: Verify against expected result
if expected_result.lower() in llm_output.lower():
    print("\n✅ Test Passed: Expected error message found.")
else:
    print("\n❌ Test Failed: Expected error message NOT found.")
