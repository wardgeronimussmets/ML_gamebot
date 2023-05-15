import numpy as np
import ScreenGrabber
import ImageDisplay
import PlayerRecogniser
import time
import cv2

WINNER_SCORE_THRESHOLD = 1/(3*8)
WINNER_TIMEOUT_SECONDS = 4


def get_level_winner(player_colors,img):    
    pixels = count_for_players(img,player_colors)
    return pixels    
    
def count_for_players(mask,player_colours,pixel_range=80):
    #default pixel value range is high, but this works very well
    #rest player counting map and use to store hits
    for player_key in player_colours:
        player_colours[player_key] = 0
    
    for i in range(len(mask)):
        for j in range(len(mask[i])):                    
            for player_pixels in player_colours:
                player_match = True
                for pixel_index in range(3):
                    if (mask[i][j][pixel_index] + pixel_range < player_pixels[pixel_index]) or (mask[i][j][pixel_index] - pixel_range > player_pixels[pixel_index]):
                        player_match = False
                        break
                if player_match:
                    player_colours[player_pixels] += 1
                    
    return player_colours 

class WinnerSearcher():
    def __init__(self,player_colors) -> None:
        self.previous_image = None
        for player_key in player_colors:
            player_colors[player_key] = 0
        self.player_colors = player_colors
        self.score_threshold = 100000#generic high value
        self.last_winner_time = time.time()
    
    def next_scan(self):
        new_img = ScreenGrabber.grab_winner_area(whole_bar=True,resized_shape=(200,40))
        winner = None
        if (self.previous_image is not None) and (time.time() - self.last_winner_time) > WINNER_TIMEOUT_SECONDS:
            mask = cv2.absdiff(new_img,self.previous_image)
            winner_matches = get_level_winner(self.player_colors,mask)
            for winn in winner_matches:
                if winner_matches[winn] >= self.score_threshold:
                    winner = winn
                    self.last_winner_time = time.time()
                    break
        else:
            self.score_threshold = WINNER_SCORE_THRESHOLD*new_img.shape[0]*new_img.shape[1]
        self.previous_image = new_img
        return winner
            
    
                
    
if __name__ == "__main__":
    while True:
        time.sleep(1)
        colors = {(4, 142, 200): 60, (140, 117, 62): 58}
        input()
        img = ScreenGrabber.grab_winner_area(whole_bar=True,resized_shape=(200,30))
        print(count_for_players(img,colors))
        
        # ImageDisplay.show_single_image(PlayerRecogniser.get_players_mask(colors,img),ImageDisplay.BGR_IMAGE)

#OLD CODE
"""

def get_level_winner(player_colors,color_range=10,winner_treshold=0.02):    
    
    new_screen_cap = ScreenGrabber.grab_winner_area(as_gray=False)    
    counting_map = {}
    for color in player_colors:
        counting_map[color] = 0
    
    n = 0
    
    for i in range(len(new_screen_cap)):
        for j in range(len(new_screen_cap[i])):
            n+=1
            #check if the color is in range of nany of the colors we want
            for color in counting_map:
                if counting_map[color]-color_range<=new_screen_cap[i][j] and counting_map[color]+color_range>=new_screen_cap[i][j]:
                    counting_map[color] += 1
    
    for key in counting_map:
        if (counting_map[key] / n) >= winner_treshold:
            print(str(key) + "won with a score of " + str(counting_map[key]/n) )
            return key
                
    print(counting_map)  
    return None
    """