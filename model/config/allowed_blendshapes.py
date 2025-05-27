

def get_allowed_blendshapes():
   allowed_blendshapes = [
    # Core expressions
    "Neutral",
    "Joy",
    "Angry",
    "Sorrow",
    "Fun",

    # General emotional controls
    "Smile",
    "Frown",
    "BrowUp",
    "BrowDown",
    "EyeWide",
    "EyeSquint",
    "CheekPuff",
    "TongueOut",

    # Eye controls
    "Blink",
    "Blink_L",
    "Blink_R",
    "LookUp",
    "LookDown",
    "LookLeft",
    "LookRight",

    # Lip sync shapes (can be used for approximate English mouth movement)
    "JawOpen",
    "MouthOpen",
    "MouthSmile_L",
    "MouthSmile_R",
    "MouthFrown_L",
    "MouthFrown_R",
    ]
   
   allowed_blendshapes_string = ', '.join(allowed_blendshapes)
   return allowed_blendshapes_string
