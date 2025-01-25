import discord
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

class Greeting(discord.Client):
    async def greeting(self):
        print(f'Вітаю! {self.user}!')
        

intents = discord.Intents.default()
intents.message_content = True


client = Greeting(intents=intents)

client.run(TOKEN)
