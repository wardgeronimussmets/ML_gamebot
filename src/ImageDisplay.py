import matplotlib.pyplot as plt


def show_single_image(img1):
    plt.figure()
    plt.imshow(img1)
    plt.show()
    
    
def show_images_2(image1,image2):
    # Create a figure with two subplots arranged side by side
    fig, axs = plt.subplots(1, 2)

    # Plot the first image in the left subplot
    axs[0].imshow(image1, cmap='gray')
    axs[0].set_title('Image 1')

    # Plot the second image in the right subplot
    axs[1].imshow(image2, cmap='gray')
    axs[1].set_title('Image 2')

    # Display the figure
    plt.show()