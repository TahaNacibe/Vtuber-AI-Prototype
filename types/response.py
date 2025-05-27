from memory_item import MemoryItem


class ResponseData:
    def __init__(self,message:str,memories: list[MemoryItem],blendshapes: dict):
        self.message = message
        self.memories = memories
        self.blendshapes = blendshapes