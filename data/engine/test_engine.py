from GameEngine import GameEngine

if __name__ == "__main__":
    engine = GameEngine()
    state = engine.reset()
    print(state)
    matrix = engine.sv_to_matrix()
    print(matrix)