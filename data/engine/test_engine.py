from GameEngine import GameEngine

if __name__ == "__main__":
    engine = GameEngine()
    state = engine.reset()
    print(state)
    matrix = engine.sv_to_matrix()
    print(matrix)
    legal_moves = engine.get_legal_actions(state)
    print(legal_moves)