from dataclasses import dataclass, field
from clases.Player import Player
from clases.Board import Board
import socket

def get_player_from_list(list: list, player_id: int) -> Player:
    player_out = Player()
    for player in list:
        if (player.player_id == player_id):
            player_out = player
            break
    return player_out

@dataclass
class Server:
    """
    Clase servidor\n
    Para poder abrir el server cambiar, server_ip a IPv4\n
    !ip addr show | grep 'inet ' | grep -v '127.0.0.1' | awk '{print $2}' | cut -d'/' -f1
    """
    server_ip: str = "127.0.0.1"
    server_port: int = 20002
    buffersize: int = 1024
    used_ports: dict = field(default_factory=dict) # Registro de jugadores que no estan con estado conectado
    active_games: list = field(default_factory=list) # lista de triuplas (id_game, id_user1, id_user2)
    online_players: list = field(default_factory=list) # Jugadores conectados
    list_of_actions = ["a", "b", "c", "d", "l", "s"]
    
    #TODO. En caso de lose se van dropeados de aqui, pero permanecen conectados
    playing_against_bots: list = field(default_factory=list) # Jugadores que jugaran vs bots
    
    #TODO. En caso de lose se van dropeados de aqui, pero permanecen conectados
    playing_against_players: list = field(default_factory=list) # Jugadores en PvP

    def start_server(self):
        udp_server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        udp_server_socket.bind((self.server_ip, self.server_port))
        self.used_ports.update({self.server_port: True})
        return udp_server_socket

    def validate_action(self, msg) -> tuple[bool, str]:
        action = msg["action"]
        print(action)
        if (action in self.list_of_actions):
            if action == "c":
                return (True, action)
            if action == "s":
                return (True, action)
            if action == "d":
                return (True, action)
        else:
            return (False, action)
        return (True, action)
    
    def connect_player(self, client_address) -> bool:
        player_id = client_address[1]
        if not self.used_ports.get(player_id):
            self.used_ports.update({player_id: True})
            board = Board()
            ### Se agrega al servidor un jugador con estado conectado
            player = Player(status=1, player_id=player_id, ships=[], remaining_lives=6, board=board)
            print(f"Se ha conectado (id):\t{player_id}")
            self.online_players.append(player)
            return True
        else:
            print(f"Puerto (id): {player_id}, ya se encuentra conectado")
            return False

    # Ojito aqui, que voy creando players x la vida, me voy a quedar sin memoria
    # Controlar la seleccion
    # Dps de selecionar la primera vez, no deberia dejar cambiar
    def select_match(self, client_address, msg)-> bool:
        player_id = client_address[1]
        player = Player()
        player = get_player_from_list(self.online_players, player_id)
        valid = msg["bot"] in [1, 0]
        if(valid and 1):
            player.update_status(2)
            self.playing_against_bots.append(player)
        elif valid:
            player.update_status(2)
            self.playing_against_players.append(player)
        else:
            return False
        return True

    def disconnect_player(self, client_address) -> bool:
        player_id = client_address[1]
        player_to_disconnect = get_player_from_list(self.online_players, player_id)
        print(player_to_disconnect)
        if player_to_disconnect is not None:
            self.used_ports.update({player_id: False})
            self.online_players.remove(player_to_disconnect)
            print(f"Se ha desconectado (id):\t{player_id}")
            return True
        else:
            print(f"Puerto (id): {player_id}, no se encuentra conectado")
            return False
