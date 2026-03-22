import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

# Step 1: Ask for negative test cases
response1 = openai.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "user", "content": "List all possible negative test cases for a login form."}
    ]
)
test_cases = response1.choices[0].message.content
print("Step 1 - Negative Test Cases:\n", test_cases)

# Step 2: For each test case, ask for expected error message
response2 = openai.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "user", "content": f"For each of these test cases, describe the expected error message:\n{test_cases}"}
    ]
)
print("\nStep 2 - Expected Error Messages:\n", response2.choices[0].message.content)