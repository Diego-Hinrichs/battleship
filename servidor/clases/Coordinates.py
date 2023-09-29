from dataclasses import dataclass

@dataclass
class Coordinates:
    """Coordenadas """
    x: int
    y: int

    def show_coordinates(self) -> tuple:
        return (self.x, self.y)