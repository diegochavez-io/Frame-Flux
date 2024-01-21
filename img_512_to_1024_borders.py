from PIL import Image
import os

def add_black_border(image_path, output_path, final_size=(1024, 1024)):
    with Image.open(image_path) as img:
        # Create a new image with desired size and black background
        new_img = Image.new('RGB', final_size, (0, 0, 0))

        # Calculate the position to paste the original image
        x = (final_size[0] - img.width) // 2
        y = (final_size[1] - img.height) // 2

        # Paste the original image onto the new image
        new_img.paste(img, (x, y))

        # Save the new image
        new_img.save(output_path)

def process_folder(input_folder, output_folder, final_size=(1024, 1024)):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
            image_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            add_black_border(image_path, output_path, final_size)

# Usage example
input_folder = '/Users/agi/Library/CloudStorage/GoogleDrive-diegovchavez@gmail.com/My Drive/dataset-footage/delenda/dlnda_catalyst'
output_folder = '/Users/agi/Desktop/del_socials/'
process_folder(input_folder, output_folder)
