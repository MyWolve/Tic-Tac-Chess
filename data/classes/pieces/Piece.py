import pygame

class Piece:
    def __init__(self, pos, color):
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.color = color
        self.on_bench = True