import cv2
import os
import random
from tqdm import tqdm  # Install tqdm library for progress bar

# Parameters
input_folder = "/Users/agi/Dropbox/TPR_AI-ART/03. Pre-Talk/Hydra/Images_v2"
output_video_path = "/Users/agi/Dropbox/TPR_AI-ART/03. Pre-Talk/Hydra/MJ_Images_v2_output_video_12fps.mp4"
frame_rate = 12
frame_hold = 1
random_order = True

def images_to_video(input_folder, output_video_path, frame_rate, frame_hold, random_order):
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

    # Process each image and write to the video
    for image_file in tqdm(image_files, desc="Creating video", unit="frame"):
        image_path = os.path.join(input_folder, image_file)
        image = cv2.imread(image_path)

        # Repeat the image for frame_hold times
        for _ in range(frame_hold):
            out.write(image)

    out.release()
    print(f"Video saved to {output_video_path}")

if __name__ == "__main__":
    images_to_video(input_folder, output_video_path, frame_rate, frame_hold, random_order)