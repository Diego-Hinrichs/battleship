from dataclasses import dataclass, field
from clases.Client import Client
from clases.utils import select_game_type, build_ships, make_attack, msg_json

@dataclass
class ClientMessage():
    action: str = "c"
    bot: int = 0 
    ships: dict = field(default_factory=dict)
    position: list = field(default_factory=list)
    
    def make_message(self, client: Client):
        if self.action == "c" and client.status == 0:
            return msg_json(self.action, self.bot, self.ships, [])

        elif self.action == "s" and client.status == 1:
            self.bot = select_game_type()
            return msg_json(self.action, self.bot, self.ships, [])
        
        elif self.action == "b" and client.status == 2:
            self.ships = build_ships()
            return msg_json(self.action, self.bot, self.ships, [])
        
        elif self.action == "a" and client.status == 4:
            self.position = make_attack()
            return msg_json(self.action, self.bot, self.ships, self.position)

        elif self.action == "t" and client.status == 4:
            return msg_json(self.action, self.bot, self.ships, [])

        elif self.action == "l" and client.status == 4:
            return msg_json(self.action, self.bot, self.ships, [])

        elif self.action == "w" and client.status == 4:
            return msg_json(self.action, self.bot, self.ships, [])

        elif self.action == "d":
            return msg_json(self.action, self.bot, self.ships, [])
        
        else:
            return msg_json(self.action, self.bot, self.ships, [])

    def __str__(self):
        return f"'action': {self.action}\
                'bot': {self.bot}\
                'ships': {self.ships}\
                'position': {self.position}"
