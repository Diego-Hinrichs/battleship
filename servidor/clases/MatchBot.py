from dataclasses import dataclass, field
from clases.Player import Player
from clases.Bot import Bot

@dataclass
class MatchBot:
    match_id: str
    match_type: int
    bot: Bot
    player_1: Player

    # Si es bot juega primero el usuario.

    def __str__(self) -> str:
        return  f"Tipo de partida: {self.match_type}\n"\
                f"Player: {self.player_1.player_id}. Vidas: {self.player_1.remaining_lives}\n"\
                f"Bot: Servidor brigido. Vidas: {self.bot.remaining_lives}"\
        