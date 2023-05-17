import torch
from matplotlib import pyplot as plt
import numpy as np
import cv2
import ScreenGrabber
import math


class ObjectDetector():
    def __init__(self) -> None:
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5/runs/train/exp5/weights/last.pt')#, force_reload=True)
        
    def get_player_distance(self,image):
        results = self.model(image)
        result_arrays = results.xyxy[0]
        centers = []
        for result in result_arrays:
            center_1 = ((result[0]+result[2])/2,(result[1]+result[3])/2)
            centers.append(center_1)
            
        distance = math.sqrt((centers[1][0] - centers[0][0]) ** 2 + (centers[1][1] - centers[0][1]) ** 2)
        
        return distance

    
    
if __name__ == "__main__":
    img = ScreenGrabber.get_screenshot()
    objd = ObjectDetector()
    objd.get_player_distance(img)