from dataclasses import dataclass, field
from clases.Player import Player
from clases.Board import Board
import socket
import json

@dataclass
class Server:
    """
    Clase servidor\n
    Para poder abrir el server cambiar, server_ip a IPv4\nz
    !ip addr show | grep 'inet ' | grep -v '127.0.0.1' | awk '{print $2}' | cut -d'/' -f1
    """
    server_ip: str = "127.0.0.1"
    server_port: int = 20002
    buffersize: int = 1024
    online_players: list = field(default_factory=list) # Jugadores conectados
    active_games: list = field(default_factory=list) # lista de triuplas (id_game, id_user1, id_user2)
    used_ports: dict = field(default_factory=dict)
    list_of_actions = ["a", "b", "c", "d", "l", "s"]

    def start_server(self):
        udp_server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        udp_server_socket.bind((self.server_ip, self.server_port))
        self.used_ports.update({self.server_port: True})
        return udp_server_socket

    def validate_action(self, recived_msg) -> tuple[bool, str]:
        recived_msg = json.loads(recived_msg)
        action = recived_msg["action"]
        if (action in self.list_of_actions):
            if action == "c":
                return (True, action)
            if action == "d":
                return (True, action)
        else:
            return (False, action)
        return (True, action)
    
    def connect_player(self, client_address) -> bool:
        player_id = client_address[1]
        # Comprobar si el usuario esta en conectado
        if not self.used_ports.get(player_id):
            self.used_ports.update({player_id: True})
            board = Board()
            player = Player(player_id=player_id, ships=[], remaining_lives=6, board=board)
            print(f"Se ha conectado (id):\t{player_id}...\n")
            self.online_players.append(player)
            return True
        else:
            print(f"Puerto (id): {player_id}, ya se encuentra conectado...\n")
            return False

    def select_match(self, client_address)-> bool:
        
        return True

    def disconnect_player(self, client_address) -> bool:
        player_id = client_address[1]
        player_to_disconnect = None 
        for player in self.online_players:
            if (player.player_id == player_id):
                player_to_disconnect = player
                self.used_ports.update({player_id: False})
        if player_to_disconnect is not None:
            self.online_players.remove(player_to_disconnect)
            print(self.online_players)
            print(f"Se ha desconectado (id):\t{player_id}...\n")
            return True
        else:
            print(self.online_players)
            print(f"Puerto (id): {player_id}, no se encuentra conectado\n")
            return False