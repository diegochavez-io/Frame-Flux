#pip install colour-science

import cv2
import numpy as np
import os
from PIL import Image, ImageEnhance
import colour

# Parameters
image_folder = "D:\_HAP\inner paint 70 e frame--2x-RIFE-RIFE4.0-48fps_scale_2x_alq-13"  # Folder containing images
lut_path = 'D:\Dropbox\_Resources\Luts\Lutify.me Professional\Teal & Orange\Labradorite.cube'  # Lookup table
output_folder = os.path.join(image_folder, 'processed')  # Output folder
saturation_level = 0  # Saturation level (0 means no change)
lut_mix = 1  # Mix factor between original image and LUT image (0 means 100% original, 1 means 100% LUT)

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Read the LUT from the file
lut = colour.read_LUT(lut_path)

# Get the list of image files in the folder
image_files = [f for f in os.listdir(image_folder) if f.endswith('.jpg') or f.endswith('.png')]

# Set the test image to the first image in the list
test_image = image_files[0]

# Process all images in the folder
for image_filename in image_files:
    # Uncomment the following line to only process the test image
    # if image_filename != test_image: continue

    # Open image
    image = Image.open(os.path.join(image_folder, image_filename))

    # Adjust saturation if the level is not zero
    if saturation_level != 0:
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(saturation_level)

    # Convert image to numpy array
    original_image_array = np.array(image)

    # Scale image data to 0-1
    image_array = original_image_array / 255.0

    # Apply LUT
    lut_image_array = lut.apply(image_array)

    # Mix original image and LUT image
    image_array = (1 - lut_mix) * image_array + lut_mix * lut_image_array

    # Scale image data back to 0-255
    image_array = image_array * 255.0

    # Ensure data is in range 0-255
    image_array = np.clip(image_array, 0, 255)

    # Convert array data type to 'uint8'
    image_array = image_array.astype('uint8')

    # Convert back to Image
    image = Image.fromarray(image_array)

    # Save image
    image.save(os.path.join(output_folder, image_filename))

print(f"Processed {len(image_files)} images.")

