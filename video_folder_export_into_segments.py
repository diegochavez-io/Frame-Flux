import os
import subprocess
import math
import random
import uuid

def get_video_length(video_file_path):
    command = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", video_file_path]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return float(result.stdout)

def splice_video_fixed_segments(video_file_path, clip_length, output_dir):
    video_length = get_video_length(video_file_path)
    num_clips_to_export = math.floor(video_length / clip_length)
    
    base_name = os.path.splitext(os.path.basename(video_file_path))[0]
    output_subdir = os.path.join(output_dir, base_name)
    
    if not os.path.exists(output_subdir):
        os.mkdir(output_subdir)

    for i in range(num_clips_to_export):
        clip_start = i * clip_length
        clip_end = clip_start + clip_length
        output_file_path = os.path.join(output_subdir, f"segment_{i+1}.mp4")

        command = ["ffmpeg", "-i", video_file_path, "-ss", str(clip_start), "-to", str(clip_end), "-c", "copy", output_file_path]
        subprocess.run(command)
        print(f"Created segment {i+1} from {clip_start:.2f} to {clip_end:.2f} seconds at {output_file_path}")

def process_video_directory_fixed_segments(directory_path, clip_duration_in_seconds, output_directory):
    for video_file in os.listdir(directory_path):
        video_file_path = os.path.join(directory_path, video_file)
        if os.path.isfile(video_file_path) and (video_file.lower().endswith('.mov') or video_file.lower().endswith('.mp4')):
            splice_video_fixed_segments(video_file_path, clip_duration_in_seconds, output_directory)

# Parameters for easy configuration
video_directory = r"E:\Delenda Warp\prep"
clip_duration_in_seconds = 60  # Change this value to your desired clip length

# Main execution
process_video_directory_fixed_segments(video_directory, clip_duration_in_seconds, video_directory)
