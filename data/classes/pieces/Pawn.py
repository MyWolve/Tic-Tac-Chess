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
        self.valid_moves = []
        if self.on_bench:
            columns = 'ABCD'
            rows = '1234'
            for c in columns:
                for r in rows:
                    self.valid_moves.append(c + r)
        else:
            self.is_at_edge(board)
            grid_name = board.get_grid_name(self.pos)
            col = ord(grid_name[0]) - ord('A')
            row = int(grid_name[1]) - 1
            dc = -1 if self.reverse else 1

            # Forward move: only to an empty square
            fwd_col = col + dc
            if 0 <= fwd_col < 4:
                fwd_name = chr(ord('A') + fwd_col) + str(row + 1)
                fwd_square = next((s for s in board.squares if s.pos == fwd_name), None)
                if fwd_square and fwd_square.occupying_piece is None:
                    self.valid_moves.append(fwd_name)

            # Diagonal captures: only to squares with an enemy piece, if capture is unlocked
            if board.can_capture[self.COLOR]:
                for dr in (-1, 1):
                    diag_col = col + dc
                    diag_row = row + dr
                    if 0 <= diag_col < 4 and 0 <= diag_row < 4:
                        diag_name = chr(ord('A') + diag_col) + str(diag_row + 1)
                        diag_square = next((s for s in board.squares if s.pos == diag_name), None)
                        if (diag_square and diag_square.occupying_piece and
                                diag_square.occupying_piece.COLOR != self.COLOR):
                            self.valid_moves.append(diag_name)