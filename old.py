@client.event
async def on_message_delete(message: str):
  user = message.author
  channel = message.channel
  embed = discord.Embed(title=f"{user} deleted a message in {message.guild}",description=(f"{user.mention} **|** {channel.mention}"),colour=discord.Colour.dark_red())
  embed.add_field(name=f"Content", value=f"{message.content}", inline=False)
  embed.add_field(name=f"ID", value=f"```\n Guild = {message.guild.id} \n Channel = {channel.id} \n User = {user.id} \n Message = {message.id} \n```", inline=False)
  embed.timestamp = message.created_at
  channel = client.get_channel(940612873904852992)
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
    link = f'https://discordapp.com/channels/{server.id}/{channel.id}/{msg.id}'
    embed = discord.Embed(title=f'{user} edited a message in {msg.guild}',description=(f"{user.mention} **|** {channel.mention}"),colour=discord.Colour.dark_red())
    embed.add_field(name=f"Original Message", value=f"{message_before.content}", inline=False)
    embed.add_field(name=f"Edited Message", value=f"{message_after.content}", inline=False)
    embed.add_field(name=f"ID", value=f"```\n Guild = {server.id} \n Channel = {channel.id} \n User = {user.id} \n Message = {msg.id} \n```", inline=False)
    embed.add_field(name=f"Message Link", value=f"[here]({link})", inline=False)
    embed.timestamp = msg.created_at
    channel = client.get_channel(940848583211618334)
    await channel.send(embed=embed)


@client.event
async def on_member_update(before, after):
  if after.bot:
    if str(before.status) == "offline":
        if str(after.status) == "online":
          channel = client.get_channel(947000928370823210) 
          online = discord.Embed(title=f'{after} is online',description=(f"User ID: `{after.id}`"),colour=discord.Colour.green())
          online.set_thumbnail(url=after.avatar_url)
          online.add_field(name=f"Server: {after.guild.name}", value=f"Server ID: `{after.guild.id}`", inline=True)
          await channel.send(embed=online)
     
    if str(before.status) == "online":
        if str(after.status) == "offline":
          channel = client.get_channel(947000928370823210)
          offline = discord.Embed(title=f'{after} is offline',description=(f"User ID: `{after.id}`"),colour=discord.Colour.light_grey())
          offline.set_thumbnail(url=after.avatar_url)
          offline.add_field(name=f"Server: {after.guild.name}", value=f"Server ID: `{after.guild.id}`", inline=True)
          await channel.send(embed=offline)