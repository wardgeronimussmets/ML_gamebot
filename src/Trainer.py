import ImageDisplay
import ScreenGrabber
# Import os for file path management
import os 
# Import Base Callback for saving models
from stable_baselines3.common.callbacks import BaseCallback
# Check Environment    
from stable_baselines3.common import env_checker
from stable_baselines3 import PPO,DQN
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.vec_env import DummyVecEnv, VecFrameStack

import GamepadEmulator
import PlayerRecogniser
import time
import Environments
import RandomBot

CHECKPOINT_DIR = './train/'
LOG_DIR = './logs/'



class TrainAndLoggingCallback(BaseCallback):

    def __init__(self, check_freq, save_path, verbose=1):
        super(TrainAndLoggingCallback, self).__init__(verbose)
        self.check_freq = check_freq
        self.save_path = save_path

    def _init_callback(self):
        if self.save_path is not None:
            os.makedirs(self.save_path, exist_ok=True)

    def _on_step(self):
        if self.n_calls % self.check_freq == 0:
            model_path = os.path.join(self.save_path, 'best_model_{}'.format(self.n_calls))
            self.model.save(model_path)

        return True
    

def load_new_bot():
    while True:
        print("attempting to add new bot")
        previous_player_colors = PlayerRecogniser.recognize_once()
        print("Already existing players are",previous_player_colors)
        gamepad = GamepadEmulator.GamePad()
        #random input so the player joins
        print("Starting random inputs")
        for i in range(10):
            RandomBot.random_input(gamepad)
        print("done with random inputs")
        gamepad.update_movement(-1,0)
        time.sleep(1)
        gamepad.update_movement(0,0)      
            

        #wait for player to drop down in the map
        new_player_colors = PlayerRecogniser.recognize_once()
        print("adding from ",new_player_colors)
        # print("player colors",new_player_colors)
        if len(previous_player_colors) + 1 == len(new_player_colors):
            #new player has been added, but which
            for new_player_key in new_player_colors:
                no_match_found = True
                for old_player_key in previous_player_colors:
                    matched = True
                    for color in range(3):
                        if abs(old_player_key[color]- new_player_key[color])>20:
                            matched = False
                    if matched:
                        no_match_found = False
                if no_match_found:
                    #that is the new player
                    new_player = new_player_key
                    break
            env = Environments.GameEnv(new_player,new_player_colors,gamepad,image_logging=True)
            print("Adding new bot with color", new_player)
            return env
        print("Failed to add new bot couldn't detect one new player")
        gamepad.destroy()
    
    
def start_training():
    #load 1 env with gamepad
    env = load_new_bot()
    env_faults = env_checker.check_env(env)
    if env is not None:
        #create new model
        model = PPO('CnnPolicy', env, tensorboard_log=LOG_DIR, verbose=1)        
        callback = TrainAndLoggingCallback(check_freq=1000, save_path=CHECKPOINT_DIR)
        print("starting to learn")
        model.learn(total_timesteps=100000, callback=callback)
        
        
if __name__ == "__main__":
    start_training()