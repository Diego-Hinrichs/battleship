from dataclasses import dataclass, field
from clases.Player import Player
from clases.Bot import Bot

@dataclass
class Game:
    game_id: str
    player_1: Player
    player_2: Player | Bot
    current_turn: str
    game_type: int = 1 # 1: PvB, 0: PvP

    def __post_init__(self):
        if isinstance(self.player_2, Bot):
            self.current_turn = self.player_1.player_id

    def __iter__(self):
        yield self.player_1
        yield self.player_2

    # -1 es en caso de lose -> jugador pasa a tener vidas == 0
    # entonces en el siguiente ataque es -1, se retorna 1 
    # para enviar msj de victoria al otro jugador 
    def win(self, player_id: str):
        if player_id == self.player_1.player_id:
            return 1 if self.player_2.remaining_lives <= 0 else 0
        elif player_id == self.player_2.player_id:
            return 1 if self.player_1.remaining_lives <= 0 else 0

    def lose(self, player_id: str):
        if player_id == self.player_2.player_id:
            return 1 if self.player_2.remaining_lives == 0 else 0
        elif player_id == self.player_1.player_id:
            return 1 if self.player_1.remaining_lives == 0 else 0

    def switch_turn(self):
        if self.current_turn == self.player_1.player_id:
            self.current_turn = self.player_2.player_id
        elif self.current_turn == self.player_2.player_id:
            self.current_turn = self.player_1.player_id

    def __str__(self) -> str:
        game_type = 'Player v/s Player' if self.game_type == 0 else 'Player v/s Bot'
        game =  f"Tipo de partida: {game_type} \n"
        game += f"{self.player_1.player_id} v/s {self.player_2.player_id}\n"
        game += f"Juega: {self.current_turn}\n"
        return game
