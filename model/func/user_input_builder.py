def get_user_message(user_input, memory_items, chat_history, user_name):
    memory_str = "\n".join(mem[1] for mem in memory_items)  # mem[1] assumed to be the memory text
    chat_str = "\n".join(f"{speaker}: {message}" for speaker, message in chat_history) # already formatted strings

    return f"""# Memory
            {memory_str}

            # Chat History
            {chat_str}

            {user_name}: {user_input}
            """
