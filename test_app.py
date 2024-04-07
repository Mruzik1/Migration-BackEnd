import requests

# The URL of the Flask app endpoint you want to test
url = "http://10.0.5.217:7676/code_migrator"

# Define the JSON payload you want to send, which includes the filename
# Adjust the payload to match the expected format of your Flask app
payload = {
    "filename": "migrated_code3.json"
}

# Send a POST request with JSON payload
response = requests.post(url, json=payload)

# Check the response
if response.status_code == 200:
    print("Success! Here's the response data:")
    print(response.json())
else:
    print(f"Failed with status code: {response.status_code}")
    print(f"Response content: {response.content}")
