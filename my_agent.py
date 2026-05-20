def agent(obs, conf):
    """
    Your Tic-Tac-Toe agent!

    obs.board: A list of 9 integers (0=empty, 1=X, 2=O)
    obs.mark: Your player ID (1 or 2)
    conf: Game configuration
    """
    # Naive logic: Pick the first empty spot
    for i, cell in enumerate(obs.board):
        if cell == 0:
            return i

    return None
