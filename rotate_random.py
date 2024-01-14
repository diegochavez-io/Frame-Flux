
#pip install pillow

from PIL import Image
import os
import random

# Parameters
folder = r"D:\feather_TD\feather_TD"  # The folder containing the images to transform

# List of transforms to apply
transforms = [
    lambda image: image.rotate(90),
    lambda image: image.rotate(180),
    lambda image: image.rotate(270),
    lambda image: image.transpose(Image.FLIP_LEFT_RIGHT),
    lambda image: image.transpose(Image.FLIP_TOP_BOTTOM)
]

# Process each image file in the directory
for filename in os.listdir(folder):
    if filename.endswith(('.jpg', '.jpeg', '.png')):
        # Open the image file
        with Image.open(os.path.join(folder, filename)) as img:
            # Apply a random transform
            transform = random.choice(transforms)
            new_img = transform(img)
            # Save the transformed image, overwriting the original
            new_img.save(os.path.join(folder, filename))

