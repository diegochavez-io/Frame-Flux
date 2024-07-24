from moviepy.editor import VideoFileClip, concatenate_videoclips, vfx
import math
import os
import random

def condense_video(input_video_path, output_dir, target_duration, fps=30, sequence_length=5, random_factor=0, speed_factor=1):
    """
    Condense a video into a shorter version by extracting frames and stitching them together.

    Args:
        input_video_path (str): Path to the input video file.
        output_dir (str): Directory where the output video file will be saved.
        target_duration (int): Target duration of the condensed video in seconds.
        fps (int): Frames per second for the output video (default: 30).
        sequence_length (int): Number of consecutive frames to include per sequence (default: 5).
        random_factor (int): Percentage of randomness to apply to frame selection (0-100).
        speed_factor (int): Speed factor to apply to the final video (e.g., 2 for 2x speed).

    Returns:
        None
    """
    # Load the input video
    video = VideoFileClip(input_video_path)

    # Get the input video duration
    input_duration = video.duration
    print(f"Input video duration: {input_duration} seconds")

    # Calculate the number of segments
    num_segments = target_duration * fps // sequence_length
    segment_interval = input_duration / num_segments
    print(f"Number of segments: {num_segments}, Interval between segments: {segment_interval} seconds")

    # Create a list to store the segments
    segments = []

    # Extract segments from the input video
    for i in range(num_segments):
        start_time = i * segment_interval
        if random_factor > 0:
            # Apply randomness to start time
            random_adjustment = random.uniform(-random_factor/100 * segment_interval, random_factor/100 * segment_interval)
            start_time = max(0, min(input_duration - (sequence_length / fps), start_time + random_adjustment))
        segment = video.subclip(start_time, start_time + (sequence_length / fps))
        segments.append(segment)

    # Concatenate the segments
    condensed_video = concatenate_videoclips(segments)

    # Apply speed factor
    if speed_factor != 1:
        condensed_video = condensed_video.fx(vfx.speedx, speed_factor)

    # Extract the base name of the input video file without extension
    input_video_name = os.path.splitext(os.path.basename(input_video_path))[0]

    # Create the output file name including the input video name and parameters
    output_video_filename = f"{input_video_name}_condensed"
    if speed_factor != 1:
        output_video_filename += f"_{speed_factor}x"
    if random_factor > 0:
        output_video_filename += f"_random_{random_factor}"
    output_video_filename += ".mp4"

    # Create the output file path
    output_video_file_path = os.path.join(output_dir, output_video_filename)

    # Write the condensed video to the output file
    condensed_video.write_videofile(output_video_file_path, codec='libx264', fps=fps)

    print(f"Video condensed and saved to {output_video_file_path}")

# User inputs
input_video_path = "/Volumes/ML 5TB/Delenda_Live_Visuals/random_clip_2_198ca0_warp_runpod_8_resolve00087779 copy.mp4"
output_dir = "/Users/agi/Dropbox/Portfolio/Delenda_Concert_Visuals "
target_duration = 180  # Target duration of the condensed video in seconds
fps = 12  # Frames per second for the output video
sequence_length = 4  # Number of consecutive frames to include per sequence
random_factor = 2  # Percentage of randomness to apply to frame selection (0-100), 0 for no randomness
speed_factor = 1  # Speed factor to apply to the final video (e.g., 2 for 2x speed), 1 for normal speed

condense_video(input_video_path, output_dir, target_duration, fps, sequence_length, random_factor, speed_factor)
