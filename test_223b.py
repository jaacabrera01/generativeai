import openai
import os

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Example regression test results and specification
test_results = """
TC001: PASS - Login with valid credentials
TC002: FAIL - Login button not clickable
TC003: FAIL - Password reset email not sent
TC004: PASS - Add new employee
TC005: FAIL - Add employee with missing fields
TC006: PASS - View employee details
"""

test_specification = """
TC001: Login with valid credentials
TC002: Login with invalid credentials
TC003: Password reset
TC004: Add new employee
TC005: Add employee with missing fields
TC006: View employee details
"""

known_anomalies = """
- Login button not clickable (known issue #A12)
- Password reset email not sent (known issue #B34)
"""

# Step 1: Analyze test results vs. specification
prompt1 = f"""
Given the following regression test results and test specification, identify which tests passed, failed, or were not executed. Highlight any discrepancies.

Test Results:
{test_results}

Test Specification:
{test_specification}
"""

response1 = openai.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": prompt1}]
)
analysis = response1.choices[0].message.content
print("Step 1 - Analysis:\n", analysis)

# Step 2: Cluster similar defects
prompt2 = f"""
Based on the failed test cases below, group similar defects together. For each cluster, provide a summary and list the affected test cases.

Failed Test Cases:
{test_results}
"""

response2 = openai.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": prompt2}]
)
clusters = response2.choices[0].message.content
print("\nStep 2 - Defect Clusters:\n", clusters)

# Step 3: Compare with known anomalies
prompt3 = f"""
Here is a list of known anomalies from previous test cycles:
{known_anomalies}

Compare the current defect clusters to the known anomalies. Mark which defects are already known and which are new.
Defect Clusters:
{clusters}
"""

response3 = openai.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": prompt3}]
)
anomaly_check = response3.choices[0].message.content
print("\nStep 3 - Known Anomalies Check:\n", anomaly_check)

# Step 4: Summarize actionable insights
prompt4 = f"""
Summarize the key findings from the regression test analysis. List actionable insights, such as areas needing retesting, new defects to log, and any updates required for the known anomalies list.

Analysis:
{analysis}

Defect Clusters:
{clusters}

Known Anomalies Check:
{anomaly_check}
"""

response4 = openai.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": prompt4}]
)
summary = response4.choices[0].message.content
print("\nStep 4 - Actionable Insights:\n", summary)