import pygame

class Piece:
    def __init__(self, pos, color, board):
        self.pos = pos
        self.COLOR = color
        self.on_bench = True
        self.bench_pos = pos
        self.img = pygame.image.load("data/imgs/W_Queen.png")

        # Stores list of valid destinations as grid_square names
        self.valid_moves: list[str] = []


    def draw(self, display, board):
            slot_center = (self.pos[0] + board.tile_size // 2, self.pos[1] + board.tile_size // 2)                                                                                                                                     
            img_rect = self.img.get_rect(center=slot_center)                                                                                                                                                                 
            display.blit(self.img, img_rect)
    
    def move(self, board, destination_square):
        self.valid_moves = []
        self.get_valid_moves(board)
        if self.COLOR == board.turn and self.is_valid_move(board, destination_square):
            dest_square = next((s for s in board.squares if s.pos == destination_square), None)
            if not dest_square:
                return 1
            
            is_capture = bool(dest_square.occupying_piece and not self.on_bench)
            if is_capture:
                self.capture(dest_square)

            coords = board.get_coords(destination_square)
            if not coords:
                return 1

            # Clear source square before moving
            for s in board.squares:
                if s.occupying_piece is self:
                    s.occupying_piece = None

            deploying_from_bench = self.on_bench
            self.pos = coords
            self.on_bench = False
            dest_square.occupying_piece = self

            board.record_move(self, destination_square, is_capture, deploying_from_bench)

            if deploying_from_bench:
                board.pieces_deployed[self.COLOR] += 1
                if len(board.deployed_pieces[self.COLOR]) < 3:
                    board.deployed_pieces[self.COLOR].append(self)
                if board.pieces_deployed[self.COLOR] >= 3:
                    board.can_capture[self.COLOR] = True
            board.clear_board_flag = True
            board.turn = 'B' if board.turn == 'W' else 'W'
            print("It is %s's turn!" % board.turn)
            self.valid_moves = []
        else:
            print("Error: Not a Valid Move!")
            return 1
    
    def capture(self, destination_square):
        try: 
            destination_square.occupying_piece.bench()
            destination_square.occupying_piece = None
        except AttributeError:
            print("You passed me an empty square, you bastard!")
            return 1
        
    def bench(self):
         self.pos = self.bench_pos
         self.on_bench = True
        
    # Overwritten by Children for specific Piece implementations
    def get_valid_moves(self, board):
         pass

    def is_valid_move(self, board, destination_square):
        for square in board.squares:
            if square.pos == destination_square:
                #if square.occupying_piece:
                occSquare = square
        if destination_square in self.valid_moves:
            if self.on_bench:
                if occSquare.occupying_piece:
                    return False
                else:
                    return True
            else:
                if occSquare.occupying_piece and occSquare.occupying_piece.COLOR == self.COLOR:
                    return False
                if occSquare.occupying_piece and not board.can_capture[self.COLOR]:
                    return False
                return True
        else:
            return False
         