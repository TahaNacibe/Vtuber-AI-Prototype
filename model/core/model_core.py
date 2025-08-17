import os
import time
import traceback
from dotenv import load_dotenv
from data.funcs.emote import get_emotes_keys_list
from logs.funcs.log_prints import print_error_message
from model.config.response_structure import get_response_structure
from model.config.rules import get_rules
from model.core.model_api import call_gemini_model
from model.core.payload_builder import build_gemini_payload
from model.func.model_message_builder import create_model_message
from model.func.user_input_builder import get_user_message
from model.utils.response_transformer import response_transformer


#i'm using api because i have 16gb or ram and a cpu that is not good enough to run the model locally (0.0)
def load_model_core(user_text, memoriesContent, chatContext, personality, gemini_api_key, user_name, max_retries = 3):
    if not gemini_api_key:
        print_error_message("Missing Gemini API key. Check your .env file.")
        return None

    if not user_text:
        print_error_message("User input is empty or not passed to load_model_core.")
        return None

    try:
        response_structure = get_response_structure()
        rules = get_rules()
        allowed_blendshapes = get_emotes_keys_list()

        model_message = create_model_message(
            personality,
            response_structure, 
            rules, 
            allowed_blendshapes
        )

        user_input = get_user_message(
            user_text,
            memoriesContent,
            chatContext,
            user_name
        )

        payload = build_gemini_payload(user_input, model_message)

        # Retry logic for transient failures (like system load)
        for attempt in range(1, max_retries + 1):
            try:
                response = call_gemini_model(payload, gemini_api_key)

                if response == "Model Failed":
                    print_error_message(f"Gemini returned 'Model Failed' on attempt {attempt}.")
                    return None

                return response_transformer(response)

            except Exception as inner_e:
                print_error_message(f"Error on Gemini call attempt {attempt}:\n{traceback.format_exc()}")

                if attempt < max_retries:
                    time.sleep(1.5)
                else:
                    raise RuntimeError(f"Gemini call failed after {max_retries} attempts: {inner_e}")

    except Exception as e:
        print_error_message("Unhandled exception in load_model_core:\n" + traceback.format_exc())
        return None