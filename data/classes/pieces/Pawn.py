import pygame

from .Piece import Piece
from ..Board import Board

class Pawn(Piece):
    def __init__(self, pos, color, board):
        super().__init__(pos, color, board)
        img_path = "data/imgs/" + color[0] + "_Pawn.png"
        self.img = pygame.image.load(img_path)
        self.img = pygame.transform.scale(self.img, (board.tile_width - 16, board.tile_height - 16))