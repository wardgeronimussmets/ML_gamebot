import matplotlib.pyplot as plt
import cv2

GRAY_IMAGE = 1
BGR_IMAGE = 2
RGB_IMAGE = 3


def show_single_image(img1,image_types):
    if image_types == BGR_IMAGE:
        img1 = cv2.cvtColor(img1,cv2.COLOR_BGR2RGB)
    plt.figure()
    plt.imshow(img1)
    plt.show()
    
    
def show_images_2(image1,image2,image_types):
    # Create a figure with two subplots arranged side by side
    fig, axs = plt.subplots(1, 2)

    if image_types == GRAY_IMAGE:
        # Plot the first image in the left subplot
        axs[0].imshow(image1, cmap='gray')
        axs[0].set_title('Image 1')

        # Plot the second image in the right subplot
        axs[1].imshow(image2, cmap='gray')
        axs[1].set_title('Image 2')
    elif image_types == RGB_IMAGE:
        # Plot the first image in the left subplot
        axs[0].imshow(image1)
        axs[0].set_title('Image 1')

        # Plot the second image in the right subplot
        axs[1].imshow(image2)
        axs[1].set_title('Image 2')
        
    elif image_types == BGR_IMAGE:
        im1 = cv2.cvtColor(image1,cv2.COLOR_BGR2RGB)
        im2 = cv2.cvtColor(image2,cv2.COLOR_BGR2RGB)
        # Plot the first image in the left subplot
        axs[0].imshow(im1)
        axs[0].set_title('Image 1')

        # Plot the second image in the right subplot
        axs[1].imshow(im2)
        axs[1].set_title('Image 2')
        


    # Display the figure
    plt.show()