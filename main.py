from typing import Final
import os
import discord
from dotenv import load_dotenv
import functionality
import json
from collections import OrderedDict

load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
   
intents: discord.Intents = discord.Intents.default()
intents.message_content = True

# File path for saving the data
DATA_FILE = "server_data.json"

# Load data from JSON file
def load_data():
    global server_data
    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)
            # Reconvert to OrderedDict to preserve the order when loading
            server_data = {
                int(guild_id): OrderedDict(users)
                for guild_id, users in data.items()
            }
    except (FileNotFoundError, json.JSONDecodeError):
        # If the file doesn't exist or is corrupted, start with an empty dictionary
        server_data = {}

# Call load_data() when the bot starts to initialize server_data

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message: discord.Message):
        print(f'Message from {message.author}: {message.content}')
        await functionality.process_response(self, message)

    
def main() -> None:
    load_data()
    client = MyClient(intents=intents)
    client.run(token=TOKEN)
    
if __name__ == '__main__':
    main()