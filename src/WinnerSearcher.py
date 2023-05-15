import numpy as np
import ScreenGrabber
import ImageDisplay
import PlayerRecogniser


def get_level_winner(player_colors):    
    
    new_screen_cap = ScreenGrabber.grab_winner_area(as_gray=False)    
    mask = PlayerRecogniser.get_players_mask(new_screen_cap)
    ImageDisplay.show_single_image(mask)


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