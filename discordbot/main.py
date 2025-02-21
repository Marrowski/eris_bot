import discord
from discord.ext import commands
from discord.utils import get

import random
import yt_dlp
import asyncio

import os

from request_api import find_anime
from database import insert_data

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
    user = message.author.name
    guild = message.guild.name
    msg = message.content
    await insert_data(user, guild, msg)
    await bot.process_commands(message)
    print(f'Отримано повідомлення! Текст:{msg}, Сервер:{guild}')
    
    if message.author.bot:
        return
        
         
@bot.command()
async def ping(ctx):
    await ctx.send(f'{ctx.author.name}, Hello!')
    
    
async def get_audio_url(url): 
    loop = asyncio.get_running_loop()
    
    def fetch_url():
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'noplaylist': True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info.get('url', '').strip()
    
    return await loop.run_in_executor(None, fetch_url)


@bot.command()
async def play(ctx, url: str):
    global voice_channel
    if ctx.author.voice and ctx.author.voice.channel:
        voice_channel = ctx.author.voice.channel
        audio_url = await get_audio_url(url)

        vc = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if not vc or not vc.is_connected():
            vc = await voice_channel.connect()
        else:
            await vc.move_to(voice_channel)

        await ctx.send(f'🎶 Connecting to {voice_channel.name}...')
        
        ffmpeg_options = {
            'options': '-vn'
        }
        before_options = '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'
        vc.play(discord.FFmpegPCMAudio(audio_url, **ffmpeg_options, before_options=before_options))
        await ctx.send(f'Your media is now playing in {voice_channel.name}.')
        
        while vc.is_playing():
            await asyncio.sleep(1)
        await ctx.send(f'🕵️‍♀️ Bot has successfully finished playing media.')  
         
    else:
        await ctx.send(f'❌ {ctx.author.mention}, connect to a voice channel first!')
        
        
@bot.command()
async def stop(ctx):
    vc = ctx.voice_client
    if vc:
        await vc.disconnect()
        await ctx.send(f'⛔ Bot has been disconnected from the channel: {voice_channel.name}')
        
    else:
        await ctx.send(f'❌ Bot is not connected to voice channel.')
        
        
@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel and after.channel is None:
        if len(before.channel.members) == 1:
            voice_client = discord.utils.get(bot.voice_clients, guild=member.guild)
            if voice_client:  
                await voice_client.disconnect()        
                
            
            text_channel = discord.utils.get(member.guild.text_channels)
            if text_channel:
                await text_channel.send(f"No people in {before.channel.name}. Disconnecting...")

        
@bot.command(name='anime')
async def anime_command(ctx, title:str):
    await find_anime(ctx, title)
    

async def info(ctx):
    user = ctx.author
    guild = ctx.guild
    msg = ctx.message.content
    return user, guild, msg

if __name__ == '__main__':
    bot.run(bot_tok)