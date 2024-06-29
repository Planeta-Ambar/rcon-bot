"""
Esse arquivo contem a implementação de funcionalidades relacionadas à comunicação da carteira de jogadores do 
Planeta Âmbar com o jogo, como:

    1. Aquisição da quantia informada de marks do dinossauro em jogo para depósito como Fragmentos de Âmbar;
    2. Transferência de Fragmentos de Âmbar para o dinossauro em jogo como marks.
"""
import os
import re 
from typing import Any, List

from mcrcon import MCRcon
from dotenv import load_dotenv

# Configuração global
load_dotenv()

HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT"))
PASSWORD = os.getenv("PASSWORD")


def get_lista(cmd_output: str) -> List[Any]:
    """
    Função de utilidade que retorna uma lista contendo os valores numéricos do  
    output de um comando no game.
    """
    nums = re.findall("\d+", cmd_output)

    return nums


def get_qtd_atual_marks(id: str) -> int:
    """
    Retorna a quantidade atual de marks que o jogador possui.
    """
    with MCRcon(host = HOST, password = PASSWORD, port = PORT) as mcr:
        mcr.command(f"/addmarks {id} 1")
        
        resp = mcr.command(f"/removemarks {id} 1")

    output = get_lista(resp)
    atual = int(output[-1])

    return atual


def get_marks_deposito(id: str, qtd: int) -> int:
    """
    Deposita a quantidade informada de marks como Fragmentos de Âmbar. Caso 
    o jogador tenha menos marks do que o informado, o total disponível será 
    depositado em sua conta.
    """
    with MCRcon(host = HOST, password = PASSWORD, port = PORT) as mcr:
        resp = mcr.command(f"/removemarks {id} {qtd}")

    vals = get_lista(resp)
    marks_atuais = get_qtd_atual_marks(id)
    val_para_deposito = int(vals[3])

    if val_para_deposito <= marks_atuais:
        return val_para_deposito
    
    else:
        return 0
    

def transferir_marks(id: str, qtd: int) -> int:
    """
    Transfere a quantidade informada de Fragmentos de Âmbar como marks. Caso 
    o jogador tenha menos Fragmentos de Âmbar do que o informado, o total de disponível
    será depositado em sua conta. 
    """
    with MCRcon(host = HOST, password = PASSWORD, port = PORT) as mcr:
        resp = mcr.command(f"/addmarks {id} {qtd}")

    lst_valores = get_lista(resp)
    val_transferido = int(lst_valores[0])

    return val_transferido