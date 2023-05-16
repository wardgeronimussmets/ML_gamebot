from gym import Env,spaces
from gym.spaces import Box,Tuple,MultiDiscrete
import numpy as np
from mss import mss
import ScreenGrabber
import GamepadEmulator
import time
import PlayerRecogniser
import cv2
import Trainer
import ImageDisplay
from WinnerSearcher import WinnerSearcher



TITLE_COLOR_THRESHOLD = 1500
PIXEL_COLOR_DIFF_THRESHOLD = 0.3 #factor that it can deviate from the maximum
WINNER_CHECKER_INTERVAL = 1.8
OBSERVATION_SHAPE = (3,300,600)
OBSERVATION_SHAPE_MASK = (3,150,300)

#model training
CHECKPOINT_DIR = './train/'
LOG_DIR = './logs/'


# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        
class MultiDiscreteUint8(spaces.MultiDiscrete):
    dtype = np.uint8

class GameEnv(Env):
    def __init__(self,player_colour,player_colours,virtual_gamepad):
        super().__init__()
        #setup spaces
        self.resize_shape = (OBSERVATION_SHAPE[2],OBSERVATION_SHAPE[1])
        #multiple observations
        #first it gets a screencap of the game itself
        #then a screencap masked with the players at a lower resolution
        #then it's own color -> hopefully it will learn that and can control multiple colors
        #this is flattened because of stable baselines
        self.observation_space = MultiDiscreteUint8(np.full(1215003,255,dtype=np.uint8))
        #action space:
        #   Discretes:
        #       0 -> No op
        #       1 -> Attack key
        #       2 -> Throw key
        #       3 -> Block key
        
        #   Discrete2:
        #       0 -> No op
        #       1 -> Jump
        
        #   Fake Continues (between 1 and -1)
        #       0 -> Movement (left and right)
        #       1 -> Movement (up and down) (player can fall quicker but not much else)
        #       2 -> Aim (left and right)
        #       3 -> Aim (up and down)
        self.action_space = MultiDiscrete([4,2,200,200,200,200])   
        
        self.gamepad = virtual_gamepad
        
        self.player_color = player_colour
        self.player_colors = player_colours
        
        self.previous_screen = None
        
        self.winner_searcher = WinnerSearcher(self.player_colors)
        
    
    def update_player_colors(self,players):
        self.player_colors = players
        self.winner_searcher = WinnerSearcher(self.player_colors)
        
    def discrete_to_continues(self,numb):
        return (numb - 100)/100
        
    def observations_to_single_box(self,current_screen,previous_screen,player_mask,own_color):
        combined = np.concatenate((current_screen,previous_screen,player_mask,own_color),axis=None)
        return combined
        
    def step(self, action):
        if action[0] == 0:
            self.gamepad.release_blocking()
        if action[0] == 1:
            #attack key
            self.gamepad.modulate_attack(True)
            
        elif action[0] == 2:
            self.gamepad.modulate_throw(True)
        elif action[0] == 3:
            self.gamepad.modulate_block(True)
            
        if action[1] == 1:
            self.gamepad.modulate_jump(True)
        elif action[1] == 0:
            self.gamepad.modulate_jump(False)
            
        left,right = self.discrete_to_continues(action[2]),self.discrete_to_continues(action[3])
        self.gamepad.update_movement(left,right)
        self.gamepad.update_aim(self.discrete_to_continues(action[4]),self.discrete_to_continues(action[5]))
        
        winner = self.winner_searcher.next_scan()
        game_done = False
        reward = 0
        if winner is not None:
            game_done = True
            for player in self.player_colors:
                if player == winner:
                    if player == self.player_color:
                        #we won
                        reward = 100
                    else:
                        #we lost
                        reward = -50
                    break
        else:
            #didn't die either -> good
            reward = 10
        
        return self.get_observation(),reward,game_done,{} #  return observation, reward, done, info

        
        
        
            
        
    
    def render(self):
        #no need to render anything
        pass
    
    def reset(self):
        #used to start a new episode, but that happens automatically -> no need
        return self.get_observation()
    
    def get_observation(self):
        screenshot = ScreenGrabber.get_resized_screenshot(self.resize_shape)
        #Add channels first, this is what stable baselines wants
        
        screen_resized = cv2.resize(screenshot,(OBSERVATION_SHAPE_MASK[2],OBSERVATION_SHAPE_MASK[1]))
        mask = PlayerRecogniser.get_players_mask(self.player_colors,screen_resized)
        
        if self.previous_screen is None:
            self.previous_screen = screenshot
        
        obs = self.observations_to_single_box(screenshot,self.previous_screen,mask,self.player_color)
        self.previous_screen = screenshot

        return obs
    


    

if __name__ == "__main__":
    env = Trainer.load_new_bot()
    sm = env.get_observation()
    input()
        

    
    
    
    
