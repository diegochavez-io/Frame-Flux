import cv2
import os
import random

# Configurations
EXTRACTION_FRAME_RATE = 1
input_folder = "/Users/agi/Dropbox/Runway/BW_Cell"
output_folder = "/Users/agi/Dropbox/Runway/BW_Cell/BW_Cell_extracted_frames"

random.seed(10)

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

def process_video(input_file):
    video_name = os.path.splitext(os.path.basename(input_file))[0]
    vidcap = cv2.VideoCapture(input_file)

    if not vidcap.isOpened():
        print(f"Error: Couldn't open the video file at {input_file}")
        return

    total_frames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    if total_frames == 0:
        print(f"Error: Couldn't retrieve total frame count for {input_file}")
        return

    frame_indices = sorted(random.sample(range(total_frames), EXTRACTION_FRAME_RATE))
    
    for idx, frame_index in enumerate(frame_indices):
        vidcap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
        success, image = vidcap.read()
        if not success:
            print(f"Error: Couldn't read frame at index {frame_index} from {input_file}")
            continue

        frame_filename = f"{video_name}_frame_{str(idx).zfill(9)}.png"
        output_path = os.path.join(output_folder, frame_filename)
        cv2.imwrite(output_path, image)
        print(f"Saved frame {idx+1} to {output_path}")

    vidcap.release()

video_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.mov')]

for video_file in video_files:
    process_video(os.path.join(input_folder, video_file))
