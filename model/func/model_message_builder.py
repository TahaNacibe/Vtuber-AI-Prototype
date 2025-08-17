# this will handle how the model will be responding to the user, based on the memories, personality layer, response structure and rules
def create_model_message( personality_layer: str, response_structure: str, rules: str,allowed_blendshapes:str) -> str:
    if not response_structure or not rules:
        raise ValueError("Response structure and rules are somehow missing, man—go check that for me.")
    
    return f"""
        You're {personality_layer};
        Please always follow these rules carefully:
        {rules}

        When you respond, make sure to strictly adhere to this response structure as JSON format:
        {response_structure}
        
        For Reactions use the allowed allowed blendshapes List:
        {allowed_blendshapes}

        Keep your tone natural, engaging, and human-like while fully respecting the above rules and structure. Your goal is to provide helpful and coherent answers based on your memories and instructions.
        """.strip()



# just some cleaning for some reason the system with the original thing is flawed if the user change the ai think the user messages are his
def get_message_owner(role: str) -> str:
    return  "You" if role == "model" else "User"