import cv2
import os
import random
import math
from tqdm import tqdm

# Parameters
input_folder = "/Users/agi/Dropbox/Midjourney/micro_b&w"
output_video_path = "/Users/agi/Dropbox/Midjourney/videos/micro_bw_12_1_3.mp4"
frame_rate = 12
bpm = 96.50  # Beats per minute
frame_hold = 1  # Number of times each frame should be repeated
accent_frame_hold = 3  # Number of times each frame should be repeated on the beat
random_order = True

def images_to_video(input_folder, output_video_path, frame_rate, bpm, frame_hold, accent_frame_hold, random_order):
    # Get all image files from the input directory
    image_files = [f for f in os.listdir(input_folder) if f.endswith(('.jpg', '.jpeg', '.png'))]

    # Shuffle the order if random_order is True
    if random_order:
        random.shuffle(image_files)
    else:
        image_files.sort()  # Sorting ensures frames are in order

    # Check if there are any images to process
    if not image_files:
        print(f"No images found in the specified directory: {input_folder}")
        return

    # Read the first image to get the dimensions
    frame = cv2.imread(os.path.join(input_folder, image_files[0]))
    height, width, layers = frame.shape

    # Create a video writer object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, frame_rate, (width, height))

    # Calculate the number of frames per beat
    frames_per_beat = frame_rate * 60 / bpm

    # Process each image and write to the video
    for i, image_file in enumerate(tqdm(image_files, desc="Creating video", unit="frame")):
        image_path = os.path.join(input_folder, image_file)
        image = cv2.imread(image_path)

        # Determine if the current frame is on the beat
        is_on_beat = math.floor(i / frames_per_beat) == i / frames_per_beat

        # Repeat the image for frame_hold times, with accent on the beat
        for _ in range(accent_frame_hold if is_on_beat else frame_hold):
            out.write(image)

    out.release()
    print(f"Video saved to {output_video_path}")

if __name__ == "__main__":
    images_to_video(input_folder, output_video_path, frame_rate, bpm, frame_hold, accent_frame_hold, random_order)