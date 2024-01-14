from moviepy.editor import ImageSequenceClip
import os
import glob

# Folder where the images are located
source_folder = 'G:\My Drive\AI\StableWarpFusion\images_out\__dan_msi\23_02055183_stable_warpfusion_0.23.0_reversed_video'
# Output file name
output_file = os.path.join(os.path.dirname(source_folder), '23_02055183_random__reversed_video.mp4')
# File patterns, change these if your images have a different naming pattern
file_patterns = ['%04d.jpg', '%04d.png', '%04d.dpx']

# Check if source_folder exists
if not os.path.isdir(source_folder):
    print(f"Error: Source folder {source_folder} does not exist.")
    exit(1)

for file_pattern in file_patterns:
    # Get a list of all files that match the file_pattern
    filenames = glob.glob(os.path.join(source_folder, file_pattern.replace("%04d", "*")))
    filenames.sort()  # Ensure the images are in order

    if not filenames:
        print(f"No images found with pattern {file_pattern}")
        continue

    print(f"Found {len(filenames)} images with pattern {file_pattern}. Processing...")
    
    # Make a clip out of these images
    clip = ImageSequenceClip(filenames, fps=30)
    
    # Write the clip to a file
    clip.write_videofile(output_file, codec='libx264')
