import discord
from discord.ext import commands
from discord.utils import get
import youtube_dl
import pafy
import asyncio
import os
from request_api import find_anime

import os
from dotenv import load_dotenv

load_dotenv()
bot_tok = os.getenv('BOT_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!',intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} успішно під`єднано!')
    
    
@bot.event
async def on_message(message):
    print(f'Отримано повідомлення! Текст:{message.content}, Сервер:{message.guild}')
    
    if message.author.bot:
        return
    await bot.process_commands(message)
        
         
@bot.command()
async def ping(ctx):
    await ctx.send(f'{ctx.author.name}, Hello!')
    
async def get_audio_url(url): 
    loop = asyncio.get_event_loop() 
    data = await loop.run_in_executor(None, lambda: os.popen(f"youtube-dl -f bestaudio --get-url {url}").read()) 
    return data.strip() 

@bot.command() 
async def play(ctx, url: str): 
    voice_channel = ctx.author.voice.channel 
    audio_url = await get_audio_url(url) 

    vc = await voice_channel.connect() 

    vc.play(discord.FFmpegPCMAudio(audio_url)) 

    while vc.is_playing(): 
        await asyncio.sleep(1) 

    await vc.disconnect() 
        

@bot.command(name='anime')
async def anime_command(ctx, title:str):
    await find_anime(ctx, title)

if __name__ == '__main__':
    bot.run(bot_tok)