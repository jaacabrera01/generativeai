import openai
import os
import json

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Example test suite (customize as needed)
test_suite = [
    {"id": "TC001", "title": "Login with valid credentials", "priority": "High", "depends_on": []},
    {"id": "TC002", "title": "Login with invalid credentials", "priority": "Medium", "depends_on": ["TC001"]},
    {"id": "TC003", "title": "Password reset", "priority": "High", "depends_on": ["TC002"]},
    {"id": "TC004", "title": "Add new employee", "priority": "Medium", "depends_on": ["TC001"]},
    {"id": "TC005", "title": "View employee details", "priority": "Low", "depends_on": ["TC004"]},
]

# Step 1: Summarize risks and dependencies (request structured JSON)
prompt1 = f"""
Given the following test suite (in JSON), summarize the risks and dependencies for each test case.
Respond with a JSON array, where each item has: id, title, risk, dependencies (list of test case IDs).

Test Suite:
{json.dumps(test_suite, indent=2)}
"""

response1 = openai.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a senior QA analyst."},
        {"role": "user", "content": prompt1}
    ],
    max_tokens=800
)
# Parse the LLM's JSON output
try:
    risks_and_dependencies_summary = json.loads(response1.choices[0].message.content)
except Exception:
    # If the model returns markdown, try to extract the JSON part
    import re
    match = re.search(r'```json(.*?)```', response1.choices[0].message.content, re.DOTALL)
    if match:
        risks_and_dependencies_summary = json.loads(match.group(1))
    else:
        raise ValueError("Could not parse risks_and_dependencies_summary as JSON.")

print("\nStep 1 - Risks and Dependencies Summary:\n", json.dumps(risks_and_dependencies_summary, indent=2))

# Step 2: Generate prioritization plan (request structured JSON)
prompt2 = f"""
Given the following test suite and the summary of risks and dependencies, generate a prioritized test execution plan.
Respond with a JSON array, where each item has: order, id, title, priority, justification.

Test Suite:
{json.dumps(test_suite, indent=2)}

Risks and Dependencies Summary:
{json.dumps(risks_and_dependencies_summary, indent=2)}
"""

response2 = openai.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a senior QA analyst."},
        {"role": "user", "content": prompt2}
    ],
    max_tokens=1000
)
# Parse the LLM's JSON output
try:
    prioritized_test_plan = json.loads(response2.choices[0].message.content)
except Exception:
    match = re.search(r'```json(.*?)```', response2.choices[0].message.content, re.DOTALL)
    if match:
        prioritized_test_plan = json.loads(match.group(1))
    else:
        raise ValueError("Could not parse prioritized_test_plan as JSON.")

print("\nStep 2 - Prioritized Test Plan:\n", json.dumps(prioritized_test_plan, indent=2))

# Save results to JSON
output = {
    "risks_and_dependencies_summary": risks_and_dependencies_summary,
    "prioritized_test_plan": prioritized_test_plan
}
with open("test_prioritization_output.json", "w") as f:
    json.dump(output, f, indent=2)
print("Results saved to test_prioritization_output.json")

# Save prioritized plan to Excel
import pandas as pd
df = pd.DataFrame(prioritized_test_plan)
df.to_excel("prioritized_test_plan.xlsx", index=False)
print("Prioritized test plan saved to prioritized_test_plan.xlsx")