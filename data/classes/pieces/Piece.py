import pygame

class Piece:
    def __init__(self, pos, color, board):
        self.pos = pos
        self.color = color
        self.on_bench = True
        self.img = pygame.image.load("data/imgs/W_Queen.png")

        # Will implement function later
        self.is_valid_move = True # HELLO

    def draw(self, display, board):
            slot_center = (self.pos[0] + board.tile_size // 2, self.pos[1] + board.tile_size // 2)                                                                                                                                     
            img_rect = self.img.get_rect(center=slot_center)                                                                                                                                                                 
            display.blit(self.img, img_rect)
    
    def move(self, display, board, destination_square):
        if self.color == board.turn and self.is_valid_move:
            coords = board.get_coords(destination_square)
            if not coords:
                return 1  # board.get_coords() threw a KeyError
            self.pos = coords
            board.clear_board_flag = True
        else:
            print("Error: Not a Valid Move!")
            return 1