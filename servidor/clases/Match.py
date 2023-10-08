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

    def __post_init__(self):
        if isinstance(self.player_2, Bot):
            # Si el segundo jugador es un bot, el primer jugador (cliente) comienza
            self.current_turn = self.player_1
        else:
            # Si el segundo jugador no es un bot, el turno se decide al azar
            import random
            self.current_turn = random.choice([self.player_1, self.player_2])

    def switch_turn(self):
        if self.current_turn == self.player_1:
            self.current_turn = self.player_2
        else:
            self.current_turn = self.player_1
