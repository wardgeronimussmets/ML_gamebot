from Environments import GameEnv

if __name__ == "__main__":
    print("starting")
    env = GameEnv()
    print(env.action_space.sample())
    