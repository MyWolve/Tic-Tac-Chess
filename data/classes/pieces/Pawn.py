import pygame

from .Piece import Piece

class Pawn(Piece):
    def __init__(self, pos, color, board):
        super().__init__(pos, color, board)
        img_path = "data/imgs/" + color[0] + "_Pawn.png"
        self.name = color[0] + "_Pawn"
        self.img = pygame.image.load(img_path)
        self.img = pygame.transform.scale2x(self.img)

        # Pawns progress forwards and "reverse" when they reach the other side of the board (like in actual Chess, just without the promoting!)
        self.reverse = False if self.COLOR == 'W' else 'True'
    
    def is_at_edge(self, board):
        if not self.on_bench and board.get_grid_name(self.pos)[0] == 'D':
            self.reverse = True
        elif not self.on_bench and board.get_grid_name(self.pos)[0] == 'A':
            self.reverse = False
        else:
            pass
    
    def get_valid_moves(self, board):
        if self.on_bench:
            columns = 'ABCD'
            rows = '1234'
            for c in columns:
                for r in rows:
                    self.valid_moves.append(c + r)
        else:
            self.is_at_edge(board)
            if not self.reverse:
                move = str(chr(ord(board.get_grid_name(self.pos)[0]) + 1) + board.get_grid_name(self.pos)[1])
                self.valid_moves.append(move)
            else:
                move = str(chr(ord(board.get_grid_name(self.pos)[0]) - 1) + board.get_grid_name(self.pos)[1])
                self.valid_moves.append(move)