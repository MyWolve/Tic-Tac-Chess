'''
Docstring for Tic-Tac-Chess

This project is inspired by this video on the Connect 4 state space (https://www.youtube.com/watch?v=i9pBeuBeupY&t=501s)
The idea being that we can calculate and visualize 'weak' and 'strong' solutions to this game. 

Tic-Tac-Chess is a small, modified, combination of both Tic-Tac-Toe and Chess and often referred to as "Tic-Tac-Chec" (https://www.bing.com/videos/riverview/relatedvideo?q=tic-tac-chess&mid=9325761329D683062C2B9325761329D683062C2B&FORM=VIRE)

The game is played on a 4x4 checkered board between 2 players: alternating turns between moves. 
Each player has 4 unique pieces:
    - Pawn
    - Bishop
    - Rook
    - Knight
which move exactly as they do in Chess. Except, the pawn reverses direction when it reaches the other side of the board. 

A player may either play (place on the board) an unplaced piece on any empty square on the board **or** move one of their pieces already on the board on their turn. But a player may only move a piece once they have
atleast 3 of their own pieces on the board.

Captured pieces are removed from the board and may be played on subsequent turns to any empty square on the board. 

The goal of Tic-Tac-Chess is to lay out your pieces so that they form 4 pieces in a row, column, or diagonal, just like in Tic-Tac-Toe. 
'''
import pygame

from data.classes.Board import Board

# pygame setup
pygame.init()

WINDOW_SIZE = (1280, 720)
screen = pygame.display.set_mode(WINDOW_SIZE)

board = Board(WINDOW_SIZE[0], WINDOW_SIZE[1])

initialize_bench_flag = True
clear_board_flag = False

# Resets the screen and draws an empty board and benches
def draw_clear_board(display):
    display.fill((40, 42, 54))
    board.draw_board(display)
    left_bench, right_bench = board.draw_bench(display)
    pygame.display.update()
    return left_bench, right_bench, display

if __name__ == "__main__":
    running = True
    left_bench, right_bench, display = draw_clear_board(screen)
    while running:

        # Runs once at game_onset to fill both benches
        if initialize_bench_flag:
            board.initialize_bench(board, left_bench, right_bench, display)
            pygame.display.update()
            initialize_bench_flag = False

        # Clears board --- enabled whenever a piece needs to be redrawn (moved, etc.)
        if clear_board_flag:
            draw_clear_board(display)
            clear_board_flag = False


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        

pygame.quit()