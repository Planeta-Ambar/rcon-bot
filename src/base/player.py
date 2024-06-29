"""
Script de implementação da class player, onde estarão reunidos os principais atributos dos 
mesmos no servidor, como:

    1. User;
    2. User da Alderon;
    3. ID da Alderon;
    4. Fragmentos de Âmbar;
    5. Dinossauro atual;
    6. Dados sobre a morte mais recente.

Além disso, uma conexão será criada e mantida com o banco de dados para a manipulação dos dados 
dos usuários.
"""
from typing import Any, Dict

from src.model.player_model import Base, PlayerTb, session
from src.base.ninho import babify, teleportar_para_pais
from src.base.carteira import get_marks_deposito, transferir_marks


class Player:
    """
    Classe que possui os atributos do jogador e que "conversará" com o modelo que 
    representa o banco de dados.
    """
    _user_id: int = 0
    _user: str = ""
    _id_alderon: str = None
    _user_alderon: str = None
    _fragmentos_ambar: int = 0
    _dino_atual: str = None
    _tamanho: float = None
    _morte_recente: Dict = None
    _ninho: dict = None


    def __init__(self) -> None:
        pass


    def set_user_id(self, user_id: int) -> None:
        """
        Define o ID do usuário do Discord.
        """
        self._user_id = int(user_id)


    def set_user(self, user: str) -> None:
        """
        Define o username do usuário do Discord.
        """
        self._user = user

        self._player = PlayerTb(id = self._user_id, user_discord = self._user)


    def existe(self) -> Any | None:
        """
        Verifica se o usuário já existe na tabela "users".
        """
        return session.query(PlayerTb).filter_by(id = self._user_id).first()


    def set_id_alderon(self, id_alderon: str) -> None:
        """
        Define o ID da Alderon Games do jogador.
        """
        self._id_alderon = id_alderon

        _id_to_update = session.query(PlayerTb).filter_by(id = self._user_id).first()
        _id_to_update.id_alderon = self._id_alderon

        session.commit()


    def set_user_alderon(self, user_alderon: str) -> None:
        """
        Define o nome de usuário da Alderon Games do jogador.
        """
        self._user_alderon = user_alderon

        _id_to_update = session.query(PlayerTb).filter_by(id = self._user_id).first()
        _id_to_update.user_alderon = self._user_alderon

        session.commit()


    def depositar_marks(self, qtd: int) -> None:
        """
        Deposita a quantia especificada de marks na carteira como Fragmentos de Âmbar. 
        """
        marks_adq = get_marks_deposito(self._id_alderon, qtd)
        _id_to_update = session.query(PlayerTb).filter_by(id = self._user_id).first()

        if not _id_to_update.fragmentos_ambar:
            _id_to_update.fragmentos_ambar = 0

        if marks_adq > 0:
            self._fragmentos_ambar += marks_adq

            _id_to_update.fragmentos_ambar = self._fragmentos_ambar

        session.commit()


    def depositar_marks_player(self, qtd: int, user: str) -> None:
        """
        Deposita a quantia especificada de marks na carteira de um jogador como Fragmentos de Âmbar (comando para admins). 
        """
        _id_to_update = session.query(PlayerTb).filter_by(user_discord = user).first()

        if not _id_to_update.fragmentos_ambar:
            _id_to_update.fragmentos_ambar = 0

        self._fragmentos_ambar += qtd

        _id_to_update.fragmentos_ambar = self._fragmentos_ambar

        session.commit()


    def transferir_fragmentos(self, qtd: int) -> None:
        """
        Transfere a quantia especificada de Fragmentos de Âmbar na carteira como marks.  
        """
        transferir_marks(self._id_alderon, qtd)

        self._fragmentos_ambar -= qtd
        _id_to_update = session.query(PlayerTb).filter_by(id = self._user_id).first()
        _id_to_update.fragmentos_ambar -= qtd

        session.commit()


    def set_fragmentos_ambar(self, fragmentos_ambar: int) -> None:
        """
        Define a quantidade atual de Fragmentos de Âmbar.
        """
        self._fragmentos_ambar = fragmentos_ambar


    def set_dino_atual(self, dino_atual: str) -> None:
        """
        Define o dinossauro atual do jogador.
        """
        self._dino_atual = dino_atual
        

    def set_tamanho(self, tamanho: float) -> None:
        """
        Define o tamanho do dinossauro atual do jogador.
        """
        self._tamanho = tamanho


    def salvar_morte_recente(self, morte_recente: Dict) -> None:
        """
        Define o dinossauro atual do jogador.
        """
        self._morte_recente = morte_recente
        
        _id_to_update = session.query(PlayerTb).filter_by(id = self._user_id).first()
        _id_to_update.morte_recente = self._morte_recente

        session.commit()


    def set_ninho(
        self, 
        id_ninho: str, 
        user: str,
        id_alderon_user: str,
        parceiro: str, 
        id_alderon_parceiro: str, 
        desc: str,
        animal: str, 
        filhotes: list,
        id_alderon_filhotes: list,
        qtd_ovos: int
    ) -> None:
        """
        Define o ninho atual do jogador.
        """
        self._ninho = {
            "id_ninho": id_ninho,
            "user": user,
            "id_alderon_user": id_alderon_user,
            "parceiro": None if parceiro is None else parceiro,
            "id_alderon_parceiro": id_alderon_parceiro if id_alderon_parceiro else None,
            "desc": desc,
            "animal": animal,
            "filhotes": filhotes if filhotes else [],
            "id_alderon_filhotes": id_alderon_filhotes if id_alderon_filhotes else [],
            "qtd_ovos": qtd_ovos
        }
        
        _id_to_update = session.query(PlayerTb).filter_by(id = self._user_id).first()
        _id_to_update.ninho = self._ninho

        session.commit()


    def get_fragmentos_ambar(self) -> int:
        """
        Retorna a quantidade atual de Fragmentos de Âmbar que o jogador possui.
        """
        return self._fragmentos_ambar


    def inventario(self) -> str:
        """
        Retorna o inventário atual do jogador.
        """
        return f"Você possui {self.get_fragmentos_ambar()} Fragmentos de Âmbar"


    def get_player(self) -> Base: # type: ignore
        """
        Retorna o objeto da classe "PlayerTb".
        """
        return self._player
    
    
    def get_user(self) -> str:
        """
        Retorna o nome de usuário do jogador no Discord.
        """
        return self._user
    

    def get_user_alderon(self) -> str:
        """
        Retorna o nome de usuário do jogador da Alderon Games.
        """
        return self._user_alderon


    def get_id_alderon(self) -> str:
        """
        Retorna o ID do jogador na Alderon Games.
        """
        return self._id_alderon
    

    def get_dino_atual(self) -> str:
        """
        Retorna o dinossauro atual utilizado pelo jogador.
        """
        return self._dino_atual
    

    def get_morte_recente(self) -> Dict:
        """
        Retorna as informações sobre a morte mais recente do jogador.
        """
        return self._morte_recente
    

    def get_ninho(self) -> dict:
        """
        Retorna informações associadas ao ninho do jogador.
        """
        return {
            "id_ninho": self._ninho["id_ninho"],
            "user": self._user,
            "id_alderon_user": self._id_alderon,
            "parceiro": self._ninho["parceiro"],
            "id_alderon_parceiro": self._ninho["id_alderon_parceiro"],
            "desc": self._ninho["desc"],
            "animal": self._ninho["animal_ninho"],
            "filhotes": self._ninho["filhotes"],
            "id_alderon_filhotes": self._ninho["id_alderon_filhotes"],
            "qtd_ovos": self._ninho["qtd_ovos"]
        }
    

    def get_ninho_por_user(self, user_alvo: str) -> dict:
        """
        Retorna informações associadas ao ninho de um jogador em específico.
        """
        player_data = session.query(PlayerTb).filter_by(user_discord = user_alvo).first()

        if player_data:
            return player_data.ninho
        

    def teleportar_user(self, id_alvo: str) -> None:
        """
        Teleporta o usuário até a posição de outro.
        """
        teleportar_para_pais(self._id_alderon, id_alvo)


    def babify_jogador(self) -> None:
        """
        Retorna o animal do jogador a etapa de filhote.
        """
        self.set_tamanho(0.0)

        _id_to_update = session.query(PlayerTb).filter_by(id = self._user_id).first()
        _id_to_update.tamanho = babify(id = self._id_alderon)

        session.commit()


class PlayerManager:
    """
    Classe que gerencia a criação e carregamento de jogadores no sistema.
    """
    def __init__(self) -> None:
        self.player = None


    def create_player(self, user_id, username) -> None:
        """
        Cria um novo jogador com as informações iniciais fornecidas.
        """
        self.player = Player()

        self.player.set_user_id(user_id)
        self.player.set_user(username)
        

    def get_player(self) -> Player:
        """
        Retorna um jogador previamente criado.
        """
        return self.player


    def load_from_database(self, user_id) -> bool:
        """
        Carrega um jogador do banco de dados se ele existir.
        """
        player_data = session.query(PlayerTb).filter_by(id = user_id).first()

        if player_data:
            self.create_player(player_data.id, player_data.user_discord)
            self.player.set_id_alderon(player_data.id_alderon)

            if player_data.fragmentos_ambar:
                self.player.set_fragmentos_ambar(player_data.fragmentos_ambar)
            
            if player_data.dino_atual:
                self.player.set_dino_atual(player_data.dino_atual)

            if player_data.tamanho:
                self.player.set_tamanho(player_data.tamanho)

            if player_data.morte_recente:
                self.player.salvar_morte_recente(player_data.morte_recente)
            
            return True
        
        return False
    

    def load_user(self, user) -> bool:
        """
        Carrega um jogador do banco de dados pelo seu username do Discord se ele existir.
        """
        player_data = session.query(PlayerTb).filter_by(user_discord = user).first()

        if player_data:
            return True
        
        return False