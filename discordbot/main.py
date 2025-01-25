import discord
from discord.ext import commands

TOKEN = '19122f0dc17e5e1e08cf350d5e10eb91d32e2363a29d9649385a9a2219b77484'


intents = discord.Intents.default()
intents.message_content = True


class MainGreeting(discord.Client):
    async def on_ready(self):
        print(f'Вітаю, {self.user}!')


client = MainGreeting(intents=intents)
client.run(TOKEN)
