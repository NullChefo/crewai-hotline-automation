import os

import requests

API_KEY = os.getenv('VOICEFLOW_API_KEY')
if API_KEY is None:
    print("VOICEFLOW_API_KEY is not set")
    exit(1)


def get_transcripts(caller_id: str):
    url = f"https://api.voiceflow.com/v1/transcripts/{caller_id}"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        transcripts = response.json()
        return transcripts
    else:
        print(f"Failed to retrieve transcripts: {response.status_code}")
        return None
