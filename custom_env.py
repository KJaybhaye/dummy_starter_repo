import random
from kaggle_environments import make
from kaggle_environments.core import environments

# ==========================================
# 1. SPECIFICATION
# ==========================================
specification = {
    "action": {"type": "integer", "minimum": 0, "maximum": 8},
    "info": {},
    "observation": {
        "board": {"type": "array", "default": [0, 0, 0, 0, 0, 0, 0, 0, 0]},
        "mark": {"type": "integer", "default": 1},
    },
    "reward": {"type": "number"},
    "agents": [2],
}


# ==========================================
# 2. THE INTERPRETER
# ==========================================
def interpreter(state, env):
    # Determine whose turn it is based on the current mark
    active_agent = 0 if state[0].observation.mark == 1 else 1
    inactive_agent = 1 - active_agent

    action = state[active_agent].action
    board = state[0].observation.board

    # Handle Invalid Moves (out of bounds, empty action, or spot taken)
    if action is None or action < 0 or action > 8 or board[action] != 0:
        state[active_agent].status = "INVALID"
        state[active_agent].reward = -1
        state[inactive_agent].status = "DONE"
        state[inactive_agent].reward = 1
        return state

    # Apply the valid move
    board[action] = state[active_agent].observation.mark

    # Update observations for both agents
    state[0].observation.board = board
    state[1].observation.board = board

    # Check for a Win
    win_lines = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],  # Rows
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],  # Columns
        [0, 4, 8],
        [2, 4, 6],  # Diagonals
    ]

    won = any(
        all(board[i] == state[active_agent].observation.mark for i in line)
        for line in win_lines
    )

    if won:
        state[active_agent].status = "DONE"
        state[active_agent].reward = 1
        state[inactive_agent].status = "DONE"
        state[inactive_agent].reward = -1
        return state

    # Check for a Draw
    if all(cell != 0 for cell in board):
        state[active_agent].status = "DONE"
        state[active_agent].reward = 0
        state[inactive_agent].status = "DONE"
        state[inactive_agent].reward = 0
        return state

    # Setup the next turn
    next_mark = 2 if state[0].observation.mark == 1 else 1
    state[0].observation.mark = next_mark
    state[1].observation.mark = next_mark

    return state


# ==========================================
# 3. THE RENDERER
# ==========================================
def renderer(state, env):
    board = state[0].observation.board
    symbols = {0: " ", 1: "X", 2: "O"}

    print(f"\n {symbols[board[0]]} | {symbols[board[1]]} | {symbols[board[2]]} ")
    print("---+---+---")
    print(f" {symbols[board[3]]} | {symbols[board[4]]} | {symbols[board[5]]} ")
    print("---+---+---")
    print(f" {symbols[board[6]]} | {symbols[board[7]]} | {symbols[board[8]]} \n")


# ==========================================
# 4. REGISTRATION & TESTING
# ==========================================
def html_renderer(*args, **kwargs):
    return "<div>HTML visualization not implemented yet. Look at the terminal!</div>"


# Register the environment in kaggle_environments
environments["custom_tictactoe"] = {
    "specification": specification,
    "interpreter": interpreter,
    "renderer": renderer,
    "html_renderer": html_renderer,  # <-- Added this key
}


# Create a basic random agent
def random_agent(obs, conf):
    empty_cells = [i for i, cell in enumerate(obs.board) if cell == 0]
    return random.choice(empty_cells) if empty_cells else None


# Create a naive agent that picks the first available spot
def first_empty_agent(obs, conf):
    for i, cell in enumerate(obs.board):
        if cell == 0:
            return i
    return None


if __name__ == "__main__":
    # Initialize our custom environment
    env = make("custom_tictactoe", debug=True)

    # Run a match between the Random bot (X) and Naive bot (O)
    steps = env.run([random_agent, first_empty_agent])

    # Render the final state of the board
    print("Final Board State:")
    env.render(mode="human")

    # Print match result
    rewards = [step.reward for step in steps[-1]]
    print(f"Rewards: Player 1 (X): {rewards[0]} | Player 2 (O): {rewards[1]}")
