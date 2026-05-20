from kaggle_environments import make
import custom_env  # Importing this executes the registration code


def main():
    # 1. Initialize the environment
    env = make("custom_tictactoe", debug=True)

    print("Starting match: my_agent.py (X) vs random_agent.py (O)...\n")

    # 2. Run the match using the file paths of the agents
    steps = env.run(["my_agent.py", "random_agent.py"])

    # 3. Render the final board
    env.render(mode="human")

    # 4. Display the results
    rewards = [step.reward for step in steps[-1]]
    print("MATCH OVER")
    print(f"Your Agent (X): {rewards[0]}")
    print(f"Random Agent (O): {rewards[1]}")


if __name__ == "__main__":
    main()
