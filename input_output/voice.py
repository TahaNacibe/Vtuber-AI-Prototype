import os
from fish_audio_sdk import WebSocketSession, TTSRequest, ReferenceAudio

sync_websocket = WebSocketSession(os.getenv("FISH_AUDIO_API_KEY"))
model_id = os.getenv("VOICE_MODEL_ID")


def stream():
    text = "Well, you know, machine learning is like, um, this really fascinating field that's basically teaching computers to, eh, figure things out on their own."
    for line in text.split():
        yield line + " "

tts_request = TTSRequest(
    text="",  # Initial text or empty string
    reference_id=model_id,
    temperature=0.7,  # Controls randomness in speech generation
    top_p=0.7,  # Controls diversity via nucleus sampling
)

# Or you can use reference audio
# tts_request = TTSRequest(
#     text="",
#     references=[
#         ReferenceAudio(
#             audio=open("lengyue.wav", "rb").read(),
#             text="Text in reference AUDIO",
#         )
#     ],
#     temperature=0.7,
#     top_p=0.7,
# )

with open("output.mp3", "wb") as f:
    for chunk in sync_websocket.tts(
        tts_request,
        stream(), # Stream the text
        backend="speech-1.6"  # Specify which TTS model to use
    ):
        f.write(chunk)