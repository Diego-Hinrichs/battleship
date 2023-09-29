from dataclasses import dataclass, field

@dataclass
class ClientMessage():
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