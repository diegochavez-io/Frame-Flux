
# pip install moviepy

from moviepy.editor import *
import os

# Input Parameters
source_file = r"E:\Delenda Warp\02065280_runpod_8x_upscale.mov" # Specify the source file directly
resized_width = 1280  # Specify the desired width for the resized videos
codec = 'libx265'  # Specify the codec (options: 'libx265', 'libx264', 'prores')

# Output file name construction
output_file_name = f"{os.path.splitext(os.path.basename(source_file))[0]}_resized_to_{resized_width}w"
output_file = os.path.join(os.path.dirname(source_file), f"{output_file_name}{os.path.splitext(source_file)[1]}")

# Processing
# Load the video file
video_clip = VideoFileClip(source_file)

# Resize the video to the specified width while maintaining the aspect ratio
resized_clip = video_clip.resize(width=resized_width)

# Write the resized video to the same directory as the source file with the specified codec, without audio
resized_clip.write_videofile(output_file, codec=codec, audio=False)

print("Video resizing and re-encoding completed.")
