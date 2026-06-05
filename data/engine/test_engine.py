from GameEngine import GameEngine

# sv = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1]

if __name__ == "__main__":
    engine = GameEngine()
    state = engine.reset()
    print(state)
    matrix = engine.sv_to_matrix()
    print(matrix)
    legal_moves = engine.get_legal_actions(state)
    print(legal_moves)
    state_test = [0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,1]
    matrix = engine.sv_to_matrix(state_test)
    print(matrix)
    legal_moves = engine.get_legal_actions(state_test)
    print(legal_moves)