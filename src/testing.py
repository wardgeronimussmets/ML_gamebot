from Environments import GameEnv
from matplotlib import pyplot as plt 
import numpy as np
import time
import PlayerRecogniser

def player_callback(players):
    print(players)

if __name__ == "__main__":
    print("starting")
    env = GameEnv()
    players = PlayerRecogniser.RecogniserInterface(player_callback)
    
    