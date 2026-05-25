# Tic-Tac-Chess

Inspired by [this video on the Connect 4 state space](https://www.youtube.com/watch?v=i9pBeuBeupY&t=501s) — and its [follow-up where he solves it](https://youtu.be/KaljD3Q3ct0?si=PEDpWkrTm9bgnV5n) — the goal of this project is to calculate and visualize the weak and strong solutions to Tic-Tac-Chess, a compact chess/Tic-Tac-Toe hybrid sometimes called ["Tic-Tac-Chec"](https://www.bing.com/videos/riverview/relatedvideo?q=tic-tac-chess&mid=9325761329D683062C2B9325761329D683062C2B&FORM=VIRE).

The smaller board and restricted piece set make this a more tractable state space to enumerate than standard chess, while the hybrid rules introduce enough complexity to make the solution non-trivial.

---

## The Game

Tic-Tac-Chess is played on a 4×4 checkered board between two players, alternating turns.

Each player has 4 pieces — a **Pawn**, **Bishop**, **Rook**, and **Knight** — held on a bench beside the board at the start of the game. Pieces move exactly as they do in chess, with one exception: **Pawns reverse direction when they reach the far edge of the board** rather than promoting.

**Turn structure:**
- On your turn you may either deploy an unplaced piece from your bench to any empty square, or move a piece already on the board.

**Captures:**
- Capturing is only enabled once you have **deployed at least 3 pieces**.
- A captured piece is returned to its owner's bench and may be placed on an empty square on a future turn.

**Winning:**
- Place 4 of your pieces in a row, column, or diagonal — just like Tic-Tac-Toe or Connect 4.

**Rules:**
- There are various implementations of these rules online; some with interesting features. For example, some rules allow En-Passent captures as in Chess or permit Pawns to move 2 squares on their first move. While these are not implemented in this version, I may add them as optional rules in the future. Feel free to fork this repo and try implementing these kinds of changes. 
---

## What's Built

- **Playable game** — full pygame implementation with board, benches, piece movement, and capture logic.
- **Move history logging** — each game is recorded to `data/history/` in a compact notation format (see below). A new file is created per game session.

### Move Notation

One move per line. Format: `[color][*bench][piece][x capture][destination]`

| Token | Meaning |
|---|---|
| `W` / `B` | White or Black |
| `*` | Deployed from bench |
| `P` `R` `K` `B` | Pawn, Rook, Knight, Bishop |
| `x` | Captured a piece |
| `A1`–`D4` | Destination square |

Example game excerpt:
```
W*PA1
B*RD4
W*KB2
B*BC3
WPA2
BRD3
WKxC3
```

---

## Roadmap

- [ ] Solution graph — enumerate the full game state space
- [ ] Weak solution — determine whether the first or second player wins with optimal play
- [ ] Strong solution — compute optimal play from any reachable position
- [ ] Visualization — render the state space graph

---

## Credits

Pixel-art chess pieces by [Dani Maccari (@danimaccari)](https://dani-maccari.itch.io/). All rights belong to them; their license carries forward in this project.
