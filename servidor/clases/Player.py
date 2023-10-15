from dataclasses import dataclass, field
from clases.Ship import Ship

@dataclass
class Player:
    status: int = 0  # 0: Desconectado; 1: Conectado; 2: Eligió modo de juego; 3: Puso barcos; 4: En partida -> Si pierde pasa a 0: Desconectado
    game_type: int = 1 # 1: PvB, 0: PvP
    player_id: str = "" 
    remaining_lives: int = 6
    ships: list[Ship] = field(default_factory=list[Ship])

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


