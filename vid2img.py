import os
import cv2
import random

# Parameters
source_file = "D:\_HAP\jellyfish_11min.mov"  # Single video file path
# source_folder = "folder_path"  # Folder containing video files
image_count = 500  # Number of images to extract per video
output_size = 512  # Desired output size of images

def extract_frames(video_path, image_count, output_size):
    vidcap = cv2.VideoCapture(video_path)
    total_frames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    min_distance = max(1, total_frames // image_count)  # Ensure min_distance is at least 1
    frames_to_extract = sorted([random.randint(i * min_distance, (i + 1) * min_distance - 1) for i in range(image_count)])

    # Check if target folder exists, if not, create it
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    
    # Open the video file
    video = cv2.VideoCapture(video_path)
    
    # Find the total number of frames
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Create a list of all possible frame numbers
    frame_numbers = list(range(total_frames))

    # Randomly shuffle the list
    random.shuffle(frame_numbers)

    # Select the first 'count' numbers from the shuffled list
    selected_frames = frame_numbers[:count]

    # Keep track of the frames saved
    frames_saved = 0
    
    for frame_number in selected_frames:
        # Set the current frame position
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        
        # Read the current frame
        ret, frame = video.read()
        
        # If the frame was successfully read
        if ret:
            # Crop the frame to a square
            height, width = frame.shape[:2]
            new_dim = min(height, width)
            start_x = (width - new_dim) // 2
            start_y = (height - new_dim) // 2
            frame = frame[start_y:start_y+new_dim, start_x:start_x+new_dim]

            # Resize the frame to the desired output size
            frame = cv2.resize(frame, (output_size, output_size))

            # Save the frame as an image
            cv2.imwrite(f"{target_folder}/{frames_saved}.jpg", frame)
            frames_saved += 1
            # Print the number of frames saved
            print(f"Frames saved: {frames_saved}")

    video.release()

    print(f"Extracted frames saved in {target_folder}.")

def main():
    # Iterate over all files in the source folder
    for filename in os.listdir(source_folder):
        # If the file is a video file
        if filename.endswith(".mp4") or filename.endswith(".mov"):
            # Define the target folder
            target_folder = f"{source_folder}/{filename}_frames"
            # Extract the frames
            extract_frames(f"{source_folder}/{filename}", target_folder, image_count, output_size)

if __name__ == "__main__":
    main()
