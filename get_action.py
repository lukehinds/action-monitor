import requests

url = "https://api.github.com/marketplace/actions"  # Endpoint for Marketplace actions
headers = {'Authorization': 'token YOUR_GITHUB_TOKEN'}  # Replace with your GitHub token

response = requests.get(url, headers=headers)
actions = response.json()

for action in actions:
    # Check for verification status in action details
    print(action['name'], action['publisher']['verified'])
