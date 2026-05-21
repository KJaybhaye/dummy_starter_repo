import random


def agent(obs, conf):
    """
    obs.balances: List of 3 elements containing remaining troops for each player
    obs.player_index: An integer (0, 1, or 2) representing who THIS agent is
    obs.current_round: The current round integer (0 to 4)
    """
    my_index = obs.player_index
    my_remaining_troops = obs.balances[my_index]

    if my_remaining_troops <= 0:
        return [0, 0, 0, 0, 0]

    # Example Logic: Randomly distribute a chunk of remaining troops across fields
    num_fields = 5
    allocation = [0] * num_fields

    # Decide to spend a random portion of total available assets this turn
    troops_to_spend = random.randint(0, my_remaining_troops)

    for _ in range(troops_to_spend):
        target_field = random.randint(0, num_fields - 1)
        allocation[target_field] += 1

    return allocation
