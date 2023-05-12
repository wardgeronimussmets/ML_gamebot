from gym import Env
from gym.spaces import Box,Tuple,MultiDiscrete
import numpy as np
from mss import mss
import cv2
import math

TITLE_COLOR_THRESHOLD = 50
PIXEL_COLOR_DIFF_THRESHOLD = 50


class GameEnv(Env):
    def __init__(self) -> None:
        super().__init__()
        #setup spaces
        self.observation_shape_channel = (1,200,400)
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
        
    def step(self, action):
        pass
    
    def render(self):
        pass
    
    def reset(self):
        pass
    
    def get_observation(self):
        raw = np.array(self.cap.grab(self.monitor))[:,:,:3]
        
        #Grayscale
        gray = cv2.cvtColor(raw,cv2.COLOR_BGR2GRAY)
        #Resize
        resized = cv2.resize(gray,self.observation_shape)
        #Add channels first, this is what stable baselines wants
        channel = np.reshape(resized,self.observation_shape_channel)
        
        return channel
    
    def difference_title_colors(self,grab_area):
        if self.last_winner_area.shape != grab_area.shape:
            raise Exception("length of winner area to compare is not the same between current and last frame")
        
        #count the amount of pixels that are different
        different_pixels = 0
        for i in range(len(grab_area[0])):
            for j in range(len(grab_area[0][0])):
                #if any of the colors is too different 
                for color in range(3):
                    if abs(grab_area[color][i][j] - self.last_winner_area[color][i][j])>PIXEL_COLOR_DIFF_THRESHOLD:
                        different_pixels += 1
                        break
                    
        diff = different_pixels/len(grab_area)            
        
        # diff = np.linalg.norm(self.last_winner_area-grab_area)
        print(diff)
        
        
        return -1
        
    
    
    def get_level_winner(self):
        grab = np.array(self.cap.grab(self.level_winner_region))[:,:,:3]
        if self.last_winner_area is not None:
            if self.difference_title_colors(grab) > TITLE_COLOR_THRESHOLD:
                #difference is big enough -> someone won the round, still need to figure out who that was though
                avg_color = np.average(grab,axis=None)
            
        #else, first time looping. Update last winner area
        
        self.last_winner_area = grab

        
        return