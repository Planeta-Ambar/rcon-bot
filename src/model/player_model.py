"""
Script de manipulação e conversação com o banco de dados que contém, também, atributos de 
criptografia para a segurança dos dados.
"""
import uuid
import binascii
from typing import Any

from Crypto.Cipher import AES

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import Comparator, hybrid_property
from sqlalchemy import create_engine, Column, Float, Integer, JSON, String

# Configurações do banco de dados
engine = create_engine('sqlite:///src/data/planeta-ambar.db', echo=True)
Base = declarative_base()
Session = sessionmaker(bind = engine)
session = Session()

# Chave randômica de encripção
key = uuid.uuid4().bytes

# Define a chave como a mesma para os critérios de WHERE
nonce = uuid.uuid4().bytes


def aes_encrypt(data: str) -> Any:
    """
    Encripta os dados fornecidos com o padrão EAX.
    """
    cipher = AES.new(key, AES.MODE_EAX, nonce = nonce)
    data = data + (" " * (16 - (len(data) % 16)))

    return cipher.encrypt(data.encode("utf-8")).hex()


def aes_decrypt(data: str) -> Any:
    cipher = AES.new(key, AES.MODE_EAX, nonce = nonce)
    
    return cipher.decrypt(binascii.unhexlify(data)).decode("utf-8").rstrip()


class PlayerTb(Base):
    """
    Classe que possui as configurações da tabela do banco de dados para os jogadores.
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key = True)
    user_discord = Column(String, nullable = False)
    user_alderon = Column(String, nullable = True)
    id_alderon = Column(String(11), nullable = True)
    fragmentos_ambar = Column(Integer, nullable = True)
    dino_atual = Column(String, nullable = True)
    tamanho = Column(Float, nullable = True)
    morte_recente = Column(JSON, nullable = True)
    ninho = Column(JSON, nullable = True)


    @hybrid_property
    def user_id(self) -> Any:
        return aes_decrypt(self.user_discord)


    @user_id.setter
    def user_id(self, value: Any) -> None:
        self.user_discord = aes_encrypt(value)


    class encrypt_comparator(Comparator):
        def operate(self, op, other, **kw):
            return op(
                self.__clause_element__(), aes_encrypt(other),
                **kw
            )

    @user_id.comparator
    def user_id(cls):
        return cls.encrypt_comparator(
            cls.id
        )


    @hybrid_property
    def user_discord_value(self) -> Any:
        return aes_decrypt(self.user_discord)


    @user_discord_value.setter
    def user_discord_value(self, value: Any) -> None:
        self.user_discord = aes_encrypt(value)


    class encrypt_comparator(Comparator):
        def operate(self, op, other, **kw):
            return op(
                self.__clause_element__(), aes_encrypt(other),
                **kw
            )

    @user_discord_value.comparator
    def user_discord_value(cls):
        return cls.encrypt_comparator(
            cls.user_discord
        )
    
    @hybrid_property
    def user_alderon_value(self) -> Any:
        return aes_decrypt(self.user_alderon)


    @user_alderon_value.setter
    def user_alderon_value(self, value: Any) -> None:
        self.user_discord = aes_encrypt(value)


    class encrypt_comparator(Comparator):
        def operate(self, op, other, **kw) -> Any:
            return op(
                self.__clause_element__(), aes_encrypt(other),
                **kw
            )


    @user_alderon_value.comparator
    def user_alderon_value(cls):
        return cls.encrypt_comparator(
            cls.user_alderon
        )
    

    @hybrid_property
    def id_alderon_value(self) -> Any:
        return aes_decrypt(self.id_alderon)


    @id_alderon_value.setter
    def id_alderon_value(self, value: Any) -> None:
        self.user_discord = aes_encrypt(value)


    class encrypt_comparator(Comparator):
        def operate(self, op, other, **kw) -> Any:
            return op(
                self.__clause_element__(), aes_encrypt(other),
                **kw
            )


    @id_alderon_value.comparator
    def id_alderon_value(cls):
        return cls.encrypt_comparator(
            cls.id_alderon
        )
    

# Para criar a tabela
Base.metadata.create_all(engine)