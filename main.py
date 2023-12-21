# Discord Modules
import discord
from discord import app_commands
from discord.ext import commands, tasks


# Utility Modules
import os
import random
from pathlib import Path
from itertools import cycle
from datetime import datetime


# Client Settings
intents = discord.Intents.all()
client = commands.AutoShardedBot(command_prefix=".", help_command=None, intents=intents)
path = os.path.dirname(__file__)


# Channel ID
channelID = 1122103608419291236 
user_join = channelID
deleted_message = channelID
edited_message = channelID
censored_message = channelID
voice_events = channelID
# User ID
ownerID = 638342719592202251


# Connect
@client.event
async def on_ready():
    for server in client.guilds:
        await client.tree.sync(guild=discord.Object(id=server.id))
    change_status.start()
    now = datetime.now()
    login_time = now.strftime("%H:%M:%S")
    print('<=>--------------------------------<=>')
    print('     ', f"Logged in as {client.user}")
    print('     ', f"User ID: {client.user.id}")
    print('     ', f"Logged in at {login_time}")
    print('     ', f"Discord Version: {discord.__version__}")
    print('<=>--------------------------------<=>')

    server = len(client.guilds)
    server_count = int(server)

    print('     ', "Connected to")
    print('     ', f"{server_count} Discord Guilds")
    print('<=>--------------------------------<=>')
    guild_number = 0
    for guild in client.guilds:
      guild_number = guild_number + 1
      print('     ', f"[{guild_number}] {guild} | ID:{guild.id}")
    print('<=>--------------------------------<=>')


# Bot Status
status_cycle = ["with papa", "Minecraft"]
status = cycle(status_cycle)

@tasks.loop(seconds=5)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))


# Iris Responses
papa = ["hi papa", "hello papa", "Minecraft?"]
user = ["halo~", "hii"]
luby = ["會長早晨！", "hi Luby姐姐"]
summy = ["小朋友唔好再沉迷BL", "考試喇同學", "hi summy"]
kelvin_2050 = ["hi Kelvin", "hello~"]


# Deleted Message Log
@client.event
async def on_message_delete(message: str):
  user = message.author
  channel = message.channel
  embed = discord.Embed(title=f"{user} deleted a message in {message.guild}",description=(f"{user.mention} **|** {channel.mention}"),colour=discord.Colour.purple())
  embed.add_field(name=f"Content", value=f"{message.content}", inline=False)
  embed.add_field(name=f"ID", value=f"```\n Channel = {channel.id} \n User = {user.id} \n Message = {message.id} \n```", inline=False)
  embed.timestamp = message.created_at
  channel = client.get_channel(deleted_message)
  await channel.send(embed=embed)


# Edited Message Log
@client.event
async def on_message_edit(message_before, message_after):
  if message_before.author == message_before.author.bot:
    return
  else:
    msg = message_after
    user = msg.author
    channel = msg.channel
    server = msg.guild
    msg_link = f"https://discord.com/channels/{server.id}/{channel.id}/{msg.id}"
    embed = discord.Embed(title=f"{user} edited a message in {msg.guild}",description=(f"{user.mention} **|** {channel.mention} **|** {msg_link}"),colour=discord.Colour.purple())
    embed.add_field(name=f"Original Message", value=f"{message_before.content}", inline=False)
    embed.add_field(name=f"Edited Message", value=f"{message_after.content}", inline=False)
    embed.add_field(name=f"ID", value=f"```\n Channel = {channel.id} \n User = {user.id} \n Message = {msg.id} \n```", inline=False)
    embed.timestamp = msg.created_at
    channel = client.get_channel(edited_message)
    await channel.send(embed=embed)


# Message Detection
@client.event
async def on_message(message):
    if message.author.id == client.user.id:
        return
    
    # Banned Words
    bannedWords = ["testcode", "testcode2"]
    if any(word in message.content for word in bannedWords):
        await message.delete()
    
    # Bot Mentions
    if client.user.mentioned_in(message):
        papa_response = random.choice(papa)
        user_response = random.choice(user)
        luby_response = random.choice(luby)
        summy_response = random.choice(summy)
        kelvin_2050_response = random.choice(kelvin_2050)
        special_ID = [638342719592202251, 863088507740356609, 819114388212154368, 674279699605880872]
        if message.author.id == 638342719592202251:
          await message.reply(papa_response)
        if message.author.id == 863088507740356609:
          await message.reply(luby_response)
        if message.author.id == 819114388212154368:
          await message.reply(summy_response)
        if message.author.id == 674279699605880872:
          await message.reply(kelvin_2050_response)
        if message.author.id not in special_ID:
          await message.reply(user_response)


# Voice Channel Log
@client.event
async def on_voice_state_update(user, before, after):
    # Channel Join Log
    if before.channel is None and after.channel is not None:
       embed = discord.Embed(title=f"{user} joined :speaker:{after.channel}",description=(f"{user.mention} **|** {after.channel.guild} **|** {after.channel.mention}"),colour=discord.Colour.purple())
       embed.add_field(name=f"ID", value=f"```\n Channel = {after.channel.id} \n User = {user.id} \n```", inline=False)
       channel = client.get_channel(voice_events)
       await channel.send(embed=embed)
       # Channel Leave Log
    if before.channel is not None and after.channel is None:
       embed = discord.Embed(title=f"{user} left :speaker:{before.channel}",description=(f"{user.mention} **|** {before.channel.guild} **|** {before.channel.mention}"),colour=discord.Colour.purple())
       embed.add_field(name=f"ID", value=f"```\n Channel = {before.channel.id} \n User = {user.id} \n```", inline=False)
       channel = client.get_channel(voice_events)
       await channel.send(embed=embed)
       # Channel Changed Log
    if before.channel != after.channel:
       embed = discord.Embed(title=f"{user} switched from :speaker:{before.channel} to :speaker:{after.channel}",description=(f"{user.mention} **|** {before.channel.guild}"),colour=discord.Colour.purple())
       embed.add_field(name=f"ID", value=f"```\n Before_Channel = {before.channel.id} \n After_Channel = {after.channel.id} \n User = {user.id} \n```", inline=False)
       channel = client.get_channel(voice_events)
       await channel.send(embed=embed)
    else:
       return


# Hello Command
@client.tree.command(name = "hello", description = "Says hello to Iris.")
async def hello(interaction):
    await interaction.response.send_message("Hello!")


# Iris Choice
@client.tree.command(name = "choose", description = "Lets Iris choose for you.")
@app_commands.describe(choice1 = "Enter first choice.")
@app_commands.describe(choice2 = "Enter second choice.")
async def choose(interaction: discord.Interaction, choice1: str, choice2: str):
    choice1 = choice1
    choice2 = choice2
    choices = [choice1, choice2]
    IRISchoose = random.choice(choices)
    await interaction.response.send_message(f"**[** {choice1} **|** {choice2} **]** \n I choose: {IRISchoose}")


# Ping Check
@client.tree.command(name = "ping", description = "Checks Iris' latency.")
async def ping(interaction):
    await interaction.response.send_message(f"{round(client.latency * 1000)}ms")


# Display Profile
@client.tree.command(name = "profile", description = "Displays your profile.", guild=discord.Object(id=863253117684678658))
async def profile(interaction):
    user = interaction.user
    # Get Points
    point_file = Path(f"{path}\\data\\points\\{user.id}.dat")
    if point_file.exists():
        point_file = open(f"{path}\\data\\points\\{user.id}.dat", "r")
        points = point_file.read()
        points = f"`{points}`"
    else:
        f = open(f"{path}\\data\\points\\{user.id}.dat", "w")
        f.write(0)
        points = f.read()
        points = f"`{points}`"
    # Get Bio
    bio_file = Path(f"{path}\\data\\Bio\\{user.id}.dat")
    if bio_file.exists():
        bio_file = open(f"{path}\\data\\Bio\\{user.id}.dat", "r")
        bio = bio_file.read()
    else:
        f = open(f"{path}\\data\\Bio\\{user.id}.dat", "w")
        f.write("empty")
        f.close()
        bio = f.read()
    # Get Badges
    badges_file = Path(f"{path}\\data\\badges\\{user.id}.dat")
    if badges_file.exists():
        badges_file = open(f"{path}\\data\\badges\\{user.id}.dat", "r")
        badges_list = badges_file.readlines()
        rez = []
        for x in badges_list:
            rez.append(x.replace("\n", ""))
        badges = str(rez)
        badges = badges.replace("[", "")
        badges = badges.replace("]", "")
        badges = badges.replace("'", "")
        badges = badges.replace(",", "")
        IRIS_badges = f"{badges}"
    else:
        IRIS_badges = "No Badges"
    # Embed Profile
    info = discord.Embed(title=f"{user.name}'s Profile",
                         description="",
                         colour=discord.Colour.dark_red())
    info.add_field(name="RNG Points", value=f"{points}", inline=True)
    info.add_field(name="Messages Sent",
                   value=f"`Under Development`",
                   inline=False)
    info.add_field(name="ProjectIRIS Badges",
                   value=f"{IRIS_badges}",
                   inline=True)
    info.add_field(name="Bio", value=f"{bio}", inline=False)
    info.set_thumbnail(url=user.avatar.url)
    await interaction.response.send_message(embed=info)


# Join Voice
@client.tree.command(name = "join", description = "Joins VC.")
async def join(interaction: discord.Interaction):
    channel = interaction.user.voice.channel
    await channel.connect()
    await interaction.response.send_message("Connected")


# Leave Voice
@client.tree.command(name = "leave", description = "Leaves VC.")
async def leave(interaction: discord.Interaction):
    await interaction.guild.voice_client.disconnect()
    await interaction.response.send_message("Disconnected")


# [Console] Say Command
@client.tree.command(name = "say", description = "Console Command", guild=discord.Object(id=952892062552981526))
@app_commands.describe(say_text = "Enter message.")
@app_commands.describe(say_channel = "Enter channel ID.")
async def say(ctx: discord.Interaction, say_channel: str, say_text: str):
    if ctx.user.id == ownerID:
      channel = client.get_channel(int(say_channel))
      message = await channel.send(say_text)
      embed = discord.Embed(title=f"[Console] Say Command",description=(f"Message successfully sent."),colour=discord.Colour.dark_red())
      embed.add_field(name=f"User", value=f"{ctx.user.mention}", inline=False)
      embed.add_field(name=f"Channel", value=f"{channel.mention}", inline=False)
      embed.add_field(name=f"Message", value=f"https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}", inline=False)
      embed.add_field(name=f"Content", value=f"{message.content}", inline=False)
      await ctx.response.send_message(embed=embed)
    else:
       await ctx.response.send_message("Only papa can use this command!")


# [Console] Sync Command Tree
@client.tree.command(name="sync", description="Owner only", guild=discord.Object(id=952892062552981526))
async def sync(interaction: discord.Interaction):
    if interaction.user.id == ownerID:
        await client.tree.sync()
        await interaction.response.send_message("Command tree synced.")
    else:
        await interaction.response.send_message("Only papa can use this command!")


# Connect
token = "token"
client.run(token)
