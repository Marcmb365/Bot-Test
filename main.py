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

GUILD_ID = 1382198913360203838
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
            await asyncio.sleep(CONFIG.get("RANDOM_MESSAGE_INTERVAL", 180))  # Wait for X minutes
            message = get_random_message()
            await channel.send(message)
    except asyncio.CancelledError:
        return

async def scheduled_dm():
    await bot.wait_until_ready()
    guild = bot.get_guild(GUILD_ID)

    if guild is None:
        raise Exception("Guild not found!")
        return
    
    if not CONFIG.get("SEND_RELIGIOUS_MESSAGE"):
        print("will not send religious message")
        return
    
    for member in guild.members:
        if not member.bot:
            try:
                IMAGE_LINK = "https://cdn.discordapp.com/attachments/1273504161866059877/1421647831168712896/IMG_0249.jpg?ex=68d9cc37&is=68d87ab7&hm=cb25809d26eacb1e68bbb858cf7d6d841a613694281df1facc93401ab80da38d&"
                await member.send(
                    content=f"{member.mention}, “أنا أراقبك منذ فترة طويلة، وأعرف متى تفتح هاتفك ومتى تغلقه. لا تحاول أن تختبئ، فأنا أرى حتى عندما تظن أنك وحدك في الظلام. قريباً جداً… سأجعلك تعرف من أنا.”"
                )
                await member.send(content=IMAGE_LINK)
                await asyncio.sleep(0.8)
            except Exception as e:
                print(f"Could not send message to {member.name}.")
                print(e)

async def smoke_loop():
    await bot.wait_until_ready()
    guild = bot.get_guild(GUILD_ID)
    channel = discord.utils.get(guild.text_channels, name="main", type=discord.ChannelType.text)

    if channel is None:
        return
    
    while True:
        await channel.send(f"<@{CONFIG.get('SCOPEIVEE_USERID')}> trynna smoke or sum :smoking:")
        await asyncio.sleep(3600)

@bot.event
async def on_ready():
    print(f"Server bot started! {bot.user.name}")

    await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
    await bot.change_presence(activity=discord.Activity(name="Bruno Mars, Anderson .Paak",type=discord.ActivityType.listening))
    asyncio.create_task(mainLoop(bot.get_guild(GUILD_ID)))
    asyncio.create_task(scheduled_dm())
    asyncio.create_task(smoke_loop())

@bot.event
async def on_message(message: discord.Message):
    SIX_SEVEN_GIF = 'https://tenor.com/view/scp-067-67-6-7-six-seven-sixty-seven-gif-13940852437921483111'
    if 'majestic' in message.content.lower() and message.author != bot.user:
        await message.channel.send("majesticshadows reference")
    elif ('6' in message.content and '7' in message.content) and message.author != bot.user:
        await message.reply(content=f"{SIX_SEVEN_GIF}")
    elif ('six' in message.content.lower() and 'seven' in message.content.lower()) and message.author != bot.user:
        await message.reply(content=f"{SIX_SEVEN_GIF}")

@bot.event
async def on_voice_state_update(member: discord.Member, before, after: discord.VoiceProtocol):

    guild = bot.get_guild(GUILD_ID)
    if before.channel is None and after.channel is not None:
        user_id = member.id
        channel = discord.utils.get(guild.text_channels, name="main", type=discord.ChannelType.text)

        USER_IDS = {
            1313715323978907693: "https://media.discordapp.net/attachments/1303269364975538196/1421169333530529893/image.png?ex=68d8b755&is=68d765d5&hm=9d2601ddf0707fa410bc22a7e83cfe913299f304a7b1c007f34d8aa82cadfd58&=&format=webp&quality=lossless",
            689656574074945580: "https://media.discordapp.net/attachments/1273504161866059877/1421353647937421382/v09044g40000cq2kn6vog65lolhs5fcg.mov?ex=68d8ba3d&is=68d768bd&hm=d0c99ec4bbe9827afe4c1b8dc368b5c39be18ce241b9b9f9a79bd5a663e48333&",
            578447958216015872: "https://tenor.com/view/yuimetal-gif-2236335851178412850",
        }

        if USER_IDS.get(user_id) is not None:
            await channel.send(f"<@{user_id}> {USER_IDS.get(user_id)}")

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

@bot.tree.command(name="kick", description="Kick a user from the server.", guild=discord.Object(id=GUILD_ID))
async def kick(interaction: discord.Interaction, user: discord.User):
    author = interaction.user

    if author.id == CONFIG.get("SCOPEMATT_USERID") or author.id == CONFIG.get("SCOPEIVEE_USERID"):
        guild = bot.get_guild(GUILD_ID)
        member = guild.get_member(user.id)

        if member is None:
            await interaction.response.send_message(f"{user.mention} is not in the server.")
            return

        try:
            await member.kick(reason="fuck off")
            await interaction.response.send_message(f"{user.mention} was kicked from the server.")
        except Exception as e:
            await interaction.response.send_message(f"Failed to kick {user.mention}.")
            print(e)

bot.run(token, log_handler=handler, log_level=logging.DEBUG)