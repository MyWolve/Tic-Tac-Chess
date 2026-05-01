import pygame

class Piece:
    def __init__(self, pos, color, board):
        self.pos = pos
        self.color = color
        self.on_bench = True
        self.img = pygame.image.load("data/imgs/W_Queen.png")

    def draw(self, display, board):
            slot_center = (self.pos[0] + board.tile_size // 2, self.pos[1] + board.tile_size // 2)                                                                                                                                     
            img_rect = self.img.get_rect(center=slot_center)                                                                                                                                                                 
            display.blit(self.img, img_rect)
    
    def move(self, display, board, destination_square):
        # IS destination_square A VALID MOVE?
        if self.color == board.turn and self.is_valid_move():
            print("hello")
            # NO? -- Try again and return 1
        # YES? -- Continue
            # CLEAR BOARD
        # REDRAW GAMESTATE EXCEPT PIECE            
        # UPDATE POSITION
        if board.get_coords(destination_square):
            self.pos = board.get_coords(destination_square)    
        else:
            return  # If this is false, it's because board.get_coords() threw a KeyError exception
        
        # self.draw() AT NEW LOCATION
        self.draw(display,board)

        pygame.display.update()