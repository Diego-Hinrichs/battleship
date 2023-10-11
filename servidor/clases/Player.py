from dataclasses import dataclass, field
from clases.Ship import Ship

@dataclass
class Player:
    status: int = 0  # 0: Desconectado; 1: Conectado; 2: Eligió modo de juego; 3: Puso barcos y esta en partida 4: En partida -> Si pierde pasa a 0: Desconectado
    match_type: int = 1 # 1: PvB, 0: PvP
    player_id: str = "" 
    remaining_lives: int = 6
    ships: list[Ship] = field(default_factory=list[Ship])

    def update_status(self, new_status):
        self.status = new_status
        return self
    
    def select_match_type(self, match_type):
        self.match_type = match_type
        return self
    
    def has_created_ships(self):
        return True if (len(self.ships) > 0) else False

    def __str__(self):
        player_str = f"==============\t{self.player_id}\t ==============\n"
        for i, ship in enumerate(self.ships, start=1):
            player_str += f"Tipo: {ship.type.upper()} --> "
            player_str += f"Coordenadas: {[c for c in ship.list_coordinates]}\n"
        return player_str


