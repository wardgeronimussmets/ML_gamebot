from gym import Env
from gym.spaces import Box,Tuple,MultiDiscrete
import numpy as np
from mss import mss
import cv2
import math
import time
import pytesseract
import ImageDisplay
import ScreenGrabber

TITLE_COLOR_THRESHOLD = 1500
PIXEL_COLOR_DIFF_THRESHOLD = 0.3 #factor that it can deviate from the maximum
WINNER_CHECKER_INTERVAL = 1.8
OBSERVATION_SHAPE = (3,300,600)

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


class GameEnv(Env):
    def __init__(self) -> None:
        super().__init__()
        #setup spaces
        self.observation_shape_channel = OBSERVATION_SHAPE
        self.observation_shape = (self.observation_shape_channel[2],self.observation_shape_channel[1])
        self.observation_space = Box(low=0,high=255,shape=self.observation_shape_channel,dtype=np.uint8)
                
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
        
        
    def step(self, action):
        pass
    
    def render(self):
        pass
    
    def reset(self):
        pass
    
    def get_observation(self):
        
        screenshot = ScreenGrabber.get_resized_screenshot(self.observation_shape)
        #Add channels first, this is what stable baselines wants
        channel = np.reshape(screenshot,self.observation_shape_channel)        
        return channel
    

    
    
    
    
