import discord
import os
from dotenv import load_dotenv

load_dotenv()
bot = os.getenv('BOT_TOKEN')

class Client(discord.Client):
    async def on_ready(self):
        print(f'Вітаю, {self.user}!')
        
        
intents = discord.Intents.default()
intents.message_content = True


client = Client(intents=intents)
client.run(bot)