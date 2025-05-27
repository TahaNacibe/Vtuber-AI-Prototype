from dotenv import load_dotenv
import os
from model.config.allowed_blendshapes import get_allowed_blendshapes
from model.config.response_structure import get_response_structure
from model.config.rules import get_rules
from model.core.model_api import call_gemini_model
from model.core.payload_builder import build_gemini_payload
from model.func.model_message_builder import create_model_message
from model.utils.response_transformer import response_transformer


#i'm using api because i have 16gb or ram and a cpu that is not good enough to run the model locally (0.0)
def load_model_core(userInput, memoriesContent):
    
    # Load the API KEY from the .env file
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    
    
    # just to check nothing is wrong with the API key
    if not api_key:
        raise ValueError("API key not found. Please set the GEMINI_API_KEY environment variable, or just get another model, you shouldn't care about that error if you read the code (0.0)")
    
    
    # if the user input is empty, raise an error
    if not userInput:
        raise ValueError("User input cannot be empty, i mean come on, you have to write something, right? (0.0)")
    
    
    # create payload
    response_structure = get_response_structure()
    rules = get_rules()
    allowed_blendshapes = get_allowed_blendshapes()
    payload = build_gemini_payload(
        userInput,
        create_model_message(memoriesContent,'sam the neighbor',response_structure, rules, allowed_blendshapes)
    )
    
    # call the API model
    try:
        response = call_gemini_model(payload, api_key)
        # print(response)
        # print("-------------------------------------------------------->")
        # transform the response
        return  response_transformer(response)
        # print(f"Model Response: {model_response} \nMemories: {new_memories}\nBlendshapes: {blendshapes}")
        
    #? in case something went wrong     
    except Exception as e:
        raise RuntimeError(f"Couldn't get the response : {str(e)}")
        