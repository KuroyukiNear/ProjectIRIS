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
Version: v2.2.1
"""

IRIS_version = "2.2.1"

# Discord Modules
import discord
from discord import app_commands
from discord.ext import commands, tasks

# Utility Modules
import os
import sys
import time
import json
import random
from pathlib import Path
from itertools import cycle
from datetime import datetime
from dotenv import load_dotenv


# Client Settings
intents = discord.Intents.all()
client = commands.AutoShardedBot(command_prefix=".", help_command=None, intents=intents)
path = os.path.dirname(__file__)
# Log Settings
user_join = True
deleted_message = True
edited_message = True
censored_message = True
voice_events = True
# Channel ID
channelID = 1122103608419291236 
user_join = channelID
deleted_message = channelID
edited_message = channelID
censored_message = channelID
voice_events = channelID
watched_message = 1198955918742802563
feedback_channel = 1199017405209383125
# Watched Words
with open("watchedWords.txt") as watchWordsFile:
    watchedWords = [line.rstrip() for line in watchWordsFile]
# Dictionaries & Lists
voice_timers = {}
space = "     "
Watchlist = [0]
ownerID = [638342719592202251, 729854914812968991]
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


os.system('title ProjectIRIS Central Controller')


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
    prLightGray(f"{space}Logged in as {client.user}")
    prLightGray(f"{space}User ID: {client.user.id}")
    prLightGray(f"{space}Logged in at {login_time}")
    prLightGray(f"{space}Iris Version: {IRIS_version}")
    prLightGray(f"{space}Discord Version: {discord.__version__}")
    prLightGray(f"{space}Python Version: {sys.version}")
    prRed('<=>--------------------------------<=>')

    server = len(client.guilds)
    server_count = int(server)

    prLightGray(f"{space}Connected to")
    prLightGray(f"{space}{server_count} Discord Guilds")
    prRed('<=>--------------------------------<=>')
    guild_number = 0
    for guild in client.guilds:
      guild_number = guild_number + 1
      prLightGray(f"{space}[{guild_number}] {guild} | ID:{guild.id} | {guild.owner}")
    prRed('<=>--------------------------------<=>')
    channel = client.get_channel(1193155470186266754)
    message = await channel.fetch_message(1193237727144054865)
    restartTimes = int(message.content) + 1
    await message.edit(content=f"{restartTimes}")
    restimemsg = await channel.fetch_message(1193237749596180480)
    await restimemsg.edit(content=f"**Last Restart:**{login_time}\n**Iris Version:** {IRIS_version}\n**Discord Version:** {discord.__version__}\n**Python Version:** {sys.version}")


# Bot Status
status_cycle = ["with papa", "Minecraft"]
status = cycle(status_cycle)

@tasks.loop(seconds=5)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))


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


# Check if user exists in customResponses.json
def user_exists(user_id):
    # Opening JSON file
    userjson = open("customResponses.json", encoding="UTF-8")
    userlist = json.load(userjson)
    # Load the existing JSON data
    with open("customResponses.json") as userjson:
        userlist = json.load(userjson)
    # Access the "users" array
    users = userlist.get("users", [])
    # Check if the user ID exists in the "users" array
    return any(user['ID'] == user_id for user in users)
def user_notExist(user_id):
    # Opening JSON file
    userjson = open("customResponses.json", encoding="UTF-8")
    userlist = json.load(userjson)
    # Access the "users" array
    users = userlist.get("users", [])
    # Check if the user ID does not exist in the "users" array
    return not any(user['ID'] == user_id for user in users)



# Message Detection
@client.event
async def on_message(message):
    now = datetime.now()
    event_time = now.strftime("%Z %d/%b/%Y %H:%M:%S")
    if message.author.id == client.user.id:
        return
    
    ## Watched Words
    if any(word.casefold() in message.content.casefold() for word in watchedWords):
        user = message.author
        channel = message.channel
        msg_link = f"https://discord.com/channels/{message.guild.id}/{channel.id}/{message.id}"
        embed = discord.Embed(title=f"Watched Word Detected from {user} in {message.guild}",description=(f"{user.mention} **|** {msg_link}"),colour=discord.Colour.purple())
        embed.add_field(name=f"Content", value=f"{message.content}", inline=False)
        embed.add_field(name=f"ID", value=f"```\n Channel = {channel.id} \n User = {user.id} \n Message = {message.id} \n```", inline=False)
        embed.timestamp = message.created_at
        channel = client.get_channel(watched_message)
        await channel.send(embed=embed)
        now = datetime.now()
        event_time = now.strftime("%Z %d/%b/%Y %H:%M:%S")
        log = f"[{event_time}] [LOG] Watched Word Detected\nUser: {user}({user.id})\nServer: {message.guild}({message.guild.id})\nContent: {message.content}"
        logfile = open(r"D:\\IRIS.log", "a", encoding="utf-8")
        logfile.write(f"\n\n{log}")
        print(log)
    
    ## Bot Mentions
    if client.user.mentioned_in(message):
        log = f"[{event_time}] [LOG] Iris pinged by {message.author}({message.author.id})"
        # Opening JSON file
        userjson = open("customResponses.json", encoding="UTF-8")
        userlist = json.load(userjson)
        # Check if user ID exists
        userid_to_check = message.author.id
        if user_exists(userid_to_check):
            # Get User
            userid_to_find = message.author.id
            users_list = userlist.get("users", [])
            for user in users_list:
                if user['ID'] == userid_to_find:
                    # Get responses
                    responses = user["responses"]
                    responses = random.choice(responses)
                    await message.reply(responses)
                    logfile = open(r"D:\\IRIS.log", "a", encoding="utf-8")
                    logfile.write(f"\n\n{log}")
                    print(log)
        if user_notExist(userid_to_check):
            log = f"[{event_time}] [LOG] Iris pinged by {message.author}({message.author.id})"
            # Opening JSON file
            userjson = open("customResponses.json", encoding="UTF-8")
            userlist = json.load(userjson)
            # Get User
            users_list = userlist.get("users", [])
            for user in users_list:
                if user['ID'] == 0:
                    # Get responses
                    responses = user["responses"]
                    responses = random.choice(responses)
                    await message.reply(responses)
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
    await interaction.response.send_message(f"**[** {choice1} **|** {choice2} **]** \n{IRISchoose}")


# Ping Check
@client.tree.command(name = "ping", description = "Checks Iris' latency.")
async def ping(interaction):
    await interaction.response.send_message(f"{round(client.latency * 1000)}ms")


# User Status Count
@tasks.loop(seconds=10)
async def usercount():
    now = datetime.now()
    refresh_time = now.strftime("%H:%M:%S")
    # Count members
    server = client.get_guild(863253117684678658) #學術寶庫
    online_members = []
    offline_members = []
    idle_members = []
    dnd_members = []
    for member in server.members:
        if member.status == discord.Status.online:
            online_members.append(member.name)
        if member.status == discord.Status.offline:
            offline_members.append(member.name)
        if member.status == discord.Status.idle:
            idle_members.append(member.name)
        if member.status == discord.Status.dnd:
            dnd_members.append(member.name)
    online = len(online_members)
    offline = len(offline_members)
    idle = len(idle_members)
    dnd = len(dnd_members)
    # Live Status Message Edit
    channel = client.get_channel(1193155470186266754)
    message = await channel.fetch_message(1193484403574325278)
    newmsg = f"**{server} Member Status**\n**Total Members: {server.member_count}**\n*Refreshes every 10 seconds* **|** *Last Refresh: {refresh_time}*\n:green_circle: {online}\n:orange_circle: {idle}\n:red_circle: {dnd}\n:white_circle: {offline}"
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


# [Console] Developer Info
## Guild List
@client.tree.command(name = "guilds", description = "Console Command", guild=discord.Object(id=952892062552981526))
async def devinfo(ctx: discord.Interaction):
    if ctx.user.id in ownerID:
        page = 0
        # Guilds
        for i in range(0, len(client.guilds), 9):
            page = page + 1
            server_list = discord.Embed(title="Project IRIS Guild List",
                                        description=f"***Page {page}***",
                                        colour=discord.Colour.dark_red())
            guilds = client.guilds[i:i + 9]
            for guild in guilds:
                server_list.add_field(
                    name=guild.name,
                    value=
                    f"`{guild.id}` \n ***{guild.member_count} members***")
            server_list.set_footer(
                text=f"Developer Info requested by {ctx.user}")
            await ctx.user.send(embed=server_list)
        await ctx.response.send_message(
            f"I'm currently connected to **{len(client.guilds)} servers** <:anime_brighteyes:943480188195442758> More detailed information has been sent to your DMs! <a:UruhaRushia_happy:940254774094364694>")
    else:
        await ctx.response.send_message("Only papa can use this command!")

## Members
@client.tree.command(name = "members", description = "Console Command", guild=discord.Object(id=952892062552981526))
@app_commands.describe(guild = "Enter guild ID.")
async def devinfo(ctx: discord.Interaction, guild: str):
    guild_id = int(guild)
    server = client.get_guild(guild_id)
    if ctx.user.id in ownerID:
        page = 0

        for i in range(0, len(server.members), 50):
            page = page + 1
            type_bot = 0
            type_user = 0
            member_list = discord.Embed(
                title=f"{server}",
                description=f"***Page {page} | Guild ID: `{server.id}` ***",
                colour=discord.Colour.dark_red())
            members = server.members[i:i + 50]
            for member in members:
                if member.bot:
                    bot = "Bot"
                    type_bot += 1
                else:
                    bot = ""
                    type_user += 1
                member_list.add_field(name=f"{member} {bot}",
                                        value=f"`{member.id}`",
                                        inline=True)
            member_list.set_footer(
                text=f"{type_user} Users | {type_bot} Bots")
            await ctx.user.send(embed=member_list)
        await ctx.response.send_message(
            f"**{server}** currently has **{len(server.members)} members** <:anime_brighteyes:943480188195442758> More detailed information has been sent to your DMs! <a:UruhaRushia_happy:940254774094364694>")
    else:
        await ctx.response.send_message("Only papa can use this command!")

## Channels
@client.tree.command(name = "channels", description = "Console Command", guild=discord.Object(id=952892062552981526))
@app_commands.describe(guild = "Enter guild ID.")
async def devinfo(ctx: discord.Interaction, guild: str):
    guild_id = int(guild)
    server = client.get_guild(guild_id)
    if ctx.user.id in ownerID:
        page = 0
        # Text Channels
        for i in range(0, len(server.text_channels), 25):
            page = page + 1
            text_channel_list = discord.Embed(
                title=f"{server}",
                description=
                f"***Page {page} | Guild ID: `{server.id}` | Text Channels ***",
                colour=discord.Colour.dark_red())
            channels = server.text_channels[i:i + 25]
            for channel in channels:
                text_channel_list.add_field(name=f"#{channel.name}",
                                            value=f"`{channel.id}`",
                                            inline=True)
            text_channel_list.set_footer(
                text=f"{len(server.text_channels)} Text Channels",)
            await ctx.user.send(embed=text_channel_list)
        # Voice Channels
        for i in range(0, len(server.voice_channels), 25):
            page = page + 1
            voice_channel_list = discord.Embed(
                title=f"{server}",
                description=
                f"***Page {page} | Guild ID: `{server.id}` | Voice Channels ***",
                colour=discord.Colour.dark_red())
            channels = server.voice_channels[i:i + 25]
            for channel in channels:
                voice_channel_list.add_field(
                    name=f":speaker:{channel.name}",
                    value=f"`{channel.id}`",
                    inline=True)
            voice_channel_list.set_footer(
                text=f"{len(server.voice_channels)} voice Channels",)
            await ctx.user.send(embed=voice_channel_list)
        await ctx.response.send_message(
            f"**{server}** currently has **{len(server.text_channels)} text channels** and **{len(server.voice_channels)} voice channels** <:anime_brighteyes:943480188195442758> More detailed information has been sent to your DMs! <a:UruhaRushia_happy:940254774094364694>")
    else:
        await ctx.response.send_message("***Error*** You can't use that command.")


# [CONSOLE] Clear DM
@client.tree.command(name = "cls", description = "Clears your DM", guild=discord.Object(id=952892062552981526))
async def cls(ctx: discord.Interaction):
    await ctx.response.send_message("This might take a while.")
    remove = 9999999999999999999999999999999999999999
    remove = remove * remove * remove
    async for message in ctx.user.history(limit=remove):
        remove = remove + 1
        if message.author.id == client.user.id:
            await message.delete()
            time.sleep(0.5)
    await ctx.channel.send("All messages in the DM has been deleted.")


# Feedback Command
@client.tree.command(name = "feedback", description = "Feedback about your experiences with Iris")
@app_commands.describe(feedback = "Enter your feedback.")
async def say(ctx: discord.Interaction, feedback: str):
    embed = discord.Embed(title=f"Feedback Received",description=(f"{feedback}"),colour=discord.Colour.dark_red())
    embed.add_field(name=f"{ctx.guild}", value=f"{ctx.user.name} | {ctx.user.mention}", inline=False)
    channel = client.get_channel(feedback_channel)
    await channel.send(embed=embed)
    await ctx.response.send_message("Your feedback has been received!")


# Info Command
@client.tree.command(name = "info", description = "More information about Iris")
async def info(ctx: discord.Interaction):
    embed = discord.Embed(title=f"Project IRIS Info",colour=discord.Colour.dark_red())
    embed.add_field(name=f"Owner", value=f"**Kuroyuki Near** `kuroyukinear`", inline=False)
    embed.add_field(name=f"Developers", value=f"**Kuroyuki Near** `kuroyukinear`", inline=False)
    embed.add_field(name=f"Public Relations", value=f"**Skully** `skull1fy`", inline=False)
    embed.add_field(name=f"Links", value=f"[More Info](https://kuroyukinear.github.io/Near/projects/ProjectIRIS.html) \n [Support Server](https://www.discord.gg/9RUy6suKsy)", inline=False)
    await ctx.response.send_message(embed=embed)


# Register new user
def register_user(user_id, wallet, bank, bio, badges, total_earned, total_spent, peak_wealth, commands_issued):
    # Opening JSON file
    userjson = open("profiles.json")
    # Load the existing JSON data
    with open("profiles.json") as userjson:
        data = json.load(userjson)

    # Create a new user object
    new_user = {
        "ID": user_id,
        "wallet": wallet,
        "bank": bank,
        "bio": bio,
        "badges": badges,
        "total_earned": total_earned,
        "total_spent": total_spent,
        "peak_wealth": peak_wealth,
        "commands_issued": commands_issued
    }

    # Add the new user to the "users" array
    data["users"].append(new_user)
    # Save the updated data back to the JSON file
    with open("profiles.json", "w") as userjson:
        json.dump(data, userjson, indent=4)


# Check if user exists in profiles.json
def user_exists(user_id):
    # Opening JSON file
    userjson = open("profiles.json")
    userlist = json.load(userjson)
    # Load the existing JSON data
    with open("profiles.json") as userjson:
        userlist = json.load(userjson)
    # Access the "users" array
    users = userlist.get("users", [])
    # Check if the user ID exists in the "users" array
    return any(user['ID'] == user_id for user in users)


# Display Profile
@client.tree.command(name = "profile", description = "Displays a user's profile")
async def profile(ctx: discord.Interaction, member: discord.Member = None):
    # Opening JSON file
    userjson = open("profiles.json")
    userlist = json.load(userjson)
    # If user is mentioned
    if member == None:
        user = ctx.user
        username = ctx.user
    else:
        user = member
        username = member

    # Check if user ID exists
    userid_to_check = user.id
    if user_exists(userid_to_check):
        # Get User
        userid_to_find = user.id
        users_list = userlist.get("users", [])
        for user in users_list:
            if user['ID'] == userid_to_find:
                # Get RixCoins
                wrix = user["wallet"]
                brix = user["bank"]
                rix = f"`{wrix + brix}`"
                
                # Get bio
                bio = user["bio"]
                # Get badges
                user_badges = user.get("badges", [])
                badges = ', '.join(map(str, user_badges))

        # Embed Profile
        info = discord.Embed(title=f"{username}'s Profile",
                            description=badges,
                            colour=discord.Colour.dark_red())
        info.add_field(name="RixCoins", value=f"{rix}", inline=True)
        info.add_field(name="Messages Sent",
                    value=f"`Under Development`",
                    inline=False)
        info.add_field(name="Bio", value=f"{bio}", inline=False)
        await ctx.response.send_message(embed=info)

    # Register if user does not exist
    else:
        register_user(
            user_id=userid_to_check,
            wallet=50,
            bank=0,
            bio="Use `/bio` to edit your bio",
            badges=["`no badges`"],
            total_earned=0,
            total_spent=0,
            peak_wealth=0,
            commands_issued=0
        )
        await ctx.response.send_message("User has just been registered. Please use `/profile` again.")


# Edit Bio
@client.tree.command(name = "bio", description = "Edit your bio")
async def bio(ctx: discord.Interaction, newbio: str):
    # Opening JSON file
    userjson = open("profiles.json")
    userlist = json.load(userjson)
    # Get user
    userid_to_find = ctx.user.id
    users_list = userlist.get("users", [])
    for user in users_list:
        if user['ID'] == userid_to_find:
            # Edit bio
            user["bio"] = newbio
    # Save the modified data back to the JSON file
    with open("profiles.json", "w") as userjson:
        json.dump(userlist, userjson, indent=4)
        await ctx.response.send_message(
            "Your bio has been changed.\nNote: if `/profile` is not working after you changed your bio, you have probably exceeded the 1,000 word limit."
        )


# Balance
@client.tree.command(name = "balance", description = "Displays a user's balance")
async def profile(ctx: discord.Interaction, member: discord.Member = None):
    # Opening JSON file
    userjson = open("profiles.json")
    userlist = json.load(userjson)
    # If user is mentioned
    if member == None:
        user = ctx.user
        username = ctx.user
    else:
        user = member
        username = member

    # Check if user ID exists
    userid_to_check = user.id
    if user_exists(userid_to_check):
        # Get User
        userid_to_find = user.id
        users_list = userlist.get("users", [])
        for user in users_list:
            if user['ID'] == userid_to_find:
                # Get RixCoins
                wrix = user["wallet"]
                brix = user["bank"]
                rix = f"`{wrix + brix}`"

        # Embed Profile
        info = discord.Embed(title=f"{username}'s Profile",
                            description=f"Networth: `{rix}`RC",
                            colour=discord.Colour.dark_red())
        info.add_field(name="Wallet", value=f"`{wrix}`RC", inline=True)
        info.add_field(name="Bank",
                    value=f"`{brix}`RC",
                    inline=True)
        await ctx.response.send_message(embed=info)

    # Register if user does not exist
    else:
        register_user(
            user_id=userid_to_check,
            wallet=50,
            bank=0,
            bio="Use `/bio` to edit your bio",
            badges=["`no badges`"],
            total_earned=0,
            total_spent=0,
            peak_wealth=0,
            commands_issued=0
        )
        await ctx.response.send_message("User has just been registered. Please use `/balance` again.")

# Connect
load_dotenv()
token = os.getenv('TOKEN')
client.run(token)

'''
<-> DEV LOG <->
11 JAN 2024
Started writing a dev log. Simply to let future me know that
I will probably be having mental breakdowns while writing this code.

21 JAN 2024
Copied the old devinfo function but discord.py has updated a lot
these few years so I spent some time debugging old code. Ugh.
I decided to stop versioning and use Source Control to commit all
changes to keep track of the updates. And I get more GitHub commit
histories. Win-Win situation I guess.
'''
