"""
Esse arquivo contem a implementação de uma comunicação direta com o jogo para funcionalidades 
relacionadas à criação de ninhos, como:

    1. "Babify" para tornar seu animal atual um filhote;
    2. Teleporte para a localização dos pais do ninho.
"""
import os

from mcrcon import MCRcon
from dotenv import load_dotenv

# Configuração global
load_dotenv()

HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT"))
PASSWORD = os.getenv("PASSWORD")


def babify(id: str) -> float:
    """
    Reduz o estágio de crescimento do animal do jogador para filhote e retorna o valor do 
    crescimento atual.
    """
    with MCRcon(host = HOST, password = PASSWORD, port = PORT) as mcr:
        mcr.command(f"/setattr {id} growth 0")

    return 0.00


def teleportar_para_pais(id: str, id_pai: str) -> None:
    """
    Teleporta o jogador atual para a posição do pai/mãe do ninho.
    """
    with MCRcon(host = HOST, password = PASSWORD, port = PORT) as mcr:
        mcr.command(f"/teleport {id} {id_pai}")
    
