import numpy as np
import sys
#from data.engine.GameEngine import GameEngine
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
def gen_random_endstate():
    pass

def is_game_over(board):
    for player in (1,2):
        for i in range(4):
            if np.all(board[i, :] == player) or np.all(board[:, i] == player):
                    return player
            if np.all(np.diag(board) == player) or np.all(np.diag(np.fliplr(board)) == player):
                return player
    return None

def _test_is_game_over():
    wins = [
        ('1s row 0, 2s row 1',    np.array([[1,1,1,1], [2,2,2,0], [2,0,0,0], [0,0,0,0]], dtype=np.int8)),
        ('1s row 1, 2s row 0',    np.array([[2,2,2,0], [1,1,1,1], [2,0,0,0], [0,0,0,0]], dtype=np.int8)),
        ('1s row 2, 2s row 3',    np.array([[0,0,0,0], [0,0,0,2], [1,1,1,1], [0,2,2,2]], dtype=np.int8)),
        ('1s row 3, 2s row 2',    np.array([[0,0,0,0], [0,0,0,2], [2,2,2,0], [1,1,1,1]], dtype=np.int8)),
        ('1s col 0, 2s col 1',    np.array([[1,0,0,0], [1,2,2,0], [1,2,0,0], [1,2,0,0]], dtype=np.int8)),
        ('1s col 1, 2s col 0',    np.array([[2,1,0,0], [0,1,2,0], [2,1,0,0], [2,1,0,0]], dtype=np.int8)),
        ('1s col 2, 2s col 3',    np.array([[0,2,1,0], [0,0,1,2], [0,0,1,2], [0,0,1,2]], dtype=np.int8)),
        ('1s col 3, 2s col 2',    np.array([[0,2,0,1], [0,0,2,1], [0,0,2,1], [0,0,2,1]], dtype=np.int8)),
        ('1s main, 2s anti',      np.array([[1,0,2,0], [0,1,2,0], [0,2,1,0], [2,0,0,1]], dtype=np.int8)),
        ('1s anti, 2s main',      np.array([[0,2,0,1], [0,2,1,0], [0,1,2,0], [1,0,0,2]], dtype=np.int8)),
    ]
    draws = [
        ('three in a row each', np.array([[1,1,1,0], [2,2,2,0], [0,0,0,0], [2,0,0,1]], dtype=np.int8)),
        ('diagonal broken',     np.array([[1,0,0,2], [0,1,2,0], [0,2,1,0], [1,0,0,2]], dtype=np.int8)),
    ]

    for label, board in wins:
        winner = is_game_over(board)
        assert winner in (1, 2), f'{label}: expected a winner, got {winner}\n{board}'
    for label, board in draws:
        winner = is_game_over(board)
        assert winner is None, f'{label}: expected None, got {winner}\n{board}'
    print(f'{len(wins) + len(draws)} cases passed')

if __name__ == "__main__":
    _test_is_game_over()