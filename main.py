from memory_v2.utils.memory_manager import MemoryManager
from model.tests.test_layer import test_app


def main():
    print("Starting Test App...")
    mem_mgr = MemoryManager()
    test_app(mem_mgr)
    print("Close Test App")
    
    


if __name__ == "__main__":
    main()