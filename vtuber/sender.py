import asyncio
import sys
import pyvts
from data.funcs.emote import get_emote_by_key
from logs.funcs.log_prints import print_error_message, print_log_message

class VTubeSender:
    def __init__(self):
        vts = pyvts.vts()
        self.emote_key = None
        self.vts = vts
    
    #? start the connections
    async def initialize_connection(self):
        try:
            await self.vts.connect()
            # await self.vts.request_authenticate_token() 
            # await self.vts.request_authenticate() 
        except ConnectionRefusedError:
            print_error_message("VTuber studio is either closed or not responding!")
            sys.exit(1)

    #? send the emote to the VTube Studio API based on key
    async def send_emote_to_api(self, emote_key:str):        
        # check key state
        if(not emote_key):
            raise ValueError("Emote key cannot be None or empty.")
        
        await self.initialize_connection()
        
        # get the hotkey ID for the emote and other details
        hotkey_object = get_emote_by_key(emote_key)
        if not hotkey_object:
            raise KeyError(f"Emote '{emote_key}' wasn't returned from the index.")
        if(hotkey_object.repeat and hotkey_object.repeatCount > 0):
            # initialize the emote reputedly based on repeat count
            for _ in range(hotkey_object.repeatCount):
                await self.start_emote(hotkey_object.actions)
            # reset emote state
            await self.vts.close()

        else:
            # preform emote only once
            await self.start_emote(hotkey_object.actions)
            # reset emote state
            await self.vts.close()
    
    #? preform an emote action
    async def start_emote(self, actions):
        # loop through the actions and start each action
        for action in actions:
            hot_key_request = self.vts.vts_request.requestTriggerHotKey(action)
            await self.vts.request(hot_key_request)
            # wait for 0.4 seconds before sending the next action to not override the previous one
            await asyncio.sleep(0.1)
        
            
            
    #? clear last emote action
    async def clear_last_emote(self):
        await self.start_emote(["default"])
        await self.vts.request(self.vts.vts_request.requestTriggerHotKey(None))
        
    
    async def ensure_connection(self):
        if not self.vts.websocket:
            print_log_message("WebSocket closed. Reconnecting...")
            self.vts = pyvts.vts()  # recreate the client
            await self.vts.connect()
            await self.vts.request_authenticate_token() 
            await self.vts.request_authenticate()
    

