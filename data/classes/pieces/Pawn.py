import pygame

from .Piece import Piece

class Pawn(Piece):
    def __init__(self, pos, color, board):
        super().__init__(pos, color, board)
        img_path = "data/imgs/" + color[0] + "_Pawn.png"
        self.name = color[0] + "_Pawn"
        self.img = pygame.image.load(img_path)
        # self.img = pygame.transform.scale(self.img, (board.tile_width - 16, board.tile_height - 16))
        self.img = pygame.transform.scale2x(self.img)
    
    def draw(self, display, board):
        slot_center = (self.x + board.tile_size // 2, self.y + board.tile_size // 2)                                                                                                                                     
        img_rect = self.img.get_rect(center=slot_center)                                                                                                                                                                 
        display.blit(self.img, img_rect)

    def erase(self, display, board):
        pass