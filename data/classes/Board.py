import pygame 
import numpy as np

from .Square import Square
from .pieces.Piece import Piece
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

        self.selected_piece: Piece | None = None
        self.turn = 'W'

        # Bench positioning: one column of 4 slots on each side
        bench_gap = 50  # gap between bench and board edge
        self.bench_slot_size = self.tile_size
        self.left_bench_x = self.offset_x - self.bench_slot_size - bench_gap
        self.right_bench_x = self.offset_x + board_pixel_w + bench_gap
        self.bench_y = self.offset_y  # align top of bench with top of board
        
        # I'm not sure if this is even needed -- Surely an easier way? 
        self.squares = self.generate_squares()
        
        # DEBUG: List points to each Piece() object created so we can manipulate them 
        self.pieces = []

        # Saves board space to matrix to check for winners
        self.board_space = np.zeros((4,4))

        # Tracks whether or not players can capture yet
        # Becomes True permanently once they have deployed 3 pieces from bench
        self.can_capture = {
            'W': False,
            'B': False
        }
        self.pieces_deployed = {
            'W': 0,
            'B': 0
        }
        self.deployed_pieces = {
            'W': [],
            'B': []
        }

        # GAME STATE FLAGS
        self.initialize_bench_flag = True
        self.clear_board_flag = False
        self.redraw_board_flag = False
        self.game_over_flag = False

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
    
    # "Reading the Card, explains the Card" - MLK
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
    
    # Returns the pos string of the clicked area: "A1"-"D4" for board squares,
    # "left_bench_N" / "right_bench_N" for bench slots, or None for a miss.
    def get_square_at(self, mouse_pos):
        for square in self.squares:
            coords = self.get_coords(square.pos)
            if coords and (coords[0] <= mouse_pos[0] < coords[0] + square.width and
                    coords[1] <= mouse_pos[1] < coords[1] + square.height):
                return square.pos
        for i in range(4):
            slot_y = self.bench_y + i * self.bench_slot_size
            if (self.left_bench_x <= mouse_pos[0] < self.left_bench_x + self.bench_slot_size and
                    slot_y <= mouse_pos[1] < slot_y + self.bench_slot_size):
                return f"left_bench_{i}"
            if (self.right_bench_x <= mouse_pos[0] < self.right_bench_x + self.bench_slot_size and
                    slot_y <= mouse_pos[1] < slot_y + self.bench_slot_size):
                return f"right_bench_{i}"
        return None
    
    def highlight_square(self, display):
        p = self.selected_piece
        if not p:
            return
        highlight_rect = pygame.Rect(p.pos[0], p.pos[1], self.tile_size, self.tile_size)
        pygame.draw.rect(display, (100, 249, 83), highlight_rect, 3) # 3px border
        
        # If p.on_bench, all destinations are valid! (except for occupied squares)
        if p.on_bench:
            print("I'm on the bench!")
            for square in self.squares:
                if square.occupying_piece == None:
                    highlight_square_rect = pygame.Rect(square.abs_x, square.abs_y, self.tile_size, self.tile_size)
                    pygame.draw.rect(display, (215, 10, 245), highlight_square_rect, 3)

        # If p is not on bench, run p.get_valid_moves() and only highlight those squares
        else:
            p.get_valid_moves(self)
            for move in p.valid_moves:
                coords = self.get_coords(move)
                if not coords:
                    continue
                highlight_square_rect = pygame.Rect(coords[0], coords[1], self.tile_size, self.tile_size)
                pygame.draw.rect(display, (215, 10, 245), highlight_square_rect, 3)
    
    def update_board_space(self):
        for square in self.squares:
            grid_pos_x = ord(square.pos[0]) - ord('A')
            grid_pos_y = int(square.pos[1]) - 1
            if square.occupying_piece:    
                self.board_space[grid_pos_y][grid_pos_x] = 1 if square.occupying_piece.COLOR == 'W' else 2
            else:
                self.board_space[grid_pos_y][grid_pos_x] = 0

    def check_winner(self):
        print(self.board_space)
        b = self.board_space
        for player in (1,2):
            for i in range(4):
                if np.all(b[i, :] == player) or np.all(b[:, i] == player):
                    return player
            if np.all(np.diag(b) == player) or np.all(np.diag(np.fliplr(b)) == player):
                return player
        return None

    def display_winner(self, winner, display):
        color_name = "White" if winner == 1 else "Black"
        print("Congratulations! %s is the winner!" % color_name)

        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        display.blit(overlay, (0, 0))

        font_large = pygame.font.SysFont(None, 80)
        font_btn = pygame.font.SysFont(None, 48)

        title_surf = font_large.render(f"{color_name} Wins!", True, (255, 215, 0))
        title_rect = title_surf.get_rect(center=(self.width // 2, self.height // 2 - 60))
        display.blit(title_surf, title_rect)

        btn_rect = pygame.Rect(0, 0, 220, 60)
        btn_rect.center = (self.width // 2, self.height // 2 + 60)
        pygame.draw.rect(display, (70, 130, 180), btn_rect, border_radius=10)
        btn_surf = font_btn.render("Continue", True, (255, 255, 255))
        display.blit(btn_surf, btn_surf.get_rect(center=btn_rect.center))

        pygame.display.update()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if btn_rect.collidepoint(event.pos):
                        waiting = False

    def draw_capture_tracker(self, display):
        pip_size = 40
        pip_gap = 6
        pad = 10
        total_w = 3 * pip_size + 2 * pip_gap
        bg_color = (55, 57, 70)
        empty_color = (130, 130, 140)
        locked_border = (100, 100, 110)
        unlocked_border = (255, 215, 0)

        for color in ('W', 'B'):
            start_x = pad if color == 'W' else self.width - pad - total_w
            border_color = unlocked_border if self.can_capture[color] else locked_border

            for i in range(3):
                slot_x = start_x + i * (pip_size + pip_gap)
                slot_rect = pygame.Rect(slot_x, pad, pip_size, pip_size)
                pygame.draw.rect(display, bg_color, slot_rect, border_radius=4)
                pygame.draw.rect(display, border_color, slot_rect, 2, border_radius=4)

                if i < len(self.deployed_pieces[color]):
                    scaled = pygame.transform.smoothscale(
                        self.deployed_pieces[color][i].img, (pip_size, pip_size)
                    )
                    display.blit(scaled, slot_rect.topleft)
                else:
                    pygame.draw.circle(display, empty_color, slot_rect.center, pip_size // 4, 2)

    def reset(self):
        self.pieces = []
        self.board_space = np.zeros((4, 4))
        self.selected_piece = None
        self.turn = 'W'
        for square in self.squares:
            square.occupying_piece = None
        self.can_capture = {'W': False, 'B': False}
        self.pieces_deployed = {'W': 0, 'B': 0}
        self.deployed_pieces = {'W': [], 'B': []}
        self.clear_board_flag = False
        self.game_over_flag = False
        self.initialize_bench_flag = True
