import cv2
import numpy as np
import math


MINIMAP_ZONE = (0.03,0.15,0.5,0.86)#format: left,right,top,bottom


def get_mini_map(frame):
    width = frame.shape[1]
    height = frame.shape[0]
    mini_map = frame[math.floor(MINIMAP_ZONE[2]*height):math.floor(MINIMAP_ZONE[3]*height),
                     math.floor(MINIMAP_ZONE[0]*width):math.floor(MINIMAP_ZONE[1]*width)]
    return mini_map
    


if __name__ == "__main__":
    
    cap = cv2.VideoCapture('src/resources/game_footage.mkv')
    
    skip_first_frames = 2000
    cap.set(1,skip_first_frames)

    while cap.isOpened():
        ret, frame = cap.read()
        
        # Make detections 
        
        mini_map = get_mini_map(frame)
        
        cv2.imshow('YOLO', mini_map)
        
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
