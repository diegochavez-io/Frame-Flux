import cv2
import os
import random

# Configurations
EXTRACTION_FRAME_RATE = 25  # Desired number of frames to extract from the entire video
input_folder = r"D:\_DEL_TEMP\Touch_HAP"

random.seed(10)

def process_video(input_file):
    # Extract the base name of the video (without extension)
    video_name = os.path.splitext(os.path.basename(input_file))[0]

    # Create the output folder based on video's name + "_frames"
    output_dir = os.path.join(os.path.dirname(input_file), video_name + "_frames")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Extract frames from the video
    vidcap = cv2.VideoCapture(input_file)

    # Check if video capture initialization was successful
    if not vidcap.isOpened():
        print(f"Error: Couldn't open the video file at {input_file}")
        return

    print(f"Reading video from {input_file}")

    total_frames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    if total_frames == 0:
        print(f"Error: Couldn't retrieve total frame count for {input_file}")
        return

    # Calculate the interval to extract the desired number of frames evenly throughout the video
    interval = total_frames // EXTRACTION_FRAME_RATE if EXTRACTION_FRAME_RATE < total_frames else 1

    frames = []
    frame_count = 0

    success, image = vidcap.read()
    while success and len(frames) < EXTRACTION_FRAME_RATE:
        if frame_count % interval == 0:
            frames.append(image)
        success, image = vidcap.read()
        frame_count += 1

    print(f"Extracted {len(frames)} frames from the video")

    # Shuffle the frames
    random.shuffle(frames)

    # Save the frames as .png files in the output folder
    for i, frame in enumerate(frames):
        output_path = os.path.join(output_dir, (str(i).zfill(9) + ".png"))
        cv2.imwrite(output_path, frame)
        print(f"Saving frame {i+1} to {output_path}")

    vidcap.release()

# Main
video_files = [f for f in os.listdir(input_folder) if f.endswith('.mov')]

for video_file in video_files:
    process_video(os.path.join(input_folder, video_file))
