from dataclasses import dataclass, field
from clases.Client import Client
import json

def msg_json(action: str, bot: int, ships: dict, position: list) -> str:
    return json.dumps({"action": action, "bot": bot, "ships": ships, "position": position})

def select_match_type() -> int:
    while(True):
        option = str(input("Quieres jugar contra un bot? [Y/n]: "))
        if option.lower() == "n":
            return 0
        elif option.lower() =="y":
            return 1

def get_single_coor(coor: str):
    while True:
        coor_input = input(f"Ingresa la coordenada {coor}: ")
        if coor_input.isdigit():
            coor = int(coor_input) # type: ignore
            break
        else:
            print(f"Coordenada {coor} no es un número válido. Inténtalo de nuevo.")
    return coor

def get_orientation() -> int:
    vertical = ['0','v','vertical', 'V', 'VERTICAL']
    horizontal = ['1','h','horizontal', 'H', 'HORIZONTAL']
    while True:
        orientation_input = input(f"Ingresa la orientación: ")
        if (orientation_input in vertical):
            return 0
        elif (orientation_input in horizontal):
            return 1
        else:
            print("Orientación no es un número válido. Inténtalo de nuevo.")

def get_coordinates(ship: str) -> dict:
    print(f"Construye {ship.upper()}")
    #TODO. un else x si la cadena viene vacia
    coor_x = get_single_coor("x")
    coor_y = get_single_coor("y")

    if ship == "barco patrulla":
        return {ship[0]: [coor_x, coor_y, 1]}
    else:
        orientation = get_orientation()
        return {ship[0]: [coor_x, coor_y, orientation]}

def make_attack():
    coor_x = get_single_coor("x")
    coor_y = get_single_coor("y")
    return [coor_x, coor_y]

def build_ships() -> dict:
    ships_dict = {}
    ships_dict.update(get_coordinates("portaviones"))
    ships_dict.update(get_coordinates("submarino"))
    ships_dict.update(get_coordinates("barco patrulla"))
    print(ships_dict)
    return ships_dict

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
            
            ### Jugar aqui
            ### Primero jugar contra bot

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
        