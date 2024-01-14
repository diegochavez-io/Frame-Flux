import os
from PIL import Image
import shutil

def sort_images_by_size(directory, min_size, good_folder, process_folder):
    # Create the directories if they don't exist
    os.makedirs(os.path.join(directory, good_folder), exist_ok=True)
    os.makedirs(os.path.join(directory, process_folder), exist_ok=True)
    
    for filename in os.listdir(directory):
        # We're only interested in files with a .jpg extension
        if not filename.endswith('.jpg'):
            continue

        filepath = os.path.join(directory, filename)
        with Image.open(filepath) as img:
            width, height = img.size

        # Close the image after checking its size
        img.close()

        # Move the file to the appropriate folder
        if width >= min_size and height >= min_size:
            shutil.move(filepath, os.path.join(directory, good_folder, filename))
        else:
            shutil.move(filepath, os.path.join(directory, process_folder, filename))

def main():
    directory = "G:\\My Drive\\dataset-footage\\shamoncassette\\tumblr"  # Replace with your directory
    min_size = 512
    good_folder = "_good"
    process_folder = "_process"
    sort_images_by_size(directory, min_size, good_folder, process_folder)

if __name__ == "__main__":
    main()
