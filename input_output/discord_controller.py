import logging

# Get the discord logger and remove its handlers
discord_logger = logging.getLogger("discord")
discord_logger.handlers = []  # Remove any handlers it added
discord_logger.setLevel(logging.CRITICAL)  # Silence all logs
discord_logger.propagate = False  # Prevent logs from bubbling up

import discord
import asyncio
import threading
from logs.funcs.log_prints import print_error_message, print_log_message, print_success_message


class DiscordBridge(discord.Client):
    def __init__(self, token, channel_name):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.messages = True
        intents.guilds = True

        super().__init__(intents=intents)

        self.token = token
        self.channel_name = channel_name
        self.channel_id = None
        self.last_message = None
        self.loop = None
        self.thread = None
        self.ready_event = threading.Event()

    async def on_ready(self):
        print_success_message(f"Logged in as {self.user}")
        for guild in self.guilds:
            for channel in guild.text_channels:
                if channel.name == self.channel_name:
                    self.channel_id = channel.id
                    print_success_message(f"Connected to channel: '{channel.name}'")
                    self.ready_event.set()
                    return
        print_error_message(f"Channel '{self.channel_name}' not found")
        self.ready_event.set()  # Still unblock, even if channel isn't found

    async def on_message(self, message):
        if message.author == self.user:
            return  # Ignore bot's own messages

        if message.channel.id == self.channel_id:
            self.last_message = {
                "owner": str(message.author),
                "message": message.content
            }

    async def _send_message(self, content):
        if self.channel_id:
            channel = self.get_channel(self.channel_id)
            if channel:
                await channel.send(content)

    def send_message(self, content):
        if self.loop and self.channel_id:
            asyncio.run_coroutine_threadsafe(self._send_message(content), self.loop)

    def get_last_message(self):
        msg = self.last_message
        return msg

    def start_bot(self):
        def run():
            self.run(self.token)

        self.thread = threading.Thread(target=run, daemon=True)
        self.thread.start()
        print_log_message("[INFO] Bot thread started")


    def stop_bot(self):
        if self.loop and self.loop.is_running():
            asyncio.run_coroutine_threadsafe(self.close(), self.loop)

    def send(self, message: str):
        if self.loop:
            asyncio.run_coroutine_threadsafe(self._send_message(message), self.loop)
