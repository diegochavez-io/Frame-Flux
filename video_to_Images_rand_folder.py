import cv2
import os
import random
import zipfile
import time

# Parameters
source_folder = r"C:\Users\diego\Videos\Works of director Chris Cunningham"  # Folder containing all the video files
image_count = 50  # Number of images to extract per video
zip_output = False  # Set to True if you want to zip the output folder

# Create a single folder for all extracted frames
output_folder = "frames"
os.makedirs(output_folder, exist_ok=True)


# Function to extract frames from a video file and save them as images
def extract_frames(video_path, image_count):
    vidcap = cv2.VideoCapture(video_path)
    total_frames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))

    if image_count > total_frames:
        print(
            f"Number of frames to extract from {video_path} is greater than the total frames in the video. Extracting {total_frames} frames instead."
        )
        image_count = total_frames

    if image_count == 0:
        print(f"No frames to extract from {video_path}.")
        return

    # Calculate a minimum distance between the frames
    min_distance = total_frames // image_count

    # Generate a list of frame numbers ensuring the minimum distance
    frames_to_extract = sorted(
        [
            random.randint(i * min_distance, (i + 1) * min_distance - 1)
            for i in range(image_count)
        ]
    )

    success, image = vidcap.read()
    count = 0
    while success:
        if count in frames_to_extract:
            # Use the first 15 characters of the source video's name as a prefix for the frame files
            video_name_prefix = os.path.splitext(os.path.basename(video_path))[0][:15]
            timestamp = int(time.time() * 1000)  # Get current timestamp in milliseconds
            frame_filename = f"{video_name_prefix}_frame{count}_{timestamp}.jpg"
            cv2.imwrite(os.path.join(output_folder, frame_filename), image)
            frames_to_extract.remove(count)
        success, image = vidcap.read()
        count += 1


# Function to zip the output folder
def zip_folder(output_folder):
    zipf = zipfile.ZipFile(f"{output_folder}.zip", "w", zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(output_folder):
        for file in files:
            zipf.write(
                os.path.join(root, file),
                os.path.relpath(
                    os.path.join(root, file), os.path.join(output_folder, "..")
                ),
            )
    zipf.close()


# Main function to process the videos
def main():
    for video_file in os.listdir(source_folder):
        if video_file.endswith(
            (".mp4", ".mov", ".avi", ".mkv")
        ):  # Add other video formats if needed
            video_path = os.path.join(source_folder, video_file)
            print(f"Extracting frames from {video_path}...")
            extract_frames(video_path, image_count)

    # Zip the output folder if zip_output is True
    if zip_output:
        zip_folder(output_folder)


if __name__ == "__main__":
    main()
