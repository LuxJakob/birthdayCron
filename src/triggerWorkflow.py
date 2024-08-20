import sys

import requests
from requests.auth import HTTPBasicAuth


owner = 'LuxJakob'
repo = 'birthdayCron'
workflow_id = 'sendReminder.yml'

token = sys.argv[1]

url = f'https://api.github.com/repos/{owner}/{repo}/actions/workflows/{workflow_id}/dispatches'

payload = {
    "ref": "main"  # or specify a branch or tag
}

response = requests.post(url, json=payload, auth=HTTPBasicAuth(owner, token))

if response.status_code == 204:
    print("Workflow triggered successfully!")
else:
    raise Exception(f"Failed to trigger workflow. Status code: {response.status_code}\nResponse: {response.text}")
