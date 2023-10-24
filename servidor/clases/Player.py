from dataclasses import dataclass, field
from clases.Ship import Ship

class Player:
    status: int
    game_type: int
    player_id: str
    ships: list[Ship]
    remaining_lives: int

    def __init__(self, status = 0, game_type = 0, player_id = "", ships = {}, remaining_lives = 6):
        self.status = status # 0: Desconectado; 1: Conectado; 2: Eligió modo de juego; 3: Puso barcos; 4: En partida -> Si pierde pasa a 0: Desconectado
        self.game_type = game_type
        self.player_id = player_id
        self.ships = ships
        self.remaining_lives = remaining_lives

    def update_status(self, new_status):
        self.status = new_status
        return self
    
    def select_game_type(self, game_type):
        self.game_type = game_type
        return self
    
    def __str__(self):
        game_type = 'Player vs Bot' if self.game_type == 1 else 'Player vs Player'
        player_str = f"============== Jugador {self.player_id} ==============\n"
        player_str += f"Tipo de partida: {game_type}\n"
        player_str += f"Estado: {self.status}\n"
        player_str += f"Vidas restantes: {self.remaining_lives}\n"
        return player_str


