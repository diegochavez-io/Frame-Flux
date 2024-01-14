

import os
import glob
from moviepy.editor import *

# Image file patterns
file_patterns = ['%04d.jpg', '%04d.png', '%04d.dpx']

# Source folder
source_folder = r"G:\My Drive\algo-film\delenda_algo_film_shoot_0822\random-frames_01"

# Output folder
output_folder = r"G:\My Drive\algo-film\delenda_algo_film_shoot_0822"


# Check if source_folder exists
if not os.path.isdir(source_folder):
    print(f"Error: Source folder {source_folder} does not exist.")
    exit(1)

# Check if output_folder exists, if not create it
if not os.path.isdir(output_folder):
    os.makedirs(output_folder)

# Extracting the first 14 characters from the last part of the source folder path
output_prefix = os.path.basename(source_folder)[:14]

for file_pattern in file_patterns:
    # Get a list of all files that match the file_pattern
    filenames = glob.glob(os.path.join(source_folder, file_pattern.replace("%04d", "*")))
    filenames.sort()  # Ensure the images are in order

    if not filenames:
        print(f"No images found with pattern {file_pattern}")
        continue

    print(f"Found {len(filenames)} images with pattern {file_pattern}. Processing...")

    # Make a clip out of these images
    clip = ImageSequenceClip(filenames, fps=24)

    # Set the output video name
    output_video = os.path.join(output_folder, f"{output_prefix}_{file_pattern.replace('%04d', '')}.mp4")

    # Write the clip to a video file
    clip.write_videofile(output_video, codec="libx264", fps=12)

print("Video creation completed.")
