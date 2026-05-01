import pygame

from .Piece import Piece

class Knight(Piece):
    def __init__(self, pos, color, board):
        super().__init__(pos, color, board)
        img_path = "data/imgs/" + color[0] + "_Knight.png"
        self.name = color[0] + "_Knight"
        self.img = pygame.image.load(img_path)
        self.img = pygame.transform.scale2x(self.img)
    