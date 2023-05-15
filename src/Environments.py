from gym import Env
from gym.spaces import Box,Tuple,MultiDiscrete,Discrete
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
OBSERVATION_SHAPE_MASK = (3,150,300)

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


class GameEnv(Env):
    def __init__(self) -> None:
        super().__init__()
        #setup spaces
        self.observation_shape_channel = OBSERVATION_SHAPE
        self.resize_shape = (self.observation_shape_channel[2],self.observation_shape_channel[1])
        #multiple observations
        #first it gets a screencap of the game itself
        #then a screencap masked with the players at a lower resolution
        #then it's own color -> hopefully it will learn that and can control multiple colors
        self.observation_space = Tuple((Box(low=0,high=255,shape=self.observation_shape_channel,dtype=np.uint8), Box(low=0,high=255,shape=OBSERVATION_SHAPE_MASK,dtype=np.uint8),Box(low=0,high=255,shape=(3,1,1),dtype=np.uint8)))
        # self.observation_space = Tuple((Box(low=0,high=255,shape=self.observation_shape_channel,dtype=np.uint8)),
        #                                (Box(low=0,high=255,shape=OBSERVATION_SHAPE_MASK,dtype=np.uint8)),
        #                                (Box(low=0,high=255,shape=(3,1,1),dtype=np.uint8)))
                
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
        
        screenshot = ScreenGrabber.get_resized_screenshot(self.resize_shape)
        #Add channels first, this is what stable baselines wants
        channel = np.reshape(screenshot,self.observation_shape_channel)        
        return channel
    
    
if __name__ == "__main__":
    env = GameEnv()
    print(env.action_space.sample())
        

    
    
    
    
