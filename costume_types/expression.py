class ExpressionItem:
    def __init__(self, actions: list[str], repeat: bool = False, repeatCount: int = 1, coolDown: float = 0):
        self.actions = actions
        self.repeat = repeat
        self.repeatCount = repeatCount
        self.coolDown = coolDown
        