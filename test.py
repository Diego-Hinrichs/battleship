from dataclasses import dataclass, field
from faker import Faker

@dataclass
class Message():
    action: str = "connect"
    bot: int = 0 
    ships: dict = field(default_factory=dict)
    position: tuple = (0,0)

    def make_message(self):
        msg = {"action": self.action, 
               "bot": self.bot, 
               "ships": self.ships, 
               "position": self.position}
        return msg
    
@dataclass
class Player:
    """Clase que define al Jugador"""
    player_id: int = None
    ships: list = field(default_factory=list)
    remaining_lives: int = 6
    # Falta agregar

    def show_player(self):
        return self.player_id, self.ships, self.remaining_lives
    
