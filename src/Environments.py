from gym import Env
from gym.spaces import Box,Tuple,MultiDiscrete
import numpy as np
from mss import mss
import cv2


class GameEnv(Env):
    def __init__(self) -> None:
        super().__init__()
        #setup spaces
        self.observation_shape_channel = (1,200,400)
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
        self.cap = mss()
        self.monitor = self.cap.monitors[1]
        

        
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
    
    
    def get_done(self):
        pass