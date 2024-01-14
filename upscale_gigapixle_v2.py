import os
from gigapixel import Gigapixel, Scale, Mode, OutputFormat
from pathlib import Path

# Parameters
exe_path = Path("C:\Program Files\Topaz Labs LLC\Topaz Gigapixel AI\Topaz Gigapixel AI.exe")
output_suffix = '-gigapixel'
source_folder = r'G:\My Drive\algo-film\delenda_algo_film_shoot_0822\_warp_sd\_dan_comp\03_segment_38_stable_warpfusion_0.23.0_'
output_folder = r'G:\My Drive\algo-film\delenda_algo_film_shoot_0822\_warp_sd\_dan_comp\03_segment_38_stable_warpfusion_0.23.0_\upsclae'  # <-- New output folder
scale_size = Scale.X2  # Update this value as needed.

# Create the output directory if it doesn't already exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

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
            output_filename = f"{filename}{output_suffix}"  # <-- Just get the filename with suffix
            output_path = Path(os.path.join(output_folder   
            , output_filename))  # <-- Construct the full path

            # Check if the output image already exists. If it does, skip this image.
            if output_path.exists():
                print(f"Output image {output_path} already exists. Skipping file {filename}.")
                continue

            # Process the image
            output_path = app.process(image_path, scale=scale_size, mode=Mode.STANDARD, delete_from_history=True, output_format=output_format)

            print(f"Processed image output at: {output_path}")
    except Exception as e:
        print(f"An error occurred while processing image {filename}: {e}")
