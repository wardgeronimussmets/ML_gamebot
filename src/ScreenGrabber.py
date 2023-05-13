import numpy as np
import cv2
import math
from mss import mss
import pygetwindow as gw
import ImageDisplay
import time
from PIL import Image

TITLE_BAR_THICKKNESS = 30 #px

    
def grab_winner_area(as_gray=False):
    grab = np.array(cap.grab(level_winner_region))[:,:,:3]
    if as_gray:
        grab = cv2.cvtColor(grab,cv2.COLOR_BGR2GRAY)
    return grab

def get_screenshot():
    raw = np.array(cap.grab(game_region))[:,:,:3]
    return raw


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
    
    #Grayscale
    gray = cv2.cvtColor(raw,cv2.COLOR_BGR2GRAY)
    #Resize
    resized = cv2.resize(gray,resize_shape)
            
    return resized

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
