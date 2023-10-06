from dataclasses import dataclass, field
from clases.Client import Client
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

def get_coordinates(ship: str) -> dict:
    print(f"Construye {ship.upper()}")
    #TODO. un else x si la cadena viene vacia
    coor_x = input(f"Ingresa la coordenada x: ")
    coor_y = input(f"Ingresa la coordenada y: ")
    if ship == "barco patrulla":
        return {ship[0]: [int(coor_x), int(coor_y), 0]}
    else:
        orientation = input(f"Ingresa la orientacion: ")
        return {ship[0]: [int(coor_x), int(coor_y), int(orientation)]}

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
            
            #TODO. ATTACK, se necesita status, 3: Coloco los barcos...
            elif self.action == "a" and client.status == 3:
                return msg_json(self.action, self.bot, self.ships, [])
            
            #TODO. Lose o rendirse, pasara a estado conectado, se resetean todos los stats
            elif self.action == "l":
                return msg_json(self.action, self.bot, self.ships, [])

            elif self.action == "d":
                return msg_json(self.action, self.bot, self.ships, [])
            
            else:
                # En cualquier otro caso, se conecta con el servidor
                # arreglar es
                return msg_json("c", 0, {}, [])
        else:
            return msg_json(self.action, self.bot, self.ships, [])

    def __str__(self):
        return f"'action': {self.action}\
                'bot': {self.bot}\
                'ships': {self.ships}\
                'position': {self.position}"
        