import numpy as np

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

        self.turn             = self.W
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

        return np.array(board_enc + bench_enc + turn + capture + reverse, dtype=np.float32)
    
    def step(self, action):
        pass

    def sv_to_matrix(self):
        """From the state vector, get a matrix visualization"""
        sv = self.get_state()
        #sv = [0, 1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        board = sv[:16]
        matrix = np.array(board).reshape(4,4)
        return matrix



