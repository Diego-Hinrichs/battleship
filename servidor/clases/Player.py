from dataclasses import dataclass, field
from clases.Board import Board

@dataclass
class Player:
    """Clase que define al Jugador"""
    status: int = 0 # 0: Desconectado. 1: Conectado. 2: Eligió modo de juego. 3: Puso barcos. 4: Esta jugando
    player_id: int = 0 
    ships: list = field(default_factory=list)
    remaining_lives: int = 6
    board: Board = field(default_factory=Board)

    def update_status(self, new_status):
        self.status = new_status
        return self
    
    # Falta agregar cosas
    def show_player(self):
        return self.player_id, self.ships, self.remaining_lives, self.board
