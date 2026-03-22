import openai
import os
import base64

openai.api_key = os.getenv("OPENAI_API_KEY")

# User story and constraints for OrangeHRM Add User
user_story = """
As an admin, I want to add a new user to the OrangeHRM system by filling out the required fields in the 'Add User' form, so that the new user can access the system with appropriate credentials.
"""
constraints = """
- All fields marked with * are required: User Role, Employee Name, Status, Username, Password, Confirm Password.
- Password must meet the strength requirements (combination of upper/lower case, symbols, numbers).
- 'Save' button should only be enabled when all required fields are valid.
- Error messages should be shown for invalid or missing input.
- 'Cancel' button should discard changes and return to the previous page.
"""

# Path to the OrangeHRM Add User page screenshot
image_path = "addemployee.png"  

# Read and encode the image in base64
with open(image_path, "rb") as image_file:
    image_data = base64.b64encode(image_file.read()).decode()

# Construct the structured prompt
messages = [
    {"role": "system", "content": "You are a senior QA analyst."},
    {"role": "user", "content": (
        "Context: Here is a user story and a GUI wireframe for the OrangeHRM 'Add User' page.\n"
        "Instruction: Generate clear, complete acceptance criteria for the user story, referencing the wireframe.\n"
        f"User Story: {user_story}\n"
        f"Constraints: {constraints}\n"
        "Output Format: Numbered list of acceptance criteria."
    )},
    {
        "role": "user",
        "content": [
            {"type": "text", "text": "Here is the OrangeHRM Add User wireframe image:"},
            {"type": "image_url", "image_url": {"url": "data:image/png;base64," + image_data}}
        ]
    }
]

# Call the OpenAI API (GPT-4o with vision)
response = openai.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    max_tokens=500
)

print("Generated Acceptance Criteria:\n", response.choices[0].message.content)