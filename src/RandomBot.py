import GamepadEmulator
import time
import random
import msvcrt

"""The random player doesn't need to be good, it needs to provide random movement to train the bot on
"""

def random_move(gamepad):
    gamepad.update_movement(random.choice([-1,0,1]),random.choice([-1,0,1]))
    time.sleep(random.randrange(1,100)/100)


def random_input(gamepad):
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
    
    #some to get activated
    print("random bot starting in 3")
    time.sleep(3)
    print("the moose is loose")
    running = True
    while running:
        random_input(gamepad)
        if msvcrt.kbhit():
            #pauzing to get everything fixed
            print("pauzing give some random input to continue")
            gamepad.update_movement(0,0)
            action = input()
            if action == "quit":
                print("I will quit")
                running = False
            else:
                print("Continuing to loose the moose")
        
        
        
        