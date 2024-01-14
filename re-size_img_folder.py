import os
from PIL import Image

# Path to the source folder
source_folder = r"F:\Algo-Film\Delenda_Shoot_230818\Photos\Square"

# Path to the output folder
output_folder = r"F:\Algo-Film\Delenda_Shoot_230818\Photos\Square\512"

# If the output folder doesn't exist, create it
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Desired output size
output_size = (512, 512)

# Iterate over all files in the source folder
for filename in os.listdir(source_folder):
    # Check if the file is an image
    if filename.endswith(".jpg") or filename.endswith(".png"):
        # Construct the full file path for the source image
        filepath = os.path.join(source_folder, filename)

        # Construct the full file path for the output image
        output_filepath = os.path.join(output_folder, filename)

        try:
            # Open the image file
            img = Image.open(filepath)

            # Calculate the scale factor
            width, height = img.size
            scale_factor = max(output_size[0] / width, output_size[1] / height)

            # Resize the image maintaining aspect ratio, scaling up if necessary
            new_size = (int(width * scale_factor), int(height * scale_factor))
            img_resized = img.resize(new_size, Image.LANCZOS)

            # Calculate the area to crop
            width, height = img_resized.size
            left = (width - output_size[0])/2
            top = (height - output_size[1])/2
            right = (width + output_size[0])/2
            bottom = (height + output_size[1])/2

            # Crop the image
            img_cropped = img_resized.crop((left, top, right, bottom))

            # Save the cropped image to the output folder
            img_cropped.save(output_filepath)

        except Exception as e:
            print(f"Error processing file {filepath}: {str(e)}")

print("Resizing and cropping completed.")
