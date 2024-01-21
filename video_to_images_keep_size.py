import cv2
import os
import numpy as np
import random
import zipfile

# Parameters
source_file = "/Users/agi/Dropbox/Delenda/Catalyst/Live-Action/A069_09032309_C009.mov"  # Single video file path
image_count = 35  # Number of images to extract per video
zip_output = False  # Set to True if you want to zip the output folder

# Get the folder of the source_file
source_folder = os.path.dirname(source_file)
# Use the same folder for the output_folder
output_folder = source_folder

# Function to extract frames from a video file and save them as images
def extract_frames(video_path, image_count):
    vidcap = cv2.VideoCapture(video_path)
    vidcap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('C', 'Y', 'U', 'V'))  # Set the encoding
    total_frames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))

    if image_count > total_frames:
        print(f"Number of frames to extract is greater than the total frames in the video. Extracting {total_frames} frames instead.")
        image_count = total_frames

    if image_count == 0:
        print("No frames to extract.")
        return

    # Calculate a minimum distance between the frames
    min_distance = total_frames // image_count

    # Generate a list of frame numbers ensuring the minimum distance
    frames_to_extract = sorted([random.randint(i * min_distance, (i + 1) * min_distance - 1) for i in range(image_count)])

    # Create a subfolder in the output_folder with the same name as the video file
    output_subfolder = os.path.join(output_folder, os.path.splitext(os.path.basename(video_path))[0])
    os.makedirs(output_subfolder, exist_ok=True)

    success, image = vidcap.read()
    count = 0
    while success:
        if count in frames_to_extract:
            # Save the image
            cv2.imwrite(os.path.join(output_subfolder, f"frame{count}.jpg"), image)
            frames_to_extract.remove(count)
        success, image = vidcap.read()
        count += 1

    return output_subfolder

# Function to zip the output folder
def zip_folder(output_folder):
    zipf = zipfile.ZipFile(f"{output_folder}.zip", 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(output_folder):
        for file in files:
            zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(output_folder, '..')))
    zipf.close()

# Main function to process the videos
def main():
    # Process a single video file
    video_path = source_file
    print(f"Extracting frames from {video_path}...")
    output_subfolder = extract_frames(video_path, image_count)
    
    # Zip the output folder if zip_output is True
    if zip_output:
        zip_folder(output_subfolder)

if __name__ == "__main__":
    main()
