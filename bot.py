import time

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

    # start = time.time()
    # dur_em_segundos = 59 * 60

    # # Roda o bot por 59 minutos
    # # Após isso, ele será reiniciado
    # while True:
    #     temp_atual = time.time()
    #     temp_passado = temp_atual - start

    #     if temp_passado >= dur_em_segundos - (5 * 60) and temp_passado < dur_em_segundos - (5 * 60) + 1:
    #         print(f"Atenção: o bot será reiniciado em 5 minutos!")

    #     if temp_passado >= dur_em_segundos:
    #         print("O bot está reiniciando.")

    #         break

    #     time.sleep(1)  # Previne alto uso de CPU

    #     config.client.close()
    

config.client.run(config.TOKEN)

