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
        self.board[x][y] = "[x]"
        return self.board

board = Board(size=5)
board.new_board()
print("Pre attack\n")
board.show_board()
board.make_attack(x = 1, y = 2)
print("Post attack\n")
board.show_board()