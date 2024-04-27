import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from discord import TextChannel
from youtube_dl import YoutubeDL

load_dotenv()
# назначение префикса для команд
client = commands.Bot(command_prefix='!', intents=discord.Intents.all())
players = {}


# проверка готовности бота к работе
@client.event
async def on_ready():
    print(f'Бот {client.user.name} готов пахать!')


# команда присоединение бота к голосовому каналу
@client.command()
async def join(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()


# команда для воспроизведения звука с URL-адреса youtube
@client.command()
async def play(ctx, url):
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    voice = get(client.voice_clients, guild=ctx.guild)

    if not voice.is_playing():
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['url']
        voice.play(discord.FFmpegPCMAudio(URL, executable="ffmpeg/ffmpeg.exe", **FFMPEG_OPTIONS))
        voice.is_playing()
        await ctx.send('ОНО РАБОТАЕТ!!! 0_0')

    # бот уже играет музыку
    else:
        await ctx.send("Бот уже играет другую музыку")
        return


# команда для возобновления голосовой связи, если она была приостановлена
@client.command()
async def resume(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if not voice.is_playing():
        voice.resume()
        await ctx.send('Бот готов продолжить пахать')


# команда для возобновления звука, если он был приостановлен
@client.command()
async def pause(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice.is_playing():
        voice.pause()
        await ctx.send('Бот отдыхает')


# команда для остановки звука
@client.command()
async def stop(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice.is_playing():
        voice.stop()
        await ctx.send('Музыка OF...')


# команда для очистки сообщений канала
@client.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)
    await ctx.send("Очистка мусора завершена")


TOKEN = 'MTIyOTY5MjU0NDU0MDA4MjIxNg.GplfGP.C3mzxtjxEVOYsAI1UZK1mgXKlpeT7K8Cc85aaY'

client.run(TOKEN)
