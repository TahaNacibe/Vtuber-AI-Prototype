


def get_response_structure():

    #? Returns the structure of the response for the API.
    return """
    response:Text a response for the user input.
    memories: [List of memories you made depending on the current input if needed return them as {
        text: TEXT, -- memory content
            weight: REAL, --> how likely is it for this memory to stick
            attachment: REAL, --> how much is this memory important and may be thing that be remembered
            memory_related_to: a person name like if you are talking to someone named Sam and a new memory about him is made save sam name here
    }],
    emote: Ex: happy
    """