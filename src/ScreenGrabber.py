import numpy as np
import cv2
import math
from mss import mss
import pygetwindow as gw
import ImageDisplay
import time
from PIL import Image

TITLE_BAR_THICKKNESS = 30 #px

    
def grab_winner_area(as_gray=False,whole_bar=False,resized_shape=None):
    if whole_bar:
        region_to_grab = level_winner_bar
    else:
        region_to_grab = level_winner_region
    grab = np.array(cap.grab(region_to_grab))[:,:,:3]
    if as_gray:
        grab = cv2.cvtColor(grab,cv2.COLOR_BGR2GRAY)
        
    if resized_shape:
        grab = cv2.resize(grab,resized_shape)
    return grab

def get_screenshot():
    raw = np.array(cap.grab(game_region))[:,:,:3]
    return raw

def get_and_save_screenshot(save_name):
    screen = get_screenshot()
    cv2.imwrite(save_name,screen)


def get_active_game_region(window_name=None):
    # Get the currently focused window
    if window_name:
        window = gw.getWindowsWithTitle(window_name)[0]
        window.activate()
        
    else:
        window = gw.getActiveWindow()
    
    print("Now it is important that the game is actually visible")
    print("In 3")
    time.sleep(1)
    print("2")
    time.sleep(1)
    print("1")
    time.sleep(1)
        
    # Get the position and size of the window
    x, y, width, height = window.topleft[0], window.topleft[1], window.width, window.height\
        
    if not window.isMaximized:
        #we don't want the title bar to be used
        y += TITLE_BAR_THICKKNESS

    # Capture a screenshot of the window
    game_region = {"top": y, "left": x, "width": width, "height": height}
    return game_region
    
def get_level_winner_region():
    monitor = game_region
    # Capture a bbox using percent values
    left = monitor["left"] + monitor["width"] * 0.4  # n-% from the left
    top = monitor["top"] + monitor["height"] * 0.3  # n-% from the top
    right = left + 0.25*monitor['width']  # n-px width
    lower = top + 0.1*monitor["height"]  # n-px height
    bbox = (math.floor(left), math.floor(top), math.floor(right), math.floor(lower))
    return bbox
    
def get_level_winner_region_bar():
    monitor = game_region
    # Capture a bbox using percent values
    left = monitor["left"]  # n-% from the left
    top = monitor["top"] + monitor["height"] * 0.2  # n-% from the top
    right = left + monitor['width']  # n-px width
    lower = top + 0.2*monitor["height"]  # n-px height
    bbox = (math.floor(left), math.floor(top), math.floor(right), math.floor(lower))
    return bbox

def get_resized_screenshot(resize_shape):
    raw = np.array(cap.grab(game_region))[:,:,:3]
    
    #Resize
    resized = cv2.resize(raw,resize_shape)
            
    return resized


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


def reinitilize():
    game_region = get_active_game_region()
    level_winner_region = get_level_winner_region()
    
########################################
#######  INITIALIZE  ###################
########################################

GAME_NAME = "Stick Fight: The Game"

cap = mss()
game_region = get_active_game_region(GAME_NAME)
level_winner_region = get_level_winner_region()
level_winner_bar = get_level_winner_region_bar()
