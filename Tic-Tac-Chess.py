import pygame

from data.classes.Board import Board

# pygame setup
pygame.init()

# The dimensions are still relatively hard-coded because of how Square offsets are calculated in Board and Square.py
# Modify with EXTREME caution
WINDOW_SIZE = (1280, 720)
screen = pygame.display.set_mode(WINDOW_SIZE)

board = Board(WINDOW_SIZE[0], WINDOW_SIZE[1])

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
        if board.initialize_bench_flag:
            board.initialize_bench(board, left_bench, right_bench, display)
            board.draw_capture_tracker(display)
            pygame.display.update()
            board.initialize_bench_flag = False

        # Redraws all pieces whenever a piece has moved; also checks for winner.
        if board.clear_board_flag:
            draw_clear_board(display)
            board.draw_pieces(display)
            board.draw_capture_tracker(display)
            pygame.display.update()
            board.clear_board_flag = False
            winner = board.check_winner()
            if winner:
                board.display_winner(winner, display)
                board.reset()
                draw_clear_board(display)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Left mouse button
                    mouse_pos = pygame.mouse.get_pos()
                    selected_square = board.get_square_at(mouse_pos)

                    if board.selected_piece:
                        p = board.selected_piece
                        board.selected_piece = None
                        is_board_square = selected_square is not None and not selected_square.startswith("bench") # Need to check for bench because they're not actually saved as "Square" objects
                        is_valid = is_board_square and (p.on_bench or selected_square in p.valid_moves)

                        # If the move is not valid (get rid of highlights), or the move action is successful (move pieces), we need to redraw the board. 
                        if not is_valid or p.move(board, selected_square):
                            board.clear_board_flag = True
                    else:
                        board.selected_piece = board.get_piece_at(mouse_pos)
                        if board.selected_piece:
                            board.highlight_square(display)
                            pygame.display.update()

                # Store the board_state in a 4x4 matrix in Board.py
                board.update_board_space()
                        
pygame.quit()