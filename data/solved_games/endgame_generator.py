"""4x4 boards holding exactly one each of pieces 1-8, every other cell 0.

Pieces 1-4 belong to player 1, pieces 5-8 to player 2. A player holds a "line"
when all four of their pieces sit on one full row, column, or diagonal.
Ten lines exist: 4 rows, 4 columns, 2 diagonals.

Every board falls in exactly one of three buckets:

    0 lines   fine. game continues, or ended with nobody connecting.
    1 line    fine. that player has WON.
    2 lines   impossible. one move only ever touches the mover's own piece,
              so no single move completes both players at once. Whoever
              connected first ended the game before this position existed.

Two is the ceiling. Each player owns exactly 4 pieces, so neither can hold
more than one line.

Size warning: the full space is 16!/8! = 518,918,400 boards, about 8.3 GB at
int8. generate_all() is a generator for that reason. If you want the won or
the two-line boards, use generate_won() / generate_two_lines(), which build
them directly instead of walking half a billion boards to find 0.01% of them.
"""

from itertools import combinations, permutations

import numpy as np

N_ROWS = N_COLS = 4
N_CELLS = N_ROWS * N_COLS
PIECES = np.arange(1, 9, dtype=np.int8)
P1, P2 = (1, 2, 3, 4), (5, 6, 7, 8)


def _build_lines():
    """(10, 4) flat cell indices, one row per line."""
    grid = np.arange(N_CELLS).reshape(N_ROWS, N_COLS)
    rows = [grid[r, :] for r in range(N_ROWS)]
    cols = [grid[:, c] for c in range(N_COLS)]
    diags = [np.diag(grid), np.diag(grid[:, ::-1])]
    return np.array(rows + cols + diags, dtype=np.intp)


LINES = _build_lines()

# Same lines as a 0/1 matrix. Turns "does this player own all 4 cells of some
# line" into one matmul, which is what makes big stacks tractable.
LINE_MASKS = np.zeros((len(LINES), N_CELLS), dtype=np.uint8)
for _i, _cells in enumerate(LINES):
    LINE_MASKS[_i, _cells] = 1


def generate_all():
    """Yield every board, one at a time. 518,918,400 of them.

    permutations() over cells rather than over pieces: the i-th chosen cell
    receives piece i+1, so the ordering is the piece assignment and each board
    comes out exactly once.
    """
    for cells in permutations(range(N_CELLS), 8):
        flat = np.zeros(N_CELLS, dtype=np.int8)
        flat[list(cells)] = PIECES
        yield flat.reshape(N_ROWS, N_COLS)


def has_line(flat, player):
    """(M,) bool over a stack of flattened boards."""
    lo, hi = (1, 4) if player == 1 else (5, 8)
    occ = ((flat >= lo) & (flat <= hi)).astype(np.uint8)
    return (occ @ LINE_MASKS.T == 4).any(axis=1)


def count_lines(boards):
    """(M,) number of lines present on each board: 0, 1, or 2."""
    flat = np.asarray(boards).reshape(-1, N_CELLS)
    return has_line(flat, 1).astype(np.int8) + has_line(flat, 2).astype(np.int8)


def winner(board):
    """1, 2, or None. Returns None for a two-line board, which has no winner
    because it is not a position any game reaches."""
    flat = np.asarray(board).reshape(1, N_CELLS)
    w1, w2 = has_line(flat, 1)[0], has_line(flat, 2)[0]
    if w1 and w2:
        return None
    if w1:
        return 1
    if w2:
        return 2
    return None


def sort_states(boards):
    """Split a stack into (open, won, two_lines).

    open      : no line. legal.
    won       : exactly one line. legal, that player won.
    two_lines : both players lined up. impossible.
    """
    boards = np.asarray(boards).reshape(-1, N_ROWS, N_COLS)
    n = count_lines(boards)
    return boards[n == 0], boards[n == 1], boards[n == 2]


# ------------------------------------------------- direct bucket construction

def _arrangements(free_cells, pieces):
    """Every injective placement of `pieces` into `free_cells`, as (M, 16)."""
    places = np.array(list(permutations(range(len(free_cells)), len(pieces))),
                      dtype=np.intp)
    out = np.zeros((len(places), N_CELLS), dtype=np.int8)
    np.put_along_axis(out, free_cells[places], np.array(pieces, np.int8), axis=1)
    return out


def generate_won(exactly_one=True):
    """All boards where someone holds a line. 5,672,448 with exactly_one.

    Built by placing the winner's four pieces on a line, then scattering the
    loser's four over the remaining twelve cells. With exactly_one, boards
    where the loser also lined up are dropped, so this returns only legal
    won positions.
    """
    blocks = []
    for win_player, lose_player in ((1, 2), (2, 1)):
        win_pieces = P1 if win_player == 1 else P2
        lose_pieces = P2 if win_player == 1 else P1
        for line in LINES:
            free = np.setdiff1d(np.arange(N_CELLS, dtype=np.intp), line)
            losers = _arrangements(free, lose_pieces)
            for perm in permutations(win_pieces):
                block = losers.copy()
                block[:, line] = np.array(perm, dtype=np.int8)
                blocks.append(block)
    out = np.concatenate(blocks)
    if exactly_one:
        out = out[count_lines(out) == 1]
    else:
        # Both families contain the two-line boards, so drop the duplicates.
        out = np.unique(out, axis=0)
    return out.reshape(-1, N_ROWS, N_COLS)


def generate_two_lines():
    """The 14,976 impossible boards: both players lined up.

    Only disjoint line pairs qualify, since the two lines need 8 distinct
    cells. On a 4x4 that is 6 row pairs, 6 column pairs, and the two diagonals,
    which miss each other because there is no centre square.
    """
    boards = []
    for a, b in combinations(range(len(LINES)), 2):
        if np.intersect1d(LINES[a], LINES[b]).size:
            continue
        for cells_1, cells_2 in ((LINES[a], LINES[b]), (LINES[b], LINES[a])):
            for perm_1 in permutations(P1):
                for perm_2 in permutations(P2):
                    flat = np.zeros(N_CELLS, dtype=np.int8)
                    flat[cells_1] = perm_1
                    flat[cells_2] = perm_2
                    boards.append(flat)
    return np.stack(boards).reshape(-1, N_ROWS, N_COLS)


if __name__ == "__main__":
    won = generate_won()
    two = generate_two_lines()
    total = 518_918_400

    print(f"total boards      {total:>12,}")
    print(f"  no line         {total - len(won) - len(two):>12,}")
    print(f"  one line (won)  {len(won):>12,}")
    print(f"  two lines (bad) {len(two):>12,}")

    print("\nexample won board:")
    print(won[0], "  winner:", winner(won[0]))
    print("\nexample two-line board:")
    print(two[0], "  winner:", winner(two[0]))