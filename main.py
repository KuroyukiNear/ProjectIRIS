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

Last Edited: 04 February 2023
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
import shutil
import random
import asyncio
import traceback
from pathlib import Path
from itertools import cycle
from datetime import datetime
from dotenv import load_dotenv
from io import StringIO, BytesIO


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
    
# Opening Config JSON file
with open("config.json") as configjson:
    # Load the existing JSON data
    configs = json.load(configjson)

# Accessing configs - channel ID
channel_id = configs.get("channel_id", {})
user_join = channel_id.get("user_join")
deleted_message = channel_id.get("deleted_message")
edited_message = channel_id.get("edited_message")
voice_events = channel_id.get("voice_events")
watched_message = channel_id.get("watched_message")
feedback_channel = channel_id.get("feedback_channel")
report_channel = channel_id.get("report_channel")
file_logger = channel_id.get("file_logger")

# Accessing configs - Log Settings
log_settings = configs.get("log_settings", {})
log_user_join = log_settings.get("user_join")
log_deleted_message = log_settings.get("deleted_message")
log_edited_message = log_settings.get("edited_message")
log_watched_message = log_settings.get("watched_message")
log_voice_events = log_settings.get("voice_events")
file_log_extensions = log_settings.get("file_log_extension", [])

# Watched Words
with open("watchedWords.txt") as watchWordsFile:
    watchedWords = [line.rstrip() for line in watchWordsFile]

# Dictionaries & Lists
voice_timers = {}
space = "     "
Watchlist = [0]
ownerID = [638342719592202251, 729854914812968991]
cooldowns = {}

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

    with open("profiles.json") as userjson:
        userlist = json.load(userjson)
    user_count = 0
    for user in userlist.get("users", []):
        user_count += 1

    prLightGray(f"{space}Connected to")
    prLightGray(f"{space}{server_count} Discord Guilds")
    prLightGray(f"{space}{user_count} Iris Users")
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


# Functions
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


# Create new log object
def create_log(guildName, guildID, channelName, channelID, authorName, authorID, messageID, eventTime, wordDetected, messageContent):
    # Opening JSON file
    logjson = open("watchedWords_log.json")
    # Load the existing JSON data
    with open("watchedWords_log.json") as logjson:
        data = json.load(logjson)
    # Create a new log object
    new_log = {
            "info": [
                {
                    "guildName": guildName,
                    "guildID": guildID
                },
                {
                    "channelName": channelName,
                    "channelID": channelID
                },
                {
                    "authorName": authorName,
                    "authorID": authorID
                },
                {
                    "messageID": messageID,
                    "eventTime": eventTime
                }
                    ],
                "wordDetected": wordDetected,
                "messageContent": messageContent
                    }
    # Add the new log to the "messages" array
    data["messages"].append(new_log)
    # Save the updated data back to the JSON file
    with open("watchedWords_log.json", "w", encoding="UTF-8") as logjson:
        json.dump(data, logjson, indent=4)


# Register new user
def register_user(user_id, wallet, bank, bio, badges, user_number, total_earned, total_spent, total_transfered, total_received, peak_wealth, commands_issued, inventory):
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
        "user_number": user_number,
        "total_earned": total_earned,
        "total_spent": total_spent,
        "total_transfered": total_transfered,
        "total_received": total_received,
        "peak_wealth": peak_wealth,
        "commands_issued": commands_issued,
        "inventory": inventory
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

# Commands Issued Counter
def commands_issued(user_id):
    # Opening JSON file
    userjson = open("profiles.json")
    userlist = json.load(userjson)
    # Load the existing JSON data
    with open("profiles.json") as userjson:
        userlist = json.load(userjson)
    # Get user
        userid_to_find = user_id
        users_list = userlist.get("users", [])
        for user in users_list:
            if user['ID'] == userid_to_find:
                # Rewrite data
                user_commands_issued = user["commands_issued"]
                new_user_commands_issued = user_commands_issued + 1
                user["commands_issued"] = new_user_commands_issued
    # Get Iris
        userid_to_find = 902720782503907358
        users_list = userlist.get("users", [])
        for user in users_list:
            if user['ID'] == userid_to_find:
                # Rewrite data
                user_commands_issued = user["commands_issued"]
                new_user_commands_issued = user_commands_issued + 1
                user["commands_issued"] = new_user_commands_issued
        # Save the modified data back to the JSON file
        with open("profiles.json", "w") as userjson:
            json.dump(userlist, userjson, indent=4)


# Function to get a random outcome based on probability distribution
def get_random_outcome(outcomes):
    rand_num = random.uniform(0, 1)
    cumulative_probability = 0

    for outcome in outcomes:
        cumulative_probability += outcome["probability"]
        if rand_num < cumulative_probability:
            # Return a random value within the specified range
            return random.choice(outcome["range"])


# Update Peak Wealth
def update_peak_wealth(user_id):
    # Opening JSON file
    with open("profiles.json", "r") as userjson:
        userlist = json.load(userjson)

    # Get user
    userid_to_find = user_id
    users_list = userlist.get("users", [])

    for user in users_list:
        if user['ID'] == userid_to_find:
            current_wealth = user['wallet'] + user['bank']

            # Check if the current wealth is higher than the recorded peak wealth
            if current_wealth > user['peak_wealth']:
                user['peak_wealth'] = current_wealth

    # Save the modified data back to the JSON file
    with open("profiles.json", "w") as userjson:
        json.dump(userlist, userjson, indent=4)


# Deleted Message Log
@client.event
async def on_message_delete(message: str):
    if message.author.id == client.user.id:
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
  if message_before.author.bot:
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
    guildName = message.guild.name
    guildID = message.guild.id
    channelName = message.channel.name
    channelID = message.channel.id
    authorName = message.author.name
    authorID = message.author.id
    messageContent = message.content
    messageID = message.id
    now = datetime.now()
    event_time = now.strftime("%Z %d/%b/%Y %H:%M:%S")

    if message.author.id == client.user.id:
        return
    
    ## Watched Words
    if any(word.casefold() in message.content.casefold() for word in watchedWords):
        matching_words = [word for word in watchedWords if word.casefold() in messageContent.casefold()]
        for matching_word in matching_words:
            wordDetected = matching_word
        now = datetime.now()
        eventTime = now.strftime("%Z %d/%b/%Y %H:%M:%S")
        create_log(guildName, guildID, channelName, channelID, authorName, authorID, messageID, eventTime, wordDetected, messageContent)
        msg_link = f"https://discord.com/channels/{guildID}/{channelID}/{messageID}"
        embed = discord.Embed(title=f"Watched Word Detected from {authorName} in {guildName}",description=(f"{message.author.mention} **|** {msg_link}"),colour=discord.Colour.purple())
        embed.add_field(name=f"Content", value=f"{message.content}", inline=False)
        embed.add_field(name=f"ID", value=f"```\n Guild = {guildID} \n Channel = {channelID} \n User = {authorID} \n Message = {messageID} \n```", inline=False)
        embed.timestamp = message.created_at
        channel = client.get_channel(watched_message)
        await channel.send(embed=embed)
    
    ## Bot Mentions
    if client.user.mentioned_in(message):
        if "@everyone" in message.content:
            return
        else:
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
        if not user_exists(userid_to_check):
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

    ## File Logger
    if message.attachments:
        # Check if there are attachments in the message
        for attachment in message.attachments:
            msg_link = f"https://discord.com/channels/{guildID}/{channelID}/{messageID}"
            if any(attachment.filename.lower().endswith(ext) for ext in file_log_extensions):
                file_log_channel = client.get_channel(file_logger)
                content = await attachment.read()
                
                # Text Files
                if attachment.filename.lower().endswith("txt"):
                    txt_file_like = StringIO(content.decode('utf-8'))
                    txtfile = discord.File(txt_file_like, filename=attachment.filename)
                    # Check word count
                    word_count = len(content.decode('utf-8').split())
                    # Check if word count is more than 300
                    if word_count > 300:
                        await file_log_channel.send(f"**{authorName}** `{authorID}`\n**{guildName}** `{guildID}`\n`{attachment.filename}` [source]({msg_link})\n```\nToo many characters\n```", file=txtfile)
                    else:
                        # Send the content normally
                        await file_log_channel.send(f"**{authorName}** `{authorID}`\n**{guildName}** `{guildID}`\n`{attachment.filename}` [source]({msg_link})\n```\n{content.decode('utf-8')}\n```", file=txtfile)

                # Images
                image_extensions = ["jpg", "jpeg", "png", "gif", "bmp", "tiff", "tif", "webp", "svg"]
                image_file_like = BytesIO(content)
                imgfile = discord.File(image_file_like, filename='your_image_filename.png')
                if any(attachment.filename.lower().endswith(ext) for ext in image_extensions):
                    await file_log_channel.send(f"**{authorName}** `{authorID}`\n**{guildName}** `{guildID}`\n`{attachment.filename}` [source]({msg_link})", file=imgfile)
                    

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
async def hello(ctx):
    commands_issued(ctx.user.id)
    await ctx.response.send_message("Hello!")


# Iris Choice
@client.tree.command(name = "choose", description = "Lets Iris choose for you.")
@app_commands.describe(choice1 = "Enter first choice.")
@app_commands.describe(choice2 = "Enter second choice.")
async def choose(ctx: discord.Interaction, choice1: str, choice2: str):
    commands_issued(ctx.user.id)
    choice1 = choice1
    choice2 = choice2
    choices = [choice1, choice2]
    IRISchoose = random.choice(choices)
    await ctx.response.send_message(f"**[** {choice1} **|** {choice2} **]** \n{IRISchoose}")


# Ping Check
@client.tree.command(name = "ping", description = "Checks Iris' latency.")
async def ping(ctx):
    commands_issued(ctx.user.id)
    await ctx.response.send_message(f"{round(client.latency * 1000)}ms")


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
async def join(ctx: discord.Interaction):
    commands_issued(ctx.user.id)
    channel = ctx.user.voice.channel
    await channel.connect()
    await ctx.response.send_message("Connected")


# Leave Voice
@client.tree.command(name = "leave", description = "Leaves VC.")
async def leave(ctx: discord.Interaction):
    commands_issued(ctx.user.id)
    await ctx.guild.voice_client.disconnect()
    await ctx.response.send_message("Disconnected")


# [Console] Say Command
@client.tree.command(name = "say", description = "Console Command", guild=discord.Object(id=952892062552981526))
@app_commands.describe(say_text = "Enter message.")
@app_commands.describe(say_channel = "Enter channel ID.")
async def say(ctx: discord.Interaction, say_channel: str, say_text: str):
    commands_issued(ctx.user.id)
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
@client.tree.command(name="sync", description="Syncs the command tree", guild=discord.Object(id=952892062552981526))
async def sync(ctx: discord.Interaction):
    if ctx.user.id in ownerID:
        commands_issued(ctx.user.id)
        await client.tree.sync()
        await ctx.response.send_message(f"Command tree synced.<:OuroKronii_cheers:940254772395655218>")
    else:
        await ctx.response.send_message("Only papa can use this command!")


# [Console] Developer Info
## Guild List
@client.tree.command(name = "guilds", description = "Console Command", guild=discord.Object(id=952892062552981526))
async def devinfo(ctx: discord.Interaction):
    if ctx.user.id in ownerID:
        commands_issued(ctx.user.id)
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

## Members List
@client.tree.command(name = "members", description = "Console Command", guild=discord.Object(id=952892062552981526))
@app_commands.describe(guild = "Enter guild ID.")
async def devinfo(ctx: discord.Interaction, guild: str):
    guild_id = int(guild)
    server = client.get_guild(guild_id)
    if ctx.user.id in ownerID:
        commands_issued(ctx.user.id)
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

## Channels List
@client.tree.command(name = "channels", description = "Console Command", guild=discord.Object(id=952892062552981526))
@app_commands.describe(guild = "Enter guild ID.")
async def devinfo(ctx: discord.Interaction, guild: str):
    guild_id = int(guild)
    server = client.get_guild(guild_id)
    if ctx.user.id in ownerID:
        commands_issued(ctx.user.id)
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
    commands_issued(ctx.user.id)
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
async def feedback(ctx: discord.Interaction, feedback: str):
    commands_issued(ctx.user.id)
    embed = discord.Embed(title=f"Feedback Received",description=(f"{feedback}"),colour=discord.Colour.dark_red())
    embed.add_field(name=f"{ctx.guild}", value=f"{ctx.user.name} | {ctx.user.mention}", inline=False)
    channel = client.get_channel(feedback_channel)
    await channel.send(embed=embed)
    await ctx.response.send_message("Your feedback has been received!")

# Report Command
@client.tree.command(name = "report", description = "Report a user")
@app_commands.describe(user_id = "Enter the user ID to be reported.")
@app_commands.describe(report_reason = "Enter your reason of reporting.")
async def report(ctx: discord.Interaction, user_id: str, report_reason: str):
    commands_issued(ctx.user.id)
    embed = discord.Embed(title=f"User Report Received",description=(f"{user_id}\n{report_reason}"),colour=discord.Colour.dark_red())
    embed.add_field(name=f"{ctx.guild}", value=f"{ctx.user.name} | {ctx.user.mention}", inline=False)
    channel = client.get_channel(report_channel)
    await channel.send(embed=embed)
    await ctx.response.send_message("User reported!")


# Info Command
@client.tree.command(name = "info", description = "More information about Iris")
async def info(ctx: discord.Interaction):
    commands_issued(ctx.user.id)
    embed = discord.Embed(title=f"Project IRIS Info",colour=discord.Colour.dark_red())
    embed.add_field(name=f"**<=> Our Team <=>**", value=f"The people that made this Project IRIS possible", inline=False)
    embed.add_field(name=f"Near `kuroyukinear`", value=f"Owner | Developer", inline=True)
    embed.add_field(name=f"Skully `skull1fy`", value=f"Public Relations", inline=True)
    embed.add_field(name=f"**<=> Links <=>**", value=f"Links related to Project IRIS", inline=False)
    embed.add_field(name=f"Socials", value=f"[Twitter](https://twitter.com/KuroyukiNear)\n[Instagram](https://instagram.com/kuroyuki.near)", inline=True)
    embed.add_field(name=f"Invites", value=f"[Bot Invite](https://discord.com/oauth2/authorize?client_id=902720782503907358&permissions=1644971949559&scope=bot)\n[Server Invite](https://discord.gg/9RUy6suKsy)", inline=True)
    await ctx.response.send_message(embed=embed)


# Display Profile
@client.tree.command(name = "profile", description = "View a user's profile")
async def profile(ctx: discord.Interaction, member: discord.Member = None):
    commands_issued(ctx.user.id)
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
                # Get bio and user number
                bio = user["bio"]
                user_number = user["user_number"]
                # Get badges
                user_badges = user.get("badges", [])
                badges = ', '.join(map(str, user_badges))

        # Embed Profile
        info = discord.Embed(title=f"{username}'s Profile",
                            description=f"User #{user_number}",
                            colour=discord.Colour.dark_red())
        info.add_field(name="Badges", value=f"{badges}", inline=False)
        info.add_field(name="RixCoins", value=f"{rix}", inline=False)
        info.add_field(name="Bio", value=f"{bio}", inline=False)
        await ctx.response.send_message(embed=info)

    # Register if user does not exist
    else:
        with open("profiles.json") as userjson:
            userlist = json.load(userjson)
            count = len(userlist.get("users", [])) # Does not need to add 1 to count as Iris will be User #0
        register_user(
            user_id=userid_to_check,
            wallet=50,
            bank=0,
            bio="Use `/bio` to edit your bio",
            badges=["`no badges`"],
            user_number=count,
            total_earned=0,
            total_spent=0,
            total_transfered=0,
            total_received=0,
            peak_wealth=0,
            commands_issued=0,
            inventory={}
        )
        await ctx.response.send_message("User has just been registered. Please use `/profile` again.")


# Edit Bio
@client.tree.command(name = "bio", description = "Edit your bio")
async def bio(ctx: discord.Interaction, newbio: str):
    commands_issued(ctx.user.id)
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
            "Your bio has been changed.\nNote: if `/profile` is not working after you changed your bio, you have probably exceeded the character limit."
        )


# Balance
@client.tree.command(name = "balance", description = "View a user's balance")
async def profile(ctx: discord.Interaction, member: discord.Member = None):
    commands_issued(ctx.user.id)
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

    # Reply if user does not exist
    else:
        await ctx.response.send_message("User has not been registered. Please use `/profile` to register.")


# Transfer RixCoins
@client.tree.command(name = "transfer", description = "Transfer RixCoins to another user")
async def profile(ctx: discord.Interaction, member: discord.Member, amount: int):
    commands_issued(ctx.user.id)
    # Opening JSON file
    userjson = open("profiles.json")
    userlist = json.load(userjson)

    # Users
    transferer = ctx.user
    receiver = member
    
    # Check if the users are the same
    if transferer.id == receiver.id:
        await ctx.response.send_message(f"***ERROR*** You can't transfer to yourself.", ephemeral=True)
        return

    # Check if transferer ID exists
    userid_to_check = transferer.id
    if user_exists(userid_to_check):
        # Get transferer
        userid_to_find = transferer.id
        users_list = userlist.get("users", [])
        for user in users_list:
            if user['ID'] == userid_to_find:
                # Get data
                transferer_rix = user["wallet"]
                total_transfered = user["total_transfered"]
    else:
        await ctx.response.send_message(f"***ERROR*** User **{transferer.name}** not found.", ephemeral=True)

    # Check if receiver ID exists
    userid_to_check = receiver.id
    if user_exists(userid_to_check):
        # Get receiver
        userid_to_find = receiver.id
        users_list = userlist.get("users", [])
        for user in users_list:
            if user['ID'] == userid_to_find:
                # Get data
                receiver_rix = user["wallet"]
                total_received = user["total_received"]
    else:
        await ctx.response.send_message(f"***ERROR*** User **{member.name}** not found.", ephemeral=True)

    # Not enough balance
    if transferer_rix < amount:
        await ctx.response.send_message("You do not have enough balance.")
        return

    # Enough balance
    elif transferer_rix >= amount:
        #New data
        new_transferer_rix = transferer_rix - amount
        new_receiver_rix = receiver_rix + amount
        new_total_transfered = total_transfered + amount
        new_total_received = total_received + amount

        # Get transferer
        userid_to_find = transferer.id
        users_list = userlist.get("users", [])
        for user in users_list:
            if user['ID'] == userid_to_find:
                # Rewrite data
                user["wallet"] = new_transferer_rix
                user["total_transfered"] = new_total_transfered
 
        # Get receiver
        userid_to_find = receiver.id
        users_list = userlist.get("users", [])
        for user in users_list:
            if user['ID'] == userid_to_find:
                # Rewrite data
                user["wallet"] = new_receiver_rix
                user["total_received"] = new_total_received

        # Save the modified data back to the JSON file
        with open("profiles.json", "w") as userjson:
            json.dump(userlist, userjson, indent=4)
        update_peak_wealth(receiver.id)

        await ctx.response.send_message(f"Transfered `{amount}`RC to {member.name}. Your remaining balance is `{new_transferer_rix}`RC")


# Deposit RixCoins
@client.tree.command(name = "deposit", description = "Deposit RixCoins to bank")
async def profile(ctx: discord.Interaction, amount: int):
    commands_issued(ctx.user.id)
    # Opening JSON file
    userjson = open("profiles.json")
    userlist = json.load(userjson)

    # Check if user ID exists
    userid_to_check = ctx.user.id
    if user_exists(userid_to_check):
        # Get user
        userid_to_find = ctx.user.id
        users_list = userlist.get("users", [])
        for user in users_list:
            if user['ID'] == userid_to_find:
                # Get data
                wallet = user["wallet"]
                bank = user["bank"]

                # Not enough balance
                if wallet < amount:
                    await ctx.response.send_message("You do not have enough balance.")
                    return

                # Enough balance
                elif wallet >= amount:
                    new_wallet = wallet - amount
                    new_bank = bank + amount  
                    user["wallet"] = new_wallet
                    user["bank"] = new_bank
                    # Save the modified data back to the JSON file
                    with open("profiles.json", "w") as userjson:
                        json.dump(userlist, userjson, indent=4)
                    await ctx.response.send_message(f"Deposited `{amount}`RC to bank. Your remaining wallet balance is `{new_wallet}`RC")
    else:
        await ctx.response.send_message(f"***ERROR*** User **{ctx.user.name}** not found.", ephemeral=True)


# Withdraw RixCoins
@client.tree.command(name = "withdraw", description = "Withdraw RixCoins from bank")
async def profile(ctx: discord.Interaction, amount: int):
    commands_issued(ctx.user.id)
    # Opening JSON file
    userjson = open("profiles.json")
    userlist = json.load(userjson)

    # Check if user ID exists
    userid_to_check = ctx.user.id
    if user_exists(userid_to_check):
        # Get user
        userid_to_find = ctx.user.id
        users_list = userlist.get("users", [])
        for user in users_list:
            if user['ID'] == userid_to_find:
                # Get data
                wallet = user["wallet"]
                bank = user["bank"]

                # Not enough balance
                if bank < amount:
                    await ctx.response.send_message("You do not have enough balance.")
                    return

                # Enough balance
                elif bank >= amount:
                    new_wallet = wallet + amount  
                    new_bank = bank - amount
                    user["wallet"] = new_wallet
                    user["bank"] = new_bank
                    # Save the modified data back to the JSON file
                    with open("profiles.json", "w") as userjson:
                        json.dump(userlist, userjson, indent=4)
                    await ctx.response.send_message(f"Withdrawn `{amount}`RC from bank. Your remaining bank balance is `{new_bank}`RC")
    else:
        await ctx.response.send_message(f"***ERROR*** User **{ctx.user.name}** not found.", ephemeral=True)


# Work
@client.tree.command(name = "work", description = "Work to earn RixCoins")
async def work(ctx: discord.Interaction):
    # Cooldown settings
    cooldown_seconds = 60  # 1 minute
    user_id = ctx.user.id
    guild_id = ctx.guild.id
    # Check if the user is on cooldown
    if (guild_id, user_id) in cooldowns and time.time() - cooldowns[(guild_id, user_id)] < cooldown_seconds:
        remaining_time = int(cooldown_seconds - (time.time() - cooldowns[(guild_id, user_id)]))
        await ctx.response.send_message(f"You are on cooldown. Please wait {remaining_time} seconds.")
        return
    else:
        commands_issued(ctx.user.id)
        cooldowns[(guild_id, user_id)] = time.time()
        # Define the probability distribution
        outcomes = [
            {"range": range(600, 801), "probability": 0.2},  # 20% chance of 600-800 coins
            {"range": range(300, 501), "probability": 0.3},  # 30% chance of 300-500 coins
            {"range": range(100, 201), "probability": 0.5},  # 50% chance of 100-200 coins
        ]

        # Opening JSON file
        userjson = open("profiles.json")
        userlist = json.load(userjson)

        # Check if user ID exists
        userid_to_check = ctx.user.id
        if user_exists(userid_to_check):
            # Get user
            userid_to_find = ctx.user.id
            users_list = userlist.get("users", [])
            for user in users_list:
                if user['ID'] == userid_to_find:
                    # Select an outcome based on the probability distribution
                    result = get_random_outcome(outcomes)
                    # Get data
                    wallet = user["wallet"]
                    user["wallet"] = wallet + result
                    new_total_earned = user["total_earned"] + result
                    user["total_earned"] = new_total_earned
                    # Save the modified data back to the JSON file
                    with open("profiles.json", "w") as userjson:
                        json.dump(userlist, userjson, indent=4)
                    update_peak_wealth(userid_to_check)
                    await ctx.response.send_message(f"You worked hard and earned `{result}`RC")
        else:
            await ctx.response.send_message(f"***ERROR*** User **{ctx.user.name}** not found.", ephemeral=True)


# Inventory Command
@client.tree.command(name="inventory", description="View your inventory")
async def inventory(ctx: discord.Interaction):
    commands_issued(ctx.user.id)
    user_id = ctx.user.id

    with open("profiles.json", "r") as userjson:
        data = json.load(userjson)

    user_data = next((user for user in data["users"] if user["ID"] == user_id), None)

    if user_data:
        inventory = user_data["inventory"]
        if not inventory:
            await ctx.send("Your inventory is empty.")
            return

        embed = discord.Embed(title=f"{ctx.user.name}'s Inventory", color=discord.Color.dark_red())
        items_per_page = 5
        page = 1

        # Load item details from items.json
        with open("items.json", "r") as itemsjson:
            items_data = json.load(itemsjson)

        # Sort inventory items by item ID
        sorted_inventory = {str(item_id): count for item_id, count in sorted(inventory.items(), key=lambda x: int(x[0]))}

        for item_id, count in list(sorted_inventory.items())[items_per_page * (page - 1): items_per_page * page]:

            # Get item details based on item ID
            item_details = items_data["items"][int(item_id) - 1]
            item_name = item_details["name"]
            item_icon = item_details["icon"]

            item_count_rightjustified = str(count).rjust(10)
            embed.add_field(name=f"[{item_id}] {item_icon}{item_name}", value=f"`{item_count_rightjustified}`", inline=False)

        total_items = sum(inventory.values())
        embed.set_footer(text=f"Page {page} | Total Items: {total_items}")

        message = await ctx.channel.send(embed=embed)
        await ctx.response.send_message(f"`/info` for more info about Iris", ephemeral=True)

        # Add reactions for pagination
        if len(inventory) > items_per_page:
            await message.add_reaction("⬅️")
            await message.add_reaction("➡️")

            def check(reaction, user):
                return user == ctx.user and reaction.message.id == message.id and str(reaction.emoji) in ["⬅️", "➡️"]

            while True:
                try:
                    reaction, user = await client.wait_for("reaction_add", timeout=60, check=check)
                    await message.remove_reaction(reaction, user)

                    if str(reaction.emoji) == "⬅️" and page > 1:
                        page -= 1
                    elif str(reaction.emoji) == "➡️" and items_per_page * page < len(inventory):
                        page += 1

                    # Update the embed with the new page and total items
                    embed.clear_fields()
                    embed.add_field(name="", value="", inline=False)

                    for item_id, count in list(sorted_inventory.items())[items_per_page * (page - 1): items_per_page * page]:
                        item_details = items_data["items"][int(item_id) - 1]
                        item_name = item_details["name"]
                        item_icon = item_details["icon"]
                        item_count_rightjustified = str(count).rjust(10)
                        embed.add_field(name=f"[{item_id}] {item_icon}{item_name}", value=f"`{item_count_rightjustified}`", inline=False)

                    embed.set_footer(text=f"Page {page} | Total Items: {total_items}")
                    await message.edit(embed=embed)

                except asyncio.TimeoutError:
                    break
    else:
        await ctx.response.send_message(f"***ERROR*** User **{ctx.user.name}** not found.", ephemeral=True)


# Item Command
@client.tree.command(name="item", description="View an item's details")
@app_commands.describe(item_id = "Enter item ID.")
async def item(ctx: discord.Interaction, item_id: int):
    commands_issued(ctx.user.id)
    # Load items data from the JSON file
    with open("items.json", "r") as file:
        items_data = json.load(file)

    # Find the item with the specified ID
    found_item = next((item for item in items_data["items"] if item["ID"] == item_id), None)

    if found_item:
        embed = discord.Embed(
            title=f"{found_item['name']}",
            color=discord.Color.dark_red()
        )

        # Sell Price
        if found_item['sell_price'] == 0:
            sell_price = "Not Sellable"
        else:
            sell_price = f"`{str(found_item['sell_price']).rjust(10)}`"
        # Buy Price
        if found_item['buy_price'] == 0:
            buy_price = "Not Buyable"
        else:
            buy_price = f"`{str(found_item['buy_price']).rjust(10)}`"

        item_id_rightjustified = str(found_item['ID']).rjust(5)
        embed.add_field(name="Description", value=found_item['desc'], inline=False)
        embed.add_field(name="ID", value=f"`{item_id_rightjustified}`", inline=True)
        embed.add_field(name="Rarity", value=found_item['rarity'], inline=True)
        embed.add_field(name="Category", value=found_item['category'], inline=True)
        embed.add_field(name="Buy Price", value=buy_price, inline=True)
        embed.add_field(name="Sell Price", value=sell_price, inline=True)

        await ctx.response.send_message(embed=embed)
    else:
        await ctx.response.send_message("**ERROR** Item not found.", ephemeral=True)


# Itemlist Command
@client.tree.command(name="itemlist", description="View a list of items")
async def itemlist(ctx: discord.Interaction):
    commands_issued(ctx.user.id)

    with open("items.json", "r") as items_json:
        items_data = json.load(items_json)["items"]

    items_per_page = 5
    total_items = len(items_data)
    total_pages = (total_items + items_per_page - 1) // items_per_page

    # Initial page
    page = 1
    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page

    items_on_page = items_data[start_index:end_index]

    if not items_on_page:
        await ctx.send("No items found.")
        return

    embed = discord.Embed(title=f"Item List", color=discord.Color.dark_red())

    for item in items_on_page:
        item_id_rightjustified = str(item['ID']).rjust(5)
        embed.add_field(name=f"{item['icon']}{item['name']}", value=f"**Item ID** `{item_id_rightjustified}`\n**{item['category']} | {item['rarity']}**", inline=False)

    embed.set_footer(text=f"Page {page}/{total_pages} | {total_items} Items")
    message = await ctx.channel.send(embed=embed)
    await ctx.response.send_message(f"`/info` for more info about Iris", ephemeral=True)

    # Add reactions for pagination
    if total_pages > 1:
        await message.add_reaction("⬅️")
        await message.add_reaction("➡️")

        def check(reaction, user):
            return user == ctx.user and reaction.message.id == message.id and str(reaction.emoji) in ["⬅️", "➡️"]

        while True:
            try:
                reaction, user = await client.wait_for("reaction_add", timeout=60, check=check)
                await message.remove_reaction(reaction, user)

                if str(reaction.emoji) == "⬅️" and page > 1:
                    page -= 1
                elif str(reaction.emoji) == "➡️" and page < total_pages:
                    page += 1

                # Update the embed with the new page
                start_index = (page - 1) * items_per_page
                end_index = start_index + items_per_page
                items_on_page = items_data[start_index:end_index]

                embed.clear_fields()
                embed.add_field(name=f"", value="", inline=False)

                for item in items_on_page:
                    item_id_rightjustified = str(item['ID']).rjust(5)
                    embed.add_field(name=f"{item['icon']}{item['name']}", value=f"**Item ID** `{item_id_rightjustified}`\n**{item['category']} | {item['rarity']}**", inline=False)

                embed.set_footer(text=f"Page {page}/{total_pages} | Total Items: {total_items}")
                await message.edit(embed=embed)

            except asyncio.TimeoutError:
                break


# Execute Console
@client.tree.command(name="console", guild=discord.Object(id=952892062552981526))
async def execute_console(ctx: discord.Interaction, code: str):
    commands_issued(ctx.user.id)
    if ctx.user.id not in ownerID:
        return await ctx.response.send_message("Only papa can use that command.")

    # Execute the provided code
    try:
        result = eval(code)
        await ctx.response.send_message(f"Result: {result}")
    except Exception as e:
        # Handle exceptions and send the traceback
        traceback_str = "\n".join(traceback.format_exception(type(e), e, e.__traceback__))
        await ctx.response.send_message(f"An error occurred:\n```{traceback_str}```")


# Status Command
@client.tree.command(name="stats", description="View a user's status")
async def stats(ctx: discord.Interaction, member: discord.Member = None):
    commands_issued(ctx.user.id)
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
                # Get data
                usernumber = str(user["user_number"]).rjust(10)
                total_earned = str(user["total_earned"]).rjust(10)
                total_spent = str(user["total_spent"]).rjust(10)
                total_transfered = str(user["total_transfered"]).rjust(10)
                total_received = str(user["total_received"]).rjust(10)
                peak_wealth = str(user["peak_wealth"]).rjust(10)
                user_commands_issued = str(user["commands_issued"]).rjust(10)

        # Embed Profile
        embed = discord.Embed(title=f"{username}'s Status", description=f"User #{usernumber}", colour=discord.Colour.dark_red())
        embed.add_field(name="Total Earned", value=f"`{total_earned}`", inline=True)
        embed.add_field(name="Total Spent", value=f"`{total_spent}`", inline=True)
        embed.add_field(name="Total Transfered", value=f"`{total_transfered}`", inline=True)
        embed.add_field(name="Total Received", value=f"`{total_received}`", inline=True)
        embed.add_field(name="Peak Wealth", value=f"`{peak_wealth}`", inline=True)
        embed.add_field(name="Commands Issued", value=f"`{user_commands_issued}`", inline=True)
        await ctx.response.send_message(embed=embed)

    # Reply if user does not exist
    else:
        await ctx.response.send_message(f"***ERROR*** User **{user}** not found.", ephemeral=True)


# Iris Remote Chat
connected_channels = {}

# IRC Connect Command
@client.tree.command(name='connect', guild=discord.Object(id=952892062552981526))
async def connect(ctx, channel_id: str):
    if ctx.user.id not in ownerID:
        return await ctx.response.send_message("Only papa can use that command.")
    
    destination_channel = client.get_channel(int(channel_id))
    
    if destination_channel:
        connected_channels[ctx.channel.id] = destination_channel.id
        connected_channels[destination_channel.id] = ctx.channel.id
        await ctx.response.send_message(f"**[IRC]** Iris has connected to **#{destination_channel.name}**.")
        forward_messages_tasks[(ctx.channel.id, destination_channel.id)] = client.loop.create_task(forward_messages(ctx.channel.id, destination_channel.id))
    else:
        await ctx.response.send_message("Invalid channel ID.")

# Forward Messages
forward_messages_tasks = {}

async def forward_messages(source_channel_id, destination_channel_id):
    source_channel = client.get_channel(source_channel_id)
    destination_channel = client.get_channel(destination_channel_id)

    try:
        while True:
            # Wait for a message from the source channel
            source_message_task = asyncio.ensure_future(client.wait_for('message', check=lambda m: m.channel == source_channel and m.author != client.user))

            # Wait for a message from the destination channel
            destination_message_task = asyncio.ensure_future(client.wait_for('message', check=lambda m: m.channel == destination_channel and m.author != client.user))

            done, _ = await asyncio.wait([source_message_task, destination_message_task], return_when=asyncio.FIRST_COMPLETED)

            # Get the completed task
            completed_task = done.pop().result()

            # Send the message to the other channel
            if completed_task.channel == source_channel:
                await destination_channel.send(f"**{completed_task.author}** {completed_task.content}")
            else:
                    await source_channel.send(f"**{completed_task.author}** {completed_task.content}")

    except asyncio.CancelledError:
        # Handle cancellation
        pass
    finally:
        forward_messages_tasks.pop((source_channel_id, destination_channel_id), None)

# IRC Disconnect Command
@client.tree.command(name='disconnect', guild=discord.Object(id=952892062552981526))
async def disconnect(ctx):
    if ctx.channel.id in connected_channels:
        paired_channel_id = connected_channels[ctx.channel.id]
        del connected_channels[paired_channel_id]
        del connected_channels[ctx.channel.id]

        source_channel = client.get_channel(ctx.channel.id)
        destination_channel = client.get_channel(paired_channel_id)

        # Check if channels are still connected
        if source_channel and destination_channel:
            # Cancel message forwarding task
            forward_task = forward_messages_tasks.get((ctx.channel.id, paired_channel_id))
            if forward_task:
                forward_task.cancel()

            await source_channel.send(f"**[IRC]** Connection has been terminated **{ctx.user}**.")
            await destination_channel.send(f"**[IRC]** Connection has been terminated by **{ctx.user}**.")
            await ctx.response.send_message(f"**[IRC]** All connections have been successfully terminated.")
        else:
            await ctx.response.send_message("**[IRC]** Iris has successfully terminated the connection; channels are no longer linked.")
    else:
        await ctx.response.send_message("**[IRC]** Not currently linked to any channels.")


# Book Item
# New Book Command
@client.tree.command(name="newbook", description="Write a new book")
async def newbook(ctx, book_name: str, book_content:str):
    book_name_count = len(book_name)
    book_content_count = len(book_content)
    if book_name_count > 16:
        await ctx.response.send_message(f"The title of the book can't be more than 16 characters.")
    if book_content_count > 800:
        await ctx.response.send_message(f"The content of the book can't be more than 800 characters.")
    else:
        commands_issued(ctx.user.id)
        # Opening JSON file
        bookjson = open("book.json")
        booklist = json.load(bookjson)
        # Load the existing JSON data
        with open("book.json") as bookjson:
            data = json.load(bookjson)
        count = len(booklist.get("books", []))
        # Create a new user object
        new_book = {
            "bookID": count,
            "bookName": book_name,
            "bookAuthor": ctx.user.id,
            "bookContent": book_content
        }
        # Add the new user to the "users" array
        data["books"].append(new_book)
        # Save the updated data back to the JSON file
        with open("book.json", "w") as bookjson:
            json.dump(data, bookjson, indent=4)
        await ctx.response.send_message(f"`{book_name}` has been added to the library.\n\n*Note: Our staff reserves the rights to ban anyone from using Iris for spam writing books.*")


# Book List Command
@client.tree.command(name="booklist", description="View a list of books")
async def booklist(ctx: discord.Interaction):
    commands_issued(ctx.user.id)

    with open("book.json", "r") as booksjson:
        books_data = json.load(booksjson)["books"]

    books_per_page = 5
    total_books = len(books_data)
    total_pages = (total_books + books_per_page - 1) // books_per_page

    # Initial page
    page = 1
    start_index = (page - 1) * books_per_page
    end_index = start_index + books_per_page

    books_on_page = books_data[start_index:end_index]

    if not books_on_page:
        await ctx.send("No books found.")
        return

    embed = discord.Embed(title=f"Iris' Library", color=discord.Color.dark_red())

    for book in books_on_page:
                    book_name = book["bookName"]
                    book_id_rightjustified = str(book["bookID"]).rjust(5)
                    author_id = book["bookAuthor"]
                    user = client.get_user(author_id)
                    embed.add_field(name=f"{book_name}", value=f"**Book ID** `{book_id_rightjustified}`\n**{user.display_name} | **`{author_id}`", inline=False)

    embed.set_footer(text=f"Page {page}/{total_pages} | {total_books} Books")
    message = await ctx.channel.send(embed=embed)
    await ctx.response.send_message(f"`/info` for more info about Iris", ephemeral=True)

    # Add reactions for pagination
    if total_pages > 1:
        await message.add_reaction("⬅️")
        await message.add_reaction("➡️")

        def check(reaction, user):
            return user == ctx.user and reaction.message.id == message.id and str(reaction.emoji) in ["⬅️", "➡️"]

        while True:
            try:
                reaction, user = await client.wait_for("reaction_add", timeout=60, check=check)
                await message.remove_reaction(reaction, user)

                if str(reaction.emoji) == "⬅️" and page > 1:
                    page -= 1
                elif str(reaction.emoji) == "➡️" and page < total_pages:
                    page += 1

                # Update the embed with the new page
                start_index = (page - 1) * books_per_page
                end_index = start_index + books_per_page
                books_on_page = books_data[start_index:end_index]

                embed.clear_fields()
                embed.add_field(name=f"", value="", inline=False)

                for book in books_on_page:
                    book_name = book["bookName"]
                    book_id_rightjustified = str(book["bookID"]).rjust(5)
                    author_id = book["bookAuthor"]
                    user = client.get_user(author_id)
                    embed.add_field(name=f"{book_name}", value=f"**Book ID** `{book_id_rightjustified}`\n**{user.display_name} | **`{author_id}`", inline=False)

                embed.set_footer(text=f"Page {page}/{total_pages} | Total Books: {total_books}")
                await message.edit(embed=embed)

            except asyncio.TimeoutError:
                break


# View Book Command
@client.tree.command(name = "viewbook", description = "View a book")
async def viewbook(ctx: discord.Interaction, book_id: str):
    commands_issued(ctx.user.id)
    # Opening JSON file
    bookjson = open("book.json")
    booklist = json.load(bookjson)
    # Find book
    book_id = int(book_id)
    books_list = booklist.get("books", [])
    for book in books_list:
        if book["bookID"] == book_id:
            # Get book data
            book_name = book["bookName"]
            book_author = book["bookAuthor"]
            user = client.get_user(book_author)
            book_content = book["bookContent"]
            total_books = len(books_list)
            embed = discord.Embed(title=f"{book_name}", color=discord.Color.dark_red())
            embed.add_field(name=f"Author", value=f"{user.display_name} `{book_author}`", inline=False)
            embed.add_field(name=f"Content", value=f"{book_content}", inline=False)
            embed.set_footer(text=f"Book {book_id} out of {total_books} books")
            await ctx.response.send_message(embed=embed)
            break
    else:
        await ctx.response.send_message("Book not found")


# Random Book Command
@client.tree.command(name = "randombook", description = "View a random book", guild=discord.Object(id=952892062552981526))
async def randombook(ctx: discord.Interaction):
    commands_issued(ctx.user.id)
    # Opening JSON file
    bookjson = open("book.json")
    booklist = json.load(bookjson)
    # Extract book IDs into a list
    book_ids = [book["bookID"] for book in booklist["books"]]
    book_id = random.choice(book_ids)
    # Find book
    book_id = int(book_id)
    books_list = booklist.get("books", [])
    for book in books_list:
        if book["bookID"] == book_id:
            # Get book data
            book_name = book["bookName"]
            book_author = book["bookAuthor"]
            user = client.get_user(book_author)
            book_content = book["bookContent"]
            total_books = len(books_list)
            embed = discord.Embed(title=f"{book_name}", color=discord.Color.dark_red())
            embed.add_field(name=f"Author", value=f"{user.display_name} `{book_author}`", inline=False)
            embed.add_field(name=f"Content", value=f"{book_content}", inline=False)
            embed.set_footer(text=f"Book {book_id} out of {total_books} books")
            await ctx.response.send_message(embed=embed)
            break
    else:
        await ctx.response.send_message("**ERROR** Please run the command again.", ephemeral=True)


# Backup Command
@client.tree.command(name="backup", description="Create a backup of a file")
async def backup(ctx: discord.Interaction, filename: str):
    if ctx.user.id in ownerID:
        commands_issued(ctx.user.id)
        try:
            # Specify the original and backup file paths
            original_filepath = filename
            backup_folder = "backups"
            backup_filename = f"{os.path.splitext(filename)[0]}-{datetime.now().strftime('%Y%m%d%H%M%S')}{os.path.splitext(filename)[1]}"
            backup_filepath = os.path.join(backup_folder, backup_filename)

            # Create the "backups" folder if it doesn't exist
            if not os.path.exists(backup_folder):
                os.makedirs(backup_folder)

            # Copy the file to the "backups" folder with the new filename
            shutil.copy(original_filepath, backup_filepath)

            await ctx.response.send_message(f"Backup created successfully: `{backup_filepath}`")
        except FileNotFoundError:
            await ctx.response.send_message(f"File not found: `{filename}`")
        except Exception as e:
            await ctx.response.send_message(f"An error occurred: {e}")
    else:
        await ctx.response.send_message("Only papa can use this command!")


# Files Command
@client.tree.command(name="files", description="View Project IRIS files")
async def files(ctx: discord.Interaction):
    if ctx.user.id in ownerID:
        commands_issued(ctx.user.id)
        try:
            script_directory = os.path.dirname(os.path.abspath(__file__))
            items = os.listdir(script_directory)

            embed = discord.Embed(title=f"{script_directory}", color=discord.Color.dark_red())

            for item in items:
                item_path = os.path.join(script_directory, item)

                if os.path.isfile(item_path):
                    # For files, display their size
                    file_size = os.path.getsize(item_path)
                    embed.add_field(name=f"{item}", value=f"`{file_size} bytes`", inline=True)
                elif os.path.isdir(item_path):
                    # For folders, calculate total size of all files within the folder
                    folder_size = sum(os.path.getsize(os.path.join(item_path, f)) for f in os.listdir(item_path) if os.path.isfile(os.path.join(item_path, f)))
                    file_count = sum(1 for _ in os.listdir(item_path) if os.path.isfile(os.path.join(item_path, _)))
                    embed.add_field(name=f"{item} ({file_count} files)", value=f"`{folder_size} bytes`", inline=True)

            await ctx.response.send_message(embed=embed)
        except Exception as e:
            await ctx.response.send_message(f"An error occurred: {e}")
    else:
        await ctx.response.send_message("Only papa can use this command!")


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
