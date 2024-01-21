from PIL import Image
import os

def resize_images(folder_path, output_folder, size=(512, 512)):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(folder_path):
        if filename.endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
            image_path = os.path.join(folder_path, filename)
            with Image.open(image_path) as img:
                img_resized = img.resize(size, Image.Resampling.LANCZOS)

                output_path = os.path.join(output_folder, filename)
                img_resized.save(output_path)

# Usage example
input_folder = '/Users/agi/Desktop/delnda_cat'
output_folder = '/Users/agi/Desktop/delnda_cat_processed'
resize_images(input_folder, output_folder)
