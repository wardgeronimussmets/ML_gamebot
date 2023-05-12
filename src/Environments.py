from gym import Env
from gym.spaces import Box,Tuple,MultiDiscrete
import numpy as np
from mss import mss
import cv2
import math
import time
import pytesseract
import ImageDisplay

TITLE_COLOR_THRESHOLD = 1500
PIXEL_COLOR_DIFF_THRESHOLD = 0.3 #factor that it can deviate from the maximum
WINNER_CHECKER_INTERVAL = 1.8

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


class GameEnv(Env):
    def __init__(self) -> None:
        super().__init__()
        #setup spaces
        self.observation_shape_channel = (1,300,600)
        self.observation_shape = (self.observation_shape_channel[2],self.observation_shape_channel[1])
        self.observation_space = Box(low=0,high=255,shape=self.observation_shape_channel,dtype=np.uint8)
        self.last_winner_area = None
        
        #action space:
        #   Discretes:
        #       0 -> No op
        #       1 -> Attack key
        #       2 -> Throw key
        #       3 -> Block key
        
        #   Discrete2:
        #       0 -> No op
        #       1 -> Jump
        
        #   Continues (between 1 and -1)
        #       0 -> Movement (left and right)
        #       1 -> Aim (left and right)
        #       2 -> Aim (up and down)
        self.action_space = Tuple((
            MultiDiscrete([4,2]),
            Box(low=-1.0,high=1.0,shape=(3,))           
        ))
        self.cap = mss()
        self.monitor = self.cap.monitors[1]
        self.level_winner_region = self.get_level_winner_region()
        
    def get_level_winner_region(self):
        monitor = self.monitor
        # Capture a bbox using percent values
        left = monitor["left"] + monitor["width"] * 0.4  # n-% from the left
        top = monitor["top"] + monitor["height"] * 0.3  # n-% from the top
        right = left + 0.25*monitor['width']  # n-px width
        lower = top + 0.1*monitor["height"]  # n-px height
        bbox = (math.floor(left), math.floor(top), math.floor(right), math.floor(lower))
        return bbox
        
    def get_level_winner_region_bar(self):
        monitor = self.monitor
        # Capture a bbox using percent values
        left = monitor["left"]  # n-% from the left
        top = monitor["top"] + monitor["height"] * 0.2  # n-% from the top
        right = left + monitor['width']  # n-px width
        lower = top + 0.2*monitor["height"]  # n-px height
        bbox = (math.floor(left), math.floor(top), math.floor(right), math.floor(lower))
        return bbox
        
    def step(self, action):
        pass
    
    def render(self):
        pass
    
    def reset(self):
        pass
    
    def get_screenshot(self):
        raw = np.array(self.cap.grab(self.monitor))[:,:,:3]
        return raw

    
    def get_resized_screenshot(self):
        raw = np.array(self.cap.grab(self.monitor))[:,:,:3]
        
        #Grayscale
        gray = cv2.cvtColor(raw,cv2.COLOR_BGR2GRAY)
        #Resize
        resized = cv2.resize(gray,self.observation_shape)
                
        return resized
        
    
    
    def get_observation(self,screenshot):
        #Add channels first, this is what stable baselines wants
        channel = np.reshape(screenshot,self.observation_shape_channel)        
        return channel
    
    
    def difference_title_colors(self,img1,img2):
        if img1.shape != img2.shape:
            raise Exception("length of winner area to compare is not the same between current and last frame")        
               
        diff = self.image_difference_in_total(img1,img2)
        return diff
    
    def image_difference_in_total(self,img1,img2):
        diff = np.linalg.norm(img1-img2)
        return diff

        
        
    def image_difference_pixels_above_threshold(self,img1,img2):
        if img1.ndim == 2:
            #GreyScale
            pixel_max = 255
            colors = [0]
            img1 = np.array([img1])
            img2 = np.array([img2])
        else:
            #rbg
            pixel_max = 255
            colors = [0,1,2]        
            
        threshold = pixel_max*PIXEL_COLOR_DIFF_THRESHOLD
        #count the amount of pixels that are different
        different_pixels = 0
        for i in range(len(img1[0])):
            for j in range(len(img1[0][0])):
                #if any of the colors is too different 
                for color in colors:
                    if abs(img1[color][i][j] - img2[color][i][j])>threshold:
                        different_pixels += 1
                        break
                    
        diff = different_pixels/len(img1)   
        return diff  
    
    
    def get_level_winner_with_pixel_counting(self,new_screen_cap):        
        if new_screen_cap.ndim == 2:
            #GreyScale
            colors = [0]
            new_screen_cap = np.array([new_screen_cap])
        else:
            #rbg
            colors = [0,1,2]    
        
        counting_map = {}
        
        for i in range(len(new_screen_cap[0])):
            for j in range(len(new_screen_cap[0][0])):
                #if any of the colors is too different 
                color_key = ""
                for color in colors:
                    color_key += str(new_screen_cap[color][i][j])+"-"
                color_key = color_key[:-1]
                if color_key in counting_map:
                    counting_map[color_key] += 1
                else:
                    counting_map[color_key] = 0
        max_same_pixels_key = max(counting_map,key=counting_map.get)
        total_pixels = len(new_screen_cap[0])
        max_same_pixels = counting_map[max_same_pixels_key]
        max_same_pixel_ratio = max_same_pixels/total_pixels
        print(max_same_pixel_ratio)
        
                    
           
    
    
    def get_level_winner_with_tesseract(self):
        new_screen_cap = np.array(self.cap.grab(self.level_winner_region))[:,:,:3]
        res = pytesseract.image_to_string(new_screen_cap)
        print(res)
    
    
    def get_level_winner_via_color_diff(self,new_screen_cap):
        
        if self.last_winner_area is not None:
            diff = self.difference_title_colors(self.last_winner_area,new_screen_cap)
            print(diff)
            if  diff > TITLE_COLOR_THRESHOLD:
                print("triggered treshold")
            
        self.last_winner_area = new_screen_cap
        return
    
    def grab_winner_area(self):
        grab = np.array(self.cap.grab(self.level_winner_region))[:,:,:3]
        return grab