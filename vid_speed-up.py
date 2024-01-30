import os
import subprocess

# Parameters for easy configuration
input_video_path = "/Users/agi/Dropbox/Delenda/Catalyst/Runway/3956478850_prob4.mp4"
output_video_path = "/Users/agi/Dropbox/Delenda/Catalyst/Runway/3956478850___x2.mp4"
speed_factor = 2  # Speed up by a factor of 2 (e.g., from 13 seconds to 6.5 seconds)

def speed_up_video(input_path, output_path, speed_factor):
    # Get the original frame rate of the input video
    frame_rate = get_frame_rate(input_path)

    # Calculate the new frame rate to maintain all frames
    new_frame_rate = frame_rate * speed_factor

    command = [
        "ffmpeg", "-i", input_path, "-vf", f"setpts={1/speed_factor}*PTS", "-r", str(new_frame_rate),
        "-c:v", "libx264", "-c:a", "aac", "-strict", "experimental", output_path
    ]

    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result.returncode != 0:
        print(f"Error occurred while speeding up the video: {result.stderr}")
    else:
        print(f"Video sped up successfully and saved to {output_path}")

def get_frame_rate(input_path):
    command = [
        "ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=r_frame_rate", "-of", "default=noprint_wrappers=1:nokey=1", input_path
    ]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    try:
        frame_rate = eval(result.stdout)
        return frame_rate
    except (ValueError, SyntaxError):
        print(f"Error getting frame rate. STDOUT: {result.stdout}, STDERR: {result.stderr}")
        return 0

# Main execution
speed_up_video(input_video_path, output_video_path, speed_factor)
