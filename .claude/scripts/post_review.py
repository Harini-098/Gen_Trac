import json
import os
from pathlib import Path
import requests

# Read review.json
with open("review.json", "r", encoding="utf-8") as f:
    response = json.load(f)

# Extract findings robustly from the JSON output wrapper
findings = None
if isinstance(response, dict):
    if "result" in response:
        res = response["result"]
        if isinstance(res, str):
            try:
                findings = json.loads(res)
            except json.JSONDecodeError:
                findings = res
        else:
            findings = res
    elif "structured_output" in response:
        res = response["structured_output"]
        if isinstance(res, str):
            try:
                findings = json.loads(res)
            except json.JSONDecodeError:
                findings = res
        else:
            findings = res

if findings is None:
    findings = response

if isinstance(findings, dict):
    findings = [findings]
elif not isinstance(findings, list):
    findings = []

# GitHub info
repo = os.environ["GITHUB_REPOSITORY"]
token = os.environ["GITHUB_TOKEN"]

with open(os.environ["GITHUB_EVENT_PATH"], "r", encoding="utf-8") as f:
    event = json.load(f)

owner, repo_name = repo.split("/")
pr_number = event["pull_request"]["number"]
commit_sha = event["pull_request"]["head"]["sha"]

headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json"
}

for finding in findings:

    payload = {
        "body": f"""### {finding['severity'].upper()}

**Finding**
{finding['finding']}

**Suggested Fix**
{finding['suggested_fix']}
""",
        "commit_id": commit_sha,
        "path": finding["file"],
        "line": finding["line"],
        "side": "RIGHT"
    }

    url = f"https://api.github.com/repos/{owner}/{repo_name}/pulls/{pr_number}/comments"

    response = requests.post(url, headers=headers, json=payload)

    print(response.status_code)
    print(response.text)