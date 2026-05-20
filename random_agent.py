import random


def agent(obs, conf):
    """A baseline agent that plays randomly."""
    empty_cells = [i for i, cell in enumerate(obs.board) if cell == 0]
    return random.choice(empty_cells) if empty_cells else None
