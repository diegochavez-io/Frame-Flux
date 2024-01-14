import os
from PIL import Image

# Path to the source folder
source_folder = r"H:\Algo-Film\Delenda_Shoot_230818\Photos\Square"
output_folder = os.path.join(source_folder, "processed")
os.makedirs(output_folder, exist_ok=True)

# Desired output size
output_size = (1024, 1024)

# Iterate over all files in the source folder
for filename in os.listdir(source_folder):
    # Check if the file is an image
    if filename.endswith(".jpg") or filename.endswith(".png"):
        # Construct the full file path
        filepath = os.path.join(source_folder, filename)

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

            # Save the cropped image back to the file
            output_filepath = os.path.join(output_folder, filename)
            img_cropped.save(output_filepath)

        except Exception as e:
            print(f"Error processing file {filepath}: {str(e)}")

print("Resizing and cropping completed.")
