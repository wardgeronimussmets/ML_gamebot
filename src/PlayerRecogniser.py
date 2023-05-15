"""Module that will look at the players in the lobby and determine how many AI are necesarry and which
one will be which color. 
"""
import ScreenGrabber
from PIL import Image,ImageTk
import mss.tools
import ImageDisplay
import cv2
import numpy as np
import math
import time
import tkinter as tk
import pygetwindow as gw
from Environments import OBSERVATION_SHAPE
import numpy as np


RECOGNIZER_SHAPE = (480,320)



def recognize_once():
    img = ScreenGrabber.get_screenshot()
    template = cv2.imread("docs\Lobby3.png")
    
    template = cv2.resize(template,RECOGNIZER_SHAPE,interpolation=cv2.INTER_LINEAR)
    to_filter = cv2.resize(img,RECOGNIZER_SHAPE,interpolation=cv2.INTER_LINEAR)
        
    to_filter = ScreenGrabber.filter_out_game_stats(to_filter)
    template = ScreenGrabber.filter_out_game_stats(template)
    
    mask = cv2.absdiff(to_filter,template)
    
    counting_map = count_pixels_in_image(mask)
    
    pixels = get_maxes_from_counting_map(counting_map,8)
    return pixels

def count_pixels_in_image(mask):
    #pixel counting on pixels where mask is not null
    PIXEL_THRESHOLD = 0.00001*RECOGNIZER_SHAPE[0]*RECOGNIZER_SHAPE[1]
    counting_map = {}
        
    for i in range(len(mask)):
        for j in range(len(mask[i])):
            total_diff = 0
            for color in range(len(mask[i][j])):
                diff = abs(mask[i][j][color] - PIXEL_THRESHOLD)
                if diff < 0:
                    diff = 0
                total_diff += diff

            if total_diff > PIXEL_THRESHOLD:
                key = tuple(mask[i][j])
                if key in counting_map:
                    counting_map[key] += 1
                else:
                    counting_map[key] = 1
    return counting_map
    


            

def get_maxes_from_counting_map(counting_map,pixel_value_range=2,pixel_value_range_background=20):    
    #scan per grey value how many pixels in range of 5 or smth
    pixels = {}
    THRESHOLD = 0.000106451*RECOGNIZER_SHAPE[0]*RECOGNIZER_SHAPE[1]
    #loops and finds the pixel that has changed the most, if there is no pixel below threshold anymore
    #it stops looping and there are no more players left
    #often the background will be included because of small changes somewhere + white from swings and effects. Don't want that
    unwated_pixels = [(20,15,10),(165,190,220)]
    for unwanted_pixel in unwated_pixels:
        counting_map = remove_pixel_from_map(counting_map,unwanted_pixel,pixel_value_range_background)
    
    while True:
        max_val_key,max_val = max_from_counting_map_loop_once(counting_map,pixel_value_range)
        if max_val<THRESHOLD:
            return pixels
        counting_map = remove_pixel_from_map(counting_map,max_val_key,pixel_value_range)
        
        pixels[max_val_key] = max_val
        
def max_from_counting_map_loop_once(counting_map,pixel_value_range):
    max_val = 0
    max_val_key = 0
    for key in counting_map:
        val = 0
        b,g,r = key
        for bi in range(-pixel_value_range,pixel_value_range+1):
            b_index = b + bi
            for gi in range(-pixel_value_range,pixel_value_range+1):
                g_index = g + gi
                for ri in range(-pixel_value_range,pixel_value_range+1):
                    r_index = r + ri
                    
                    key2 = (b_index,g_index,r_index)
                    if key2 in counting_map:
                        val += counting_map[key2]
        if val > max_val:
            max_val = val
            max_val_key = key
    return max_val_key,max_val


    
def remove_pixel_from_map(map,pixel_value,pixel_value_range):
    #remove keys from counting map
    b,g,r = pixel_value
    for bi in range(-pixel_value_range,pixel_value_range+1):
        b_index = b + bi
        for gi in range(-pixel_value_range,pixel_value_range+1):
            g_index = g + gi
            for ri in range(-pixel_value_range,pixel_value_range+1):
                r_index = r + ri
                
                key = (b_index,g_index,r_index)
                if key in map:
                    del map[key]  
    return map  
    
    
    
   


def get_players_mask(pixels,image_to_filter,pixel_value_range=70):
    #default pixel value range is high, but this works very well
    mask = image_to_filter.copy()
    for i in range(len(image_to_filter)):
        for j in range(len(image_to_filter[i])):                    
            player_matches = []
            for player_pixels in pixels:
                player_match = True
                for pixel_index in range(3):
                    if (image_to_filter[i][j][pixel_index] + pixel_value_range < player_pixels[pixel_index]) or (image_to_filter[i][j][pixel_index] - pixel_value_range > player_pixels[pixel_index]):
                        player_match = False
                        break
                player_matches.append(player_match)
            if True not in player_matches:
                mask[i][j] = (0,0,0)
    return mask                  



if __name__ == "__main__":
    pixels = {(2, 149, 198): 87, (140, 116, 63): 70}
    
    image = [[[0,0,0],[10,20,10]],
             [[135,110,65],[0,0,0]]]
    mask = get_players_mask(pixels,image,10)
    print(mask)



#Old code 
"""

def start_recognizing(time_interval=0.2,times_to_recognize=10):
    print("Doesn't work")
    exit()
    
    players = {}
    
    for i in range(times_to_recognize):
        pixels = recognize_once()
        for pix in pixels:
            if pix in players:
                players[pix] += pixels[pix]
            else:
                #check if similar color has been entered
                found_similar = False
                for ki in range(-5,5):
                    if pix+ki in players:
                        players[pix+ki] += pixels[pix]
                        found_similar = True
                        break
                if not found_similar:
                    players[pix] = pixels[pix]
        time.sleep(time_interval)
        
    #only select the ones with the most matching pixels
    players_sorted = dict(sorted(players.items(),key=lambda x:x[0],reverse=True))
    previous_player = None
    final_players_colours = []
    stopped_counting_players = False
    for player in players_sorted:
        if previous_player is not None:
            if players_sorted[previous_player] >= players_sorted[player]/2:
                #rest isn't going to be relevant anymore
                stopped_counting_players = True
                break                                
            final_players_colours.append(previous_player)
        previous_player = player
    if not stopped_counting_players:
        final_players_colours.append(previous_player)
        
        
    print(final_players_colours)
    return final_players_colours
    

def recognize_once():
    img = ScreenGrabber.get_screenshot()
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    
    
    
    template = cv2.imread("docs\Lobby2.png",cv2.IMREAD_GRAYSCALE)
    template = cv2.resize(template,(600,300))
    to_filter = cv2.resize(gray,(600,300))
    
    
    to_filter = filter_out_game_stats(to_filter)
    template = filter_out_game_stats(template)
    
    # ImageDisplay.show_single_image(to_filter)

    
    mask = cv2.absdiff(template,to_filter)
        
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
    
    return pixels
     

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
    BACKGROUND_PIXEL_VALUEs = [8,25,42,228,245]
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

########################################################################################################
class RecogniserInterface:
    def __init__(self,players_callback):
        
        self.players_callback = players_callback
        
        # Create a Tkinter window
        root = tk.Tk()
        self.root = root
        root.title("Add and Delete Players")

        # Set the size of the window
        root.geometry("300x500")

        # Create a frame for the entries
        entry_frame = tk.Frame(root)
        self.entry_frame = entry_frame
        entry_frame.pack(padx=10, pady=10)

        # Create a list to hold the entry widgets and delete buttons
        self.entries = []
        
        #create explanation label
        expl_label = tk.Label(root,text="Correct format is 111,222,333")
        expl_label.pack(side=tk.TOP)

        # Create a button to add a new field
        add_button = tk.Button(root, text="+ Add Player", command=lambda: self.add_entry())
        add_button.pack(side=tk.TOP)
        
        #create plot button
        plot_button = tk.Button(root, text="Show screenshot", command=lambda: self.show_screen_plot())
        plot_button.pack(side=tk.TOP)
        
        #create save button
        save_button = tk.Button(root, text="Save players",command=lambda:self.compute_player_input())
        save_button.pack(side=tk.TOP)
        
        root.focus_set()

        # Run the Tkinter event loop
        root.mainloop()
        
    def show_screen_plot(self):
        window = self.get_root_window()
        window.minimize()
        time.sleep(0.3)
        
        ImageDisplay.show_single_image(ScreenGrabber.get_resized_screenshot((800,400)))
        time.sleep(0.1)
        window.activate()
        
     
    def get_root_window(self):
        window = gw.getWindowsWithTitle("Add and Delete Players")[0]
        return window

        
    
    def compute_player_input(self):
        player_colors = []
        for entrie in self.entries:
            user_input = entrie[0].get()
            user_input_spl = user_input.split(",")
            player_colors.append(user_input_spl)
        self.players_callback(player_colors)
    
    # Create a function to get the pixel value
    def get_pixel(self,event):
        x, y = event.x, event.y
        pixel_value = self.screen_cap[y, x]
        print("Pixel value:", pixel_value)
        
    # Create a function to delete an entry and delete button
    def delete_entry(self,entry, delete_button):
        # Remove the entry widget and delete button from the list
        self.entries.remove((entry, delete_button))

        # Destroy the entry widget and delete button
        entry.destroy()
        delete_button.destroy()
    

    # Create a function to add a new entry and delete button
    def add_entry(self):
        # Create a new entry widget and delete button
        entry = tk.Entry(self.entry_frame)
        delete_button = tk.Button(self.entry_frame, text="Delete", command=lambda: self.delete_entry(entry, delete_button))

        # Pack the entry widget and delete button
        entry.pack(side=tk.TOP, pady=(0, 5))
        delete_button.pack(side=tk.TOP)

        # Add the entry widget and delete button to the list
        self.entries.append((entry, delete_button))



    
if __name__ == "__main__":
    RecogniserInterface(None)
    
    """