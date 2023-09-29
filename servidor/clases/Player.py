from dataclasses import dataclass, field

@dataclass
class Player:
    """Clase que define al Jugador"""
    player_id: int = None
    ships: list = field(default_factory=list)
    remaining_lives: int = 6
    board: list = field(default_factory=list)
    # Falta agregar cosas

    def show_player(self):
        return self.player_id, self.ships, self.remaining_lives, self.board
    