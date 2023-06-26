# Discord API
import discord
from discord.ext import commands, tasks
# pip install DiscordUtils[voice]
# pip install DiscordUtils

# Tools
from itertools import cycle
import logging
import os
import random
from pathlib import Path
import time
import datetime

# Keep Alive
from keep_alive import keep_alive

# Data Files
from IRIS import badges
from IRIS import items
from IRIS import itemRarity

gawds = [638342719592202251, 707595898200260728]
intents = discord.Intents.all()
client = commands.AutoShardedBot(command_prefix=".",owner_ids = set(gawds), help_command=None, intents=intents)

dot = ":white_small_square:"

### User Data ###
# OP Users


with open("./data/godmode.dat") as f:
    godmode = f.read().splitlines()
for gcommand in godmode:
    godmode_commands = client.command_prefix + gcommand

# Banned Users
with open("./data/blacklist.dat") as f:
    blacklist = f.read().splitlines()
for userID in blacklist:
    blacklisted = int(userID)
with open("./data/commands.dat") as f:
    commands = f.read().splitlines()
for command in commands:
    commands = client.command_prefix + command

### Imported Variables ###
# Badges
developer_badge = badges.developer_badge
developer_badge_png = badges.developer_badge_png
admin_badge = badges.admin_badge
admin_badge_png = badges.admin_badge_png
mod_badge = badges.mod_badge
mod_badge_png = badges.mod_badge_png
catgirl_badge = badges.catgirl_badge
catgirl_badge_png = badges.catgirl_badge_png
betatester_badge = badges.betatester_badge
betatester_badge_png = badges.betatester_badge_png
bot_tag = badges.bot_tag
# Items
GodModeGuideBook = items.GodModeGuideBook
GodModeGuideBook_img = items.GodModeGuideBook_img
# Item Data
UR_info = itemRarity.UR_info
SSR_info = itemRarity.SSR_info
SR_info = itemRarity.SR_info
R_info = itemRarity.R_info
UC_info = itemRarity.UC_info
C_info = itemRarity.C_info
UR = itemRarity.UR
SSR = itemRarity.SSR
SR = itemRarity.SR
R = itemRarity.R
UC = itemRarity.UC
C = itemRarity.C


@client.event
async def on_message(message):
  if message.channel.id == 975007803271958558:
    if message.author.id == 975003707932557323:
      send = f"{message.content}"
      channel = client.get_channel(980053325015830600)
      await channel.send(send)

    else:
      send = f"**{message.author}** {message.content}"
      channel = client.get_channel(980053325015830600)
      await channel.send(send)
  else:
    await client.process_commands(message)


'''
    if message.content.startswith(commands):
        if message.author.id != blacklisted:
            await client.process_commands(message)
        else:
            await message.reply("***Error*** You are blacklisted and not allowed to use this command.")

    if message.content.startswith(godmode_commands):
        if message.author.id not in gawds:
          await message.reply("***Error*** You are not allowed to use that command.")
        else:
          await client.process_commands(message)
'''


# Events
@client.event
async def on_ready():
    change_status.start()
    print('<=>--------------------------------<=>')
    print('     ', f"Logged in as, {client.user}")
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

    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    with open(f"./data/log/connect.log", "a") as log:
        print(f"Iris connected at <{st}>", file=log)


@client.event
async def on_guild_join(guild):
    server_count = len(client.guilds)
    server_count = int(server_count)
    embed = discord.Embed(title="Iris has joined " + guild.name,
                          description=guild.description,
                          color=discord.Color.dark_red())
    embed.set_thumbnail(url=guild.icon_url)
    embed.add_field(name="Owner", value=guild.owner, inline=True)
    embed.add_field(name="Region", value=guild.region, inline=True)
    embed.add_field(name="Member Count", value=guild.member_count, inline=True)
    embed.add_field(name="Server Creation Date",
                    value=guild.created_at,
                    inline=True)
    embed.add_field(name="Owner Registration Date",
                    value=guild.owner.created_at,
                    inline=True)
    embed.add_field(name="Server Number",
                    value=(f'{server_count}'),
                    inline=True)
    embed.add_field(name="Owner ID",
                    value=(f'`{guild.owner.id}`'),
                    inline=True)
    embed.add_field(name="Server ID", value=(f'`{guild.id}`'), inline=True)
    channel = client.get_channel(940613140020883486)
    await channel.send(embed=embed)
    await guild.system_channel.send(
        "Hellooo!!!! I'm Iris~ Thank you for inviting me. type `.help` to see what I can do! <:Menhera_admire:943480259272134736>"
    )


@client.event
async def on_member_join(user):
    server = user.guild
    if user.bot:
        type = "Bot"
    else:
        type = "User"
    embed = discord.Embed(title=f'{user} joined {server}',
                          description=(f"{user.mention} **|** `{user.id}`"),
                          colour=discord.Colour.dark_red())
    embed.set_thumbnail(url=user.avatar_url)
    embed.add_field(name=f"Account Creation Date",
                    value=f"{user.created_at}",
                    inline=True)
    embed.add_field(name=f"Account Type", value=f"{type}", inline=True)
    embed.add_field(name=f"Member Count",
                    value=f"{server.member_count}",
                    inline=True)
    embed.set_footer(text=f"{user.name}", icon_url=user.avatar_url)
    channel = client.get_channel(940850341338021889)
    await channel.send(embed=embed)


# Bot Status
status = cycle([
    'bit.ly/98K8eH', 'Project IRIS', '.help', 'Project IRIS',
    'linktr.ee/KNear', 'Project IRIS'
])


@tasks.loop(seconds=5)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))


###
# Common Commands
###


# Ping
@client.command()
async def ping(ctx):
    await ctx.send(
        f'My ping is currently {round(client.latency  * 1000)}ms <:anime_brighteyes:943480188195442758>'
    )


# Ask
@client.command(aliases=['question', 'ask'])
async def _8ball(ctx, *, question):
    responses = open("./data/answers.dat", "r")
    responses = responses.readlines()
    embed = discord.Embed(title=question,
                          description=random.choice(responses),
                          colour=discord.Colour.dark_red())
    embed.set_footer(text=f"{ctx.author} | {ctx.guild}",
                     icon_url=ctx.author.avatar_url)
    channel = client.get_channel(941182583859978300)
    await channel.send(embed=embed)
    await ctx.reply(embed=embed)


# Developer Mail
@client.command(pass_context=True)
async def mail(ctx, *, message):
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    user = ctx.author
    with open('./data/log/Mail.log', 'a') as messagelog:
        print(f"<{st}> <{user}> {message}", file=messagelog)
    embed = discord.Embed(title="Message Received :incoming_envelope:",
                          description=f"{message}",
                          colour=discord.Colour.dark_red())
    embed.set_footer(text=f"Mailed by {ctx.author}",
                     icon_url=ctx.author.avatar_url)
    channel = client.get_channel(940619908885139516)
    await channel.send(embed=embed)
    await ctx.reply(embed=embed)


# Server Information
@client.command()
async def guildinfo(ctx):
    server = ctx.guild
    embed = discord.Embed(title=server.name,
                          description=server.description,
                          color=discord.Color.dark_red())
    embed.set_thumbnail(url=server.icon_url)
    embed.add_field(name="Owner", value=server.owner, inline=True)
    embed.add_field(name="Region", value=server.region, inline=True)
    embed.add_field(name="Member Count",
                    value=server.member_count,
                    inline=True)
    embed.add_field(name="Server Creation Date",
                    value=server.created_at,
                    inline=True)
    embed.add_field(name="Owner Registration Date",
                    value=server.owner.created_at,
                    inline=True)
    embed.add_field(name="Owner ID",
                    value=(f'`{server.owner.id}`'),
                    inline=True)
    embed.add_field(name="Server ID", value=(f'`{server.id}`'), inline=True)
    await ctx.reply(embed=embed)


@client.command()
async def cleardm(ctx):
    await ctx.reply("This might take a while.")
    remove = 9999999999999999999999999999999999999999
    remove = remove * remove * remove
    async for message in ctx.author.history(limit=remove):
        remove = remove + 1
        if message.author.id == client.user.id:
            await message.delete()
            time.sleep(0.5)
    await ctx.reply("All messages in the DM has been deleted.")


'''
###
# Moderation Commands
###

# Clear Command
@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount : int):
  await ctx.channel.purge(limit=amount + 1)

# Manage Members
@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, *, reason=None):
  await member.kick(reason=reason)
  await ctx.reply(f"Kicked {member.mention}")
  dm = discord.Embed(title=f"You were kicked from {ctx.guild.name}", description = f"Kicked by {ctx.author}", colour=discord.Colour.dark_red())
  dm.set_thumbnail(url=ctx.guild.icon_url)
  dm.add_field(name="Reason", value=f"{reason}", inline=False)
  await member.send(embed=dm)

# Ban Members
@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason=None):
  await member.ban(reason=reason)
  await ctx.reply(f"Banned {member.mention}")
  dm = discord.Embed(title=f"You were banned from {ctx.guild.name}", description = f"Banned by {ctx.author}", colour=discord.Colour.dark_red())
  dm.set_thumbnail(url=ctx.guild.icon_url)
  dm.add_field(name="Reason", value=f"{reason}", inline=False)
  await member.send(embed=dm)

#Unban Members
@client.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
  banned_users = await ctx.guild.bans()
  member_name, member_discriminator = member.split('#')

  for ban_entry in banned_users:
    user = ban_entry.user

    if (user.name, user.discriminator) == (member_name, member_discriminator):
      await ctx.guild.unban(user)
      await ctx.reply(f"Unbanned {user.mention}")
      return

# Manage Roles
@client.command()
@commands.has_permissions(manage_roles=True)
async def newrole(ctx, *, name):
    guild = ctx.guild
    try:
        await guild.create_role(name=name)
        await ctx.reply("<:yes:946357574792544286> Role created.")
    except discord.Forbidden:
        await ctx.reply("You're not allowed to do that <:Rem_pouting:940254772135616572>")
    except discord.HTTPException:
        await ctx.reply("<:no:946357626990633000> Failed to move role")
    except discord.InvalidArgument:
        await ctx.reply("<:no:946357626990633000> Invalid argument")

@client.command()
@commands.has_permissions(manage_roles=True)
async def giverole(ctx, user: discord.Member, role: discord.Role):
    try:
        await user.add_roles(role)
        await ctx.reply(f"<:yes:946357574792544286> {role.mention} has been assigned to {user.mention}")
    except discord.Forbidden:
        await ctx.reply("You do not have permission to do that <:Rem_pouting:940254772135616572>")
    except discord.HTTPException:
        await ctx.reply("<:no:946357626990633000> Failed to assign roles")
    except discord.InvalidArgument:
        await ctx.reply("<:no:946357626990633000> Invalid argument")

@client.command()
@commands.has_permissions(manage_roles=True)
async def moverole(ctx, role: discord.Role, pos: int):
    try:
        await role.edit(position=pos)
        await ctx.reply("<:yes:946357574792544286> Role moved.")
    except discord.Forbidden:
        await ctx.reply("You do not have permission to do that <:Rem_pouting:940254772135616572>")
    except discord.HTTPException:
        await ctx.reply("<:no:946357626990633000> Failed to move role")
    except discord.InvalidArgument:
        await ctx.reply("<:no:946357626990633000> Invalid argument") 
'''


###
# Cryptocurrency
###
# Register
@client.command(aliases=['reg'])
async def register(ctx):
    user = ctx.author.id
    start_tokens = '100'
    f = open(f"./data/tokens/{user}.dat", "x")
    f.write(start_tokens)

    await ctx.reply("Registered successfully")


# Balance
@client.command(aliases=['bal'])
async def balance(ctx):
    user = ctx.author.id
    rxc = open(f"./data/tokens/{user}.dat", "r")
    user_rxc = rxc.read()
    embed = discord.Embed(title=f"RixCoin owned by {ctx.author.name}",
                          description=f"{user_rxc}RXC",
                          colour=discord.Colour.dark_red())
    await ctx.reply(embed=embed)


# Daily
@client.command()
async def daily(ctx):
    user = ctx.author.id
    bal = open(f"./data/tokens/{user}.dat", "r")
    bal = bal.readline()
    bal = int(bal)
    daily = 100
    new_bal = daily + bal
    with open(f"./data/tokens/{user}.dat", "w") as token:
        print(new_bal, file=token)
    embed = discord.Embed(title="Daily RixCoin",
                          description=f"Received {daily} RXC",
                          colour=discord.Colour.dark_red())
    await ctx.reply(embed=embed)


# Transfer RixCoins to other users
'''
userget = User who receives the RixCoins
usergive = User who transfers the RixCoins
'''


@client.command()
async def give(ctx, userget: discord.Member, *, amount: int):
    # User ID & name lists
    usergive_id = ctx.author.id
    usergive_name = ctx.author.name
    userget_id = userget.id
    userget_name = userget.name

    # Userget Balance
    userget_bal = open(f"./data/tokens/{userget_id}.dat", "r")
    userget_bal = userget_bal.readline()
    userget_bal = int(userget_bal)
    userget_new_bal = userget_bal + amount
    with open(f"./data/tokens/{userget_id}.dat", "w") as userget_dat:
        print(userget_new_bal, file=userget_dat)

    # Usergive Balance
    usergive_bal = open(f"./data/tokens/{usergive_id}.dat", "r")
    usergive_bal = usergive_bal.readline()
    usergive_bal = int(userget_bal)
    usergive_new_bal = usergive_bal - amount
    with open(f"./data/tokens/{usergive_id}.dat", "w") as usergive_dat:
        print(usergive_new_bal, file=usergive_dat)

    success = discord.Embed(
        title="Successfully Transfered",
        description=
        f"{usergive_name} successfully transfered {amount} RXC to {userget_name}",
        colour=discord.Colour.dark_red())

    await ctx.reply(embed=success)


# System Shop
@client.command()
async def shop(ctx):
    menu = discord.Embed(
        title="System Shop",
        description=f"Items provided by the system. (non-NFTs)",
        colour=discord.Colour.dark_red())

    menu.add_field(name="Alphy's Baked Potatas(#0001)",
                   value="5 RXC",
                   inline=True)

    menu.add_field(name="Greeny's Fried Chicken(#0002)",
                   value="10 RXC",
                   inline=True)

    menu.add_field(name="Mikasa's Scarf(#6969)",
                   value="99999999 RXC",
                   inline=True)

    menu.set_footer(text="Use .sbuy {Item Code} to buy item. Do not include #")
    await ctx.reply(embed=menu)


# System Shop Buy
@client.command()
async def sbuy(ctx, *, item_code):
    user = ctx.author.id

    bal = open(f"./data/tokens/{user}.dat", "r")
    bal = bal.readline()
    bal = int(bal)

    price = open(f"./data/system_shop/{item_code}.dat", "r")
    price = price.readline()
    price = int(price)

    new_bal = bal - price

    with open(f"./data/tokens/{user}.dat", "w") as token:
        print(new_bal, file=token)

    with open(f"./data/system_shop/inventory/{item_code}/{user}.dat",
              "w") as inv:
        inv = inv + 1
        print(inv, file=inv)

    success = discord.Embed(
        title=f"Successfully Bought",
        description=f"Item: #{item_code} RixCoins left: {new_bal}",
        colour=discord.Colour.dark_red())
    await ctx.send(embed=success)


# Work
@client.command()
async def work(ctx):
    user = ctx.author.id
    earned = int(1)

    bal = open(f"./data/tokens/{user}.dat", "r")
    bal = bal.readline()
    bal = int(bal)

    new_bal = bal + earned

    with open(f"./data/tokens/{user}.dat", "w") as token:
        print(new_bal, file=token)

    await ctx.reply('You worked as ur mum and earned 1 RXC :>')


# Redeem Gift Codes
@client.command()
async def redeem(ctx, *, code=None):
    # Read gift code data
    with open("./data/RedeemCodes.dat") as f:
        valid_codes = f.read().splitlines()
    # Random loot amount
    RXC = random.randrange(20, 690)
    bread = random.randrange(3, 10)
    # Invalid gift code
    if code == None or code not in valid_codes:
        await ctx.reply(f"`{code}` is not a valid gift code.")
    # Valid gift code
    if code in valid_codes:
        embed = discord.Embed(title=f"Redeemed Successfully",
                              description=f"Gift Code: `{code}`",
                              colour=discord.Colour.teal())
        embed.add_field(
            name="You just got",
            value=
            f"{dot}**RixCoin** *{RXC}*\n{dot}**Bread** *{bread}*\nMore gift codes: [click here](https://twitter.com/Project_IRIS_26)"
        )
        await ctx.reply(embed=embed)


###
# NSFW
###


# Hentai
@client.command()
async def hentai(ctx):
    hentai = r"./images/hentai/all"
    pic = random.choice(os.listdir(hentai))
    file = discord.File(f"./images/hentai/all/{pic}", filename=pic)
    await ctx.reply(file=file)


# nhentai
@client.command()
async def nhentai(ctx):
    code = open("./data/nhentai.dat", "r")
    code = code.readlines()
    nhentaicode = random.choice(code)
    link = f'https://nhentai.net/g/{nhentaicode}'
    nhentai = discord.Embed(title=f"nhentai",
                            description=f"{nhentaicode}",
                            colour=discord.Colour.dark_red())
    nhentai.add_field(name="Link", value=f'[click me]({link})')
    await ctx.reply(embed=nhentai)


# Pussy
@client.command()
async def pussy(ctx):
    await ctx.send(
        "https://media.discordapp.net/attachments/401263317957738496/835270984264450068/834598351446081546.gif"
    )


###
# Bot Owner Commands
###


# Clear Command
@client.command()
async def godclear(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)


# Manage Users
@client.command()
async def godkick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.reply(f"Kicked {member.mention}")
    dm = discord.Embed(title=f"You were kicked from {ctx.guild.name}",
                       description=f"Kicked by {ctx.author}",
                       colour=discord.Colour.dark_red())
    dm.set_thumbnail(url=ctx.guild.icon_url)
    dm.add_field(name="Reason", value=f"{reason}", inline=False)
    await member.reply(embed=dm)


@client.command()
async def godban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.reply(f"Banned {member.mention}")
    dm = discord.Embed(title=f"You were banned from {ctx.guild.name}",
                       description=f"Banned by {ctx.author}",
                       colour=discord.Colour.dark_red())
    dm.set_thumbnail(url=ctx.guild.icon_url)
    dm.add_field(name="Reason", value=f"{reason}", inline=False)
    await member.reply(embed=dm)


@client.command()
async def godunban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name,
                                               member_discriminator):
            await ctx.guild.unban(user)
            await ctx.reply(f'Unbanned {user.mention}')
            return


# Manage Roles
@client.command()
async def godnewrole(ctx, *, name):
    guild = ctx.guild
    await guild.create_role(name=name)
    await ctx.reply(f'Role `{name}` has been created')


@client.command()
async def godgiverole(ctx, user: discord.Member, role: discord.Role):
    await user.add_roles(role)
    await ctx.reply(
        f"{ctx.author.name}, {user.name} has been given a role called: {role.name}."
    )


@client.command()
async def godmoverole(ctx, role: discord.Role, pos: int):
    await role.edit(position=pos)
    await ctx.reply("Role moved.")


# Say Command
@client.command(pass_context=True)
async def say(ctx, *, text):
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    message = ctx.message
    await message.delete()
    await ctx.send(f"{text}")
    with open('./data/log/say.log', 'a') as say:
        print(f"<{st}>  {text}", file=say)


# Generate RixCoin
@client.command()
async def rixgen(ctx, member: discord.Member, *, amount: int):
    user_id = member.id
    user_name = member.name
    bal = open(f"./data/tokens/{user_id}.dat", "r")
    bal = bal.readline()
    bal = int(bal)
    new_bal = bal + amount
    with open(f"./data/tokens/{user_id}.dat", "w") as token:
        print(new_bal, file=token)
    await ctx.reply(
        f"Successfully generated {amount} RXC into {user_name}'s inventory. <a:SakuraMiko_sus:940254774052388874>"
    )


# Developer Info
@client.command()
async def devinfo(ctx, mode: str = None, *, guildID: int = None):
    if ctx.author.id in gawds:
        page = 0

        if mode == "guilds":
            guildID = None
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
                    text=f"Developer Info requested by {ctx.author}",
                    icon_url=ctx.author.avatar_url)
                await ctx.author.send(embed=server_list)
            await ctx.reply(
                f"I'm currently connected to **{len(client.guilds)} servers** <:anime_brighteyes:943480188195442758> More detailed information has been sent to your DMs! <a:UruhaRushia_happy:940254774094364694>"
            )

        if mode == "members":
            guildID != None
            # Members
            server = client.get_guild(guildID)
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
                        bot = bot_tag
                        type_bot += 1
                    else:
                        bot = ""
                        type_user += 1
                    member_list.add_field(name=f"{member} {bot}",
                                          value=f"`{member.id}`",
                                          inline=True)
                member_list.set_footer(
                    text=f"{type_user} Users | {type_bot} Bots",
                    icon_url=server.icon_url)
                await ctx.author.send(embed=member_list)
            await ctx.reply(
                f"**{server}** currently has **{len(server.members)} members** <:anime_brighteyes:943480188195442758> More detailed information has been sent to your DMs! <a:UruhaRushia_happy:940254774094364694>"
            )

        if mode == "channels":
            guildID != None
            # Channels
            server = client.get_guild(guildID)
            # Text Channels
            for i in range(0, len(server.text_channels), 50):
                page = page + 1
                text_channel_list = discord.Embed(
                    title=f"{server}",
                    description=
                    f"***Page {page} | Guild ID: `{server.id}` | Text Channels ***",
                    colour=discord.Colour.dark_red())
                channels = server.text_channels[i:i + 50]
                for channel in channels:
                    text_channel_list.add_field(name=f"#{channel.name}",
                                                value=f"`{channel.id}`",
                                                inline=True)
                text_channel_list.set_footer(
                    text=f"{len(server.text_channels)} Text Channels",
                    icon_url=server.icon_url)
                await ctx.author.send(embed=text_channel_list)
            # Voice Channels
            for i in range(0, len(server.voice_channels), 50):
                page = page + 1
                voice_channel_list = discord.Embed(
                    title=f"{server}",
                    description=
                    f"***Page {page} | Guild ID: `{server.id}` | Voice Channels ***",
                    colour=discord.Colour.dark_red())
                channels = server.voice_channels[i:i + 50]
                for channel in channels:
                    voice_channel_list.add_field(
                        name=f":speaker:{channel.name}",
                        value=f"`{channel.id}`",
                        inline=True)
                voice_channel_list.set_footer(
                    text=f"{len(server.voice_channels)} voice Channels",
                    icon_url=server.icon_url)
                await ctx.author.send(embed=voice_channel_list)
            await ctx.reply(
                f"**{server}** currently has **{len(server.text_channels)} text channels** and **{len(server.voice_channels)} voice channels** <:anime_brighteyes:943480188195442758> More detailed information has been sent to your DMs! <a:UruhaRushia_happy:940254774094364694>"
            )

        if mode == None:
            await ctx.reply("***Error*** The mode is not specified.")
    else:
        await ctx.reply("***Error*** You can't use that command.")


# DM User
@client.command()
async def msg(ctx, user: discord.User, *, message: str):
    await user.send(message)
    await ctx.reply(
        f'Message `{message}` has been sent to **{user.name}** <:anime_brighteyes:943480188195442758>'
    )


# Spam
@client.command()
async def spam(ctx, amount: int, *, message: str):
    for i in range(amount):
        await ctx.send(message)


# Speak
@client.command()
async def speak(ctx, channelID: int, *, message: str):
    channel = client.get_channel(channelID)
    await channel.send(message)


# Create Invite
@client.command()
async def creinv(ctx, *, channelID: int):
    invchannel = client.get_channel(channelID)
    link = await invchannel.create_invite(max_age=0, max_uses=0)
    embed = discord.Embed(title=f"{invchannel.guild}",
                          description=f"[Invite Link]({link})",
                          colour=discord.Colour.dark_red())
    embed.set_footer(text=f"Requested by {ctx.author}",
                     icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)


# Guild Information for Developers
@client.command()
async def guild(ctx, *, guildID: int):
    server = client.get_guild(guildID)
    embed = discord.Embed(title=server.name,
                          description=server.description,
                          color=discord.Color.dark_red())
    embed.set_thumbnail(url=server.icon_url)
    embed.add_field(name="Owner", value=server.owner, inline=True)
    embed.add_field(name="Region", value=server.region, inline=True)
    embed.add_field(name="Member Count",
                    value=server.member_count,
                    inline=True)
    embed.add_field(name="Server Creation Date",
                    value=server.created_at,
                    inline=True)
    embed.add_field(name="Owner Registration Date",
                    value=server.owner.created_at,
                    inline=True)
    embed.add_field(name="Owner ID",
                    value=(f'`{server.owner.id}`'),
                    inline=True)
    embed.add_field(name="Server ID", value=(f'`{server.id}`'), inline=True)
    await ctx.send(embed=embed)


# User Information for Developers
@client.command()
async def user(ctx, *, userID: int):
    user = client.get_user(userID)
    if user.bot:
        type = "Bot"
        bot = bot_tag
    else:
        type = "User"
        bot = ""

    embed = discord.Embed(title=f"{user} {bot}",
                          colour=discord.Colour.dark_red())
    embed.set_thumbnail(url=user.avatar_url)
    embed.add_field(name=f"User ID", value=f"`{user.id}`", inline=True)
    embed.add_field(name="Account Type", value=f"{type}", inline=True)
    embed.add_field(name="Account Creation Date",
                    value=f"{user.created_at}",
                    inline=True)
    embed.set_footer(text=f"{user.name}", icon_url=user.avatar_url)
    await ctx.send(embed=embed)


# Edit Message
@client.command()
async def edit(ctx, msg_id: int, channel: discord.TextChannel, *,
               content: str):
    msg = await channel.fetch_message(msg_id)
    await msg.edit(content=content)
    await ctx.send(
        f"Message `{msg.id}` has been edited <:anime_brighteyes:943480188195442758>"
    )


# Add Gift Code
@client.command()
async def addcode(ctx, *, code=None):
    # Read  the gift codes to check if the code is available
    with open("./data/RedeemCodes.dat") as f:
        valid_codes = f.read().splitlines()
    # Error if the gift code is not specified or available
    if code == None or code in valid_codes:
        await ctx.send(
            "***Error*** Either the gift code is not specified or available.")
    else:
        with open("./data/RedeemCodes.dat", "a") as f:
            f.write(f"\n{code}")
        await ctx.send(f"`{code}` has been added.")


# Get a list of gift codes
@client.command()
async def checkcode(ctx):
    # Available Codes
    with open("./data/RedeemCodes.dat") as f:
        available_codes = f.read().splitlines()
    a_codes = '\n'.join(map(str, available_codes))
    # Expired Codes
    with open("./data/ExpRedeemCodes.dat") as f:
        expired_codes = f.read().splitlines()
    e_codes = '\n'.join(map(str, expired_codes))

    # Embed List of Gift Codes
    embed = discord.Embed(title="Gift Codes",
                          description="List of Gift Codes",
                          colour=discord.Colour.dark_red())
    embed.add_field(name="Currently Available", value=f"`{a_codes}`")
    embed.add_field(name="Expired/Outdated", value=f"`{e_codes}`")
    await ctx.author.send(embed=embed)
    await ctx.send(
        "Since it's top secret, the list of gift codes have been send to you privately."
    )


# Expire Gift Code
@client.command()
async def expcode(ctx, *, code):
    with open("./data/RedeemCodes.dat") as v:
        valid_codes = v.read().splitlines()
    if code == None or code not in valid_codes:
        await ctx.send(
            "***Error*** Either the gift code is not specified or not found.")
    else:
        with open("./data/ExpRedeemCodes.dat", "a") as e:
            e.write(f"\n{code}")
        with open("./data/RedeemCodes.dat", "r") as v:
            lines = v.readlines()
        with open("./data/RedeemCodes.dat", "w") as v:
            for line in lines:
                if line.strip("\n") != code:
                    v.write(line)
        await ctx.send(f"`{code}` has been set to expired.")


# Add Badge
@client.command()
async def addbadge(ctx, userID: int, *, badgeID):
    if badgeID == "admin":
        badge = admin_badge
    if badgeID == "mod":
        badge = mod_badge
    if badgeID == "neko":
        badge = catgirl_badge
    user = client.get_user(userID)

    # Error if the user has already owned the badge
    with open(f"./data/badges/{userID}.dat") as f:
        got_badges = f.read().splitlines()
    if badge in got_badges:
        await ctx.send("***Error*** The user has already owned that badge.")

    else:
        badges_file = Path(f"./data/badges/{user.id}.dat")
        # Add badge if file already exists
        if badges_file.exists():
            badges_file = open(f"./data/badges/{user.id}.dat", "a")
            badges_file.write(f"\n{badge}")
            await ctx.reply(
                f"The {badge}`{badgeID}` badge has been added to **{user}**")
        # Create new file and add badge if file doesn't exist
        else:
            badges_file = open(f"./data/badges/{user.id}.dat", "x")
            badges_file.write(f"\n{badge}")
            await ctx.reply(
                f"The {badge}`{badgeID}` badge has been added to **{user}**")


# Check Blacklist
@client.command()
async def blacklisted(ctx):
    with open("./data/blacklist.dat") as f:
        blacklisted_users = f.read().splitlines()
    user = '\n'.join(map(str, blacklisted_users))
    amount = len(blacklisted_users)
    embed = discord.Embed(title="Project IRIS Blacklist", description="")
    embed.add_field(name=f"{amount} Blacklisted Users", value=f"`{user}`")
    embed.set_footer(text=f"Use .botban to blacklist a user",
                     icon_url=client.user.avatar_url)
    await ctx.reply(embed=embed)


# Blacklist User
@client.command()
async def blacklist(ctx, userID: int = None):
    if userID == None:
        await ctx.reply("***Error*** The user ID is not specified.")
    else:
        user = client.get_user(userID)
        file = open("./data/blacklist.dat", "a")
        file.write(f"\n{str(user.id)}")
        file.close()
        await ctx.reply(f"**{user} | {user.mention}** has been blacklisted.")


###
# Help Commands
###


@client.command()
async def help(ctx):
    help = discord.Embed(title="Help Page",
                         description=f"Project IRIS Help Page",
                         colour=discord.Colour.dark_red())

    help.add_field(
        name="Common Commands",
        value=
        "**.ping** Displays the ping \n**.ask `question` ** Answers a Yes/No question. \n**.mail `message` ** Sends a message to the developers. \n**.info** Displays the information page. \n**.guildinfo** Displays the current guild's information page. \n**.cleardm** Clears your DM with Iris.",
        inline=False)

    help.add_field(
        name="Utility Commands",
        value=
        "**.clear `amount` ** Clears a specific amount of messages. \n**.kick `@user` `reason` ** Kicks a member. \n**.ban `@user` `reason` ** Bans a member. \n**.unban `user#0000` ** Unbans a user \n**.newrole `rolename` ** Creates a new role. \n**.giverole `@user` `@role` ** Assigns a role to a user. \n**.moverole `@role` `position` ** Moves a role to a given position.",
        inline=False)

    help.add_field(
        name="Currency Commands",
        value=
        "**.reg** Registers a RixCoin account. \n**.bal** Displays your account balance. \n**.daily** Claim daily RixCoin reward. \n**.give `@user` `amount` ** Transfers RixCoin to another user. \n**.redeem `giftCode` ** Redeems a gift from a gift code.",
        inline=False)

    help.add_field(
        name="NSFW Commands",
        value=
        "**.hentai** Sends a random hentai image. \n**.nhentai** Sends a random nhentai code and a clickable link. \n**.pussy** Sends a pussy GIF.",
        inline=False)

    help.add_field(
        name="User Profile",
        value=
        "**.profile** Displays your user profile. \n**.bio `newBio` ** Lets you edit your bio \n**.badges** Shows a list of badges and how to obtain them.",
        inline=False)

    help.set_footer(text=f"Prefix: . | Use .info for more information",
                    icon_url=client.user.avatar_url)

    await ctx.author.send(embed=help)
    await ctx.reply("DM sent! <:NanashiMumei_eyes:940254772659892264>")


# Developer Help
@client.command(aliases=["godmode", "gawdmode"])
async def helpdev(ctx):

    help = discord.Embed(title="Project IRIS God Mode",
                         description=f"Developer Only Commands",
                         colour=discord.Colour.dark_red())

    help.add_field(
        name="RixCoin",
        value=
        "**.rixgen `@user` `amount` ** Generate RixCoins into a user's inventory. \n**.addcode `newGiftCode` ** Adds a new gift code to be redeemed. \n**.expcode `validGiftCode` ** Sets a valid gift code to expired. \n **.checkcode** Get a list of valid and expired gift codes.",
        inline=False)

    help.add_field(
        name="Information",
        value=
        "**.devinfo `mode` `guildID`** Displays an information page for developers.\nModes: `guilds/channels/members`\nGuild ID is only needed for `members` and `channels` mode. \n**.guild `guildID` ** Gets information about a specific guild. \n**.user `userID` ** Gets information about a specific user.",
        inline=False)

    help.add_field(
        name="Messaging",
        value=
        "**.say `message` ** Sends a message to the current channel.\n**.spam `amount` `message` ** Spams a specific message. \n**.speak `channelID` `message` ** Sends a message to a specific channel without having the user to be in the server. \n**.edit `messageID` `channelID` `newMessage` ** Edits a message sent by Iris.",
        inline=False)

    help.add_field(
        name="Blacklist",
        value=
        "**.blacklisted** Gets a list of user IDs that have been blacklisted. \n **.blacklist `userID` ** Adds a user to the blacklist.",
        inline=False)

    help.add_field(
        name="Miscellaneous",
        value=
        "**.creinv `channelID` ** Creates an invite for the specific channel. \n **.addbadge `userID` `badgeID` ** Gives a user a badge. \nAdd `god` before a moderation command for God Mode.",
        inline=False)

    help.set_footer(text=f"Prefix: . | Use .info for more information")

    if ctx.author.id in gawds:
        await ctx.author.send(embed=help)
        await ctx.reply(
            f"<a:GodModeGuideBook:965899341762035733> ***Guide to God Mode*** has been added to your inventory."
        )

    else:
        await ctx.reply(
            f"You are not allowed to use the forbidden power of the Gods, you hooman!"
        )


@client.command()
async def info(ctx):
    # Twitter
    iristwitter = "https://twitter.com/Project_IRIS_26"
    neartwitter = "https://twitter.com/KuroyukiNear"
    alphatwitter = "https://twitter.com/Meow_Alpha"
    nifftytwitter = "https://twitter.com/alastor607"
    website = "none"
    # Bot Invites
    invite = "https://discord.com/api/oauth2/authorize?client_id=902720782503907358&permissions=1644971949559&scope=bot"
    inviteNitrogen = "https://discord.com/api/oauth2/authorize?client_id=958713810707972127&permissions=137976343616&scope=bot"
    # Server Invites
    support_server = "https://discord.gg/9RUy6suKsy"
    EcchiDB = "https://discord.gg/zqYtgmXZxP"
    # Other Links
    devteaminfo = "https://pastebin.com/raw/i77dMTcz"
    bottopgg = "none"
    servertopgg = "https://top.gg/servers/927883828998053909"
    serverdisboard = "https://disboard.org/server/927883828998053909"

    links = discord.Embed(title=f"Information Page",
                          description="**Links**",
                          colour=discord.Colour.dark_red())

    links.add_field(name="Official Website",
                    value=f'[click me]({website})',
                    inline=True)

    links.add_field(
        name="Discord Servers",
        value=
        f"Support Server [click me]({support_server}) \nEcchi Database [click me]({EcchiDB})",
        inline=True)

    links.add_field(
        name="Twitter",
        value=
        f"Iris [click me]({iristwitter}) \n[Dev] Near [click me]({neartwitter}) \n[Dev] Alpha [click me]({alphatwitter}) \n[Art] Niffty [click me]({nifftytwitter})",
        inline=True)

    links.add_field(
        name="Bot Invites",
        value=
        f"Iris [click me]({invite}) \nNitrogen [click me]({inviteNitrogen})",
        inline=True)

    links.add_field(
        name="Server Listings",
        value=
        f"Top.gg [click me]({servertopgg}) \nDisboard [click me]({serverdisboard})"
    )

    links.add_field(name="Other Links",
                    value=f"DevTeam Info [click me]({devteaminfo})",
                    inline=True)

    server = len(client.guilds)
    server_count = int(server)
    Near = client.get_user(638342719592202251)
    Alpha = client.get_user(707595898200260728)
    info = discord.Embed(title=f"Bot Information",
                         description="",
                         colour=discord.Colour.dark_red())
    info.add_field(name="Developers", value=f"{Near} \n{Alpha}", inline=False)
    info.add_field(name="Prefix",
                   value=f"{client.command_prefix}",
                   inline=False)
    info.add_field(name="Guilds", value=f"{server_count}", inline=False)
    info.add_field(name="Discord Version",
                   value=f"{discord.__version__}",
                   inline=False)
    info.set_thumbnail(url=client.user.avatar_url)

    await ctx.reply(embed=info)
    await ctx.author.send(embed=links)
    await ctx.send(
        "URLs has been sent to your DMs! <:GawrGura_glance:943480212706963456>"
    )


# https://top.gg/bot/902720782503907358

###
# User Profile
###


# Display Profile
@client.command()
async def profile(ctx, *, member: discord.Member = None):
    if member == None:
        user = ctx.author
    else:
        user = member
    # Get RixCoins
    rix_file = Path(f"./data/tokens/{user.id}.dat")
    if rix_file.exists():
        rix_file = open(f"./data/tokens/{user.id}.dat", "r")
        rix = rix_file.read()
        rix = f"`{rix}`"
    else:
        rix = "You don't have a RixCoin account.\nUse `.reg` to register."
    # Get Bio
    bio_file = Path(f"./data/bio/{user.id}.dat")
    if bio_file.exists():
        bio_file = open(f"./data/bio/{user.id}.dat", "r")
        bio = bio_file.read()
    else:
        bio = "Your bio is empty. Use `.bio` to edit your bio."
    # Get Badges
    badges_file = Path(f"./data/badges/{user.id}.dat")
    if badges_file.exists():
        badges_file = open(f"./data/badges/{user.id}.dat", "r")
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
    info.add_field(name="RixCoins", value=f"{rix}", inline=True)
    info.add_field(name="Messages Sent",
                   value=f"`Under Development`",
                   inline=False)
    info.add_field(name="Project IRIS Badges",
                   value=f"{IRIS_badges}",
                   inline=True)
    info.add_field(name="Bio", value=f"{bio}", inline=False)
    info.set_thumbnail(url=user.avatar_url)
    await ctx.reply(embed=info)


# Edit Bio
@client.command()
async def bio(ctx, *, bio):
    user = ctx.author
    bio_file = Path(f"./data/bio/{user.id}.dat")
    if bio_file.exists():
        bio_file = open(f"./data/bio/{user.id}.dat", "w")
        bio_file.write(bio)
        await ctx.reply(
            "Your bio has been changed.\nNote: if `.profile` is not working after you changed your bio, you have probably exceeded the 1,000 word limit."
        )
    else:
        bio_file = open(f"./data/bio/{user.id}.dat", "x")
        bio_file.write(bio)
        await ctx.reply(
            "Your bio has been changed.\nNote: if `.profile` is not working after you changed your bio, you have probably exceeded the 1,000 word limit."
        )


# Badges List
@client.command()
async def badges(ctx, *, badgeID=None):
    all = discord.Embed(
        title=f"Project IRIS Badges",
        description=
        "Use **.badges `badgeID` ** to get info on a specific badge.",
        colour=discord.Colour.dark_red())
    all.add_field(
        name="Obtainable Badges",
        value=
        f"{admin_badge}**Support Server Administrator**\n***Badge ID***  `admin`\n{mod_badge}**Support Server Moderators**\n***Badge ID***  `mod`"
    )
    all.add_field(
        name="Unobtainable Badges",
        value=
        f"{developer_badge}**Project IRIS Developers**\n***Badge ID***  `IRISdev`\n{betatester_badge}**Project IRIS Beta Tester**\n***Badge ID***  `BetaTester`\n{catgirl_badge}**Verified Catgirl**\n***Badge ID***  `neko`"
    )
    all.set_footer(text=f"Project IRIS Badges")

    # Administrator Badge
    admin = discord.Embed(
        title=f"{admin_badge} Support Server Admnistrator Badge",
        description="**Badge ID: `admin` **",
        colour=discord.Colour.dark_red())
    admin.add_field(
        name="Information",
        value=
        "Given to the administrators of our official support server to appreciate their hard work."
    )
    admin.add_field(
        name="How to Obtain",
        value=
        "Apply for administrator in our support server. But first you need to become a moderator."
    )
    admin.set_thumbnail(url=admin_badge_png)
    admin.set_footer(text=f"Use  .badges  to view all badges.")

    # Moderator Badge
    mod = discord.Embed(title=f"{mod_badge} Support Server Moderator Badge",
                        description="**Badge ID: `mod` **",
                        colour=discord.Colour.dark_red())
    mod.add_field(
        name="Information",
        value=
        "Given to the moderators of our official support server to appreciate their hard work."
    )
    mod.add_field(
        name="How to Obtain",
        value=
        "Apply for moderator in our support server. But first you need to become a helper."
    )
    mod.set_thumbnail(url=mod_badge_png)
    mod.set_footer(text=f"Use  .badges  to view all badges.")

    # Developer Badge
    dev = discord.Embed(title=f"{developer_badge} Developer Badge",
                        description="**Badge ID: `IRISdev` **",
                        colour=discord.Colour.dark_red())
    dev.add_field(
        name="Information",
        value=
        "Owned by the members of the Project IRIS Development Team and will not be given out to others."
    )
    dev.add_field(name="How to Obtain", value="***Unobtainable***")
    dev.set_thumbnail(url=developer_badge_png)
    dev.set_footer(text=f"Use  .badges  to view all badges.")

    # Beta Tester Badge
    bt = discord.Embed(
        title=f"{betatester_badge} Project IRIS Beta Tester Badge",
        description="**Badge ID: `BetaTester` **",
        colour=discord.Colour.dark_red())
    bt.add_field(
        name="Information",
        value="Owned by Beta Testers that are chosen by Alpha, the Co-Owner.")
    bt.add_field(name="How to Obtain", value="***Unobtainable***")
    bt.set_thumbnail(url=betatester_badge_png)
    bt.set_footer(text=f"Use  .badges  to view all badges.")

    # Verified Catgirl Badge
    neko = discord.Embed(
        title=f"{catgirl_badge} Project IRIS Beta Tester Badge",
        description="**Badge ID: `neko` **",
        colour=discord.Colour.dark_red())
    neko.add_field(
        name="Information",
        value="Only real & verified cat girls are allowed to own them.")
    neko.add_field(name="How to Obtain", value="***Unobtainable***")
    neko.set_thumbnail(url=catgirl_badge_png)
    neko.set_footer(text=f"Use  .badges  to view all badges.")

    if badgeID == None:
        await ctx.reply(embed=all)
    if badgeID == "admin":
        await ctx.reply(embed=admin)
    if badgeID == "mod":
        await ctx.reply(embed=mod)
    if badgeID == "IRISdev":
        await ctx.reply(embed=dev)
    if badgeID == "BetaTester":
        await ctx.reply(embed=bt)
    if badgeID == "neko":
        await ctx.reply(embed=neko)


# Item List
@client.command(aliases=["items"])
async def item(ctx, *, itemID=None):
    all = discord.Embed(
        title=f"Project IRIS Items",
        description="Use **.item `itemID` ** to get info on a specific badge.",
        colour=discord.Colour.dark_red())
    all.add_field(name=f"{GodModeGuideBook} Guide to God Mode",
                  value=f"***Item ID: `godBook` ***")
    all.set_footer(text=f"Project IRIS Items")

    # godBook
    godBook = discord.Embed(title=f"{GodModeGuideBook} Guide to God Mode",
                            description="***Item ID: `godBook` ***",
                            colour=discord.Colour.dark_red())
    godBook.add_field(
        name="Information",
        value=
        "A guide book written by Odin as he has amnesia. Now owned by Project IRIS developers and is used to rule the world."
    )
    godBook.set_thumbnail(url=GodModeGuideBook_img)
    godBook.set_footer(text=f"Use  .item  to view all items.")
    '''
  # petCollar
  petCollar = discord.Embed(title=f"{GodModeGuideBook} Guide to God Mode", description = "***Item ID: `godBook` ***", colour=discord.Colour.dark_red())
  petCollar.add_field(name="Information",value="A guide book written by Odin as he has amnesia. Now owned by Project IRIS developers and is used to rule the world.")
  petCollar.set_thumbnail(url=GodModeGuideBook_img)
  petCollar.set_footer(text=f"Use  .badges  to view all badges.")
  '''

    if itemID == None:
        await ctx.reply(embed=all)
    if itemID == "godBook":
        await ctx.reply(embed=godBook)
    if itemID == "petCollar":
        await ctx.reply(embed=petCollar)


# Config Log
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='./data/log/config.log',
                              encoding='utf-8',
                              mode='w')
handler.setFormatter(
    logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# Connect
keep_alive()
token = os.environ.get("TOKEN")
client.run(token)
'''
bit.ly/98K8eH Rick Roll
bit.ly/3ka9U1Y Website
'''
'''

'''
