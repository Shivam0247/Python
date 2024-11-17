from PIL import Image, ImageFilter, ImageEnhance
import matplotlib.pyplot as plt
import numpy as np
import os

def list_files_in_directory(directory):
    """List all files in the specified directory for debugging purposes."""
    try:
        files = os.listdir(directory)
        print("Files in directory:", files)
    except Exception as e:
        print(f"Error accessing directory: {str(e)}")

def load_image(file_path):
    """Load an image from the specified file path."""
    try:
        image = Image.open(file_path)
        image.show()
        return image
    except Exception as e:
        print(f"Error loading image at {file_path}: {str(e)}")
        return None

def apply_filter(image, filter_type):
    """Apply a specified filter to the image."""
    if filter_type == 'gaussian_blur':
        return image.filter(ImageFilter.GaussianBlur(radius=2))
    elif filter_type == 'edge_detection':
        return image.filter(ImageFilter.FIND_EDGES)
    else:
        print("Invalid filter type!")
        return image

def resize_image(image, new_size):
    """Resize the image to a new size (width, height)."""
    return image.resize(new_size)

def crop_image(image, crop_area):
    """Crop the image to a specific area (left, upper, right, lower)."""
    return image.crop(crop_area)

def adjust_brightness(image, factor):
    """Adjust the brightness of the image."""
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(factor)

def convert_to_grayscale(image):
    """Convert the image to grayscale."""
    return image.convert("L")

def display_histogram(image):
    """Display the histogram for each color channel of the image."""
    image_array = np.array(image)
    
    if len(image_array.shape) == 2:  # Grayscale image
        plt.hist(image_array.ravel(), bins=256, color='black')
        plt.title('Grayscale Histogram')
    else:  # Color image
        colors = ('red', 'green', 'blue')
        for i, color in enumerate(colors):
            plt.hist(image_array[:, :, i].ravel(), bins=256, color=color, alpha=0.6, label=f'{color.capitalize()} channel')
        plt.title('Color Histogram')
        plt.legend()

    plt.xlabel('Pixel Intensity')
    plt.ylabel('Frequency')
    plt.show()

# Example usage:
if __name__ == "__main__":
    # Define the directory and image path
    directory = os.path.expanduser("~/Documents/PythonLab/Practical 11")  # Adjust the path for macOS
    list_files_in_directory(directory)  # List files in directory for debugging

    # Load an image
    image_path = os.path.join(directory, "1.jpg")  # Ensure this file exists in the specified directory
    image = load_image(image_path)

    if image:
        # Apply a Gaussian blur filter
        blurred_image = apply_filter(image, "gaussian_blur")
        blurred_image.show()
        
        # Resize the image to (200, 200)
        resized_image = resize_image(image, (200, 200))
        resized_image.show()

        # Crop the image to a specific region
        cropped_image = crop_image(image, (50, 50, 200, 200))
        cropped_image.show()

        # Adjust brightness
        brighter_image = adjust_brightness(image, 1.5)
        brighter_image.show()

        # Convert the image to grayscale
        grayscale_image = convert_to_grayscale(image)
        grayscale_image.show()

        # Display histogram
        display_histogram(image)
