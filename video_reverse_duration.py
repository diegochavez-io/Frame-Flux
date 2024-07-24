import cv2
import os

def process_video(input_path, output_path, reverse=False, new_duration=None):
    # Check if the input video file exists
    if not os.path.isfile(input_path):
        print(f"Error: Input video file '{input_path}' does not exist.")
        return

    # Open the input video
    cap = cv2.VideoCapture(input_path)

    # Get video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    print(f"Original FPS: {fps}, Frame count: {frame_count}, Width: {width}, Height: {height}")

    # Read all frames
    frames = []
    for i in range(frame_count):
        ret, frame = cap.read()
        if not ret:
            print(f"Failed to read frame {i}")
            break
        frames.append(frame)

    cap.release()
    print(f"Total frames read: {len(frames)}")

    # Reverse frames if requested
    if reverse:
        frames = frames[::-1]

    # Calculate new FPS to adjust duration
    if new_duration is not None:
        new_fps = len(frames) / new_duration
    else:
        new_fps = fps

    print(f"New FPS: {new_fps}")

    # Write output video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, new_fps, (width, height))

    for frame in frames:
        out.write(frame)

    out.release()
    print(f"Processed video saved to {output_path}")

if __name__ == "__main__":
    input_path = "/Users/agi/Dropbox/Organic/_comfyUI/AD_00020_prob4_thf4_prob4_thf4.mp4"  # Replace with your input video path
    output_path = "/Users/agi/Dropbox/Organic/_comfyUI/AD_00020_prob4_thf4_prob4_thf4_7.mp4"  # Replace with your output video path

    # Set options
    reverse_video = False  # Set to False if you don't want to reverse the video
    new_video_duration = 7  # New duration in seconds (set to None to keep original duration)

    # Process the video
    process_video(input_path, output_path, reverse=reverse_video, new_duration=new_video_duration)
