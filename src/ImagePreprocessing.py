import numpy as np
import cv2

def hightlight_in_image(pixels,image_to_filter,pixel_value_range=70,different_highlight_color=None):
    #default pixel value range is high, but this works very well
    mask = image_to_filter.copy()
    for i in range(len(image_to_filter)):
        for j in range(len(image_to_filter[i])):                    
            player_matches = []
            for player_pixels in pixels:
                player_match = True
                for pixel_index in range(3):
                    if (image_to_filter[i][j][pixel_index] + pixel_value_range < player_pixels[pixel_index]) or (image_to_filter[i][j][pixel_index] - pixel_value_range > player_pixels[pixel_index]):
                        player_match = False
                        break
                player_matches.append(player_match)
            if True not in player_matches:
                mask[i][j] = (0,0,0)
            else:
                if different_highlight_color:
                    mask[i][j] = different_highlight_color
    return mask


def image_similarity(img1,img2):
    h, w, c  = img1.shape
    diff = cv2.subtract(img1, img2)
    err = np.sum(diff**2)
    mse = err/(float(h*w))
    return mse