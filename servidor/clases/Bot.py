from dataclasses import dataclass, field
from clases.Ship import Ship
from clases.Board import Board
import random

@dataclass(init=False)
class Bot:
    remaining_lives: int = 6
    ships: list[Ship]
    board: Board = Board()
    
    def build_random_ship(self):
        for ship in self.board.ships_sizes:
            print(ship)
    