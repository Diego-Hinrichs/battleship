from dataclasses import dataclass, field
from clases.Player import Player
from clases.Bot import Bot
from clases.Coordinates import Coordinates

@dataclass
class Match:
    match_id: str
    player_1: Player
    player_2: Player | Bot
    current_turn: Player | Bot
    match_type: int = 1 # 1: PvB, 0: PvP

    def __post_init__(self):
        if isinstance(self.player_2, Bot):
            # Si el segundo jugador es un bot, el primer jugador (cliente) comienza
            self.current_turn = self.player_1
        else:
            # Si el segundo jugador no es un bot, el turno se decide al azar
            import random
            self.current_turn = random.choice([self.player_1, self.player_2])

    def is_match_finish(self) -> tuple[bool, str | None]:
        pl1 = self.player_1.remaining_lives
        pl2 = self.player_2.remaining_lives
        if pl2 == 0:
            return (True, self.player_1.player_id)
        elif pl1 == 0:
            return (True, self.player_2.player_id)
        else:
            return (False, None)
    
    def switch_turn(self):
        if self.current_turn == self.player_1:
            self.current_turn = self.player_2
        elif self.current_turn == self.player_2:
            self.current_turn = self.player_1

    def __str__(self) -> str:
        match_type = 'Player v/s Player' if self.match_type == 0 else 'Player v/s Bot'
        match =  f"Tipo de partida: {match_type} \n"
        match += f"{self.player_1.player_id} v/s {self.player_2.player_id}\n"
        match += f"Juega: {self.current_turn.player_id}\n"
        return match
