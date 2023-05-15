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
    
     
    # pixels = PlayerRecogniser.recognize_once()
    pixels = {(2, 149, 198): 87, (140, 116, 63): 70}
    print(pixels)
    
    while True:
        img = ScreenGrabber.get_resized_screenshot(PlayerRecogniser.RECOGNIZER_SHAPE)
        mask = PlayerRecogniser.get_players_mask(pixels,img,50)
        ImageDisplay.show_single_image(mask,ImageDisplay.BGR_IMAGE)
    
    