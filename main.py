import discord
import time
import asyncio
import random
import json
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
CONFIG = json.loads(open('config.json').read())

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
            await asyncio.sleep(CONFIG.get("RANDOM_MESSAGE_INTERVAL", 180))  # Wait for X minutes
    except asyncio.CancelledError:
        return

async def scheduled_dm():
    await bot.wait_until_ready()
    guild = bot.get_guild(GUILD_ID)

    if guild is None:
        raise Exception("Guild not found!")
        return
    
    for member in guild.members:
        if not member.bot:
            try:
                await member.send(
                    content=f"{member.mention}, ✝️🙏 This is a Christian blessing chain. If you’re reading this, God has already touched your day with His love. Don’t break the blessing! Send this to 10 friends and watch what happens. Within 24 hours, you’ll hear good news. If you keep it to yourself, nothing bad will happen… but you’ll be missing out on the chance to share His light! 🌟🙏✝️"
                )
                await asyncio.sleep(1)
            except Exception as e:
                print(f"Could not send message to {member.name}.")
                print(e)

@bot.event
async def on_ready():
    print(f"Server bot started! {bot.user.name}")

    await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
    await bot.change_presence(activity=discord.Activity(name="Bruno Mars, Anderson .Paak",type=discord.ActivityType.listening))
    asyncio.create_task(mainLoop(bot.get_guild(GUILD_ID)))
    asyncio.create_task(scheduled_dm())

@bot.event
async def on_message(message: discord.Message):
    if 'majestic' in message.content.lower():
        await message.channel.send("majesticshadows reference")

@bot.event
async def on_voice_state_update(member: discord.Member, before, after: discord.VoiceProtocol):
    print("yo")
    guild = bot.get_guild(GUILD_ID)
    if before.channel is None and after.channel is not None:
        print("hi")
        user_id = member.id

        WZO_USER_ID = 882213922822832170
        VIDEO_LINK = "https://media.discordapp.net/attachments/1273504161866059877/1421353647937421382/v09044g40000cq2kn6vog65lolhs5fcg.mov?ex=68d8ba3d&is=68d768bd&hm=d0c99ec4bbe9827afe4c1b8dc368b5c39be18ce241b9b9f9a79bd5a663e48333&"
        if user_id == WZO_USER_ID:
            channel = discord.utils.get(guild.text_channels, name="main", type=discord.ChannelType.text)
            await channel.send(f"{member.mention} {VIDEO_LINK}")

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