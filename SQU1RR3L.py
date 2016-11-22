import discord
import os
import asyncio
import logging

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message, user: discord.Member=None):
    prefix = 's?'
    if message.content.lower().startswith(prefix + 'help'):
        await client.send_message(message.channel, 'Available commands: `help`, `userinfo`, `messages`\nBot prefix: `s?`')

    elif message.content.lower().startswith(prefix + 'userinfo'):
        author = message.author
        server = message.server

        roles = [x.name for x in author.roles if x.name != "@everyone"]

        joined_at = author.joined_at
        since_created = (message.timestamp - author.created_at).days
        since_joined = (message.timestamp - joined_at).days
        user_joined = joined_at.strftime("%d %b %Y %H:%M")
        user_created = author.created_at.strftime("%d %b %Y %H:%M")
        created_on = "{}\n({} days ago)".format(user_created, since_created)
        joined_on = "{}\n({} days ago)".format(user_joined, since_joined)

        game = "Currently {}".format(author.status)

        if author.game is None:
            pass
        elif author.game.url is None:
            game = "Playing {}".format(author.game)
        else:
            game = "Streaming: [{}]({})".format(author.game, author.game.url)

        if roles:
            roles = sorted(roles, key=[x.name for x in server.role_hierarchy
                                       if x.name != "@everyone"].index)
            roles = ", ".join(roles)
        else:
            roles = "None"

        data = discord.Embed(description=game, colour=author.colour)
        data.add_field(name="Discord join date", value=created_on)
        data.add_field(name="Server join date", value=joined_on)
        data.add_field(name="Roles", value=roles, inline=False)
        data.set_footer(text="User ID: " + author.id)

        if author.avatar_url:
            name = str(author)
            name = " ~ ".join((name, author.nick)) if author.nick else name
            data.set_author(name=name, url=author.avatar_url)
            data.set_thumbnail(url=author.avatar_url)
        else:
            data.set_author(name=author.name)

        try:
            await client.send_message(message.channel, embed=data)
        except discord.HTTPException:
            await client.send_message(message.channel, "I need the `Embed links` permission "
                               "to send this")

    elif message.content.lower().startswith(prefix + 'messages'):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1

path = os.getcwd()
rawtoken = open(path + '\\token.txt')
token = rawtoken.read()
client.run(token)