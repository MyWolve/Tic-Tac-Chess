import pygame

class Piece:
    def __init__(self, pos, color, board):
        self.pos = pos
        self.COLOR = color
        self.on_bench = True
        self.bench_pos = pos
        self.IMG = pygame.image.load("data/imgs/W_Queen.png")

        # Will implement function later
        self.valid_moves = []


    def draw(self, display, board):
            slot_center = (self.pos[0] + board.tile_size // 2, self.pos[1] + board.tile_size // 2)                                                                                                                                     
            img_rect = self.IMG.get_rect(center=slot_center)                                                                                                                                                                 
            display.blit(self.img, img_rect)
    
    def move(self, board, destination_square):
        if self.COLOR == board.turn:
            coords = board.get_coords(destination_square)
            if not coords:
                return 1  # board.get_coords() threw a KeyError
            self.pos = coords
            board.clear_board_flag = True

            # Update Piece
            self.on_bench = False

            # Update square with occupying piece
            for square in board.squares:
                 if square.pos == destination_square:
                      square.occupying_piece = self
        else:
            print("Error: Not a Valid Move!")
            return 1
    
    def bench(self, board):
         self.pos = self.bench_pos
        
    # Overwritten by Children for specific Piece implementations
    def get_valid_moves(self):
         pass
         