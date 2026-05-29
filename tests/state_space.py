"""
State-space exploration for Tic-Tac-Chess piece placement.

Question: how many distinct ways can we place the 8 unique pieces
(W/B Pawn, Rook, Knight, Bishop) on a 4x4 board, ignoring replacement by game rules?

Because every piece is distinguishable, placing k of them on the 16
squares is an *ordered selection without replacement* — a permutation:

    P(16, k) = 16 * 15 * ... * (16 - k + 1) = 16! / (16 - k)!

For all 8 pieces:  P(16, 8) = 518,918,400.

If all white pieces were identical and all black pieces were identical,
then we could calculate a combination of the two that would drop this value dramatically:
    C(16, k) = 16 * 15 * ... * (k^2 * (k-1)^2 * ... * 1^2) = 16! / ((16-k)! * k!)
    C(16,4) * C(12,4) = 900,900

This script does two things:
  1. EMPIRICALLY enumerates placements for small k (actually generating
     them with itertools) and checks the count equals P(16, k).
  2. GRAPHS the closed-form curve for k = [0,8] on a log scale, alongside
     the indistinguishable-pieces count for contrast.

Run:  .venv/Scripts/python.exe tests/state_space.py
"""

from itertools import permutations, combinations
from math import perm, comb
from pathlib import Path

BOARD_SQUARES = 16   # 4 x 4
N_PIECES      = 8    # 4 white + 4 black, each unique

# Enumerate for real only while the count stays cheap to materialize.
# P(16, 5) = 524,160 (fast); P(16, 6) = 5.7M starts to drag.
EMPIRICAL_MAX_K = 6


def empirical_count(k: int) -> int:
    """Brute-force count of ordered placements of k unique pieces.

    Each permutation of k squares (out of 16) is one distinct assignment:
    piece_0 -> squares[0], piece_1 -> squares[1], ...  We never store them;
    we just count, so memory stays flat.
    """
    return sum(1 for _ in permutations(range(BOARD_SQUARES), k))


def verify_formula() -> None:
    """The actual test: enumeration must match the closed form."""
    print(f"{'k':>2} | {'enumerated':>12} | {'P(16,k)':>12} | match")
    print("-" * 44)
    for k in range(EMPIRICAL_MAX_K + 1):
        got      = empirical_count(k)
        expected = perm(BOARD_SQUARES, k)
        ok       = got == expected
        assert ok, f"mismatch at k={k}: {got} != {expected}"
        print(f"{k:>2} | {got:>12,} | {expected:>12,} | {'OK' if ok else 'FAIL'}")
    print(f"\nFull placement (k=8): P(16,8) = {perm(BOARD_SQUARES, N_PIECES):,}")


def graph(out_path: Path) -> None:
    """Log-scale plot of the state-space growth, distinguishable vs not."""
    import matplotlib
    matplotlib.use("Agg")          # headless: write a file, don't open a window
    import matplotlib.pyplot as plt

    ks = list(range(N_PIECES + 1))

    # Distinguishable pieces: ordered selection -> permutations.
    distinguishable = [perm(BOARD_SQUARES, k) for k in ks]

    # Indistinguishable within color: choose squares for whites, then for
    # blacks, from what remains. Split k as evenly as the game would (W first).
    def indistinct(k: int) -> int:
        w = (k + 1) // 2          # whites placed first
        b = k - w
        return comb(BOARD_SQUARES, w) * comb(BOARD_SQUARES - w, b)

    indistinguishable = [indistinct(k) for k in ks]

    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.plot(ks, distinguishable, "o-", label="Distinguishable pieces  P(16,k)")
    ax.plot(ks, indistinguishable, "s--", label="Indistinguishable within color")
    ax.set_yscale("log")
    ax.set_xlabel("number of pieces placed (k)")
    ax.set_ylabel("distinct board configurations  (log scale)")
    ax.set_title("Tic-Tac-Chess placement state space on a 4x4 board")
    ax.grid(True, which="both", ls=":", alpha=0.5)
    ax.legend()

    # Annotate the headline number.
    full = perm(BOARD_SQUARES, N_PIECES)
    ax.annotate(f"{full:,}",
                xy=(N_PIECES, full),
                xytext=(N_PIECES - 2.6, full / 18),
                arrowprops=dict(arrowstyle="->"))

    fig.tight_layout()
    fig.savefig(out_path, dpi=130)
    print(f"\nGraph written to {out_path}")


if __name__ == "__main__":
    verify_formula()
    graph(Path(__file__).with_name("state_space.png"))
