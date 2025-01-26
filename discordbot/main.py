import discord
from discord.ext import commands
from discord.utils import get
import youtube_dl
import pafy
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
    print(f'Вітаю,{bot.user}!')
    
    
@bot.event
async def on_message(message):
    print(f'Отримано повідомлення! Текст:{message.content}, Сервер:{message.guild}')
    
    if message.author.bot:
        return
    await bot.process_commands(message)
        
         
@bot.command()
async def ping(ctx):
    await ctx.send(f'{ctx.author.name}, ти шукав мене?')
    
@bot.command()
async def play(ctx, url:str):
    if not ctx.author.voice:
        return await ctx.send('Ви не під`єднані до каналу!')
    voice_channel = ctx.author.voice.channel
    if ctx.voice_client is None:
        vc = await voice_channel.connect
    else:
        await ctx.voice_client.move_to(voice_channel)
        vc = ctx.voice_client
    
    
    video = pafy.new(url)
    best = video.getbestaudio
    source = await discord.FFmpegOpusAudio.from_probe(best.url, method='fallback')
    
    vc.play(source)
    
    
@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()
    else:
        await ctx.send('Бот не під`єднаний до голосового каналу.')  
        

@bot.command(name='anime')
async def anime_command(ctx, title:str):
    await find_anime(ctx, title)

if __name__ == '__main__':
    bot.run(bot_tok)