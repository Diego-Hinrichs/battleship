from dataclasses import dataclass, field
from clases.Player import Player
from clases.Board import Board
from clases.Game import Game
from clases.Bot import Bot
from clases.Coordinates import Coordinates
from clases.utils import get_player
from dotenv import load_dotenv
import socket, os

load_dotenv(dotenv_path="../.env")
SERVER_LOCAL = os.getenv("SERVER_LOCAL")
SERVER_UNIVERSIDAD = os.getenv("SERVER_UNIVERSIDAD")
SERVER_PORT = os.getenv("SERVER_PORT")

# TODO. DEFINIR CUANTAS PARTIDAS PODRA JUGAR UN UNICO CLIENTE EN SIMULTANEO
# Se realiza con IP:PORT
@dataclass
class Server:
    server_ip: str | None
    server_port: str | None
    buffersize: int
    active_games: list[Game] = field(default_factory=list[Game])
    online_players: list[Player] = field(default_factory=list[Player])
    
    def __init__(self):
        self.server_ip = SERVER_LOCAL
        self.server_port = SERVER_PORT
        self.buffersize = 1024
        self.active_games = []
        self.online_players = []
        self.list_of_actions = ["a", "b", "c", "d", "t", "w", "l", "s"]
    
    def start_new_game_pvp(self, player: Player):
        for player_1 in self.online_players:
            if player_1.game_type == 1 or player_1.status == 4:
                continue
            if player_1.game_type == 0 and player_1 != player and player_1.status == 3:
                player.update_status(4)
                player_1.update_status(4)
                game = Game(game_id=f"{player.player_id}_{player_1.player_id}", game_type=0, player_1=player_1, player_2=player, current_turn=player_1.player_id)
                self.active_games.append(game)
                print(f"Se ha creado una partida:\nPlayer 1: {player_1.player_id}\nPlayer 2: {player.player_id}")
            else:
                print(f"No hay jugadores esperando partida")

    def start_new_game_pvb(self, player: Player):
        if player.status == 3:
            bot = Bot()
            bot.build_random_ship()
            game = Game(game_id=player.player_id, player_1=player, player_2=bot, current_turn=player.player_id)
            self.active_games.append(game)
            player.update_status(4)

    def start_server(self):
        udp_server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        udp_server_socket.bind((self.server_ip, int(self.server_port))) # type: ignore
        return udp_server_socket

    def validate_action(self, msg) -> tuple[bool, str]:
        action = msg["action"]
        if (action.lower() in self.list_of_actions):
            return (True, action)
        else:
            return (False, action)
        
    def connect_player(self, client_address: tuple) -> bool:
        player_id = f"{client_address[0]}:{str(client_address[1])}"
        
        # Verificar si el jugador ya está conectado
        for player in self.online_players:
            if player.player_id == player_id:
                print(f"Jugador {player_id} ya se encuentra conectado")
                return False

        # Si el jugador no está en línea, crear un nuevo jugador y agregarlo
        new_player = Player(player_id=player_id, remaining_lives=6, ships=[])
        new_player.update_status(1)
        self.online_players.append(new_player)
        print(f"El jugador {player_id} se ha conectado")
        return True

    #TODO. control de partidas simultaneas x usuario

    def select_game(self, client_address: tuple, msg: dict)-> bool:
        player: Player
        player, index = get_player(self.online_players, client_address)
        if player.status == 1:
            if(msg["bot"] == 0): # PvP
                player.select_game_type(0).update_status(2)
                self.online_players[index] = player
                return True
            elif (msg["bot"] == 1): # PvP
                player.select_game_type(1).update_status(2)
                self.online_players[index] = player
                return True
            else:
                return False
        else:
            return False

    def build_ships(self, client_address: tuple, msg: dict) -> bool:
        ships_in = msg['ships']
        if len(ships_in) == 0: 
            return False
        player, index = get_player(self.online_players, client_address)
        temp_board = Board()
        new_board = temp_board.make_ships(ships_in) # Overlap, fuera de rango y demases
        if not new_board:
            return False
        else:
            player.ships = temp_board.ships
            self.online_players[index] = player
            player.update_status(3)
            return True

    def user_attack(self, game: Game, coor: Coordinates) -> bool:
        if game.current_turn == game.player_1.player_id:
            game.switch_turn()
            ships = game.player_2.ships
            for ship in ships:
                if coor in ship.list_coordinates:
                    ship.list_coordinates.remove(coor)
                    game.player_2.remaining_lives -=1
                    print(f"Jugador {game.player_1.player_id} acertó en: {coor}")
                    return True
            return False
        
        elif game.current_turn == game.player_2.player_id:
            game.switch_turn()
            ships = game.player_1.ships
            for ship in ships:
                if coor in ship.list_coordinates:
                    ship.list_coordinates.remove(coor)
                    game.player_1.remaining_lives -=1
                    print(f"Jugador {game.player_2.player_id} acertó en: {coor}\n")
                    return True
            return False
        else:
            return False

    def bot_attack(self, game: Game, coor: Coordinates | None) -> bool:
        if game.current_turn == game.player_2.player_id and isinstance(game.player_2, Bot):
            game.switch_turn()
            coor = game.player_2.get_random_attack_coordinates()
            ships = game.player_1.ships
            for ship in ships:
                if coor in ship.list_coordinates:
                    game.player_1.remaining_lives -=1
                    print(f"Bot acertó en: {coor}")
                    return True
            return False
        else:
            return False
    
    def disconnect_player(self, client_address: tuple) -> bool:
        player, index = get_player(self.online_players, client_address)
        if player in self.online_players:
            self.online_players.remove(player)
            print(f"\nSe ha desconectado (id):\t{player.player_id}")
            return True
        else:
            print(f"\nJugador: {client_address}, no se encuentra conectado")
            return False
