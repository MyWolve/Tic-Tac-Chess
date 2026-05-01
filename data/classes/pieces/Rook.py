import pygame

from .Piece import Piece

class Rook(Piece):
    def __init__(self, pos, color, board):
        super().__init__(pos, color, board)
        img_path = "data/imgs/" + color[0] + "_Rook.png"
        self.name = color[0] + "_Rook"
        self.img = pygame.image.load(img_path)
        self.img = pygame.transform.scale2x(self.img)