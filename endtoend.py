# --- Imports ---
import openai
import os
import base64
import pandas as pd
import re

# Paths to the screenshots
login_image_path = "opensource-demo-orangehrm.jpg"
add_employee_image_path = "addemployee.png"
view_employee_image_path = "viewemployee.png"

# Read and encode the images in base64
def encode_image(path):
    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

login_image_data = encode_image(login_image_path)
add_employee_image_data = encode_image(add_employee_image_path)
view_employee_image_data = encode_image(view_employee_image_path)


# User stories and constraints for OrangeHRM E2E scenarios
user_stories = """
1. As a user, I want to log in to the OrangeHRM system using valid credentials so that I can access the dashboard.
2. As an admin, I want to add a new employee to the OrangeHRM system by filling out the required fields in the 'Add Employee' form, so that the new employee is registered in the system.
3. As an admin, I want to view an employee's details in the OrangeHRM system so that I can verify their information.
"""
constraints = """
- Login requires valid username and password.
- All fields marked with * are required when adding an employee (e.g., First Name, Last Name, Employee ID).
- 'Save' button should only be enabled when all required fields are valid.
- Error messages should be shown for invalid or missing input.
- After adding, the employee should be searchable and viewable in the employee list.
- Employee details page should display all entered information correctly.
- 'Cancel' button should discard changes and return to the previous page.
"""

print("\n--- Hands-On Objective 2.2.2b: Few-Shot Prompting for Gherkin Test Cases ---\n")

# Few-shot examples
few_shot_examples = """
Example 1:
User Story: As a user, I want to reset my password so that I can regain access if I forget it.
Test Conditions:
- User is on the login page
- User clicks "Forgot Password"
- User enters a valid email

Gherkin Test Case:
Given the user is on the login page
When the user clicks "Forgot Password" and enters a valid email
Then a password reset link is sent to the user's email

Example 2:
User Story: As an admin, I want to add a new employee so that the employee can access the system.
Test Conditions:
- Admin is logged in
- Admin navigates to Add Employee
- Admin fills all required fields

Gherkin Test Case:
Given the admin is logged in and on the Add Employee page
When the admin fills all required fields and clicks Save
Then the new employee is added to the system
"""

# New user story and test conditions (can be replaced as needed)
new_user_story = """
User Story: As a user, I want to log in to the OrangeHRM system using valid credentials so that I can access the dashboard.
Test Conditions:
- User is on the login page
- User enters valid username and password
- User clicks Login
"""

few_shot_prompt = f"""{few_shot_examples}
Now, for the following user story and test conditions, generate Gherkin-style test cases:

{new_user_story}

Gherkin Test Case:
"""

messages_gherkin = [
    {"role": "system", "content": "You are a senior QA analyst and test designer."},
    {"role": "user", "content": few_shot_prompt}
]

response_gherkin = openai.chat.completions.create(
    model="gpt-4o",
    messages=messages_gherkin,
    max_tokens=400
)
gherkin_output = response_gherkin.choices[0].message.content
print(gherkin_output)

# Step 1: Generate acceptance criteria for all scenarios
messages_acceptance = [
    {"role": "system", "content": "You are a senior QA analyst."},
    {"role": "user", "content": (
        "Context: Here are user stories and GUI wireframes for the OrangeHRM login, add employee, and view employee pages.\n"
        "Instruction: Generate clear, complete acceptance criteria for all the user stories, referencing the relevant wireframe for each scenario.\n"
        f"User Stories:\n{user_stories}\n"
        f"Constraints:\n{constraints}\n"
        "Output Format: Numbered list of acceptance criteria, grouped by user story."
    )},
    {
        "role": "user",
        "content": [
            {"type": "text", "text": "Here is the OrangeHRM Login wireframe image:"},
            {"type": "image_url", "image_url": {"url": "data:image/png;base64," + login_image_data}},
            {"type": "text", "text": "Here is the OrangeHRM Add Employee wireframe image:"},
            {"type": "image_url", "image_url": {"url": "data:image/png;base64," + add_employee_image_data}},
            {"type": "text", "text": "Here is the OrangeHRM View Employee wireframe image:"},
            {"type": "image_url", "image_url": {"url": "data:image/png;base64," + view_employee_image_data}}
        ]
    }
]

response_acceptance = openai.chat.completions.create(
    model="gpt-4o",
    messages=messages_acceptance,
    max_tokens=1200
)
acceptance_criteria = response_acceptance.choices[0].message.content
print("Step 1 - Acceptance Criteria:\n", acceptance_criteria)

# Step 2: Generate functional test cases from acceptance criteria

# Add stricter prompt for markdown table formatting
messages_testcases = [
    {"role": "system", "content": "You are a senior QA analyst."},
    {"role": "user", "content": (
        "Given the following acceptance criteria, generate a set of functional test cases. "
        "For each test case, include: Test Case ID, Title, Preconditions, Steps, Test Data, Expected Result. "
        "Output as a markdown table. Each test case should be on a single row, with multi-step instructions separated by <br> within the same cell. Do not wrap or split rows. Ensure the table is readable in markdown viewers.\n\n"
        f"Acceptance Criteria:\n{acceptance_criteria}"
    )}
]


# Add a function to clean up the markdown table output
import re

def clean_markdown_table(table_str):
    lines = table_str.split('\n')
    cleaned_lines = []
    buffer = ""
    row_start_pattern = re.compile(r'^\|\s*TC\\d{3,}')  # Matches lines starting with | TC001, | TC002, etc.
    for line in lines:
        if row_start_pattern.match(line) or line.strip().startswith('| Test Case ID'):
            if buffer:
                cleaned_lines.append(buffer)
            buffer = line.strip()
        else:
            buffer += " " + line.strip()
    if buffer:
        cleaned_lines.append(buffer)
    return '\n'.join(cleaned_lines)


response_testcases = openai.chat.completions.create(
    model="gpt-4o",
    messages=messages_testcases,
    max_tokens=1000
)
test_cases_md = response_testcases.choices[0].message.content

# Function to parse markdown table to list of dicts
def parse_markdown_table(md_table):
    lines = [line.strip() for line in md_table.split('\n') if line.strip()]
    # Find header and separator
    header_idx = None
    sep_idx = None
    for i, line in enumerate(lines):
        if re.match(r'^\|.*\|$', line):
            if header_idx is None:
                header_idx = i
            elif sep_idx is None:
                sep_idx = i
                break
    if header_idx is None or sep_idx is None:
        raise ValueError("Markdown table header or separator not found.")
    headers = [h.strip() for h in lines[header_idx].strip('|').split('|')]
    data_lines = lines[sep_idx+1:]
    rows = []
    for line in data_lines:
        if not line.startswith('|'):
            # Merge with previous row if broken
            if rows:
                rows[-1][-1] += ' ' + line.strip()
            continue
        cells = [c.strip() for c in line.strip('|').split('|')]
        # Pad cells if row is short
        while len(cells) < len(headers):
            cells.append('')
        rows.append(cells)
    # Remove extra columns if any
    rows = [r[:len(headers)] for r in rows]
    return [dict(zip(headers, r)) for r in rows]

# Parse the markdown table
try:
    test_cases_list = parse_markdown_table(test_cases_md)
    df = pd.DataFrame(test_cases_list)
    excel_path = "functional_test_cases.xlsx"
    df.to_excel(excel_path, index=False)
    print(f"\nStep 2 - Functional Test Cases exported to {excel_path}\n")
except Exception as e:
    print("\nStep 2 - Functional Test Cases (Markdown Table):\n", test_cases_md)
    print(f"\n[Warning] Could not parse and export to Excel: {e}\n")

# Step 3: Verify coverage of acceptance criteria by test cases
messages_coverage = [
    {"role": "system", "content": "You are a senior QA analyst."},
    {"role": "user", "content": (
        "Given the following acceptance criteria and test cases, create a markdown table that maps each acceptance criterion to the test cases that cover it. "
        "If any acceptance criterion is not covered, highlight it.\n\n"
        f"Acceptance Criteria:\n{acceptance_criteria}\n\n"
        f"Test Cases:\n{test_cases_md}"
    )}
]

response_coverage = openai.chat.completions.create(
    model="gpt-4o",
    messages=messages_coverage,
    max_tokens=800
)
coverage_table = response_coverage.choices[0].message.content
print("\nStep 3 - Coverage Table:\n", coverage_table)

# Step 4: Meta-prompt for end-to-end test procedure generation/refinement
messages_meta = [
    {"role": "system", "content": "You are a senior QA analyst and test designer."},
    {"role": "user", "content": (
        "Given the following user story, acceptance criteria, and functional test cases, create a comprehensive end-to-end test procedure. "
        "If the prompt or output can be improved for better coverage or clarity, suggest refinements. "
        "Output the end-to-end test procedure and any prompt improvement suggestions.\n\n"
        f"User Stories:\n{user_stories}\n\n"
        f"Acceptance Criteria:\n{acceptance_criteria}\n\n"
        f"Test Cases:\n{test_cases_md}"
    )}
]

response_meta = openai.chat.completions.create(
    model="gpt-4o",
    messages=messages_meta,
    max_tokens=1000
)
meta_output = response_meta.choices[0].message.content
print("\nStep 4 - End-to-End Test Procedure & Meta-Prompt Suggestions:\n", meta_output)