from gigapixel import Gigapixel, Scale, Mode, OutputFormat
from pathlib import Path
import os

# Parameters
exe_path = Path('C:\\Program Files\\Topaz Labs LLC\\Topaz Gigapixel AI\\Topaz Gigapixel AI.exe')
output_suffix = '-gigapixel'
source_folder = "G:\My Drive\AI\SGXL_Output\LookingGlasss_04_snapshot-000240"
scale_size = Scale.X6  # Update this value as needed.

# Create Gigapixel instance.
app = Gigapixel(exe_path, output_suffix)

# Process each image in the source folder.
for filename in os.listdir(source_folder):
    try:
        if filename.endswith(".jpg") or filename.endswith(".png"): 
            image_path = Path(os.path.join(source_folder, filename))

            # Determine the output format based on the source image file extension.
            file_extension = image_path.suffix.lower()
            if file_extension == '.jpg':
                output_format = OutputFormat.JPG
            elif file_extension == '.png':
                output_format = OutputFormat.PNG
            else:
                print(f"Unsupported file extension {file_extension}. Skipping file {filename}.")
                continue

            # Construct the output path
            output_path = Path(f"{str(image_path.resolve())}{output_suffix}")

            # Check if the output image already exists. If it does, skip this image.
            if output_path.exists():
                print(f"Output image {output_path} already exists. Skipping file {filename}.")
                continue

            # Process the image
            output_path = app.process(image_path, scale=scale_size, mode=Mode.STANDARD, delete_from_history=True, output_format=output_format)

            print(f"Processed image output at: {output_path}")
    except Exception as e:
        print(f"An error occurred while processing image {filename}: {e}")
