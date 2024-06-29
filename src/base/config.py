"""
Arquivo de configuração global.
"""
import os
from dotenv import load_dotenv

import discord
from discord import app_commands

# Configuração global
load_dotenv()

HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
PASSWORD = os.getenv("PASSWORD")
TOKEN = os.getenv("DISCORD_TOKEN")

# Configurações do Discord
intents = discord.Intents.default()
client = discord.Client(intents = intents)
tree = app_commands.CommandTree(client)