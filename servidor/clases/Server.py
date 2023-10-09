from dataclasses import dataclass, field
from clases.Player import Player
from clases.Board import Board
from clases.Match import Match
from clases.Bot import Bot
from clases.Coordinates import Coordinates
from clases.utils import get_player
import socket, threading

@dataclass
class Server:
    """
    Clase servidor\n
    """
    server_ip: str = "127.0.0.1"
    server_port: int = 20001
    buffersize: int = 1024
    active_games: list[Match] = field(default_factory=list[Match])
    online_players: list[Player] = field(default_factory=list[Player])
    list_of_actions= ["a", "b", "c", "d", "l", "s"]
    inactivity_timeout: int = 3

    def start_inactivity_timer(self, player):
        player.inactivity_timer = threading.Timer(self.inactivity_timeout, self.disconnect_player_due_to_inactivity, args=(player,))
        player.inactivity_timer.start()

    def reset_inactivity_timer(self, player):
        if player.inactivity_timer:
            player.inactivity_timer.cancel()
        self.start_inactivity_timer(player)

    def disconnect_player_due_to_inactivity(self, player):
        self.online_players.remove(player)
        print(f"Jugador {player.player_id} desconectado debido a inactividad.")
        #TODO. Si se desconecta en partida el otro jugador gana y pasa a conectado (0)

    def start_server(self):
        udp_server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        udp_server_socket.bind((self.server_ip, self.server_port))
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
            if action == "a":
                return CON_TUPLE
            if action == "b":
                return CON_TUPLE
            if action == "d":
                return CON_TUPLE
        else:
            return NEG_TUPLE
        return CON_TUPLE
    
    def connect_player(self, client_address: tuple) -> bool:
        print(self.online_players)
        player_id = f"{client_address[0]}:{str(client_address[1])}"
        new_player = Player(player_id=player_id, remaining_lives=6, ships=[])
        if not new_player in self.online_players:
            new_player.update_status(1)
            self.online_players.append(new_player)
            self.start_inactivity_timer(new_player)
            return True
        else:
            print(f"Puerto (id): {player_id}, ya se encuentra conectado")
            return False

    def select_match(self, client_address: tuple, msg: dict)-> bool:
        player_id = f"{client_address[0]}:{str(client_address[1])}"
        player, index = get_player(self.online_players, player_id)
        # Si el jugador esta conectado, pero no ha seleccionado tipo de partida
        if player.status == 1:
            if(msg["bot"] == 0): # PvP
                player.update_status(2)
                player.select_match_type(0)
                self.online_players[index] = player
                return True
            elif (msg["bot"] == 1): # PvP
                player.update_status(2)
                player.select_match_type(1)
                self.online_players[index] = player
                #TODO. iniciar partida contra bot...
                return True
            else:
                return False
        return True

    def build_ships(self, client_address: tuple, msg: dict) -> bool:
        ships_in = msg['ships']
        player_id = f"{client_address[0]}:{str(client_address[1])}"
        player, index = get_player(self.online_players, player_id)
        temp_board = Board()
        new_board = temp_board.make_ships(ships_in)
        if not new_board:
            return False
        else:
            player.ships = temp_board.ships
            self.online_players[index] = player
            player.update_status(3)
            return True

    def attack(self, match: Match, coor: Coordinates | None) -> bool:
        # Ataca player 1
        if match.current_turn.player_id == match.player_1.player_id:
            match.switch_turn()
            ships = match.player_2.ships
            for ship in ships:
                if coor in ship.list_coordinates:
                    match.player_2.remaining_lives -=1
                    print(f"Jugador acerto en: {coor}")
                    return True
            return False

        # Ataca Bot
        elif match.current_turn.player_id == match.player_2.player_id and isinstance(match.player_2, Bot):
            match.switch_turn()
            coor = match.player_2.get_random_attack_coordinates()
            ships = match.player_1.ships
            for ship in ships:
                if coor in ship.list_coordinates:
                    match.player_1.remaining_lives -=1
                    print(f"Bot acerto en: {coor}")
                    return True
            print(f"Bot no acerto en: {coor}")
            return False
        else:
            print(f"Algo salio mal -> class Server: linea 118")
            return False
    
    def disconnect_player(self, client_address: tuple) -> bool:
        player_id = f"{client_address[0]}:{str(client_address[1])}"
        player_to_disconnect, index = get_player(self.online_players, player_id)
        if player_to_disconnect is not None:
            if player_to_disconnect in self.online_players:
                self.online_players.remove(player_to_disconnect)
                print(f"Se ha desconectado (id):\t{player_id}")
                return True
            else:
                return False
        else:
            print(f"Puerto (id): {player_id}, no se encuentra conectado")
            return False
