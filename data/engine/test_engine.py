from GameEngine import GameEngine

if __name__ == "__main__":
    engine = GameEngine()
    state = engine.reset()
    print(state)
    matrix = engine.sv_to_matrix()
    print(matrix)
    legal_moves = engine.get_legal_actions(state)
    print(legal_moves)
    state_test = [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1]
    legal_moves = engine.get_legal_actions(state_test)
    print(legal_moves)