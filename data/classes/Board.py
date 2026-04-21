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

        # Bench positioning: one column of 4 slots on each side
        bench_gap = 50  # gap between bench and board edge
        self.bench_slot_size = self.tile_size
        self.left_bench_x = self.offset_x - self.bench_slot_size - bench_gap
        self.right_bench_x = self.offset_x + board_pixel_w + bench_gap
        self.bench_y = self.offset_y  # align top of bench with top of board
        
        self.squares = self.generate_squares()

    def generate_squares(self):
        output = []
        for y in range(4):
            for x in range(4):
                output.append(
                    Square(x, y, self.tile_width, self.tile_height,
                           self.offset_x, self.offset_y)
                )
        return output

    def draw(self, display):
        # draw checkerboard in screen center
        for square in self.squares:
            square.draw(display)
        # draw bench slots (4 stacked vertically on each side)
        bench_color = (180, 170, 160)
        bench_border_color = (100, 100, 100)
        for i in range(4):
            slot_y = self.bench_y + i * self.bench_slot_size
            # left bench
            left_rect = pygame.Rect(
                self.left_bench_x, slot_y,
                self.bench_slot_size, self.bench_slot_size
            )
            pygame.draw.rect(display, bench_color, left_rect)
            pygame.draw.rect(display, bench_border_color, left_rect, 2)
            # right bench
            right_rect = pygame.Rect(
                self.right_bench_x, slot_y,
                self.bench_slot_size, self.bench_slot_size
            )
            pygame.draw.rect(display, bench_color, right_rect)
            pygame.draw.rect(display, bench_border_color, right_rect, 2)
    
    def initialize(self, display):
        pass