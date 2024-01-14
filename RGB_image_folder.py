import os
from PIL import Image

# Path to the source folder
source_folder = r"E:\CAT_2308\1. Media\Photos"

# Path to the output folder
output_folder = r"E:\CAT_2308\1. Media\Photos\Output"

# If the output folder doesn't exist, create it
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Iterate over all files in the source folder
for filename in os.listdir(source_folder):
    # Check if the file is an image
    if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".tif"):
        # Construct the full file path for the source image
        filepath = os.path.join(source_folder, filename)

        # Construct the full file path for the output image
        output_filepath = os.path.join(output_folder, filename)

        try:
            # Open the image file
            img = Image.open(filepath)

            # Check if the image mode is CMYK and convert to RGB if necessary
            if img.mode == "CMYK":
                img_rgb = img.convert("RGB")
                img_rgb.save(output_filepath)
            else:
                print(f"{filename} is not CMYK. Copying without conversion.")
                img.save(output_filepath)

        except Exception as e:
            print(f"Error processing file {filepath}: {str(e)}")

print("Color profile conversion completed.")
