import pygame

from .Piece import Piece

class Knight(Piece):
    def __init__(self, pos, color, board):
        super().__init__(pos, color, board)
        img_path = "data/imgs/" + color[0] + "_Knight.png"
        self.name = color[0] + "_Knight"
        self.img = pygame.image.load(img_path)
        self.img = pygame.transform.scale2x(self.img)
    
    def get_valid_moves(self, board):
        self.valid_moves = []
        if self.on_bench:
            columns = 'ABCD'
            rows = '1234'
            for c in columns:
                for r in rows:
                    self.valid_moves.append(c + r)
        else:
            grid_name = board.get_grid_name(self.pos)
            col = ord(grid_name[0]) - ord('A')
            row = int(grid_name[1]) - 1

            for dc, dr in [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]:
                c, r = col + dc, row + dr
                if 0 <= c < 4 and 0 <= r < 4:
                    name = chr(ord('A') + c) + str(r+1)
                    target = next((s for s in board.squares if s.pos == name), None)
                    if not (target and target.occupying_piece and target.occupying_piece.COLOR == self.COLOR):
                        self.valid_moves.append(name)