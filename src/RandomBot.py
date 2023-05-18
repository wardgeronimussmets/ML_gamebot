import GamepadEmulator
import time
import random

"""The random player doesn't need to be good, it needs to provide random movement to train the bot on
"""


def random_input():
    #apply random movement, biased to the right
    horizontal_move = random.random()
    if horizontal_move > 0.6:
        horizontal_move = -1
    else:
        horizontal_move = 1
    vertical_move = random.random()
    if vertical_move > 0.5:
        vertical_move = -1
    else:
        vertical_move = 1
    
    gamepad.update_movement(horizontal_move,vertical_move)
    
    time.sleep(0.2)
    
    #random aim
    gamepad.update_aim(random.uniform(-1,1),random.uniform(-1,1))
    time.sleep(0.2)
    
    #random jump
    is_jumping = random.choice([True,False])
    if is_jumping:
        #make sure no pulling down on the movement joystick is happening, otherwise the player won't jump but will stay down on the ground
        #also an extra wait time to give it some air time
        if vertical_move < 0:
            vertical_move = 0
        gamepad.update_movement(horizontal_move,vertical_move)
        gamepad.modulate_jump(True)
        time.sleep(1)
    else:
        gamepad.modulate_jump(False)
        time.sleep(0.2)
    
    #random blocking action
    choice = random.choice([0,1,2,3])
    if choice == 0:
        gamepad.release_blocking()
    elif choice == 1:
        gamepad.modulate_attack(True)
    elif choice == 2:
        gamepad.modulate_block(True)
    elif choice == 3:
        gamepad.modulate_throw(True)
            
    time.sleep(1)



if __name__=="__main__":
    gamepad = GamepadEmulator.GamePad()
    
    while True:
        #some to get activated
        for x in range(0,3):
            random_input()
        print("waiting for other activation")
        time.sleep(10)
        
        
        
        