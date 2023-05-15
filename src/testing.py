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
    
     
    pixels = {(0, 133, 199): 85, (202, 166, 93): 56}
    #pixels = PlayerRecogniser.recognize_once()
    print(pixels)
    
    winnersearch = WinnerSearcher.WinnerSearcher(pixels)
    
    while True:
        time.sleep(1)
        print(winnersearch.next_scan())
        # img = ScreenGrabber.get_resized_screenshot(PlayerRecogniser.RECOGNIZER_SHAPE)
        # mask = PlayerRecogniser.get_players_mask(pixels,img,70)
        # ImageDisplay.show_images_2(img,mask,ImageDisplay.BGR_IMAGE)
    
    