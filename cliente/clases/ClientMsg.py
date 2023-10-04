from dataclasses import dataclass, field
import json

def msg_json(action: str, bot: int, ships: dict, position: list) -> str:
    return json.dumps({"action": action, "bot": bot, "ships": ships, "position": position})

def select_match_type() -> int:
    """
    0: Player vs Bot
    1: Player vs Player
    """
    chosse =  False
    while(not chosse):
        option = str(input("Quieres jugar contra un bot? [Y/n]: "))
        if option.lower() == "n":
            return 0
        elif option.lower() =="y":
            return 1
    return 1

def make_single_ship(ship_type: str, ships_dict: dict) -> dict:
    if ship_type == "b":
        coor = str(input("Selecciona coordenadas: [x,y].\nPor ejemplo: 10,10\n"))
        x, y = coor.split(",")
        ships_dict.update({ship_type: [int(x), int(y), 0]})
    else:
        coor = str(input("Selecciona coordenadas y orientación: [x,y,o].\nPor ejemplo: 10,10,1\n"))
        x, y, o = coor.split(",")
        ships_dict.update({ship_type: [int(x), int(y), int(o)]})
    return ships_dict

def build_ships() -> dict:
    ships_dict = {}
    ships = ["p", "b", "s"]
    while(len(ships) > 0):
        option = str(input(f"Selecciona un barco a construir {[i for i in ships]}: ")).lower()
        if(option in ships):
            if option== "s":
                ships.remove("s")
                make_single_ship(option, ships_dict)

            if option == "p":
                ships.remove("p")
                make_single_ship(option, ships_dict)

            if option == "b":
                ships.remove("b")
                make_single_ship(option, ships_dict)
        else:
            print(f"Ya construiste {option}: {ships_dict.get(option)}")
    print(ships_dict)
    return ships_dict

@dataclass
class ClientMessage():
    action: str = "c"
    bot: int = 0 
    ships: dict = field(default_factory=dict)
    position: list = field(default_factory=list)
    
    list_of_actions = ["a", "b", "c", "d", "l", "s"]

    def make_message(self):
        if (self.action in self.list_of_actions):

            #TODO. ATTACK
            if self.action == "a":
                return msg_json(self.action, self.bot, self.ships, [])
            
            #TODO. Msj desde el servidor y actualizar status en cliente
            if self.action == "b":
                self.ships = build_ships()
                return msg_json(self.action, self.bot, self.ships, [])
            
            #TODO. Msj desde el servidor y actualizar status en cliente
            if self.action == "c":
                return msg_json(self.action, self.bot, self.ships, [])
            
            #TODO. Msj desde el servidor y actualizar status en cliente
            if self.action == "d":
                return msg_json(self.action, self.bot, self.ships, [])
            
            #TODO. LOSE
            if self.action == "l":
                return msg_json(self.action, self.bot, self.ships, [])
            
            #TODO. Msj desde el servidor y actualizar status en cliente
            if self.action == "s":
                self.bot = select_match_type()
                return msg_json(self.action, self.bot, self.ships, [])
        else:
            return msg_json(self.action, self.bot, self.ships, [])

    def __str__(self):
        return f"'action': {self.action}\
                'bot': {self.bot}\
                'ships': {self.ships}\
                'position': {self.position}"
        