import requests


url = "http://10.0.5.217:7676/code_migrator"
payload = {
    "repo_url": "https://github.com/Mruzik1/Migration-Test.git",
    "from_lang": "Vue.js",
    "to_lang": "React",
    "task_type": "describe_files"
}
response = requests.post(url, json=payload)

if response.status_code == 200:
    print(response.json())
else:
    print(f"Failed with status code: {response.status_code}")