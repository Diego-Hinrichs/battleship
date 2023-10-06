from dataclasses import dataclass, field
from clases.Ship import Ship
from clases.Coordinates import Coordinates

@dataclass
class Board:
    overlap_coordinates: list[Coordinates] = field(default_factory=list[Coordinates])
    ships: list[Ship] = field(default_factory=list[Ship])
    size: int = 5
    ships_sizes = {'s': 3, 'p':2, 'b':1}

    #TODO. Esto deberia esta en la clase ships
    def make_ships(self, ships: dict[str, list]) -> bool:
        # Si la coordenada esta dentro del tablero
        for i in ships:
            ship = ships.get(i)
            coord = Coordinates(ship[0], ship[1])
            if (0 <= coord.x < self.size) and (0 <= coord.y < self.size):
                new_ship = Ship(orientation = ship[2], size = self.ships_sizes.get(i,1), type = i)
                ship_coordinates = new_ship.coordinates_list(coord) # Lista con coordenadas del barco
                if ship_coordinates:
                    overlap = ship_coordinates.is_overlaped(self.overlap_coordinates)
                    if not overlap: # Falso
                        for i in ship_coordinates.list_coordinates:
                            self.overlap_coordinates.append(i)
                    elif overlap: # Verdadero
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

