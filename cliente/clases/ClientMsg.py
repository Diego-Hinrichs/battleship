from dataclasses import dataclass, field
from clases.Client import Client
from clases.utils import select_match_type, build_ships, make_attack, msg_json

@dataclass
class ClientMessage():
    action: str = "c"
    bot: int = 0 
    ships: dict = field(default_factory=dict)
    position: list = field(default_factory=list)
    
    list_of_actions = ["a", "b", "c", "d", "l", "s"]

    def make_message(self, client: Client):
        if (self.action in self.list_of_actions):
            if self.action == "c" and client.status == 0:
                return msg_json(self.action, self.bot, self.ships, [])

            elif self.action == "s" and client.status == 1:
                self.bot = select_match_type()
                return msg_json(self.action, self.bot, self.ships, [])
            
            elif self.action == "b" and client.status == 2:
                self.ships = build_ships()
                return msg_json(self.action, self.bot, self.ships, [])
            
            elif self.action == "a" and client.status == 3:
                self.position = make_attack()
                return msg_json(self.action, self.bot, self.ships, self.position)

            elif self.action == "l":
                return msg_json(self.action, self.bot, self.ships, [])

            elif self.action == "d":
                # Si client.status == 0??
                return msg_json(self.action, self.bot, self.ships, [])
            
            else:
                #TODO. En cualquier otro caso, se conecta con el servidor
                return msg_json("c", 0, {}, [])
        else:
            return msg_json(self.action, self.bot, self.ships, [])

    def __str__(self):
        return f"'action': {self.action}\
                'bot': {self.bot}\
                'ships': {self.ships}\
                'position': {self.position}"
        