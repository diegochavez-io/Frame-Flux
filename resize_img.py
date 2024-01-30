from PIL import Image
import os

def resize_and_crop(image_path, output_path, size=(512, 512)):
    with Image.open(image_path) as img:
        # Calculate aspect ratio of the desired size
        target_ratio = size[0] / size[1]

        # Calculate aspect ratio of input image
        img_ratio = img.width / img.height

        # Determine dimensions to crop the image to maintain aspect ratio
        if img_ratio > target_ratio:
            new_height = img.height
            new_width = int(target_ratio * new_height)
        else:
            new_width = img.width
            new_height = int(new_width / target_ratio)

        # Calculate top-left corner of the cropped area
        left = (img.width - new_width) / 2
        top = (img.height - new_height) / 2

        # Crop and resize the image
        img_cropped = img.crop((left, top, left + new_width, top + new_height))
        img_resized = img_cropped.resize(size, Image.Resampling.LANCZOS)

        # Save the resized image
        img_resized.save(output_path)

def resize_images(input_folder, output_folder, size=(512, 512)):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
            image_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            resize_and_crop(image_path, output_path, size)

# Usage for a folder
input_folder = '/Users/agi/Desktop/moth'
output_folder = '/Users/agi/Desktop/moth_processed'
resize_images(input_folder, output_folder)
