


def get_response_structure():

    #? Returns the structure of the response for the API.
    return """
    response:Text a response for the user input.
    memories: [List of memories you made depending on the current input if needed return them as {
        text: TEXT, -- memory content
            weight: REAL, --> how likely is it for this memory to stick
            attachment: REAL, --> how much is this memory important and may be thing that be remembered
    }],
    blendshapes: Ex (don't have to only use 3 can use as many as needed and how needed): {
    "blendshapes": {
        "Smile": 0.9,
        "EyeSquint": 0.6,
        "MouthSmile_L": 0.8
    }
    }
    """