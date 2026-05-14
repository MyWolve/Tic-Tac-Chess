import pygame 

from .Square import Square
from .pieces.Pawn import Pawn
from .pieces.Rook import Rook
from .pieces.Knight import Knight
from .pieces.Bishop import Bishop

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
        self.turn = 'W'

        # Bench positioning: one column of 4 slots on each side
        bench_gap = 50  # gap between bench and board edge
        self.bench_slot_size = self.tile_size
        self.left_bench_x = self.offset_x - self.bench_slot_size - bench_gap
        self.right_bench_x = self.offset_x + board_pixel_w + bench_gap
        self.bench_y = self.offset_y  # align top of bench with top of board
        
        # I'm confusing myself, I'm not sure if this is even needed -- Surely an easier way? 
        self.squares = self.generate_squares()
        # List points to each Piece() object created so we can manipulate them
        self.pieces = []

        # GAME STATE FLAGS
        self.initialize_bench_flag = True
        self.clear_board_flag = False
        self.redraw_board_flag = False

    def generate_squares(self):
        output = []
        for y in range(4):
            for x in range(4):
                output.append(
                    Square(x, y, self.tile_width, self.tile_height,
                           self.offset_x, self.offset_y)
                )
        return output
    
    # draw checkerboard in screen center
    def draw_board(self, display):
        for square in self.squares:
            square.draw_squares(display)
    
    def draw_bench(self, display):
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
        
        return left_rect, right_rect
    
    # Initializes W_Piece and B_Piece objects and draws them on the board at GAME START
    def initialize_bench(self, board, left_bench, right_bench, display):
        # Iterate through each slot in left bench
        W_Pawn = Pawn((left_bench.x, left_bench.y), "W", board);                            W_Pawn.draw(display, board)
        W_Rook = Rook((left_bench.x, left_bench.y - self.tile_size), "W", board);           W_Rook.draw(display, board)
        W_Knight = Knight((left_bench.x, left_bench.y - self.tile_size * 2), "W", board);   W_Knight.draw(display,board)
        W_Bishop = Bishop((left_bench.x, left_bench.y - self.tile_size * 3), "W", board);   W_Bishop.draw(display,board)
        # Iterate through each slot in right bench
        B_Pawn = Pawn((right_bench.x, right_bench.y), "B", board);                          B_Pawn.draw(display,board)
        B_Rook = Rook((right_bench.x, right_bench.y - self.tile_size), "B", board);         B_Rook.draw(display,board)
        B_Knight = Knight((right_bench.x, right_bench.y - self.tile_size * 2), "B", board); B_Knight.draw(display,board)
        B_Bishop = Bishop((right_bench.x, right_bench.y - self.tile_size * 3), "B", board); B_Bishop.draw(display,board)

        # Add pieces to global inventory
        self.pieces.extend([W_Pawn, W_Rook, W_Knight, W_Bishop, B_Pawn, B_Rook, B_Knight, B_Bishop])

        # self.draw_piece_test_fillBoard(display, board)
        # self.draw_piece_test_fillBoard_NEW(display, board)
    
    def draw_pieces(self, display):
        for piece in self.pieces:
            piece.draw(display,self)
            
    # Test function for get_coords()
    def draw_piece_test_fillBoard(self, display, board):
        column_letter = ['A', 'B', 'C', 'D']
        for column in range(4):
            for row in range(1,5):
                W_Pawn = Pawn((self.get_coords(column_letter[column] + str(row))), "W", board)
                Pawn.draw(W_Pawn, display, board)

    # Test function as above BUT with new square.pos
    def draw_piece_test_fillBoard_NEW(self, display, board):
        for square in board.squares:
            coords = self.get_coords(square.pos)
            if coords:
                W_Pawn = Pawn((coords[0], coords[1]), "W", board)
                Pawn.draw(W_Pawn, display, board)

    # Get hard-coded coordinate for each grid-square.
    """
    |A1|B1|C1|D1|
    |A2|B2|C2|D2|
    |A3|B3|C3|D3|
    |A4|B4|C4|D4|
    """
    # Can DEFINITELY refactor this later for dynamic board sizes
    def get_coords(self, gridSquare):
        coordinates = {
            "A1": (352,72), "A2": (352,216), "A3": (352,360), "A4": (352,504),
            "B1": (496,72), "B2": (496,216), "B3": (496,360), "B4": (496,504),
            "C1": (640,72), "C2": (640,216), "C3": (640,360), "C4": (640,504),
            "D1": (784,72), "D2": (784,216), "D3": (784,360), "D4": (784,504)
        }
        try:
            return coordinates[gridSquare][0], coordinates[gridSquare][1]        
        except KeyError:
            print("ERROR: Grid square must be a valid move. ([A-D][1-4])")
    
    def get_grid_name(self, coords):
        coordinates = {
            "A1": (352,72), "A2": (352,216), "A3": (352,360), "A4": (352,504),
            "B1": (496,72), "B2": (496,216), "B3": (496,360), "B4": (496,504),
            "C1": (640,72), "C2": (640,216), "C3": (640,360), "C4": (640,504),
            "D1": (784,72), "D2": (784,216), "D3": (784,360), "D4": (784,504)
        }
        reverse = {v: k for k, v in coordinates.items()}
        return reverse.get(coords)
    
    # Returns the Piece object at a location given by mouse_pos
    def get_piece_at(self, mouse_pos):
        for piece in self.pieces:
            if (piece.pos[0] <= mouse_pos[0] < piece.pos[0] + self.tile_size and
                    piece.pos[1] <= mouse_pos[1] < piece.pos[1] + self.tile_size):
                print(str(piece) + " @ " + str(piece.pos))
                return piece
        return None
    
    # Returns the Square object at a location given by mouse_pos
    def get_square_at(self, mouse_pos):
        for square in self.squares:
            coords = self.get_coords(square.pos)
            if (coords[0] <= mouse_pos[0] < coords[0] + square.width and
                    coords[1] <= mouse_pos[1] < coords[1] + square.height):
                print(str(mouse_pos) + " is within square " + square.pos)
                return square
        return None
    
    def highlight_square(self, display):
        # Draw a highlighted barrier around the selected piece
        p = self.selected_piece
        highlight_rect = pygame.Rect(p.pos[0], p.pos[1], self.tile_size, self.tile_size)
        pygame.draw.rect(display, (100, 249, 83), highlight_rect, 3) # 3px border
        # If p.on_bench, all destinations are valid!
        if p.on_bench:
            print("I'm on the bench!")
            for square in self.squares:
                highlight_square_rect = pygame.Rect(square.abs_x, square.abs_y, self.tile_size, self.tile_size)
                pygame.draw.rect(display, (215, 10, 245), highlight_square_rect, 3)
        # If p is not on bench, run p.get_valid_moves() and only highlight those squares
        else:
            p.get_valid_moves(self)
            for move in p.valid_moves:
                highlight_square_rect = pygame.Rect(self.get_coords(move)[0], self.get_coords(move)[1], self.tile_size, self.tile_size)
                pygame.draw.rect(display, (215, 10, 245), highlight_square_rect, 3)