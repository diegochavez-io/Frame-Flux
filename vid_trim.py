
import os
import subprocess
import shutil

# Directory containing exported clips
input_directory = "/Users/agi/Dropbox/Delenda/Catalyst/Live-Action/5sec"
output_directory = "/Users/agi/Dropbox/Delenda/Catalyst/Live-Action/5sec/trimmed"

if not os.path.exists(output_directory):
    os.makedirs(output_directory)

def detect_black_frames(video_file_path):
    command = [
        "ffmpeg", "-i", video_file_path,
        "-vf", "blackdetect=d=0.1:pix_th=0.00", "-an", "-f", "null", "-"
    ]
    result = subprocess.run(command, stderr=subprocess.PIPE, text=True)
    return result.stderr

def trim_video(input_file_path, output_file_path):
    command = [
        "ffmpeg", "-i", input_file_path, "-ss", "1", "-c", "copy", output_file_path
    ]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.returncode, result.stderr

for filename in os.listdir(input_directory):
    if filename.endswith(".mp4"):
        input_file_path = os.path.join(input_directory, filename)
        output_file_path = os.path.join(output_directory, filename)

        black_frames_info = detect_black_frames(input_file_path)

        if "black_start:" in black_frames_info:
            # Trim the video to remove the 1-second black frame
            return_code, trim_info = trim_video(input_file_path, output_file_path)
            if return_code != 0:
                print(f"Error trimming video {filename}: {trim_info}")
            else:
                print(f"Trimmed video {filename} to remove 1-second black frame.")
        else:
            # No black frames detected, copy the video as is
            shutil.copy(input_file_path, output_file_path)
            print(f"Copied video {filename} without changes.")

print("Processing completed.")
