import os
import subprocess

# Path to the source video
video_path = r"G:\My Drive\dataset-footage\shamoncassette\video\sc-2\spliced_2\clip_3.mp4"  # replace with the path to your video

# Path to the output folder
output_folder = r"G:\My Drive\dataset-footage\shamoncassette\video\sc-2\spliced_2\frames"  # replace with the path to your output folder

# Desired output frames per second
fps = 12  # replace with your desired fps

def video_to_frames(video_path, output_folder, fps=1):
    # Make the output folder if it doesn't already exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Construct the ffmpeg command
    cmd = f'ffmpeg -i "{video_path}" -vf "fps={fps}" "{os.path.join(output_folder, "frame_%04d.png")}"'

    # Call ffmpeg
    subprocess.call(cmd, shell=True)

# Call the function
video_to_frames(video_path, output_folder, fps)
