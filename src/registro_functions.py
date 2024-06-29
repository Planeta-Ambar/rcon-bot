"""
Script que contem todas as funções relacionadas ao registro de jogadores no Discord.
"""
import re
import discord

from src.base.config import client, tree
from src.base.player import PlayerManager, session

# Instanciando o objeto PlayerManager
player_manager = PlayerManager()


@tree.command(
    name = "registrar",
    description = "Registra seu ID da Alderon Games",
    guild = discord.Object(id = 1196189171530870795)
)
async def registrar(interaction: discord.Interaction, id_alderon: str) -> None:
    """
    Realiza o registro do usuário no banco de dados do Planeta Âmbar com o seu ID do Discord, nome de usuário e ID da Alderon 
    Games.
    """
    # Verifica se o canal atual é o "registro"
    if interaction.channel.name == "registro":
        # Pega o ID e user do usuário no Discord
        user_id = interaction.user.id
        username = interaction.user.name

        # Cria um novo objeto player
        player_manager.create_player(user_id, username)
        
        # Verifica se o user existe; se não, ele é criado na base de dados
        if player_manager.get_player().existe():
            await interaction.response.send_message(f"Usuário {id_alderon} já existe")

        else:
            # Verifica se o ID fornecido pelo usuário está no padrão correto
            # Se não estiver, uma mensagem de erro será exibida
            padrao = re.match("(\d{3}\-\d{3}\-\d{3})", id_alderon)

            if padrao:
                session.add(player_manager.get_player().get_player())

                player_manager.get_player().set_id_alderon(id_alderon)

                session.commit()

                await interaction.response.send_message(f"Usuário {id_alderon} registrado com sucesso")

            else:
                await interaction.response.send_message(f"O ID {id_alderon} não é válido")                

    # Caso o canal não seja o correto
    else:
        link_registro = interaction.guild.get_channel(1197591391660945508).mention

        await interaction.response.send_message(f"Comando disponível apenas no canal {link_registro}")