from dataclasses import dataclass, field
from clases.Board import Board

@dataclass
class Player:
    """Clase que define al Jugador"""
    current_action: int = 0 # 0: desconectado, 1: conectado
    player_id: int = 0
    ships: list = field(default_factory=list)
    remaining_lives: int = 6
    board: Board = field(default_factory=Board)

    # Falta agregar cosas
    def show_player(self):
        return self.player_id, self.ships, self.remaining_lives, self.board
