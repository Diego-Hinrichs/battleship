from dataclasses import dataclass, field
from clases.Coordinates import Coordinates

@dataclass
class Ship:
    size: int
    list_coordinates: list[Coordinates] = field(default_factory=list[Coordinates])
    orientation: int = 0 # Vertical
    type: str = "Barco patrulla"
    
    def is_overlaped(self, overlap: list[Coordinates]):
        #print(f"Coordenadas_input:{self.list_coordinates}")
        #print(f"Overlap_list: {overlap}")
        if len(overlap) == 0:
            return False
        else:
            for coord in self.list_coordinates:
                if coord in overlap:
                    #print(f"Overlap_here: {coord}")
                    return True
            return False
                #return True if coord in overlap else False

    #TODO. Esto deberia estar en la clase coordinates
    def coordinates_list(self, coord: Coordinates):
        # Lista de coordenadas del barco si es horizontal
        if self.orientation == 1:
            for i in range(self.size):
                if (coord.x + i >= 5) or (coord.y >= 5):
                    return False # Fuera de rango
                else:
                    new_coord = Coordinates(coord.x + i, coord.y)
                    self.list_coordinates.append(new_coord)
            return self
        
        # Lista de coordenadas del barco si es vertical
        elif self.orientation == 0:
            for i in range(self.size):
                if (coord.x >= 5) or (coord.y + i >= 5):
                    return False # Fuera de rango
                else:
                    new_coord = Coordinates(coord.x, coord.y + i)
                    self.list_coordinates.append(new_coord)
            return self
        
    def __str__(self) -> str:
        return  f"Tamaño: {self.size}\n"\
                f"Orientacion: {'Horizontal' if self.orientation else 'Vertical'}\n"\
                f"Tipo: {self.type}\n" \
                f"Coordenadas: {[c for c in self.list_coordinates]}\n"