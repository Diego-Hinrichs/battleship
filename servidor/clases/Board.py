from dataclasses import dataclass, field

@dataclass
class Board:
    size: int = 5
    board: list = field(default_factory=list)

    def new_board(self):
        self.board = [[f"[-]" for _ in range(self.size)] for _ in range(self.size)]
        return self.board

    def show_board(self):
        for row in self.board:
            print(" ".join(row))
            print(" ")
    
    def make_attack(self, x, y):
        try:
            self.board[x][y] = "[x]"
            self.show_board()
            return self.board
        except IndexError:
            print(f"Coordenada incorrecta, jugar 0-{self.size-1}")
            
