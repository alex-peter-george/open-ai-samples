import requests
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

# Set your OpenAI API key
api_key = "fd2e0aa746cf48efa326e6c360915d88"

# Define the API endpoint URL
url = "https://api.openai.com/v1/completions"

# Define the request data (model and prompt)
data = {
    "model": "text-davinci-002",
    "prompt": "Once upon a time, there was..."
}

# Set the headers (including the API token)
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# Make the API request
response = requests.post(url, json=data, headers=headers, verify=False)

# Process the response (e.g., print the completion)
if response.status_code == 200:
    completion = response.json()["choices"][0]["text"]
    print(f"Generated completion: {completion}")
else:
    print(f"Error: {response.status_code} - {response.text}")
