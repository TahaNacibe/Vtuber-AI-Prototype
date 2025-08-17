import re
import json

def response_transformer(response: dict):
    try:
        # Step 1: Extract raw content
        raw_text = response['candidates'][0]['content']['parts'][0]['text']
        
        # Step 2: Extract JSON inside triple backticks
        json_match = re.search(r'```json\n(.*?)\n```', raw_text, re.DOTALL)
        if not json_match:
            raise ValueError("No JSON block found in response.")

        json_str = json_match.group(1)
        
        # Step 3: Parse the JSON
        data = json.loads(json_str)
        
        # Step 4: Extract components
        message = data.get("response", "")
        new_memories = data.get("memories", [])
        blendshapes_data = data.get("emote", "")
        model_emote = blendshapes_data 

        return message, new_memories, model_emote

    except (KeyError, IndexError, json.JSONDecodeError) as e:
        raise RuntimeError(f"Failed to parse response: {e}")
