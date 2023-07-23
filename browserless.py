import requests
import json

# Define the headers for the request
headers = {
    'Cache-Control': 'no-cache',
    'Content-Type': 'application/json',
}

# Define the data to be sent in the request
payload = {
    "url": "https://github.com/username",  # replace 'username' with the actual GitHub username
    "elements": [
        {
            "selector": ".repo"  # CSS selector for the pinned projects
        },
        {
            "selector": "span[itemprop='programmingLanguage']"  # CSS selector for the programming languages
        }
    ]
}

# Convert Python object to JSON string
data_json = json.dumps(payload)

# Send the POST request
response = requests.post(f"https://chrome.browserless.io/scrape?token={'0af8da42-e7eb-4c99-a98e-34d924416991'}", headers=headers, data=data_json)

# Parse the response
response_data = response.json()


print(response_data)
# Extract the project names and languages
project_names = [result['text'] for result in response_data['data'][0]['results']]
project_languages = [result['text'] for result in response_data['data'][1]['results']]

# Print the project names and languages
for name, language in zip(project_names, project_languages):
    print(f"Project: {name}, Language: {language}")
