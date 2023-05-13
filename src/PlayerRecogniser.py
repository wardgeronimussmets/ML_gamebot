"""Module that will look at the players in the lobby and determine how many AI are necesarry and which
one will be which color. 
"""
import ScreenGrabber
from PIL import Image
import mss.tools
import ImageDisplay
import cv2


def start_recognizing():
    img = ScreenGrabber.get_screenshot()
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    filtered = filter_background_out(gray)
    

def filter_background_out(to_filter):
    template = cv2.imread("docs\Lobby2.png",cv2.IMREAD_GRAYSCALE)
    template = cv2.resize(template,(600,300))
    to_filter = cv2.resize(to_filter,(600,300))
    mask = cv2.absdiff(template,to_filter)
    ImageDisplay.show_single_image(mask)
    
    #pixel counting on pixels where mask is not null
    PIXEL_THRESHOLD = 10
    counting_map = {}
    for i in range(len(mask)):
        for j in range(len(mask[i])):
            if mask[i][j] > 10:
                key = mask[i][j]
                if key in counting_map:
                    counting_map[key] += 1
                else:
                    counting_map[key] = 1
    counting_map_by_key = dict(sorted(counting_map.items(),key=lambda item:item[0]))
    
    get_maxes_from_counting_map(counting_map,pixel_value_range=8)
    
    return -1  
    
    
def get_maxes_from_counting_map(counting_map,pixel_value_range=2):
    #scan per grey value how many pixels in range of 5 or smth
    THRESHOLD = 30
    pixels = {
        
    }
    #loops and finds the pixel that has changed the most, if there is no pixel below threshold anymore
    #it stops looping and there are no more players left
    max_val = THRESHOLD + 1
    while max_val > THRESHOLD:
        max_val_key,max_val = max_from_counting_map_loop_once(counting_map)
        #remove keys from counting map
        for k in range(-pixel_value_range,pixel_value_range+1):
            key_ind = max_val_key + k
            if key_ind in counting_map:
                del counting_map[key_ind]
        pixels[max_val_key] = max_val
    print(pixels)
    
    l = []
    for p in pixels:
        l.append([p])
    ImageDisplay.show_single_image(l)
    
             
        
def max_from_counting_map_loop_once(counting_map,pixel_value_range=2):
    max_val = 0
    max_val_key = 0
    for key in counting_map:
        val = 0
        for k in range(-pixel_value_range,pixel_value_range+1):
            key_ind = key + k
            if key_ind in counting_map:
               val += counting_map[key_ind]
        if val > max_val:
            max_val = val
            max_val_key = key
    return max_val_key,max_val
    
if __name__ == "__main__":
    start_recognizing()
