from Environments import GameEnv
from matplotlib import pyplot as plt 
import numpy as np
import time
import PlayerRecogniser
import WinnerSearcher
import ImageDisplay
import ScreenGrabber

def player_callback(players):
    print(players)

if __name__ == "__main__":
    print("starting")
    
    ImageDisplay.show_single_image(ScreenGrabber.grab_winner_area()) 
    
     
    
    exit()
    env = GameEnv()
    players = [160,135]
    while True:
        time.sleep(1)
        print(WinnerSearcher.get_level_winner(players))
    
    