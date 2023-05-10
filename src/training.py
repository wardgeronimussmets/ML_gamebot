from Environments import GameEnv
from matplotlib import pyplot as plt 
import numpy as np


def test_samples(env):
    print(env.action_space.sample())
    plt.figure()
    obs = env.get_observation()[0]
    print(obs.shape)
    plt.imshow(obs)
    plt.show()

if __name__ == "__main__":
    print("starting")
    env = GameEnv()
    test_samples(env)

    
    