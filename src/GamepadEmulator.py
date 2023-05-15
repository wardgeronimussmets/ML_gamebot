import vgamepad as vg
import time 

class GamePad():
    def __init__(self) -> None:
        self.gamepad = vg.VX360Gamepad()
        
    def jump(self):
        self.press_and_release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
        
        
    def press_and_release_button(self,button):
        self.gamepad.press_button(button=button)
        self.gamepad.update()
        time.sleep(0.2)
        self.gamepad.release_button(button=button)
        self.gamepad.update()
        
        
if __name__ == "__main__":
    gam = GamePad()
    time.sleep(5)
    for x in range(3):
        print("jumping")
        gam.jump()
        time.sleep(3)