import pygame 

from .Square import Square

class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # Square tiles sized to fit 4 rows within the window height (with padding)
        self.tile_size = int(height * 0.8) // 4
        self.tile_width = self.tile_size
        self.tile_height = self.tile_size
        # Center the 4x4 board in the window
        board_pixel_w = self.tile_size * 4
        board_pixel_h = self.tile_size * 4
        self.offset_x = (width - board_pixel_w) // 2
        self.offset_y = (height - board_pixel_h) // 2
        self.selected_piece = None
        self.turn = 'white'
        self.config = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR'],
        ]
        self.squares = self.generate_squares()
        self.setup_board()

    def generate_squares(self):
        output = []
        for y in range(4):
            for x in range(4):
                output.append(
                    Square(x, y, self.tile_width, self.tile_height,
                           self.offset_x, self.offset_y)
                )
        return output

    def get_square_from_pos(self, pos):
        for square in self.squares:
            if (square.x, square.y) == (pos[0], pos[1]):
                return square

    def get_piece_from_pos(self, pos):
        pass
        #return self.get_square_from_pos(pos).occupying_piece

    def setup_board(self):
        pass

    def draw(self, display):
        for square in self.squares:
            square.draw(display)