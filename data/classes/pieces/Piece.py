import pygame

class Piece:
    def __init__(self, pos, color, board):
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.color = color
        self.on_bench = True
        self.img = None

    def draw(self, display, board):
        slot_center = (self.x + board.tile_size // 2, self.y + board.tile_size // 2)
        img_rect = self.img.get_rect(center=slot_center)
        display.blit(self.img, img_rect)