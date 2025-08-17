from costume_types.expression import ExpressionItem


expressions_index = {
        "happy": ExpressionItem(actions=["Happy"], repeat=False, repeatCount=0, coolDown=0),
        "default": ExpressionItem(actions=["Default"], repeat=False, repeatCount=0, coolDown=0),
        "excited": ExpressionItem(actions=["Excited"], repeat=False, repeatCount=0, coolDown=0),
        "surprised": ExpressionItem(actions=["Surprised"], repeat=False, repeatCount=0, coolDown=0),
        "fear": ExpressionItem(actions=["Fear"], repeat=False, repeatCount=0, coolDown=0),
        "confused": ExpressionItem(actions=["Confused"], repeat=False, repeatCount=0, coolDown=0),
        "head_dazing": ExpressionItem(actions=["HeadDazingRight", "HeadDazingLeft"], repeat=False, repeatCount=0, coolDown=0),
        "blink_left_eye": ExpressionItem(actions=["BlinkLeftEye"], repeat=False, repeatCount=0, coolDown=0),
        "blink_left_eye": ExpressionItem(actions=["BlinkRightEye"], repeat=False, repeatCount=0, coolDown=0),
        "blush": ExpressionItem(actions=["Blush"], repeat=False, repeatCount=0, coolDown=0),
        "close_both_eye": ExpressionItem(actions=["CloseBothEye"], repeat=False, repeatCount=0, coolDown=0),
        "happy_mouth_open": ExpressionItem(actions=["HappyMouthOpen"], repeat=False, repeatCount=0, coolDown=0),
        "turn_left": ExpressionItem(actions=["HeadLeftSide"], repeat=False, repeatCount=0, coolDown=0),
        "turn_right": ExpressionItem(actions=["HeadRightSide"], repeat=False, repeatCount=0, coolDown=0),
        "look_up": ExpressionItem(actions=["HeadUp"], repeat=False, repeatCount=0, coolDown=0),
        "look_down": ExpressionItem(actions=["HeadDown"], repeat=False, repeatCount=0, coolDown=0),
        "lifeless_eyes": ExpressionItem(actions=["LifelessEyes"], repeat=False, repeatCount=0, coolDown=0),
        "little_mad": ExpressionItem(actions=["LittleMad"], repeat=False, repeatCount=0, coolDown=0),
        "little_sad": ExpressionItem(actions=["LittleSad"], repeat=False, repeatCount=0, coolDown=0),
        "look_right": ExpressionItem(actions=["LookRight"], repeat=False, repeatCount=0, coolDown=0),
        "scarry": ExpressionItem(actions=["Scarry"], repeat=False, repeatCount=0, coolDown=0),
        "nod_in_agreeing": ExpressionItem(actions=["HeadUp","HeadDown"], repeat=True, repeatCount=3, coolDown=300),
        "nod_in_disagreeing": ExpressionItem(actions=["HeadRightSide","HeadLeftSide"], repeat=True, repeatCount=3, coolDown=300),
        "so_scared": ExpressionItem(actions=["SoScared"], repeat=False, repeatCount=0, coolDown=0),
}