import unittest
from data.engine.GameEngine import GameEngine

class TestGameEngine(unittest.TestCase):

    def setUp(self):
        self.engine = GameEngine()
        self.initial_state = self.engine.reset()

    def test_reset_returns_correct_state_length(self):
        self.assertEqual(len(self.initial_state), 29)

    def test_reset_board_is_empty(self):
        board = self.initial_state[:16]
        self.assertTrue(all(sq == 0 for sq in board))

    def test_reset_turn_is_white(self):
        self.assertEqual(self.initial_state[24], 0)
    
    def test_sv_to_matrix_shape(self):
        matrix = self.engine.sv_to_matrix()
        rows = matrix.strip().split("\n")
        self.assertEqual(len(rows), 4)

    def test_get_legal_actions_bench_deploy(self):
        # All pieces on bench at start → legal moves are placements on empty squares
        state = self.initial_state
        legal = self.engine.get_legal_actions(state)
        self.assertIsInstance(legal, list)
        self.assertTrue(len(legal) > 0)

    def test_get_legal_actions_known_state(self):
        # White pawn at index 0, moving forward (col +1 = index 1)
        state = [1,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0,     # board
                 1,0,0,0, 0,0,0,0,                       # bench
                 0,                                      # turn = W
                 0,0,                                    # can_capture
                 0,1]                                    # pawn_reverse
        legal = self.engine.get_legal_actions(state)
        expected_pawn_move = GameEngine.PAWN * 16 + 1   # dest index 1
        self.assertIn(expected_pawn_move, legal)


    def test_get_legal_actions_known_state_2(self):
        state = [0,1,0,0, 2,0,5,0, 0,6,0,0, 0,0,0,0, 
                 1,1,0,0, 1,1,0,0,
                 0,
                 0,0,
                 0,1]
        legal = self.engine.get_legal_actions(state)
        expected_game_state = [2, 16, 21, 24, 28, 32, 34, 35, 37, 39, 40, 42, 43, 44, 45, 46, 47, 48, 50, 51, 53, 55, 56, 58, 59, 60, 61, 62, 63]
        self.assertEqual(expected_game_state, legal)

    def test_get_legal_actions_known_state_3(self):
        state = [0,1,0,0, 2,0,5,0, 0,0,0,0, 0,6,0,0, 
                 1,1,0,0, 1,1,0,0,
                 0,
                 1,1,
                 0,1]
        legal = self.engine.get_legal_actions(state)
        expected_game_state = [2, 6, 16, 21, 22, 24, 28, 32, 34, 35, 37, 39, 40, 41, 42, 43, 44, 46, 47, 48, 50, 51, 53, 55, 56, 57, 58, 59, 60, 62, 63]
        self.assertEqual(expected_game_state, legal)

    def test_get_legal_actions_known_state_4(self):
        state = [0,1,0,0, 2,0,5,0, 0,0,0,0, 0,6,0,0, 
                 1,1,0,0, 1,1,0,0,
                 1,
                 1,1,
                 0,1]
        legal = self.engine.get_legal_actions(state)
        expected_game_state = [1, 5, 17, 21, 25, 28, 30, 31, 32, 34, 35, 37, 39, 40, 41, 42, 43, 44, 46, 47, 48, 50, 51, 53, 55, 56, 57, 58, 59, 60, 62, 63]
        self.assertEqual(expected_game_state, legal)

if __name__ == "__main__":
    unittest.main()