from dataclasses import dataclass, field
from clases.Board import Board
from clases.Ship import Ship

@dataclass
class Player:
    """Clase Jugador\n
    Status:
    0: Desconectado
    1: Conectado
    2: Eligio modo de juego
    3: Puso barcos
    4: Esta jugando\n
    Match_type:
    1: PvB
    0: PvP
    """
    status: int = 0 
    match_type: int = 1 # 1: PvB, 0: PvP
    player_id: str = "" 
    remaining_lives: int = 6
    ships: list[Ship] = field(default_factory=list[Ship])

    def update_status(self, new_status):
        self.status = new_status
        return self
    
    def select_match_type(self, match_type):
        self.match_type = match_type
        return self

    def __str__(self) -> str:
        return f"{'Jugador:':<17}{self.player_id}\n" \
            f"{'Status:':<17}{self.status}\n" \
            f"{'Tipo de partida:':<17}{'Player vs Bot' if self.match_type else 'Player vs Player'}\n" \
            f"{'Vidas:':<17}{self.remaining_lives}\n" \
            f"{'Board:':<17}{self.ships}\n"
