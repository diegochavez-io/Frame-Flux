
import os
import glob
import random
from moviepy.editor import *

# Video file
input_file = r"E:\Delenda Warp\prep\02065280_runpod_2_pixel_sort.mov"

# Extracted frames and output paths based on the video file's directory
input_directory = os.path.dirname(input_file)
filename_base = os.path.splitext(os.path.basename(input_file))[0]
temp_frames_folder = os.path.join(input_directory, filename_base + "_temp_frames")
output_folder = os.path.join(input_directory, filename_base + "_output")

# Ensure directories exist
if not os.path.exists(temp_frames_folder):
    os.makedirs(temp_frames_folder)
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Codec option
codec = 'prores'
file_extension = '.mov'

# Check if frames have been extracted
frames_count = len(glob.glob(os.path.join(temp_frames_folder, "*.png")))
video_duration = VideoFileClip(input_file).duration
fps = 24

# If the number of extracted frames doesn't match the expected number, extract frames
if frames_count != int(video_duration * fps):
    print("Extracting frames...")
    clip = VideoFileClip(input_file)
    clip.write_images_sequence(os.path.join(temp_frames_folder, "frame%04d.png"))
else:
    print("Frames already extracted. Skipping extraction process.")

def create_glitched_video(seed, version):
    random.seed(seed)
    frames = sorted(glob.glob(os.path.join(temp_frames_folder, "*.png")))
    glitched_frames = []

    while frames:
        chunk_length = random.randint(5, 30)
        current_chunk = frames[:chunk_length]
        frames = frames[chunk_length:]

        playback_mode = random.randint(0, 2)

        if playback_mode == 0:
            glitched_frames.extend(current_chunk)
        elif playback_mode == 1:
            glitched_frames.extend(current_chunk[::-1])
        else:
            random.shuffle(current_chunk)
            glitched_frames.extend(current_chunk)

        for idx, frame in enumerate(current_chunk):
            if random.random() < 0.3:
                hold_frames = random.randint(1, 4)
                glitched_frames.extend([frame] * hold_frames)

            if random.random() < 0.3:
                repeat_frames = random.randint(1, 3)
                glitched_frames.extend([frame] * repeat_frames)

    all_frames = sorted(glob.glob(os.path.join(temp_frames_folder, "*.png")))
    for idx in range(0, len(glitched_frames), 50):
        if random.random() < 0.3:
            random_frame = random.choice(all_frames)
            glitched_frames.insert(idx, random_frame)
            glitched_frames.insert(idx + 1, random_frame)
            glitched_frames.insert(idx + 2, random_frame)

    output_prefix = os.path.basename(temp_frames_folder)
    output_video = os.path.join(output_folder, f"{output_prefix}_glitched_v{version}{file_extension}")

    glitched_clip = ImageSequenceClip(glitched_frames, fps=24)
    glitched_clip.write_videofile(output_video, codec=codec, fps=24)

    print(f"Video art version {version} creation completed.")

# Create Three Versions of Glitched Videos
seeds = [42, 123, 789]
for i, seed in enumerate(seeds, 1):
    create_glitched_video(seed, version=i)
