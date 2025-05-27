def build_gemini_payload(
    user_input: str, 
    model_message: str) -> dict:
    return {
        "contents": [
            {
                "role": "model",
                "parts": [
                    {"text": model_message or ""},
                ],
            },
            {
                "role": "user",
                "parts": [
                    {"text": user_input},
                ],
            },
        ]
    }
