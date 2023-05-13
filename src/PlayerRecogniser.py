"""Module that will look at the players in the lobby and determine how many AI are necesarry and which
one will be which color. 
"""
import ScreenGrabber
from PIL import Image
import mss.tools
import ImageDisplay
import cv2
import numpy as np
import math

def start_recognizing():
    img = ScreenGrabber.get_screenshot()
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    
    
    
    template = cv2.imread("docs\Lobby2.png",cv2.IMREAD_GRAYSCALE)
    template = cv2.resize(template,(600,300))
    to_filter = cv2.resize(gray,(600,300))
    
    to_filter_no_stats = filter_out_game_stats(to_filter)
    ImageDisplay.show_images_2(to_filter,to_filter_no_stats)
    exit()
    
    mask = cv2.absdiff(template,to_filter)
    
    # ImageDisplay.show_images_2(template,to_filter)
    
    #pixel counting on pixels where mask is not null
    PIXEL_THRESHOLD = 10
    counting_map = {}
    for i in range(len(mask)):
        for j in range(len(mask[i])):
            if mask[i][j] > PIXEL_THRESHOLD:
                key = mask[i][j]
                if key in counting_map:
                    counting_map[key] += 1
                else:
                    counting_map[key] = 1
                        
    pixels = get_maxes_from_counting_map(counting_map,pixel_value_range=8)
    print(pixels)
    
    highlight_pixel_values_in_image(to_filter,pixels,10)
    
    l = []
    for p in pixels:
        l.append([p])
    ImageDisplay.show_images_2(to_filter,l,as_grayscale=False)
    
    return -1  

def filter_out_game_stats(image_to_filter):
    #at the bottom right there are some stats like how many people are playing etc
    filter_mask = np.ones(image_to_filter.shape,dtype=np.uint8)
    START_HIDING_AT_HORI = 0.85 #in %
    START_HIDING_AT_VERT = 0.78 #in %
    horizontal_limit = math.floor(len(filter_mask[0]) * START_HIDING_AT_HORI)
    vertical_limit = math.floor(len(filter_mask) * START_HIDING_AT_VERT)
    for i in range(len(filter_mask)):
        for j in range(len(filter_mask[i])):
            if j>horizontal_limit and i>vertical_limit:
                filter_mask[i][j] = 0
    return cv2.multiply(image_to_filter,filter_mask)
            
    
def highlight_pixel_values_in_image(image,pixels,range_pixel):
    for i in range(len(image)):
        for j in range(len(image[i])):
            p = image[i][j]
            is_good_pixel = False
            for pixel in pixels:
                if p >= pixel-range_pixel and p <= pixel+range_pixel:
                    is_good_pixel = True
                    break
            if not is_good_pixel:
                image[i][j] = 0
    ImageDisplay.show_single_image(image)
    
def get_maxes_from_counting_map(counting_map,pixel_value_range=2):    
    #scan per grey value how many pixels in range of 5 or smth
    THRESHOLD = 40
    pixels = {}
    #loops and finds the pixel that has changed the most, if there is no pixel below threshold anymore
    #it stops looping and there are no more players left
    #often the background will be included because of small changes somewhere
    
    #remove background pixels
    BACKGROUND_PIXEL_VALUEs = [8,25]
    for bacground_pixel in BACKGROUND_PIXEL_VALUEs:
        counting_map = remove_pixel_from_map(counting_map,bacground_pixel,pixel_value_range)
    
    while True:
        max_val_key,max_val = max_from_counting_map_loop_once(counting_map,pixel_value_range)
        if max_val<THRESHOLD:
            return pixels
        counting_map = remove_pixel_from_map(counting_map,max_val_key,pixel_value_range)
        
        pixels[max_val_key] = max_val
    
def remove_pixel_from_map(map,pixel_value,pixel_value_range):
    #remove keys from counting map
    for k in range(-pixel_value_range,pixel_value_range+1):
        key_ind = pixel_value + k
        if key_ind in map:
            del map[key_ind]   
    return map       
        
def max_from_counting_map_loop_once(counting_map,pixel_value_range):
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
