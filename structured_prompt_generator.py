
# Structured Prompt Generator
# This script allows users to create a structured prompt by inputting various components such as role,
# defining the context, instruction, input data, constraints, and output format. The generated prompt is then printed in a structured format.
def create_structured_prompt():
    print("Enter each component for your structured prompt:")
    role = input("Role: ")
    context = input("Context: ")
    instruction = input("Instruction: ")
    input_data = input("Input Data: ")
    constraints = input("Constraints: ")
    output_format = input("Output Format: ")

    prompt = (
        f"**Role:** {role}\n"
        f"**Context:** {context}\n"
        f"**Instruction:** {instruction}\n"
        f"**Input Data:** {input_data}\n"
        f"**Constraints:** {constraints}\n"
        f"**Output Format:** {output_format}\n"
    )

    print("\n--- Structured Prompt ---\n")
    print(prompt)

if __name__ == "__main__":
    create_structured_prompt()


#**Role:** QA Engineer
#**Context:** Testing all scenarios for the login functionality of the application.
#**Instruction:** As an admin, verify that login succeeds with correct credentials and fails with incorrect credentials. Also, verify that non-admin users cannot log in.
#**Input Data:** 
 # - Admin: jaacabrera.school@gmail.com / test1234
 # - Non-admin: [provide sample non-admin credentials]
#**Constraints:** Only admin users should have login access.
#**Output Format:** List each test scenario and its expected result as bullet points.