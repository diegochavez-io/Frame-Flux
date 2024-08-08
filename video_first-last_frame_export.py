import cv2
import os
import glob

# User inputs
# Uncomment the following line and comment out the 'video_path' line to process a folder of videos
folder_path = "path/to/folder"  # Path to the folder containing video files
# video_path = "path/to/video.mp4"  # Path to the single video file

extract_first = True  # Set to True to extract the first frame
extract_last = True   # Set to True to extract the last frame

def extract_frame(video_path, extract_first=True, extract_last=False):
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"Error: Could not open video {video_path}.")
        return

    # Prepare the base filename for output
    base_filename = os.path.splitext(os.path.basename(video_path))[0]
    output_dir = os.path.dirname(video_path)
    
    # Extract the first frame
    if extract_first:
        ret, frame = cap.read()
        if ret:
            first_frame_path = os.path.join(output_dir, f"{base_filename}_first-frame.png")
            cv2.imwrite(first_frame_path, frame)
            print(f"First frame saved to {first_frame_path}")
        else:
            print(f"Error: Could not read the first frame from {video_path}.")
    
    # Extract the last frame
    if extract_last:
        cap.set(cv2.CAP_PROP_POS_FRAMES, cap.get(cv2.CAP_PROP_FRAME_COUNT) - 1)
        ret, frame = cap.read()
        if ret:
            last_frame_path = os.path.join(output_dir, f"{base_filename}_last-frame.png")
            cv2.imwrite(last_frame_path, frame)
            print(f"Last frame saved to {last_frame_path}")
        else:
            print(f"Error: Could not read the last frame from {video_path}.")

    cap.release()

# Process a single video or a folder of videos
if 'video_path' in globals():
    extract_frame(video_path, extract_first, extract_last)
elif 'folder_path' in globals():
    video_files = glob.glob(os.path.join(folder_path, "*.mp4"))  # Adjust the file extension if necessary
    for video_file in video_files:
        extract_frame(video_file, extract_first, extract_last)
else:
    print("Error: Please specify either a video_path or a folder_path.")
