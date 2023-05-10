from gym import Env
from gym.spaces import Box,MultiBinary,Tuple,MultiDiscrete
import numpy as np

class GameEnv(Env):
    def __init__(self) -> None:
        super().__init__()
        #setup spaces
        self.observation_space = Box(low=0,high=255,shape=(1,83,100),dtype=np.uint8)
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
        pass
    
    
    def get_done(self):
        pass