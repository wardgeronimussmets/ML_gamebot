# Import os for file path management
import os 
# Import Base Callback for saving models
from stable_baselines3.common.callbacks import BaseCallback
# Check Environment    
from stable_baselines3.common import env_checker
from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.vec_env import DummyVecEnv, VecFrameStack

import GamepadEmulator
import PlayerRecogniser
import time
import Environments

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
    print("adding new bot")
    previous_player_colors = PlayerRecogniser.recognize_once()
    gamepad = GamepadEmulator.GamePad()
    #random input so the player joins
    for i in range(4):
        gamepad.modulate_jump(True)
        time.sleep(0.1)
        gamepad.modulate_jump(False)
        time.sleep(0.1)
    new_player_colors = PlayerRecogniser.recognize_once()
    for key in new_player_colors:
        if key not in previous_player_colors:
            new_player = key
            env = Environments.GameEnv(new_player,new_player_colors,gamepad)
            return env
    
    
def start_training():
    #load 1 env with gamepad
    env = load_new_bot()
    if env is not None:
        #create new model
        model = PPO('CnnPolicy', env, tensorboard_log=LOG_DIR, verbose=1)
        callback = TrainAndLoggingCallback(check_freq=1000, save_path=CHECKPOINT_DIR)
        model.learn(total_timesteps=100000, callback=callback)
        
        
if __name__ == "__main__":
    start_training()