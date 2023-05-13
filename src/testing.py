from Environments import GameEnv
from matplotlib import pyplot as plt 
import numpy as np
import time


def test_samples(env):
    print(env.action_space.sample())
    plt.figure()
    obs = env.get_observation()[0]
    print(obs.shape)
    plt.imshow(obs)
    plt.show()
    
def test_winner(enb):
    plt.figure()
    grab,avg = enb.get_level_winner()
    plt.imshow(grab)
    plt.show()
    avg_np = np.full((100,100),avg)
    plt.figure()
    plt.imshow(avg_np)
    plt.show()

if __name__ == "__main__":
    print("starting")
    env = GameEnv()
    # test_samples(env)
    # input()
    while True:
        time.sleep(1)
        env.get_observation()
    
    