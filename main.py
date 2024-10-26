from typing import Final
import os
import discord
from dotenv import load_dotenv
import functionality

load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
print(TOKEN)
   
intents: discord.Intents = discord.Intents.default()
intents.message_content = True

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message: discord.Message):
        print(f'Message from {message.author}: {message.content}')
        await functionality.process_response(self, message)

    
def main() -> None:
    client = MyClient(intents=intents)
    client.run(token=TOKEN)
    
if __name__ == '__main__':
    main()