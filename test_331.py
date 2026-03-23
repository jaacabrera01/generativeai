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
real_error = test_data["error_message"]
anonymized_error = real_error.replace(test_data["user_email"], "[ANONYMIZED]")

anonymized_data = {
    "user_email": "[ANONYMIZED]",
    "password": "[ANONYMIZED]",
    "error_message": anonymized_error
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

# --- Environmental Impact Simulation ---
# Constants (example values, adjust as needed)
ENERGY_PER_1K_TOKENS_WH = 0.35   # Watt-hours per 1,000 tokens
CO2_PER_1K_TOKENS_G = 0.20       # Grams CO₂ per 1,000 tokens

# User input: number of API calls and tokens per call
try:
    num_calls = int(input("\nEnter number of GenAI API calls: "))
    avg_tokens = int(input("Enter average tokens per call: "))
except Exception:
    print("Invalid input. Using defaults: 1 call, 800 tokens.")
    num_calls = 1
    avg_tokens = 800

# Calculations
total_tokens = num_calls * avg_tokens
energy_wh = (total_tokens / 1000) * ENERGY_PER_1K_TOKENS_WH
co2_g = (total_tokens / 1000) * CO2_PER_1K_TOKENS_G

# Output
print("\n--- GenAI Test Task Environmental Impact ---")
print(f"Total tokens processed: {total_tokens}")
print(f"Estimated energy used: {energy_wh:.2f} Wh")
print(f"Estimated CO₂ emissions: {co2_g:.2f} grams")

print("\nContext:")
print("- 1 Wh = energy to power a 1-watt device for 1 hour.")
print("- 1 gram CO₂ ≈ driving a car for ~7 meters.")
print(f"Equivalent to powering a LED bulb for about {energy_wh/9:.2f} hours (9W bulb).")
print(f"Equivalent to driving a car for about {co2_g*7:.2f} meters.")

print("\nEstimates based on published LLM energy/CO₂ research.")