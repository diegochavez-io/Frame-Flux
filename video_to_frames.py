import cv2
import os

VIDEO_SOURCE_FILE = "/Users/agi/Dropbox/_MAKE/_IG/Gen-3/_Gen-3_Alpha_H.mp4"
EXTRACTION_FRAME_RATE = 24

output_folder = "/Users/agi/Dropbox/Runway/Gen-3/_frames"
source_file_name = os.path.basename(VIDEO_SOURCE_FILE)
source_file_folder = os.path.splitext(source_file_name)[0]

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

    frame_indices = list(range(total_frames))

    for idx, frame_index in enumerate(frame_indices):
        vidcap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
        success, image = vidcap.read()
        if not success:
            print(f"Error: Couldn't read frame at index {frame_index} from {input_file}")
            continue

        frame_filename = f"{video_name}_frame_{str(idx).zfill(9)}.png"
        output_path = os.path.join(output_folder, f"{source_file_folder}", frame_filename)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        cv2.imwrite(output_path, image)
        print(f"Saved frame {idx+1} to {output_path}")

    vidcap.release()

process_video(VIDEO_SOURCE_FILE)
