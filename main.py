import os
import asyncio
import subprocess
from dotenv import load_dotenv
from input_output.discord_controller import DiscordBridge
from vtuber.sender import VTubeSender
from model.utils.db_manager import ChatDbManager
from model.core.model_core import load_model_core
from input_output.text_to_voice import text_to_voice
from memory_v2.utils.memory_manager import MemoryManager
from model.func.chat_db import get_last_n_messages, save_message
from logs.funcs.log_prints import print_action_message, print_error_message, print_log_message, print_success_message

async def main():
    
    #* response controller params
    loaded_old_messages_count = 10
    loaded_related_memories_count = 50
    similarity_threshold = 1.75
    
    #* memory params
    user_related_ratio: float = 0.5
    other_users_related_ratio: float = 0.25
    globally_related_ratio: float = 0.25
    memories_count_threshold: int = 100
    
    #* mentions
    current_message_owner = None
    default_user_name = "Yukios"
    personality = None
    
    #* voice settings params
    voice_speed = 1.1
    voice_id = "MiueK1FXuZTCItgbQwPu"
    
    #* paths params
    memories_db_path = "memory_v2/db/memories.db"
    chat_db_path = "model/db/chat.db"
    
    #* auto params
    is_running_as_admin = False # change that to true if you run as admin other wise you have open VTuber studio
    v_tube_path = r"E:\Software\Steam\steamapps\common\VTube Studio"
    
    #? load env file data
    load_dotenv()
    elevens_labs_api_key = os.getenv("ELEVEN_LABS_API_KEY")
    gemini_api_key = os.getenv("GEMINI_API_KEY")

    #? discords params
    discord_app_token = os.getenv("DISCORD_TOKEN")
    discord_channel_name = "general"
    use_discord = False # update that to connect to discord chat
    discord_is_connected = False
    
    #? discord instant connection
    if use_discord:
        print_action_message("Start Discord connection...")
        discord_bridge = DiscordBridge(discord_app_token, discord_channel_name)
        discord_bridge.start_bot() 
        print_log_message("Bot is running in background, continuing with other code...")   
    else:
        print_log_message("Skip Discord Connection") 
    
    
    #? load personality from file
    try:
        with open("personality.txt", "r", encoding="utf-8") as persona:
            personality = persona.read()
            print_log_message("Loaded Personality Context")
    except Exception as e:
        print_error_message(f"Error getting personality file {e}")
        
    
    #? initialize program needed Models
    print_action_message("Start Core Processes...")
    memory_manager = MemoryManager(
        similarity_threshold,
        memories_db_path
    )
    print_success_message("Initialized Memory Manager")
    
    chat_db_manager = ChatDbManager(
        chat_db_path
    )
    print_success_message("Initialized Chats Storage Services")
    
    vTuber_core = VTubeSender()
    print_success_message("Initialized VTuber Model Handler")
    
    
    #? start VTube studio app
    if is_running_as_admin:
        print_action_message("Start VTube Studio...")
        if os.path.exists(v_tube_path):
            subprocess.Popen([v_tube_path])
            print_success_message("  VTube Studio Lunched")
        else:
            print_error_message("VTube Studio executable not found! Check the path.")
    
    
    #? Start data bases connections and initialize storage services
    print_action_message("Start Storage Services...")
    
    chat_db_manager.connect()
    print_success_message("Chat Data Base Connected")
    
    chat_db_manager.start_db()
    print_success_message("Chat Storage Started")
    
    
    #? Start VTube Models Connections
    print_action_message("Start VTube Model Controller...")
    await vTuber_core.initialize_connection()
    print_success_message("Connection to VTube Studio was Completed")


    #? chat loop
    print_success_message("Start Chat")
    # user input place holder will act as message holder with twitch and discord
    user_input = None
    
    # start chat loop
    while True:
        #? if it's discord connected Then switch to discord Flow
        if use_discord:
            # get the last message from the chat
            msg = discord_bridge.get_last_message()
            # if message exist
            if msg and discord_bridge.last_message:
                discord_bridge.last_message = None
                chat_message = f"{msg["owner"]} : {msg["message"]}"
                current_message_owner = msg["owner"]
                user_input = chat_message
                
                
                # switch chat state
                if user_input == f"{default_user_name} switch -d":
                    # final farewell
                    discord_bridge.send_message("Switching To Terminal Chat... GoodBye (^u^)/")
                    print_log_message("Switching To Terminal Chat... GoodBye (^u^)/")
                    discord_bridge.stop_bot()
                    # change state
                    discord_bridge = None
                    discord_is_connected = False
                    use_discord = False
                    current_message_owner = None
                    continue 
                continue
        
        #? normal Terminal chat Flow
        if not discord_is_connected:
            user_input = input("You: ")
            # switch to default user
            current_message_owner = default_user_name
            # change state back to the discord 
            if user_input == f"{default_user_name} switch -d":
                use_discord = True
                print_log_message("Switching To Discord Chat... GoodBye (^u^)/")
                continue
        
            # exit on command
            if user_input == "exit":
                print_action_message("Stop Model Core...")
                print_log_message("Exit Program")
                break
        
        if user_input and user_input != f"{default_user_name} switch -d":
            #? continue flow of the work
            # load last N messages
            last_chat_messages  = get_last_n_messages(chat_db_manager,loaded_old_messages_count)
                    
            # get the memories related to the chat based on user input through FAISS
            related_memories = memory_manager.get_memories(
                user_input, 
                current_message_owner,
                loaded_related_memories_count,
                user_related_ratio,
                other_users_related_ratio,
                globally_related_ratio,
                memories_count_threshold,
                )
                        
            # log
            print_log_message(f"Retrieved {len(related_memories)} related memory.")
            #? request response from Model
            result = load_model_core(
                user_input, 
                related_memories, 
                last_chat_messages, 
                personality,
                gemini_api_key,
                current_message_owner)
            # log
            if result is None:
                continue
            
            model_response, new_memories, model_emote = result
            print_log_message("Received model response.")
            
            # show response
            if use_discord and discord_bridge:
                discord_bridge.send(model_response)
            else:
                print_log_message(f"[Model] {model_response}")
                
                
            #? send emote to VTuber model
            if model_emote:
                await vTuber_core.send_emote_to_api(emote_key=model_emote)
                # log
                print_log_message(f"Emote Key '{model_emote}' was sent to Model.")
                        
                    
            #? send the message to voice cable
            text_to_voice(
                model_response,
                voice_id,
                voice_speed, 
                elevens_labs_api_key)
            # log
            print_log_message("Voice Response channeled to Output.")
                    
                    
            #? update saved data
            if new_memories and len(new_memories) > 0:
                # the empty string is for tokens in case the memories are too big and you need to filter based on shared key words
                for mem in new_memories:
                            memory_manager.add_new_memory(
                            mem["text"], 
                            memory_manager.embedder.encode(mem["text"]),
                            "",
                            wight=mem["weight"],
                            attachment=mem["attachment"],
                            memory_related_to=current_message_owner)
                print_log_message(f"Add {len(new_memories)} new memory to local db.")
                        
                        
            #? update chat log in SQL db
            save_message(current_message_owner, user_input, chat_db_manager)
            save_message("model", model_response, chat_db_manager)
            print_log_message("Create new messages items to local db.")
            
        
        
    
    




if __name__ == "__main__":
    asyncio.run(main())
    