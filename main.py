import requests
import time
import os
import csv

def search_github_actions(token):
    actions = []
    page = 1
    per_page = 30
    total_count = 0
    delay = 3600 / 5000

    while True:
        print(f"Retrieving page {page}...")  # Progress indicator

        url = f"https://api.github.com/search/code?q=filename:action.yml+OR+filename:action.yaml+path:/&per_page={per_page}&page={page}"
        headers = {'Authorization': f'Token {token}'}
        response = requests.get(url, headers=headers)

        if response.status_code == 403:
            print("Rate limit exceeded, waiting for 1 hour")
            time.sleep(3600)
            continue

        data = response.json()

        for item in data.get('items', []):
            if item['path'] in ['action.yml', 'action.yaml']:
                actions.append(item)
                total_count += 1
                print(f"Found Action: {item['repository']['full_name']}")
                print(f"Total Actions found: {total_count}")

        if 'next' not in response.links:
            break

        page += 1
        time.sleep(delay)

    return actions, total_count

def save_actions_to_csv(actions, filename='github_actions.csv'):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'HTML URL', 'Repository'])

        for action in actions:
            writer.writerow([action['name'], action['html_url'], action['repository']['full_name']])

def main():
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        raise ValueError("GitHub token not found in environment variables")

    actions, count = search_github_actions(token)
    print(f"Total GitHub Actions found: {count}")
    save_actions_to_csv(actions)

if __name__ == "__main__":
    main()
