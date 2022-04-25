import os
import time

import discord
import discord.ext
from discord.ext import commands, tasks
from discord.ext.commands import CheckFailure, check, has_permissions
from discord.utils import get
from discord_components import Button, ButtonStyle, DiscordComponents
from dotenv import load_dotenv

from src.commands import addCommands
from src.keepAlive import keep_alive

client = discord.Client()
client = commands.Bot(command_prefix='ttt!')
client.remove_command('help')
DiscordComponents(client)

load_dotenv()

@client.event
async def on_ready():
    print("bot online")
    print(client.user)

addCommands(client)

keep_alive()
client.run(os.getenv('TOKEN'))
