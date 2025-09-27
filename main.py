import discord
import time
import asyncio
import random
from discord.ext import commands

import logging
from dotenv import load_dotenv
from random_message import get_random_message
from randomfact import get_random_fact
import os

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename="discord.log",encoding="utf-8",mode="w")
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

running = False

GUILD_ID = 1082610699802517585

bot = commands.Bot(command_prefix=";", intents=intents)
task_loop = None

async def mainLoop(guild):
    print("running")
    try:
        print("1")
        channel = discord.utils.get(guild.text_channels, name="main", type=discord.ChannelType.text)
        while True:
            if channel is None:
                print("Channel not found!")
                return
            message = get_random_message()
            await channel.send(message)
            await asyncio.sleep(300)  # Wait for 5 minutes
    except asyncio.CancelledError:
        return

@bot.event
async def on_ready():
    print(f"Server bot started! {bot.user.name}")

    await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
    await bot.change_presence(activity=discord.Activity(name="Bruno Mars, Anderson .Paak",type=discord.ActivityType.listening))
    await asyncio.create_task(mainLoop(bot.get_guild(GUILD_ID)))

@bot.tree.command(name="roll",description="Roll the dice",guild=discord.Object(id=GUILD_ID))
async def roll(interaction: discord.Interaction, min: int, max: int):
    user: discord.User
    user = interaction.user
    result = random.randint(min, max)

    await interaction.response.send_message("Rolling the dice... :game_die:")
    await asyncio.sleep(random.randint(1,3))
    await interaction.edit_original_response(content=f"{user.mention}, you rolled **{result}**!")
    
@bot.tree.command(name="ping",description="Check the bot's latency.",guild=discord.Object(id=GUILD_ID))
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong! Latency is {bot.latency * 1000:.2f}ms")

@bot.tree.command(name="randomfact", description="Get a random fact.", guild=discord.Object(id=GUILD_ID))
async def randomfact(interaction: discord.Interaction):
    await interaction.response.send_message("Thinking...")
    random_fact = await get_random_fact()
    print(random_fact)

    await interaction.edit_original_response(content=random_fact)


bot.run(token, log_handler=handler, log_level=logging.DEBUG)