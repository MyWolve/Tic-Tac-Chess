import pygame

from .Piece import Piece

class Bishop(Piece):
    def __init__(self, pos, color, board):
        super().__init__(pos, color, board)
        img_path = "data/imgs/" + color[0] + "_Bishop.png"
        self.name = color[0] + "_Bishop"
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
            pass