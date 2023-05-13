    # def difference_title_colors(self,img1,img2):
    #     if img1.shape != img2.shape:
    #         raise Exception("length of winner area to compare is not the same between current and last frame")        
               
    #     diff = self.image_difference_in_total(img1,img2)
    #     return diff
    
    # def image_difference_in_total(self,img1,img2):
    #     diff = np.linalg.norm(img1-img2)
    #     return diff

        
        
    # def image_difference_pixels_above_threshold(self,img1,img2):
    #     if img1.ndim == 2:
    #         #GreyScale
    #         pixel_max = 255
    #         colors = [0]
    #         img1 = np.array([img1])
    #         img2 = np.array([img2])
    #     else:
    #         #rbg
    #         pixel_max = 255
    #         colors = [0,1,2]        
            
    #     threshold = pixel_max*PIXEL_COLOR_DIFF_THRESHOLD
    #     #count the amount of pixels that are different
    #     different_pixels = 0
    #     for i in range(len(img1[0])):
    #         for j in range(len(img1[0][0])):
    #             #if any of the colors is too different 
    #             for color in colors:
    #                 if abs(img1[color][i][j] - img2[color][i][j])>threshold:
    #                     different_pixels += 1
    #                     break
                    
    #     diff = different_pixels/len(img1)   
    #     return diff  
    
    
    # def get_level_winner_with_pixel_counting(self,new_screen_cap):        
    #     if new_screen_cap.ndim == 2:
    #         #GreyScale
    #         colors = [0]
    #         new_screen_cap = np.array([new_screen_cap])
    #     else:
    #         #rbg
    #         colors = [0,1,2]    
        
    #     counting_map = {}
        
    #     for i in range(len(new_screen_cap[0])):
    #         for j in range(len(new_screen_cap[0][0])):
    #             #if any of the colors is too different 
    #             color_key = ""
    #             for color in colors:
    #                 color_key += str(new_screen_cap[color][i][j])+"-"
    #             color_key = color_key[:-1]
    #             if color_key in counting_map:
    #                 counting_map[color_key] += 1
    #             else:
    #                 counting_map[color_key] = 0
    #     max_same_pixels_key = max(counting_map,key=counting_map.get)
    #     total_pixels = len(new_screen_cap[0])
    #     max_same_pixels = counting_map[max_same_pixels_key]
    #     max_same_pixel_ratio = max_same_pixels/total_pixels
    #     print(max_same_pixel_ratio)
        
                    
           
    
    
    # def get_level_winner_with_tesseract(self):
    #     new_screen_cap = np.array(self.cap.grab(self.level_winner_region))[:,:,:3]
    #     res = pytesseract.image_to_string(new_screen_cap)
    #     print(res)
    
    
    # def get_level_winner_via_color_diff(self,new_screen_cap):
        
    #     if self.last_winner_area is not None:
    #         diff = self.difference_title_colors(self.last_winner_area,new_screen_cap)
    #         print(diff)
    #         if  diff > TITLE_COLOR_THRESHOLD:
    #             print("triggered treshold")
            
    #     self.last_winner_area = new_screen_cap
    #     return