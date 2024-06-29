import os

import discord

from src import (
    registro_functions, 
    carteira_functions,
    ninho_functions
)
from src.base import config


@config.client.event
async def on_ready():
    await registro_functions.tree.sync(guild = discord.Object(id = 1196189171530870795))
    await carteira_functions.tree.sync(guild = discord.Object(id = 1196189171530870795))
    await ninho_functions.tree.sync(guild = discord.Object(id = 1196189171530870795))

    print("Pronto")


config.client.run(config.TOKEN)

