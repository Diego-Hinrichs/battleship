from dataclasses import dataclass, field
from clases.Ship import Ship
from clases.Coordinates import Coordinates

class Board:
    # Overlap_coordinates, no deberia esta en esta clase, deberia entrar como parametros 
    def __init__(self, size=5):
        self.__overlap_coordinates = []
        self.ships = []
        self.size = size
        self.ships_sizes = {'s': 3, 'b': 2, 'p': 1}

    #TODO. Todo esto deberia esta en la clase ships
    def add_overlap_coordinate(self, coordinate: Coordinates):
        self.__overlap_coordinates.append(coordinate)

    def make_ships(self, ships: dict[str, list]) -> bool:
        for i in ships:
            ship = ships.get(i)
            coord = Coordinates(ship[0], ship[1])
            if (0 <= coord.x < self.size) and (0 <= coord.y < self.size):
                new_ship = Ship(orientation = ship[2], size = self.ships_sizes.get(i,1), type = i)
                ship_coordinates = new_ship.coordinates_list(coord)
                if ship_coordinates:
                    overlap = ship_coordinates.is_overlaped(self.__overlap_coordinates)
                    if not overlap:
                        for i in ship_coordinates.list_coordinates:
                            self.add_overlap_coordinate(i)
                    elif overlap:
                        return False
                if not ship_coordinates:
                    return False
                
                elif ship_coordinates:
                    self.ships.append(ship_coordinates)
            else:
                return False
        return True

    def __str__(self) -> str:
        return f"Barcos: {self.ships}"

