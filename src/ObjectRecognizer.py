import cv2
import numpy as np
import math
import ImageDisplay
import ImagePreprocessing
import random

from GameScreenCapturer import screenCapturer


MINIMAP_ZONE = (0.03,0.15,0.5,0.86)#format: left,right,top,bottom
MINIMAP_COLORS = (105,118,116)

SPEED_COLOR = (50,190,230)
SPEEDOMETER_ZONE = (0.83,0.908,0.88,0.94)#format: left,right,top,bottom


def get_mini_map(frame):
    width = frame.shape[1]
    height = frame.shape[0]
    mini_map = frame[math.floor(MINIMAP_ZONE[2]*height):math.floor(MINIMAP_ZONE[3]*height),
                     math.floor(MINIMAP_ZONE[0]*width):math.floor(MINIMAP_ZONE[1]*width)]
    
    #highlight minimap
    highlighted = ImagePreprocessing.hightlight_in_image([MINIMAP_COLORS],mini_map,10)
    return highlighted
    

def get_speed(frame):
    width = frame.shape[1]
    height = frame.shape[0]
    speedometer_frame = frame[math.floor(SPEEDOMETER_ZONE[2]*height):math.floor(SPEEDOMETER_ZONE[3]*height),
                     math.floor(SPEEDOMETER_ZONE[0]*width):math.floor(SPEEDOMETER_ZONE[1]*width)]
    enhanced_frame = ImagePreprocessing.hightlight_in_image([SPEED_COLOR],speedometer_frame,20,different_highlight_color=(250,250,250))
    first_digit,second_digit,third_digit = np.split(cv2.resize(enhanced_frame,(enhanced_frame.shape[0]//3*3,enhanced_frame.shape[1])),3,axis=1)
    # ImageDisplay.show_multiple_images([speedometer_frame,enhanced_frame,first_digit,second_digit,third_digit],ImageDisplay.BGR_IMAGE)

    numbs_recog = NumberRecognizer()
    speed = int(str(numbs_recog.which_number(first_digit))+str(numbs_recog.which_number(second_digit))+str(numbs_recog.which_number(third_digit)))
    print(speed)

    return enhanced_frame

class NumberRecognizer():
    def __init__(self) -> None:
        self.nums = []
        for x in range(10):
            self.nums.append(cv2.imread('src/resources/speedo_numbs/'+str(x)+'.png'))
    def which_number(self,img):
        if img.shape != self.nums[0].shape:
            img = cv2.resize(img,(self.nums[0].shape[1],self.nums[0].shape[0]))
        mses = []
        for x in range(len(self.nums)):
            mse = ImagePreprocessing.image_similarity(img,self.nums[x])
            print(mse)
            ImageDisplay.show_images_2(img,self.nums[x],ImageDisplay.BGR_IMAGE)
            #TODO: doesn't always work as well because the images can get shifted
            mses.append(mse)
        return mses.index(min(mses))
        

def recognize_from_video():
    cap = cv2.VideoCapture('src/resources/game_footage.mkv')
    
    skip_first_frames = 2600
    cap.set(1,skip_first_frames)

    while cap.isOpened():
        ret, frame = cap.read()
        # Make detections 
        resized = cv2.resize(frame,(720,480))
        get_speed(resized)
        
        cv2.imshow('YOLO',resized)
        
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def recognize_from_gameplay(screenshot):
    get_speed(screenshot)

def start_recognize_from_gameplay():
    screenCap = screenCapturer.ScreenCapturer()
    screenCap.start_capturing("FlatOut", recognize_from_gameplay)
    

if __name__ == "__main__":
    start_recognize_from_gameplay()
    
