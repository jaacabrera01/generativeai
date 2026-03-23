import openai
import os
import base64

# Step 1: Set up API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Step 2: Define keyword library (documentation)
keyword_library = """
Keyword Library:
- OpenBrowser: Launches the browser
- GoTo: Navigates to a given URL
- InputText: Types text into a field
- ClickButton: Clicks a button by label
- VerifyText: Checks if text is present on the page
- CloseBrowser: Closes the browser
"""

# Step 3: Few-shot examples (training the LLM with context)
few_shot_examples = """
Example Test Script 1:
OpenBrowser
GoTo    https://www.saucedemo.com
InputText    user-name    test_user
InputText    password    wrong_pass
ClickButton    login-button
VerifyText    Invalid password
CloseBrowser

Example Test Script 2:
OpenBrowser
GoTo    https://www.saucedemo.com   
InputText    user-name    standard_user
InputText    password    secret_sauce
ClickButton    login-button
VerifyText    Products
CloseBrowser
"""

# Step 4: Define new requirement
new_requirement = "Create a keyword-driven test script to verify that a user can successfully log out after login."

# Step 5: Send prompt to LLM (few-shot prompting)
messages = [
    {
        "role": "system",
        "content": "You are an AI assistant that generates and validates keyword-driven test scripts using the provided keyword library."
    },
    {
        "role": "user",
        "content": f"{keyword_library}\n\n{few_shot_examples}\n\nRequirement: {new_requirement}\n\nGenerate the test script."
    }
]

response = openai.chat.completions.create(
    model="gpt-4o",
    messages=messages
)

generated_script = response.choices[0].message.content
print("Generated Test Script:\n")
print(generated_script)

# Step 6: Debugging support (simulate AI assistant checking script)
debug_prompt = f"""
System Prompt: You are a QA assistant that validates keyword-driven test scripts.
Check the following script for errors or improvements:

{generated_script}
"""

debug_response = openai.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": debug_prompt}]
)

print("\nDebugging Feedback:\n")
print(debug_response.choices[0].message.content)
