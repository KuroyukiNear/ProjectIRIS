import discord
from discord.ext import commands, tasks
from discord import app_commands
from itertools import cycle
import random

intents = discord.Intents.all()
client = commands.AutoShardedBot(command_prefix=".", help_command=None, intents=intents)

# Connect
@client.event
async def on_ready():
    for server in client.guilds:
        await client.tree.sync(guild=discord.Object(id=server.id))
    change_status.start()
    print('<=>--------------------------------<=>')
    print('     ', f"Logged in as {client.user}")
    print('     ', f"User ID: {client.user.id}")
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


# Channel ID
channelID = 1122103608419291236
user_join = int(channelID)
deleted_message = int(channelID)
edited_message = int(channelID)
censored_message = int(channelID)


# Iris Responses
papa = ["hi papa", "hellooo papa", "hii", "Minecraft?"]
user = ["who da fak are you", "你乜水"]
luby = ["會長早晨！", "hi Luby姐姐"]
summy = ["小朋友唔好再沉迷BL", "考試喇同學"]
kelvin_2050 = ["hi Kelvin", "hello~"]



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

@client.event
async def on_message_edit(message_before, message_after):
  if message_before.author == message_before.author.bot:
    return
  else:
    msg = message_after
    user = msg.author
    channel = msg.channel
    server = msg.guild
    link = f"https://discordapp.com/channels/{server.id}/{channel.id}/{msg.id}"
    embed = discord.Embed(title=f"{user} edited a message in {msg.guild}",description=(f"{user.mention} **|** {channel.mention}"),colour=discord.Colour.purple())
    embed.add_field(name=f"Original Message", value=f"{message_before.content}", inline=False)
    embed.add_field(name=f"Edited Message", value=f"{message_after.content}", inline=False)
    embed.add_field(name=f"ID", value=f"```\n Channel = {channel.id} \n User = {user.id} \n Message = {msg.id} \n```", inline=False)
    embed.add_field(name=f"Message Link", value=f"[here]({link})", inline=False)
    embed.timestamp = msg.created_at
    channel = client.get_channel(edited_message)
    await channel.send(embed=embed)

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


@client.tree.command(name = "hello", description = "Says hello to Iris.")
async def hello(interaction):
    await interaction.response.send_message("Hello!")

# [Console] Say Command
@client.tree.command(name = "say", description = "Console Command", guild=discord.Object(id=952892062552981526))
@app_commands.describe(say_text = "Enter message.")
@app_commands.describe(say_channel = "Enter channel ID.")
async def say(ctx: discord.Interaction, say_channel: str, say_text: str):
    if ctx.user.id == 638342719592202251:
      channel = client.get_channel(int(say_channel))
      message = await channel.send(say_text)
      embed = discord.Embed(title=f"[Console] Say Command",description=(f"Message successfully sent."),colour=discord.Colour.dark_red())
      embed.add_field(name=f"User", value=f"{ctx.user.mention}", inline=False)
      embed.add_field(name=f"Channel", value=f"{channel.mention}", inline=False)
      embed.add_field(name=f"Message", value=f"https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}", inline=False)
      embed.add_field(name=f"Content", value=f"{message.content}", inline=False)
      await ctx.response.send_message(embed=embed)
    else:
       await ctx.response.send_message("You are not allowed to use that command.")

# 傻逼偵測器
@client.tree.command(name = "傻逼偵測器", description = "偵測用戶傻逼指數", guild=discord.Object(id=863253117684678658))
async def sbmeter(interaction):
    if interaction.user.id == 638342719592202251:
       sbPercentage = 0.00
    else:
       randomPercentage= random.random() * 100
       sbPercentage = round(randomPercentage, 2)
    if sbPercentage > 20:
       sbIndicator = ":white_check_mark:"
    else:
       sbIndicator = ":negative_squared_cross_mark:"
    embed = discord.Embed(title=f"傻逼偵測器",colour=discord.Colour.dark_red())
    embed.add_field(name=f"用戶", value=f"{interaction.user.mention}", inline=False)
    embed.add_field(name=f"傻逼指數", value=f"{sbPercentage}%", inline=False)
    embed.add_field(name=f"是否傻逼", value=f"{sbIndicator}", inline=False)
    await interaction.response.send_message(embed=embed)

@client.tree.command(name = "choose", description = "Lets Iris choose for you.")
@app_commands.describe(choice1 = "Enter first choice.")
@app_commands.describe(choice2 = "Enter second choice.")
async def choose(interaction: discord.Interaction, choice1: str, choice2: str):
    choice1 = choice1
    choice2 = choice2
    choices = [choice1, choice2]
    IRISchoose = random.choice(choices)
    await interaction.response.send_message(IRISchoose)

# Ping Check
@client.tree.command(name = "ping", description = "Checks Iris' latency.")
async def ping(interaction):
    await interaction.response.send_message(f"{round(client.latency * 1000)}ms")






# Connect
token = "OTAyNzIwNzgyNTAzOTA3MzU4.GQK1w3.2fLlg2PHIbQYu5SqGZBYGUYQBQX-ZiQ3RcuRAo"
client.run(token)


