from dotenv import load_dotenv
from elevenlabs import ElevenLabs, play
from logs.funcs.log_prints import print_error_message, print_log_message


def text_to_voice(text:str,voice_id:str, voice_speed:float,elevens_labs_api_key):
    # fall back state
    if not elevens_labs_api_key or elevens_labs_api_key == "":
        print_error_message("ElevensLabs API is missing or maybe you didn't add it!")
        return

    # start client
    client = ElevenLabs(api_key=elevens_labs_api_key)
    
    try:
        # Generate and play instantly without saving
        audio = client.text_to_speech.convert(
            text=text,
            voice_id=voice_id,
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128",
            voice_settings={
            "stability": 0.3,
            "similarity_boost": 0.3,
            "style": 0.1,
            "use_speaker_boost": False,
            "speed": voice_speed  # 👈 slow it down slightly for robotic tone
        }
        )

        play(audio)
    except Exception as e:
        print_log_message(f"ElevenLabs Error: {e.body['detail']['message']}")
        return
