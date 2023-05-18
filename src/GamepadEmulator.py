import vgamepad as vg
import time 

JUMP = vg.XUSB_BUTTON.XUSB_GAMEPAD_A
ATTACK = vg.XUSB_BUTTON.XUSB_GAMEPAD_X
BLOCKING  = 75758
THROW = vg.XUSB_BUTTON.XUSB_GAMEPAD_Y


class GamePad():
    def __init__(self) -> None:
        succeeded = False
        for x in range(5):
            try:
                self.gamepad = vg.VX360Gamepad()
                print("Succesfully started gamepad")
                succeeded = True
                break
            except Exception as e:
                print(e)
        if not succeeded:
            exit()
        self.blocking_action = None
        self.jumping = None
        
    def modulate_jump(self,wants_to_jump):
        if wants_to_jump and not self.jumping:
            self.gamepad.press_button(JUMP)
        elif not wants_to_jump and self.jumping:
            self.gamepad.release_button(JUMP)
        self.gamepad.update()
        
    def modulate_attack(self,wants_to_attack):
        if wants_to_attack:
            if not self.blocking_action == ATTACK:
                #were doing something that would prevent this -> release that button 
                if self.blocking_action != BLOCKING:
                    if self.blocking_action is not None:
                        self.gamepad.release_button(self.blocking_action)
                else:
                    self.gamepad.left_trigger_float(0)
                self.gamepad.press_button(ATTACK)
                self.blocking_action = ATTACK
                    
        else:
            if self.blocking_action == ATTACK:
                self.gamepad.release_button(ATTACK)
                self.blocking_action = None
        
        self.gamepad.update()
    
    
    def modulate_block(self,wants_to_block):
        if wants_to_block:
            if not self.blocking_action == BLOCKING:
                #were doing something that would prevent this -> release that button 
                if self.blocking_action is not None:
                    self.gamepad.release_button(self.blocking_action)
                self.gamepad.left_trigger_float(1)
                self.blocking_action = BLOCKING
        else:
            if self.blocking_action == BLOCKING:
                self.gamepad.left_trigger_float(0)
                self.blocking_action = None
        self.gamepad.update()
        
    def modulate_throw(self,wants_to_throw):
        if wants_to_throw:
            if not self.blocking_action == THROW:
                #were doing something that would prevent this -> release that button 
                if self.blocking_action != BLOCKING:
                    if self.blocking_action is not None:
                        self.gamepad.release_button(self.blocking_action)
                else:
                    self.gamepad.left_trigger_float(0)
                self.gamepad.press_button(THROW)
                self.blocking_action = THROW
                    
        else:
            if self.blocking_action == THROW:
                self.gamepad.release_button(THROW)
                self.blocking_action = None
        
        self.gamepad.update()
        
        
        
    def release_blocking(self):
        if self.blocking_action == BLOCKING:
            self.gamepad.left_trigger_float(0)
        else:
            if self.blocking_action is not None:
                self.gamepad.release_button(self.blocking_action)
        self.blocking_action = None
        self.gamepad.update()
        
                
            
        
        
        
        
    def press_and_release_button(self,button):
        self.gamepad.press_button(button=button)
        self.gamepad.update()
        time.sleep(0.2)
        self.gamepad.release_button(button=button)
        self.gamepad.update()
        
    def update_movement(self,x_movement,y_movement):
        try:
            self.gamepad.left_joystick_float(x_value_float=x_movement,y_value_float=y_movement)
            self.gamepad.update()
        except Exception:
            print("Failed to input left joystick")
    
    def update_aim(self,x_aim,y_aim):
        try:
            self.gamepad.right_joystick_float(x_value_float=x_aim,y_value_float=y_aim)
            self.gamepad.update()
        except Exception:
            print("Failed to input the right joystick")
            
    def destroy(self):
        self.gamepad.reset()
        
        
if __name__ == "__main__":
    gam = GamePad()
    time.sleep(5)
    for x in range(3):
        print("jumping")
        gam.press_and_release_button(JUMP)
        time.sleep(3)