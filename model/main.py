from ..memory_v2.utils.memory_manager import MemoryManager
from model.tests.test_layer import test_app


def main():
    mem_mgr = MemoryManager()
    test_app(mem_mgr)
    
    


if __name__ == "main":
    main()