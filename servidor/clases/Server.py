from dataclasses import dataclass, field
from clases.Player import Player
from clases.Board import Board
from clases.Ship import Ship
from clases.Coordinates import Coordinates
import socket

def get_player(online_players: list[Player], player_id: int) -> tuple[Player, int]:
    player_index = -1
    player_out = Player()
    for index, player in enumerate(online_players):
        if (player.player_id == player_id):
            player_out = player
            player_index = index
            break
    return (player_out, player_index)

@dataclass
class Server:
    """
    Clase servidor\n
    """
    server_ip: str = "127.0.0.1"
    server_port: int = 20002
    buffersize: int = 1024
    used_ports: dict = field(default_factory=dict) # Registro de jugadores que no estan con estado conectado (0)
    active_games: list = field(default_factory=list) # lista de triuplas (id_game, id_user1, id_user2)
    online_players: list = field(default_factory=list) # Jugadores conectados
    list_of_actions = ["a", "b", "c", "d", "l", "s"]

    def start_server(self):
        udp_server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        udp_server_socket.bind((self.server_ip, self.server_port))
        self.used_ports.update({self.server_port: True})
        return udp_server_socket

    def validate_action(self, msg) -> tuple[bool, str]:
        action = msg["action"]
        CON_TUPLE = (True, action)
        NEG_TUPLE = (False, action)
        if (action.lower() in self.list_of_actions):
            if action == "c":
                return CON_TUPLE
            if action == "s":
                return CON_TUPLE
            if action == "b":
                return CON_TUPLE
            if action == "d":
                return CON_TUPLE
        else:
            return NEG_TUPLE
        return CON_TUPLE
    
    def connect_player(self, client_address: tuple) -> bool:
        player_id = client_address[1]
        # no TODO. Cambiar a if player.status = 0
        # pq se crea el jugador una vez conectado
        # entonces primero se asocia el puerto
        if not self.used_ports.get(player_id):
            self.used_ports.update({player_id: True})
            board = Board()
            ### Se agrega al servidor un jugador con estado conectado
            player = Player(status=1, player_id=player_id, remaining_lives=6, ships=[])
            self.online_players.append(player)
            return True
        else:
            print(f"Puerto (id): {player_id}, ya se encuentra conectado")
            return False

    def select_match(self, client_address: tuple, msg: dict)-> bool:
        player_id = client_address[1]
        player, index = get_player(self.online_players, player_id)
        # Si el jugador esta conectado, pero no ha seleccionado tipo de partida
        if player.status == 1:
            if(msg["bot"] == 0): # PvP
                player.update_status(2)
                player.select_match_type(0)
                self.online_players[index] = player
                return True
            elif (msg["bot"] == 1): # Contra bot
                player.update_status(2)
                player.select_match_type(1)
                self.online_players[index] = player
                return True
            else:
                return False
        return False

    def build_ships(self, client_address: tuple, msg: dict) -> bool:
        ships_in = msg['ships'] # [x, y, orientacion]
        player_out, player_idx = get_player(self.online_players, client_address[1])
        temp_board = Board()
        new_board = temp_board.make_ships(ships_in)
        
        if not new_board:
            return False
        else:
            player_out.ships = temp_board.ships
            self.online_players[player_idx] = player_out
            print(player_out)
            return True

    def disconnect_player(self, client_address: tuple) -> bool:
        player_id = client_address[1]
        player_to_disconnect, _ = get_player(self.online_players, player_id)
        if player_to_disconnect is not None:
            self.used_ports.update({player_id: False})
            if player_to_disconnect in self.online_players:
                self.online_players.remove(player_to_disconnect)
                print(f"Se ha desconectado (id):\t{player_id}")
                return True
            else:
                return False
        else:
            print(f"Puerto (id): {player_id}, no se encuentra conectado")
            return False
