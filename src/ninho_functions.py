"""
Script que contem todas as funções relacionadas à criação de ninhos.
"""
import uuid
import yaml
import discord

from src.base.config import tree
from src.base.player import PlayerManager

# Instanciando o objeto PlayerManager
player_manager = PlayerManager()

# Carregando as espécies disponíveis
with open("src/def/especies.yaml") as stream:
    try:
        especies = yaml.safe_load(stream)

    except yaml.YAMLError as exc:
        print(exc)


@tree.command(
    name = "ninho",
    description = "Cria um ninho para uma determinada espécie",
    guild = discord.Object(id = 1196189171530870795)
)
async def ninho(interaction: discord.Interaction, especie: str, desc: str, qtd_ovos: int, tempo_restante: str) -> None:
    """
    Cria um ninho com base nos parâmetros fornecidos. Há uma verificação para que o bot não aceite valores inválidos para o 
    animal. Além disso, a descrição e quantidade de ovos devem ser informados, além de quando o ninho estará disponível 
    (ex: 'em 20 minutos').
    """
    # Verifica se o canal atual é o "ninhos"
    if interaction.channel.name == "ninhos":
        # Pega o ID do usuário no Discord
        user_id = interaction.user.id

        # Define a espécie escolhida (null por enquanto)
        especie_escolhida = None

        # Tenta carregar o usuário a partir do banco de dados
        if player_manager.load_from_database(user_id = user_id):
            for especie_disp in especies["animais_disponiveis"]:
                if str.lower(especie_disp.split(' ')[0]) == str.lower(especie):
                    especie_escolhida = especie_disp

            if especie_escolhida is None or qtd_ovos is None or tempo_restante is None:
                await interaction.response.send_message("Comando utilizado de forma incorreta! Informe os parâmetros do /ninho de forma correta!")

            else:
                id_ninho = str(uuid.uuid4())[:8]

                embed = discord.Embed(title = f"Ninho de {especie_escolhida}", colour = discord.Colour.blue())

                embed.add_field(name = "O ID desse ninho é: ", value = id_ninho)
                embed.add_field(name = "Pais", value = f"{interaction.user.display_name} [{player_manager.get_player().get_id_alderon()}]", inline = False)
                embed.add_field(name = "Descrição", value = desc, inline = False)
                embed.add_field(name = "Ovos disponíveis", value = "\U0001F95A" * qtd_ovos, inline = False)
                embed.add_field(name = "Filhotes", value = "Nenhum", inline = False)

                player_manager.get_player().set_ninho(
                    id_ninho = id_ninho, 
                    user = interaction.user.display_name,
                    id_alderon_user = player_manager.get_player().get_id_alderon(),
                    parceiro = None,
                    id_alderon_parceiro = None,
                    desc = desc,
                    animal = especie_escolhida,
                    filhotes = None,
                    id_alderon_filhotes = None, 
                    qtd_ovos = qtd_ovos
                )

                await interaction.response.send_message(embed = embed)

        # Se o usuário não existe na base
        else:
            await interaction.response.send_message("Sem o registro, não é permitido acessar o ninho!")

    # Caso o canal não seja o correto
    else:
        link_ninho = interaction.guild.get_channel(1197591462091706398).mention

        await interaction.response.send_message(f"Comando disponível apenas no canal {link_ninho}")


@tree.command(
    name = "juntar_a_ninho",
    description = "Junte-se a um ninho criado por outro jogador",
    guild = discord.Object(id = 1196189171530870795)
)
async def juntar_a_ninho(interaction: discord.Interaction, user_alvo: str, parceiro_ou_filhote: str) -> None:
    """
    Conecta um jogador a um ninho criado por outro. O jogador interessado deve informar o user do Discord do jogador responsável
    pelo ninho desejado e se deseja se juntar como parceiro ou filhote; haverá uma verificação para que não existam mais de 2 parceiros e mais 
    filhotes do que ovos disponíveis.
    """
    # Verifica se o canal atual é o "ninhos"
    if interaction.channel.name == "ninhos":
        # Pega o ID do usuário no Discord
        user_id = interaction.user.id

        # Tenta carregar o usuário a partir do banco de dados
        if player_manager.load_from_database(user_id = user_id):
            # Tenta carregar o jogador alvo
            if player_manager.load_user(user = str.lower(user_alvo)):
                # Carrega os dados do ninho
                dados_ninho = player_manager.get_player().get_ninho_por_user(user_alvo = user_alvo)

                if str.lower(parceiro_ou_filhote) not in ["parceiro", "filhote"]:
                    await interaction.response.send_message("Você deve informar se deseja ser o parceiro do ninho ou um filhote!")

                elif dados_ninho["parceiro"] is not None and str.lower(parceiro_ou_filhote) == "parceiro":
                    await interaction.response.send_message("O ninho já tem um parceiro!")

                elif dados_ninho["qtd_ovos"] == 0 and str.lower(parceiro_ou_filhote) == "filhote":
                    await interaction.response.send_message("O ninho está cheio!")

                else:
                    if parceiro_ou_filhote == "parceiro":
                        filhotes_output = ""

                        pais = f"{dados_ninho['user']} [{dados_ninho['id_alderon_user']}]\n \
                                 {interaction.user.display_name} [{player_manager.get_player().get_id_alderon()}]"
                        
                        for filhote, id_alderon_filhote in zip(dados_ninho["filhotes"], dados_ninho["id_alderon_filhotes"]):
                            filhotes_output += f"{filhote} [{id_alderon_filhote}]\n"
                        
                        embed = discord.Embed(title = f"Ninho de {dados_ninho['animal']}", colour = discord.Colour.blue())

                        embed.add_field(name = "O ID desse ninho é: ", value = dados_ninho["id_ninho"])
                        embed.add_field(name = "Pais", value = pais, inline = False)
                        embed.add_field(name = "Descrição", value = dados_ninho["desc"], inline = False)
                        embed.add_field(name = "Ovos disponíveis", value = "\U0001F95A" * dados_ninho["qtd_ovos"], inline = False)
                        embed.add_field(name = "Filhotes", value = "Nenhum" if filhotes_output is None else filhotes_output, inline = False)

                        player_manager.get_player().set_ninho(
                            id_ninho = dados_ninho["id_ninho"], 
                            user = dados_ninho["user"],
                            id_alderon_user = dados_ninho["id_alderon_user"],
                            parceiro = interaction.user.display_name,
                            id_alderon_parceiro = player_manager.get_player().get_id_alderon(),
                            desc = dados_ninho["desc"],
                            animal = dados_ninho["animal"], 
                            filhotes = dados_ninho["filhotes"],
                            id_alderon_filhotes = dados_ninho["id_alderon_filhotes"],
                            qtd_ovos = dados_ninho["qtd_ovos"]
                        )

                        await interaction.response.send_message(embed = embed)

                    else:
                        filhotes_output = ""

                        if dados_ninho['parceiro']:
                            pais = f"{dados_ninho['user']} [{dados_ninho['id_alderon_user']}]\n \
                                 {dados_ninho['parceiro']} [{dados_ninho['id_alderon_parceiro']}]"
                            
                        else:
                            pais = f"{dados_ninho['user']} [{dados_ninho['id_alderon_user']}"
            
                        dados_ninho["filhotes"].append(interaction.user.display_name)
                        dados_ninho["id_alderon_filhotes"].append(player_manager.get_player().get_id_alderon())

                        for filhote, id_alderon_filhote in zip(dados_ninho["filhotes"], dados_ninho["id_alderon_filhotes"]):
                            filhotes_output += f"{filhote} [{id_alderon_filhote}]\n"
                        
                        embed = discord.Embed(title = f"Ninho de {dados_ninho['animal']}", colour = discord.Colour.blue())

                        embed.add_field(name = "O ID desse ninho é: ", value = dados_ninho["id_ninho"])
                        embed.add_field(name = "Pais", value = pais, inline = False)
                        embed.add_field(name = "Descrição", value = dados_ninho["desc"], inline = False)
                        embed.add_field(name = "Ovos disponíveis", value = "\U0001F95A" * int(dados_ninho["qtd_ovos"] - 1), inline = False)
                        embed.add_field(name = "Filhotes", value = filhotes_output, inline = False)

                        player_manager.get_player().set_ninho(
                            id_ninho = dados_ninho["id_ninho"], 
                            user = dados_ninho["user"],
                            id_alderon_user = dados_ninho["id_alderon_user"],
                            parceiro = interaction.user.display_name,
                            id_alderon_parceiro = player_manager.get_player().get_id_alderon(),
                            desc = dados_ninho["desc"],
                            animal = dados_ninho["animal"],  
                            filhotes = dados_ninho["filhotes"],
                            id_alderon_filhotes = dados_ninho["id_alderon_filhotes"],
                            qtd_ovos = int(dados_ninho["qtd_ovos"]) - 1
                        )

                        await interaction.response.send_message(embed = embed)
            
            # Se o usuário alvo não existe na base
            else:
                await interaction.response.send_message("O usuário requisitado não é registrado!")

        # Se o usuário não existe na base
        else:
            await interaction.response.send_message("Sem o registro, não é permitido acessar o ninho!")

    # Caso o canal não seja o correto
    else:
        link_ninho = interaction.guild.get_channel(1197591462091706398).mention

        await interaction.response.send_message(f"Comando disponível apenas no canal {link_ninho}")

                    
@tree.command(
    name = "teleportar_ao_ninho",
    description = "Teleporte-se a um ninho criado por outro jogador",
    guild = discord.Object(id = 1196189171530870795)
)
async def teleportar_ao_ninho(interaction: discord.Interaction, user_alvo: str) -> None:
    """
    Teleporta um jogador a um ninho criado por outro. O jogador interessado deve informar o user do Discord do jogador responsável
    pelo ninho.
    """
    # Verifica se o canal atual é o "ninhos"
    if interaction.channel.name == "ninhos":
        # Pega o ID do usuário no Discord
        user_id = interaction.user.id

        # Tenta carregar o usuário a partir do banco de dados
        if player_manager.load_from_database(user_id = user_id):
            # Tenta carregar o jogador alvo
            if player_manager.load_user(user = str.lower(user_alvo)):
                dados_ninho = player_manager.get_player().get_ninho_por_user(user_alvo = user_alvo)
                
                try:
                    player_manager.get_player().teleportar_user(user_alvo = dados_ninho["id_alderon_user"])

                except ConnectionRefusedError:
                    await interaction.response.send_message("O usuário requisitado não é registrado!")

            # Se o usuário alvo não existe na base
            else:
                await interaction.response.send_message("O usuário requisitado não é registrado!")

        # Se o usuário não existe na base
        else:
            await interaction.response.send_message("Sem o registro, não é permitido acessar o ninho!")

    # Caso o canal não seja o correto
    else:
        link_ninho = interaction.guild.get_channel(1197591462091706398).mention

        await interaction.response.send_message(f"Comando disponível apenas no canal {link_ninho}")


@tree.command(
    name = "babify",
    description = "Faz com que seu animal atual retorne a etapa de filhote",
    guild = discord.Object(id = 1196189171530870795)
)
async def babify(interaction: discord.Interaction) -> None:
    """
    Retorna o animal atual a etapa de filhote.
    """
    # Verifica se o canal atual é o "ninhos"
    if interaction.channel.name == "ninhos":
        # Pega o ID do usuário no Discord
        user_id = interaction.user.id

        # Tenta carregar o usuário a partir do banco de dados
        if player_manager.load_from_database(user_id = user_id):
            # Tenta realizar o processo de "babify"
            try:
                player_manager.get_player().babify_jogador()

            except ConnectionRefusedError:
                await interaction.response.send_message("Você deve estar online no servidor!")

        # Se o usuário não existe na base
        else:
            await interaction.response.send_message("Sem o registro, não é permitido acessar o ninho!")

    # Caso o canal não seja o correto
    else:
        link_ninho = interaction.guild.get_channel(1197591462091706398).mention

        await interaction.response.send_message(f"Comando disponível apenas no canal {link_ninho}")