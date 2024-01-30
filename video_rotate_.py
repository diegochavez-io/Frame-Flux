import os
import subprocess

# Parameters for easy configuration
input_video_path = "/Users/agi/Desktop/7946213.mp4"
output_video_path = "/Users/agi/Desktop/7946213_rotated_video.mp4"
rotation_angle = 90  # Specify the rotation angle (90, 180, or 270 degrees)

def rotate_video(input_path, output_path, angle):
    command = [
        "ffmpeg", "-i", input_path, "-vf", f"transpose={angle}", "-c:v", "libx264", "-crf", "18", "-preset", "slow", output_path
    ]

    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result.returncode != 0:
        print(f"Error occurred while rotating the video: {result.stderr}")
    else:
        print(f"Video rotated successfully and saved to {output_path}")

# Main execution
rotate_video(input_video_path, output_video_path, rotation_angle)
