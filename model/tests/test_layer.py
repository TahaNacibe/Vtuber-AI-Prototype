from memory_v2.utils.memory_manager import MemoryManager
from model.core.model_core import load_model_core


def test_app(mem_mgr: MemoryManager):
    print("=== Memory Manager Test App ===")

    while True:
        print("\nChoose an option:")
        print("1 - Add new memory")
        print("2 - Browse all memories")
        print("3 - Search memories by input")
        print("4 - display")
        print("5 - chat")
        print("6 - Exit")

        choice = input("Your choice: ").strip()

        if choice == '1':
            text = input("Enter memory text: ").strip()
            tokens = text.split()  # simple tokenization by splitting spaces
            embedding = mem_mgr.embedder.encode(text)
            mem_mgr.add_new_memory(text, embedding, tokens)
            print("Memory added!")

        elif choice == '2':
            mem_mgr.cursor.execute("SELECT * FROM memories")
            memories = mem_mgr.cursor.fetchall()
            if memories:
                print("\n--- Memories ---")
                for mem in memories:
                    print(f"[{mem}]")
            else:
                print("No memories found.")

        elif choice == '3':
            query = input("Enter search query: ").strip()
            try:
                results = mem_mgr.get_memories(query, limit=5)
                if results:
                    print("\n--- Search Results ---")
                    print(f"Found {len(results)} matching memories:")
                    for mem in results:
                        print(f"[{mem}]")
                else:
                    print("No matching memories found.")
            except Exception as e:
                print("Error during search:", e)

        elif choice == "4":
            mem_mgr.get_all_for_view()

        elif choice == "5":
            print("loading memory items for input...")
            memories = mem_mgr.get_all_for_view()
            print("loaded memory, start calling model...")
            while True:
                userInput = input("enter message: ")
                if(userInput == "exit"):
                    break
                # get the data from a response
                model_response, new_memories, blendshapes = load_model_core(userInput, memories)
                print(f"Model Response: {model_response} \nMemories: {new_memories}\nBlendshapes: {blendshapes}")
                for mem in new_memories:
                    mem_mgr.add_new_memory(
                    mem["text"], 
                    mem_mgr.embedder.encode(mem["text"]),
                    "",
                    wight=mem["weight"],
                    attachment=mem["attachment"])
        elif choice == '6':
            print("Exiting...")
            break

        else:
            print("Invalid choice, try again.")