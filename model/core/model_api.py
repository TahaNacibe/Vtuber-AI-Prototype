import requests


def call_gemini_model(payload: dict, api_key: str) -> dict:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    response = requests.post(url, json=payload)
    
    if response.status_code != 200:
        raise RuntimeError(f"API call failed: {response.status_code} - {response.text}")
    
    return response.json()