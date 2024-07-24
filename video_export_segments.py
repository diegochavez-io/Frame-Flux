import os
import subprocess

# Parameters for easy configuration
video_file_path = "/Users/agi/Dropbox/TPR_AI-ART/02. Assets/22_02055183_st__feather_images__TDMovieOut-2_tvai.mp4"
clip_duration_in_seconds = 10
num_videos_to_export = 5

# Create a new directory
output_directory = "/Users/agi/Dropbox/Runway/Int"
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Function to get the video length
def get_video_length(video_file_path):
    if not os.path.exists(video_file_path):
        print(f"The file {video_file_path} does not exist.")
        return 0

    command = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", video_file_path
    ]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    try:
        return float(result.stdout)
    except ValueError:
        print(f"Error getting video length. STDOUT: {result.stdout}, STDERR: {result.stderr}")
        return 0

# Function to trim the video
def trim_video(video_file_path, clip_length, output_dir, limit):
    video_length = get_video_length(video_file_path)
    if video_length == 0:
        print("Video length is 0, exiting.")
        return

    num_clips_to_export = min(int(video_length // clip_length), limit)
    print(f"Number of clips to export: {num_clips_to_export}")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    source_file_name = os.path.splitext(os.path.basename(video_file_path))[0]

    for i in range(num_clips_to_export):
        clip_start = i * clip_length
        clip_end = clip_start + clip_length

        output_file_name = f"{source_file_name}_clip_{i + 1}.mp4"
        output_file_path = os.path.join(output_dir, output_file_name)
        
        command = [
            "ffmpeg", "-i", video_file_path, "-ss", str(clip_start), "-to", str(clip_end),
            "-c:v", "libx264", "-crf", "18", "-c:a", "aac", "-strict", "experimental", output_file_path
        ]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if result.returncode != 0:
            print(f"Error occurred while processing clip {i + 1}. STDERR: {result.stderr.decode()}")
        else:
            print(f"Created clip {i + 1} at {output_file_name}")

# Main execution
trim_video(video_file_path, clip_duration_in_seconds, output_directory, num_videos_to_export)