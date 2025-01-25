import discord

TOKEN = '19122f0dc17e5e1e08cf350d5e10eb91d32e2363a29d9649385a9a2219b77484'

class Greeting(discord.Client):
    async def greeting(self):
        print(f'Вітаю! {self.user}!')
        

intents = discord.Intents.default()
intents.message_content = True


client = Greeting(intents=intents)

client.run(TOKEN)
