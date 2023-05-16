from gym import Env
from gym.spaces import Box,Tuple,MultiDiscrete
import numpy as np
from mss import mss
import ScreenGrabber
import GamepadEmulator
import time
import PlayerRecogniser
import cv2




TITLE_COLOR_THRESHOLD = 1500
PIXEL_COLOR_DIFF_THRESHOLD = 0.3 #factor that it can deviate from the maximum
WINNER_CHECKER_INTERVAL = 1.8
OBSERVATION_SHAPE = (3,300,600)
OBSERVATION_SHAPE_MASK = (3,150,300)

#model training
CHECKPOINT_DIR = './train/'
LOG_DIR = './logs/'


# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        


class GameEnv(Env):
    def __init__(self,player_colour,player_colours,virtual_gamepad):
        super().__init__()
        #setup spaces
        self.resize_shape = (OBSERVATION_SHAPE[2],OBSERVATION_SHAPE[1])
        #multiple observations
        #first it gets a screencap of the game itself
        #then a screencap masked with the players at a lower resolution
        #then it's own color -> hopefully it will learn that and can control multiple colors
        self.observation_space = Tuple((Box(low=0,high=255,shape=OBSERVATION_SHAPE,dtype=np.uint8), 
                                        Box(low=0,high=255,shape=OBSERVATION_SHAPE_MASK,dtype=np.uint8),
                                        Box(low=0,high=255,shape=(3,1,1),dtype=np.uint8)))
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
        #       1 -> Movement (up and down) (player can fall quicker but not much else)
        #       2 -> Aim (left and right)
        #       3 -> Aim (up and down)
        self.action_space = Tuple((
            MultiDiscrete([4,2]),
            Box(low=-1.0,high=1.0,shape=(4,))           
        ))
        
        self.gamepad = virtual_gamepad
        
        self.player_color = player_colour
        self.player_colors = player_colours
    
    def update_player_colors(self,players):
        self.player_colors = players
        
        
    def step(self, action):
        if action[0][0] == 0:
            self.gamepad.release_blocking()
        if action[0][0] == 1:
            #attack key
            self.gamepad.modulate_attack(True)
            
        elif action[0][0] == 2:
            self.gamepad.modulate_throw(True)
        elif action[0][0] == 3:
            self.gamepad.modulate_block(True)
            
        if action[0][1] == 1:
            self.gamepad.modulate_jump(True)
        elif action[0][1] == 0:
            self.gamepad.modulate_jump(False)
            
        self.gamepad.update_movement(action[1][0],action[1][1])
        self.gamepad.update_aim(action[1][2],action[1][3])
            
        
    
    def render(self):
        #no need to render anything
        pass
    
    def reset(self):
        #used to start a new episode, but that happens automatically -> no need
        pass
    
    def get_observation(self):
        screenshot = ScreenGrabber.get_resized_screenshot(self.resize_shape)
        #Add channels first, this is what stable baselines wants
        channel = np.reshape(screenshot,OBSERVATION_SHAPE)        
        
        screen_resized = cv2.resize(screenshot,(OBSERVATION_SHAPE_MASK[2],OBSERVATION_SHAPE_MASK[1]))
        mask = PlayerRecogniser.get_players_mask(self.player_colors,screen_resized)
        mask = np.reshape(mask,OBSERVATION_SHAPE_MASK)
        
        return (channel,mask,self.player_color)
    


    

if __name__ == "__main__":
    env = GameEnv()
    while True:
        action = env.action_space.sample()
        print(action)
        time.sleep(3)
        env.step(action)
        
        

    
    
    
    
