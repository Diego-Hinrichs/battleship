from dataclasses import dataclass, field

@dataclass
class Ship:
    coordinates: list[tuple] = field(default_factory=list[tuple])
    size: int = 1
    type: str = "Barco patrulla"
      
    def __str__(self) -> str:
        return f"Tamaño: {self.size}; Tipo: {self.type}; Coordenadas: {self.coordinates}"
    
ship = Ship()
print(ship)