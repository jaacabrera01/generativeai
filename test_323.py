import openai
import os
import logging

# --- Setup logging for audit trail ---
logging.basicConfig(filename='genai_access.log', level=logging.INFO)

# --- Access control (simple demo) ---
AUTHORIZED_USERS = ['alice', 'bob', 'jaacabrera']
current_user = os.getenv('USER') or 'unknown'

if current_user not in AUTHORIZED_USERS:
    print("Access denied: unauthorized user.")
    exit()

logging.info(f"User {current_user} accessed GenAI testing script.")

# --- Example of sensitive test data (risk) ---
test_data = {
    "user_email": "realuser@example.com",
    "password": "SuperSecret123!",
    "error_message": "Login failed for user realuser@example.com"
}

print("WARNING: Sending real user data to GenAI API is a privacy risk!")

# --- Mitigation: Anonymize data before sending ---
anonymized_data = {
    "user_email": "[ANONYMIZED]",
    "password": "[ANONYMIZED]",
    "error_message": "Login failed for user [ANONYMIZED]"
}

# --- Simulate sending to GenAI API ---
openai.api_key = os.getenv("OPENAI_API_KEY")

prompt = f"Analyze this test data for login issues:\n{anonymized_data}"

response = openai.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": prompt}]
)
output = response.choices[0].message.content

print("\n--- GenAI Output (with anonymized data) ---")
print(output)

print("\nMitigation strategies used:")
print("- Data anonymization before sending to GenAI")
print("- Access control and audit logging")
print("- Warning about insecure practices")
print("\nCheck 'genai_access.log' for audit trail.")