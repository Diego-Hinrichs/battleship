from dataclasses import dataclass, field
from clases.Ship import Ship
from clases.Board import Board
from clases.Coordinates import Coordinates
import random

@dataclass
class Bot:
    player_id = "Bot"
    remaining_lives: int = 6
    board: Board = Board()
    ships: list[Ship] = field(default_factory=list) 
    played_coordinates: list[Coordinates] = field(default_factory=list)

    def build_random_ship(self):
        ship_types = list(self.board.ships_sizes.keys())
        generated_ships = []
        for ship in ship_types:
            while True:
                ship_size = self.board.ships_sizes.get(ship, 1)

                # Generar coordenadas aleatorias para el barco
                x = random.randint(0, self.board.size - 1)
                y = random.randint(0, self.board.size - 1)
                orientation = random.randint(0, 1)

                # Crear un nuevo barco aleatorio
                new_ship = Ship(size=ship_size, orientation=orientation, type=ship)
                if new_ship.coordinates_list(Coordinates(x, y)):
                    overlap = any(new_ship.is_overlaped(ship.list_coordinates) for ship in generated_ships)

                    # Verificar si el barco está dentro de los límites
                    if (0 <= x < self.board.size) and (0 <= y < self.board.size) and not overlap:
                        generated_ships.append(new_ship)
                        break

        self.ships.extend(generated_ships)

    def get_random_attack_coordinates(self):
        while True:
            x = random.randint(0, self.board.size-1)
            y = random.randint(0, self.board.size-1)
            coor = Coordinates(x, y)
            if coor not in self.played_coordinates:
                self.played_coordinates.append(coor)
                return coor

    def __str__(self):
        bot_str  = f"==============\t{self.player_id}\t ==============\n"
        bot_str += f"Vidas restantes del bot: {self.remaining_lives}\n"
        for i, ship in enumerate(self.ships, start=1):
            bot_str += f"Tipo: {ship.type.upper()} -- "
            bot_str += f"Coordenadas: {[c for c in ship.list_coordinates]}\n"
        return bot_str
    