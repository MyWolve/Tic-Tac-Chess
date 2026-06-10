# Running Tests

This project uses Python's `unittest` framework. Tests are located in the `tests/` directory and follow the naming convention `*_test.py`.

## Quick Start

### Method 1: Using the test runner script
```bash
python3 run_tests.py
```

### Method 2: Using unittest directly
```bash
python3 -m unittest discover -s tests -p "*_test.py" -v
```

### Method 3: Running specific test file
```bash
python3 -m unittest tests.GameEngine_test -v
```

### Method 4: Running specific test case
```bash
python3 -m unittest tests.GameEngine_test.TestGameEngine.test_reset_returns_correct_state_length -v
```

## Test Structure

- `tests/GameEngine_test.py`: Tests for the GameEngine class
  - Tests for reset() functionality
  - Tests for sv_to_matrix() functionality
  - Tests for get_legal_actions() functionality

## Expected Output

All 7 tests should pass with no errors:
```
test_get_legal_actions_bench_deploy ... ok
test_get_legal_actions_known_state ... ok
test_get_legal_actions_known_state_2 ... ok
test_reset_board_is_empty ... ok
test_reset_returns_correct_state_length ... ok
test_reset_turn_is_white ... ok
test_sv_to_matrix_shape ... ok

Ran 7 tests in 0.000s
OK
```
