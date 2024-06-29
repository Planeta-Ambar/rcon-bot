"""
Script que contem todas as funções relacionadas à carteira dos jogadores no Discord.
"""
import discord
from discord.ext import commands

from src.base.config import tree
from src.base.player import PlayerManager

# Instanciando o objeto PlayerManager
player_manager = PlayerManager()


def realizar_deposito(marks: int) -> str:
    """
    Verifica a quantidade inicial de Fragmentos de Âmbar que o usuário possui. Após isso, a quantidade atual de 
    Fragmentos de Âmbar (após o depósito) é adquirida. Por fim, há o cálculo da diferença entre os valores para saber 
    se o usuário tinha marks suficientes para o depósito.
    """
    qtd_inicial = player_manager.get_player().get_fragmentos_ambar()

    player_manager.get_player().depositar_marks(marks)

    qtd_atual = player_manager.get_player().get_fragmentos_ambar()
    diff = qtd_atual - qtd_inicial

    if diff > 0:
        output = f"Você depositou {marks} marks ({marks} Fragmento(s) de Âmbar )"

    else:
        output = f"Você não possui marks suficientes"

    return output


def realizar_transferencia(fragmentos_ambar: int) -> str:
    """
    Verifica a quantidade de Fragmentos de Âmbar que o usuário possui e, caso suficiente, realiza a transferência 
    da quantidade indicada como marks.
    """
    fragmentos_disponiveis = player_manager.get_player().get_fragmentos_ambar()

    # Verifica se a quantidade disponível é, pelo menos, igual à quantidade que o usuário quer transferir
    # Isso evita que o usuário tenha, potencialmente, um bug de Fragmentos de Âmbar infinitos
    if fragmentos_disponiveis >= fragmentos_ambar:
        player_manager.get_player().transferir_fragmentos(fragmentos_ambar)

        output = f"Você transferiu {fragmentos_ambar} Fragmento(s) de Âmbar ({fragmentos_ambar} marks) de sua conta"

    else:
        output = f"Você não possui Fragmentos de Âmbar suficientes"

    return output


@tree.command(
    name = "depositar",
    description = "Deposita a quantidade especificada de marks como Fragmentos de Âmbar",
    guild = discord.Object(id = 1196189171530870795)
)
async def depositar(interaction: discord.Interaction, marks: int) -> None:
    """
    Deposita a quantidade fornecida de marks na carteira do usuário como Fragmentos de Âmbar. Há uma série de verificações para 
    que a quantia depositada seja coerente com o que o usuário possui in-game. O usuário deve estar online para que o comando 
    funcione corretamente.
    """
    # Verifica se o usuário não tem privilégios de administrador
    if interaction.user.guild_permissions.administrator == False:
        # Verifica se o canal atual é o "carteira"
        if interaction.channel.name == "carteira":
            # Pega o ID do usuário no Discord
            user_id = interaction.user.id
            
             # Tenta carregar o usuário a partir do banco de dados
            if player_manager.load_from_database(user_id = user_id):
                output = realizar_deposito(marks)

                await interaction.response.send_message(output)

            # Se o usuário não existe na base
            else:
                await interaction.response.send_message("Sem o registro, não é permitido acessar a carteira!")

        # Caso o canal não seja o correto
        else:
            link_carteira = interaction.guild.get_channel(1197595632219721858).mention

            await interaction.response.send_message(f"Comando disponível apenas no canal {link_carteira}")

    # O usuário tem privilégios de administrador
    else:
        # Tenta carregar o usuário a partir do banco de dados
        if player_manager.load_from_database(user_id = user_id):
            output = realizar_deposito(interaction, marks)

            await interaction.response.send_message(output)

        # Se o usuário não existe na base
        else:
            await interaction.response.send_message("Sem o registro, não é permitido acessar a carteira!")


@commands.has_permissions(administrator = True, ban_members = True)
@tree.command(
    name = "depositar_para_user",
    description = "Deposita a quantidade especificada de marks como Fragmentos de Âmbar para um usuário",
    guild = discord.Object(id = 1196189171530870795)
)
async def depositar_para_user(interaction: discord.Interaction, marks: int, user_alvo: str) -> None:
    """
    Deposita a quantidade fornecida de marks na carteira do usuário alvo como Fragmentos de Âmbar. Há uma série de verificações para 
    que a quantia depositada seja coerente com o que o usuário possui in-game. O usuário deve estar online para que o comando 
    funcione corretamente.
    """
    # Pega o ID do usuário no Discord
    user_id = interaction.user.id

    # Tenta carregar o usuário a partir do banco de dados
    if player_manager.load_from_database(user_id = user_id):
        # Tenta carregar o usuário alvo a partir do banco de dados
        if player_manager.load_user(user = user_alvo):
            # Adiciona Fragmentos de Âmbar à carteira do usuário alvo
            player_manager.get_player().depositar_marks_player(marks, user_alvo)
            
            output = f"Você depositou {marks} marks ({marks} Fragmento(s) de Âmbar) para o usuário {user_alvo}"

            await interaction.response.send_message(output)

        else:
            await interaction.response.send_message(f"O usuário {user_alvo} não está cadastrado!")

    # Se o usuário não existe na base
    else:
        await interaction.response.send_message("Sem o registro, não é permitido acessar a carteira!")


@tree.command(
    name = "transferir",
    description = "Transfere a quantidade especificada de Fragmentos de Âmbar como marks",
    guild = discord.Object(id = 1196189171530870795)
)
async def transferir(interaction: discord.Interaction, fragmentos_ambar: int) -> None:
    """
    Transfere a quantidade de Fragmentos de Âmbar especificada pelo usuário como marks. Há a verificação da quantidade de Fragmentos 
    que o usuário possui atualmente, para evitar exploits de marks infinitos por parte dos jogadores e para garantir que a 
    transferência ocorra somente se o usuário possui pelo menos a quantia que especificou em sua carteira.
    """
    # Verifica se o usuário não tem privilégios de administrador
    if interaction.user.guild_permissions.administrator == False:
        # Verifica se o canal atual é o "carteira"
        if interaction.channel.name == "carteira":
            # Pega o ID do usuário no Discord
            user_id = interaction.user.id
            
            # Tenta carregar o usuário a partir do banco de dados
            if player_manager.load_from_database(user_id = user_id):
                output = realizar_transferencia(fragmentos_ambar)

                await interaction.response.send_message(output)

            # Se o usuário não existe na base
            else:
                await interaction.response.send_message("Sem o registro, não é permitido acessar a carteira!")

        # Caso o canal não seja o correto
        else:
            link_carteira = interaction.guild.get_channel(1197595632219721858).mention

            await interaction.response.send_message(f"Comando disponível apenas no canal {link_carteira}")

    # O usuário tem privilégios de administrador
    else:
        # Tenta carregar o usuário a partir do banco de dados
        if player_manager.load_from_database(user_id = user_id):
            output = realizar_transferencia(fragmentos_ambar)

            await interaction.response.send_message(output)

        # Se o usuário não existe na base
        else:
            await interaction.response.send_message("Sem o registro, não é permitido acessar a carteira!")


@tree.command(
    name = "inventario",
    description = "Exibe os itens atuais em seu inventário",
    guild = discord.Object(id = 1196189171530870795)
)
async def inventario(interaction: discord.Interaction) -> None:
    """
    Exibe o inventário atual do jogador, que consiste na quantidade de Fragmentos de Âmbar que o mesmo possui atualmente.
    """
    # Verifica se o usuário não tem privilégios de administrador
    if interaction.user.guild_permissions.administrator == False:
        # Verifica se o canal atual é o "carteira"
        if interaction.channel.name == "carteira":
            # Pega o ID do usuário no Discord
            user_id = interaction.user.id
            
            # Tenta carregar o usuário a partir do banco de dados
            if player_manager.load_from_database(user_id = user_id):
                out = player_manager.get_player().inventario()

                await interaction.response.send_message(out)

            # Se o usuário não existe na base
            else:
                await interaction.response.send_message("Sem o registro, não é permitido acessar a carteira!")

        # Caso o canal não seja o correto
        else:
            link_carteira = interaction.guild.get_channel(1197595632219721858).mention

            await interaction.response.send_message(f"Comando disponível apenas no canal {link_carteira}")

    # O usuário tem privilégios de administrador
    else:
        # Tenta carregar o usuário a partir do banco de dados
        if player_manager.load_from_database(user_id = user_id):
            out = player_manager.get_player().inventario()

            await interaction.response.send_message(out)

        # Se o usuário não existe na base
        else:
            await interaction.response.send_message("Sem o registro, não é permitido acessar a carteira!")