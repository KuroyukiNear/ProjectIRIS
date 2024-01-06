"""
 ____            _           _     ___ ____  ___ ____  
|  _ \ _ __ ___ (_) ___  ___| |_  |_ _|  _ \|_ _/ ___| 
| |_) | '__/ _ \| |/ _ \/ __| __|  | || |_) || |\___ \ 
|  __/| | | (_) | |  __/ (__| |_   | ||  _ < | | ___) |
|_|   |_|  \___// |\___|\___|\__| |___|_| \_\___|____/ 
              |__/                                     


When I wrote this code,
only God and I knew how it worked.
Now, only God knows.

Last Edited: 07 January 2023
Version: v2.2.0
"""

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
ownerID = [638342719592202251, 729854914812968991]
# Iris Responses
papa = ["hi papa", "hello papa", "ello"]
user = ["halo~", "hii"]
luby = ["會長早晨！", "hi Luby姐姐"]
summy = ["小朋友唔好再沉迷BL", "考試喇同學", "hi summy"]
# Banned Words
bannedWords = ["testcode", "testcode2"]
# Dictionaries & Lists
voice_timers = {}
space = "     "
# Utils
now = datetime.now()
login_time = now.strftime("%Z %d/%b/%Y %H:%M:%S")
logfile = Path("D:\\IRIS.log")
# Colour Code Functions
def prRed(skk): print("\033[91m {}\033[00m" .format(skk))
def prGreen(skk): print("\033[92m {}\033[00m" .format(skk))
def prYellow(skk): print("\033[93m {}\033[00m" .format(skk))
def prLightPurple(skk): print("\033[94m {}\033[00m" .format(skk))
def prPurple(skk): print("\033[95m {}\033[00m" .format(skk))
def prCyan(skk): print("\033[96m {}\033[00m" .format(skk))
def prLightGray(skk): print("\033[97m {}\033[00m" .format(skk))
def prBlack(skk): print("\033[98m {}\033[00m" .format(skk))


# Connect
@client.event
async def on_ready():
    logfile = Path("D:\\IRIS.log")
    if logfile.is_file():
        logfile = open(r"D:\\IRIS.log", "a")
        prYellow(f"[{login_time}] [INFO] Log file exists in file path.")
    else:
        logfile = open(r"D:\\IRIS.log", "a")
        logfile.write(f"Project IRIS Console Log \nCreated on {login_time} \n<->=============================<->")
        prYellow(f"[{login_time}] [INFO] Log file does not exist.")
        prYellow(f"[{login_time}] [INFO] New log file created.")

    for server in client.guilds:
        await client.tree.sync(guild=discord.Object(id=server.id))
    change_status.start()
    usercount.start()
    prYellow(f"[{login_time}] [INFO] Iris has logged in.")
    logfile.write(f"\n[{login_time}] [INFO] Iris has logged in.")
    prRed('<=>--------------------------------<=>')
    prPurple(f"{space}Logged in as {client.user}")
    prPurple(f"{space}User ID: {client.user.id}")
    prPurple(f"{space}Logged in at {login_time}")
    prPurple(f"{space}Discord Version: {discord.__version__}")
    prRed('<=>--------------------------------<=>')

    server = len(client.guilds)
    server_count = int(server)

    prPurple(f"{space}Connected to")
    prPurple(f"{space}{server_count} Discord Guilds")
    prRed('<=>--------------------------------<=>')
    guild_number = 0
    for guild in client.guilds:
      guild_number = guild_number + 1
      prPurple(f"{space}[{guild_number}] {guild} | ID:{guild.id}")
    prRed('<=>--------------------------------<=>')
    channel = client.get_channel(1193155470186266754)
    message = await channel.fetch_message(1193237727144054865)
    restartTimes = int(message.content) + 1
    await message.edit(content=f"{restartTimes}")
    restimemsg = await channel.fetch_message(1193237749596180480)
    await restimemsg.edit(content=f"**Last Restart**: {login_time}")


# Bot Status
status_cycle = ["with papa", "Minecraft"]
status = cycle(status_cycle)

@tasks.loop(seconds=5)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))


# Deleted Message Log
@client.event
async def on_message_delete(message: str):
  if message in bannedWords:
    return
  else:
    user = message.author
    channel = message.channel
    embed = discord.Embed(title=f"{user} deleted a message in {message.guild}",description=(f"{user.mention} **|** {channel.mention}"),colour=discord.Colour.purple())
    embed.add_field(name=f"Content", value=f"{message.content}", inline=False)
    embed.add_field(name=f"ID", value=f"```\n Channel = {channel.id} \n User = {user.id} \n Message = {message.id} \n```", inline=False)
    embed.timestamp = message.created_at
    channel = client.get_channel(deleted_message)
    await channel.send(embed=embed)
    now = datetime.now()
    event_time = now.strftime("%Z %d/%b/%Y %H:%M:%S")
    log = f"[{event_time}] [LOG] Message Deleted\nUser: {user}({user.id})\nServer: {message.guild}({message.guild.id})\nContent: {message.content}"
    logfile = open(r"D:\\IRIS.log", "a", encoding="utf-8")
    logfile.write(f"\n\n{log}")
    print(log)


# Edited Message Log
@client.event
async def on_message_edit(message_before, message_after):
  if message_before.author == message_before.author.bot:
    return
  if message_before.content == message_after.content:
     return
  else:
    msg = message_after
    user = msg.author
    channel = msg.channel
    server = msg.guild
    msg_link = f"https://discord.com/channels/{server.id}/{channel.id}/{msg.id}"
    embed = discord.Embed(title=f"{user} edited a message in {server}",description=(f"{user.mention} **|** {channel.mention} **|** {msg_link}"),colour=discord.Colour.purple())
    embed.add_field(name=f"Original Message", value=f"{message_before.content}", inline=False)
    embed.add_field(name=f"Edited Message", value=f"{message_after.content}", inline=False)
    embed.add_field(name=f"ID", value=f"```\n Channel = {channel.id} \n User = {user.id} \n Message = {msg.id} \n```", inline=False)
    embed.timestamp = msg.created_at
    channel = client.get_channel(edited_message)
    await channel.send(embed=embed)
    now = datetime.now()
    event_time = now.strftime("%Z %d/%b/%Y %H:%M:%S")
    log = f"[{event_time}] [LOG] Message Edited\nUser: {user}({user.id})\nServer: {server}({server.id})\nContent: {message_before.content}\nEdited Content: {message_after.content}"
    logfile = open(r"D:\\IRIS.log", "a", encoding="utf-8")
    logfile.write(f"\n\n{log}")
    print(log)


# Message Detection
@client.event
async def on_message(message):
    now = datetime.now()
    event_time = now.strftime("%Z %d/%b/%Y %H:%M:%S")
    if message.author.id == client.user.id:
        return
    
    # Banned Words
    if any(word in message.content for word in bannedWords):
        log = f"[{event_time}] [LOG] Banned word detected."
        logfile = open(r"D:\\IRIS.log", "a", encoding="utf-8")
        logfile.write(f"\n\n{log}")
        print(log)
        await message.delete()
        log = f"[{event_time}] [LOG] Banned word deleted."
        logfile = open(r"D:\\IRIS.log", "a", encoding="utf-8")
        logfile.write(f"\n\n{log}")
        print(log)
    
    # Bot Mentions
    if client.user.mentioned_in(message):
        log = f"[{event_time}] [LOG] Iris pinged by {message.author}({message.author.id})"
        papa_response = random.choice(papa)
        user_response = random.choice(user)
        luby_response = random.choice(luby)
        summy_response = random.choice(summy)
        special_ID = [638342719592202251, 863088507740356609, 819114388212154368]
        if message.author.id == 638342719592202251:
          await message.reply(papa_response)
        if message.author.id == 863088507740356609:
          await message.reply(luby_response)
        if message.author.id == 819114388212154368:
          await message.reply(summy_response)
        if message.author.id not in special_ID:
          await message.reply(user_response)
        logfile = open(r"D:\\IRIS.log", "a", encoding="utf-8")
        logfile.write(f"\n\n{log}")
        print(log)


# Voice Channel Log
@client.event
async def on_voice_state_update(user, before, after):
    now = datetime.now()
    event_time = now.strftime("%Z %d/%b/%Y %H:%M:%S")

    # Channel Join Log
    if before.channel is None and after.channel is not None:
        voice_timers[user.id] = now

        embed = discord.Embed(title=f"{user} joined :speaker:{after.channel}",
                              description=(f"{user.mention} **|** {after.channel.guild} **|** {after.channel.mention}"),
                              colour=discord.Colour.green())
        embed.add_field(name=f"ID", value=f"```\n Channel = {after.channel.id} \n User = {user.id} \n```", inline=False)
        channel = client.get_channel(voice_events)
        await channel.send(embed=embed)

        log = f"[{event_time}] [LOG] Channel Join\nUser: {user}({user.id})\nServer: {after.channel.guild}({after.channel.guild.id})\nChannel: {after.channel}({after.channel.id})"
        logfile = open(r"D:\\IRIS.log", "a", encoding="utf-8")
        logfile.write(f"\n\n{log}")
        print(log)

    # Channel Leave Log
    elif before.channel is not None and after.channel is None:
        if user.id in voice_timers:
            start_time = voice_timers.pop(user.id)
            duration = now - start_time
            inthours = duration.seconds // 3600
            hours = str(inthours)
            intminutes = (duration.seconds // 60) % 60
            minutes = str(intminutes)
            intseconds = duration.seconds % 60
            seconds = str(intseconds)
            duration_str = f"{hours.zfill(2)}:{minutes.zfill(2)}:{seconds.zfill(2)}"

            embed = discord.Embed(title=f"{user} left :speaker:{before.channel}",
                                  description=(f"{user.mention} **|** {before.channel.guild} **|** {before.channel.mention}\n"
                                               f"Duration: {duration_str}"),
                                  colour=discord.Colour.red())
            embed.add_field(name=f"ID", value=f"```\n Channel = {before.channel.id} \n User = {user.id} \n```",
                            inline=False)
            channel = client.get_channel(voice_events)
            await channel.send(embed=embed)

            log = f"[{event_time}] [LOG] Channel Leave\nUser: {user}({user.id})\nServer: {before.channel.guild}({before.channel.guild.id})\nChannel: {before.channel}({before.channel.id})\nDuration: {duration_str}"
            logfile = open(r"D:\\IRIS.log", "a", encoding="utf-8")
            logfile.write(f"\n\n{log}")
            print(log)

    # Channel Switch Log
    elif before.channel != after.channel:
        if before.channel is not None and after.channel is not None:
            embed = discord.Embed(
                title=f"{user} switched from :speaker:{before.channel} to :speaker:{after.channel}",
                description=(f"{user.mention} **|** {after.channel.guild}"),
                colour=discord.Colour.orange())
            embed.add_field(name=f"ID",
                            value=f"```\n Before_Channel = {before.channel.id} \n After_Channel = {after.channel.id} \n User = {user.id} \n```",
                            inline=False)
            channel = client.get_channel(voice_events)
            await channel.send(embed=embed)

            log = f"[{event_time}] [LOG] Channel Switch\nUser: {user}({user.id})\nServer: {after.channel.guild}({after.channel.guild.id})\nBefore Channel: {before.channel}({before.channel.id}) | After Channel: {after.channel}({after.channel.id})"
            logfile = open(r"D:\\IRIS.log", "a", encoding="utf-8")
            logfile.write(f"\n\n{log}")
            print(log)

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


# User Status Count
@tasks.loop(seconds=60)
async def usercount():
    channel = client.get_channel(1193155470186266754)
    message = await channel.fetch_message(1193159545493663834)
    newmsg = int(message.content) + 1
    await message.edit(content=newmsg)


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
    if ctx.user.id in ownerID:
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
    if interaction.user.id in ownerID:
        await client.tree.sync()
        await interaction.response.send_message("Command tree synced.")
    else:
        await interaction.response.send_message("Only papa can use this command!")



# Connect
token = "token"
client.run(token)
