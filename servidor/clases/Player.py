from dataclasses import dataclass, field
from clases.Board import Board

@dataclass
class Player:
    """Clase que define al Jugador"""
    status: int = 0 # 0: Desconectado; 1: Conectado; 2: Eligió modo de juego; 3: Puso barcos; 4: Esta jugando -> Si pierde pasa a 0: Desconectado
    match_type: int = 1 # 1: PvB, 0: PvP
    player_id: int = 0 
    remaining_lives: int = 6
    board: Board = field(default_factory=Board)

    def update_status(self, new_status):
        self.status = new_status
        return self
    
    def select_match_type(self, match_type):
        """
        1: Player vs Bot
        0: Player vs Player
        """
        self.match_type = match_type
        return self

    def __str__(self) -> str:
        return f"{'Jugador:':<17}{self.player_id}\n" \
            f"{'Status:':<17}{self.status}\n" \
            f"{'Tipo de partida:':<17}{'Player vs Bot' if self.match_type else 'Player vs Player'}\n" \
            f"{'Vidas:':<17}{self.remaining_lives}\n" \
            f"{'Board:':<17}{self.board}\n"
