from dataclasses import dataclass

@dataclass
class Coordinates:
    """Coordenadas """
    x: int
    y: int

    def __iter__(self):
        yield self.x
        yield self.y

    def __str__(self) -> str:
        return f"(Coordenada: {self.x},{self.y})"