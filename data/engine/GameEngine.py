class GameEngine:
    """
    Standard RL environment interface:
        state                = engine.reset()
        state, reward, done  = engine.step(action)
        legal_actions        = engine.get_legal_actions()

    State vector (length 29, we can initialize it Sv_0 = [0_0, 0_1, 0_2, ..., 1_25]):
        [0:16]  board   — 0=empty, 1-4=W piece by type, 5-8=B piece by type
        [16:24] bench   — binary flags (0=on_bench), W pieces [0:4] then B pieces [4:8]
        [24]    turn    — 0=W, 1=B
        [25:27] capture — binary, [W_can_capture, B_can_capture]
        [27:29] pawn    — binary, [W_reverse, B_reverse]

    Action encoding:
        action = piece_type * 16 + dest_row * 4 + dest_col
        piece_type: 0=Pawn, 1=Rook, 2=Knight, 3=Bishop
    """

    # Piece value for action encoding
    PAWN, ROOK, KNIGHT, BISHOP = 0, 1, 2, 3

    W, B = 0, 1
    STATE_SIZE = 29

    def reset(self):
        """Reset to start-of-game. Returns initial state vector."""
        # board[row][col] = (player, piece_type) or None
        self.board = [[None] * 4 for _ in range(4)]

        # on_bench[player][piece_type] — True until deployed (or after capture)
        self.on_bench = [[0] * 4, [0] * 4]

        # piece_pos[player][piece_type] = (col, row) when on board, else None
        self.piece_pos = [[None] * 4, [None] * 4]

        self.turn             = 0
        self.pieces_deployed  = [0, 0]
        self.can_capture      = [0, 0]

        # Pawn bounce: False=forward (col+1), True=reverse (col-1).
        # W starts advancing toward col D; B starts advancing toward col A.
        self.pawn_reverse = [0, 1]

        return self.get_state()
    
    def get_state(self):
        """Encode the full game state as a float32 numpy vector."""
        board_enc = []
        for row in range(4):
            for col in range(4):
                cell = self.board[row][col]
                if cell is None:
                    board_enc.append(0)
                else:
                    # W → 1..4, B → 5..8
                    board_enc.append(cell)

        bench_enc = (
            # pt = piece_type
            [int(self.on_bench[self.W][pt]) for pt in range(4)] +
            [int(self.on_bench[self.B][pt]) for pt in range(4)]
        )

        turn = [self.turn]

        capture = [
            int(self.can_capture[self.W]),
            int(self.can_capture[self.B])
        ]

        reverse = [
            int(self.pawn_reverse[self.W]),
            int(self.pawn_reverse[self.B])
        ]

        return board_enc + bench_enc + turn + capture + reverse
    
    def step(self, action):
        """
        Implements the action, steps the world forward a time step, and returns:
            @sv - updated world state
            @reward - reward earned (+1, 0)
            @done - is the game over?
        """
        pass

    def get_legal_actions(self, state):
        """Return legal actions given a board state"""
        board = state[:16]
        turn = int(state[24])
        can_capture = state[25:27]
        p_reverse = state[27:29]
        
        def _pawn_moves(board, turn, can_capture, p_reverse):
            p_val = 1 if turn == 0 else 5
            valid_moves = []

            for i, square in enumerate(board):
                # If Pawn is on the board
                if square == p_val:
                    # If p_reverse == 0: (Pawn moves forward)
                    if p_reverse[turn] == 0:
                        # Next square empty?
                        try: 
                            if board[i + 1] == 0:
                                # Yes - Go ahead
                                valid_moves.append(self.PAWN * 16 + i + 1)
                        except IndexError:
                            continue

                        # Anyone on the diagonal -> top-right
                        try:
                            if board[i - 3] and board[i - 3] != 0:
                                # If pawn is white
                                if p_val == 1:
                                    # If piece is black -> top-right
                                    if board[i-3] in range(5,9) if turn == 0 else range(1,5):
                                        if can_capture[turn]:   
                                            valid_moves.append(self.PAWN * 16 + i - 3)
                        except IndexError:
                            continue
                        
                        # Anyone on the diagonal -> bottom-right
                        try:
                            if board[i + 5] and board[i + 5] != 0:
                                # If piece is black -> bottom-right
                                if board[i+5] in range(5,9) if turn == 0 else range(1,5):
                                    if can_capture[turn]:
                                        valid_moves.append(self.PAWN * 16 + i + 5)
                        except IndexError:
                            continue

                    # reverse == 1
                    elif p_reverse[turn] == 1:

                        # Next square empty?
                        try:
                            if board[i-1] == 0:
                                valid_moves.append(self.PAWN * 16 + i - 1)
                        except IndexError:
                            continue
                        
                        # Anyone on the diagonal? top-left
                        try:
                            if board[i - 5] and board[i - 5] != 0:
                                # If piece is white -> top-left
                                if board[i-5] in range(1,5) if turn == 1 else range(5,9):
                                    if can_capture[turn]:
                                        valid_moves.append(self.PAWN * 16 + i - 5)
                        except IndexError:
                            continue
                        
                        # Anyone on the diagonal? bottom-left
                        try:
                            if board[i + 3] and board[i + 3] != 0:
                            # If piece is white -> bottom-left
                                if board[i+3] in range(1,5) if turn == 1 else range(5,9):
                                    if can_capture[turn]:
                                        valid_moves.append(self.PAWN * 16 + i + 3)
                        except IndexError:
                            continue
                        
            if p_val in board:
                return valid_moves
            else:
                return [self.PAWN * 16 + i for i, sq in enumerate(board) if sq == 0]


        def _rook_moves(board, turn, can_capture):
            p_val = 2 if turn == 0 else 6
            enemy = range(5, 9) if turn == 0 else range(1, 5)
            valid_moves = []

            for i, square in enumerate(board):
                if square == p_val:
                    row_start = (i // 4) * 4

                    # Left: nearest to farthest
                    for j in range(i - 1, row_start - 1, -1):
                        if board[j] != 0:
                            if board[j] in enemy and can_capture[turn]:
                                valid_moves.append(self.ROOK * 16 + j)
                            break
                        valid_moves.append(self.ROOK * 16 + j)

                    # Right: nearest to farthest
                    for j in range(i + 1, row_start + 4):
                        if board[j] != 0:
                            if board[j] in enemy and can_capture[turn]:
                                valid_moves.append(self.ROOK * 16 + j)
                            break
                        valid_moves.append(self.ROOK * 16 + j)

                    # Up: nearest to farthest
                    for j in range(i - 4, -1, -4):
                        if board[j] != 0:
                            if board[j] in enemy and can_capture[turn]:
                                valid_moves.append(self.ROOK * 16 + j)
                            break
                        valid_moves.append(self.ROOK * 16 + j)

                    # Down: nearest to farthest
                    for j in range(i + 4, 16, 4):
                        if board[j] != 0:
                            if board[j] in enemy and can_capture[turn]:
                                valid_moves.append(self.ROOK * 16 + j)
                            break
                        valid_moves.append(self.ROOK * 16 + j)

            if p_val in board:
                return valid_moves
            # Piece is on bench
            else:
                return [self.ROOK * 16 + i for i, sq in enumerate(board) if sq == 0]


        def _knight_moves(board, turn, can_capture):
            p_val = 3 if turn == 0 else 7
            for square in board:
                if square == p_val:
                    pass
                    # While squares to check:
                        # If square to the right-up:
                            # Is empty?:
                                # Yes - Go ahead
                            # can_capture?:
                                # Yes - Go ahead
                            # No - Not a valid move
                        # elif square to the right-down:
                            # Is empty?:
                                # Yes - Go ahead
                            # can_capture?:
                                # Yes - Go ahead
                            # No - Not a valid move
                        # elif squares to the bottom-left:
                            # Is empty?:
                                # Yes - Go ahead
                            # can_capture?:
                                # Yes - Go ahead
                            # No - Not a valid move
                        # elif squares to the bottom-right:
                        # Is empty?:
                            # Yes - Go ahead
                        # can_capture?:
                            # Yes - Go ahead
                        # No - Not a valid move
                        # elif square to the left-up:
                            # Is empty?:
                                # Yes - Go ahead
                            # can_capture?:
                                # Yes - Go ahead
                            # No - Not a valid move
                        # elif square to the left-down:
                            # Is empty?:
                                # Yes - Go ahead
                            # can_capture?:
                                # Yes - Go ahead
                            # No - Not a valid move
                         # elif square to the top-left:
                            # Is empty?:
                                # Yes - Go ahead
                            # can_capture?:
                                # Yes - Go ahead
                            # No - Not a valid move
                             # elif square to the top-right:
                            # Is empty?:
                                # Yes - Go ahead
                            # can_capture?:
                                # Yes - Go ahead
                            # No - Not a valid move

                    return None # Temporary return statement
                
            # Piece is on bench
            return [self.KNIGHT * 16 + i for i, square in enumerate(board) if square == 0]
        
        def _bishop_moves(board, turn, can_capture):
            p_val = 4 if turn == 0 else 8
            for square in board:
                if square == p_val:
                    pass
                    # While squares to check:
                        # If squares to the top-right:
                            # is empty?
                                # Yes- Go ahead
                            # can_capture?
                                # Yes - Go ahead
                            # No - Not a valid move
                        # elif squares to the top-left:
                            # is empty?
                                # Yes- Go ahead
                            # can_capture?
                                # Yes - Go ahead
                            # No - Not a valid move
                        # elif squares to the bottom-right:
                            # is empty?
                                # Yes- Go ahead
                            # can_capture?
                                # Yes - Go ahead
                            # No - Not a valid move
                        # elif squares to the bottom-left:
                            # is empty?
                                # Yes- Go ahead
                            # can_capture?
                                # Yes - Go ahead
                            # No - Not a valid move
                    
                    return None # Temporary return statement
                
            # Piece is on bench        
            return [self.BISHOP * 16 + i for i, square in enumerate(board) if square == 0]

        
        legal_moves = []
        legal_moves += _pawn_moves(board, turn, can_capture, p_reverse) or [] # [0,15]
        legal_moves += _rook_moves(board, turn, can_capture) or []            # [16,31]
        legal_moves += _knight_moves(board, turn, can_capture) or []          # [32,47]
        legal_moves += _bishop_moves(board, turn, can_capture) or []          # [48,63]

        return legal_moves

    def sv_to_matrix(self, state_vector=None):
        """From the state vector, get a matrix visualization"""
        if state_vector is None:
            state_vector = self.get_state()
        #sv = [0, 1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        board = state_vector[:16]
        matrix = "\n".join(str(board[i*4:(i+1)*4]) for i in range(4))
        return matrix



