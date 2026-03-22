import openai
import os
import base64

# Step 1: Set up API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Step 2: Load an image (example screenshot for testing)
image_path = "/Users/jaacabrera/Documents/Python Scripts/ITSQB-Gen AI/InvalidPassword.png"

with open(image_path, "rb") as image_file:
    base64_str = base64.b64encode(image_file.read()).decode("utf-8")

image_url = f"data:image/png;base64,{base64_str}"

# Step 3: Define structured prompt components
prompts = [
    {
        "role": "QA tester",
        "context": "System should reject invalid passwords and show an error message.",
        "instruction": "Verify if the screenshot contains the error message after failed login.",
        "input_data": {"type": "image_url", "url": image_url},
        "constraints": "Only describe visible UI elements, do not infer hidden logic.",
        "output_format": "Respond with PASS if error message is visible, FAIL if not."
    },
    {
        "role": "Developer",
        "context": "System should handle login errors gracefully.",
        "instruction": "Check if the screenshot shows proper error handling.",
        "input_data": {"type": "image_url", "url": image_url},
        "constraints": "Focus on UI clarity, not backend logic.",
        "output_format": "Summarize findings in 2 sentences."
    },
    {
        "role": "End-user",
        "context": "User attempted login with wrong password.",
        "instruction": "Describe what the user sees on the screen.",
        "input_data": {"type": "image_url", "url": image_url},
        "constraints": "Keep answer simple and user-friendly.",
        "output_format": "Plain English description."
    }
]

# Step 4: Run each structured prompt through the LLM
for i, p in enumerate(prompts, start=1):
    print(f"\n--- Prompt {i}: {p['role']} ---")
    
    # Build multimodal message
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": f"Role: {p['role']}\nContext: {p['context']}\nInstruction: {p['instruction']}\nConstraints: {p['constraints']}\nOutput Format: {p['output_format']}"},
                {"type": "image_url", "image_url": {"url": p['input_data']['url']}}
            ]
        }
    ]
    
    # Send to LLM
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )
    
    # Print response
    print("LLM Response:")
    print(response.choices[0].message.content)
