import cv2
import os
import random

random.seed(10)

input_file = r"G:\My Drive\algo-film\delenda_algo_film_shoot_0822\_original_shoot_clips\algo_film_del_0822__02034565.mov"
output_folder = r'G:\My Drive\algo-film\delenda_algo_film_shoot_0822\random-frames_01\\'

# Check if the input video file exists
if not os.path.exists(input_file):
    print(f"Error: The video file {input_file} does not exist!")
    exit()

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Extract frames from the video
vidcap = cv2.VideoCapture(input_file)

# Check if video capture initialization was successful
if not vidcap.isOpened():
    print(f"Error: Couldn't open the video file at {input_file}")
    exit()

print(f"Reading video from {input_file}")

frames = []
success, image = vidcap.read()
while success:
    frames.append(image)
    success, image = vidcap.read()

print(f"Extracted {len(frames)} frames from the video")

# Shuffle the frames
random.shuffle(frames)

# Save the frames as .png files in the output folder
for i, frame in enumerate(frames):
    output_path = os.path.join(output_folder, (str(i).zfill(9) + ".png"))
    cv2.imwrite(output_path, frame)
    print(f"Saving frame {i+1} to {output_path}")

# Create a video from the shuffled frames
width  = int(vidcap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fourcc = cv2.VideoWriter_fourcc(*'PRORES')
out = cv2.VideoWriter('output.mov', fourcc, 24.0, (width, height))

for frame in frames:
    out.write(frame)

out.release()
