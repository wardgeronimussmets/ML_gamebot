import GamepadEmulator
import time
import random

if __name__=="__main__":
    gamepad = GamepadEmulator.GamePad()
    while True:
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
        gamepad.modulate_jump(random.choice([True,False]))
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
        
        