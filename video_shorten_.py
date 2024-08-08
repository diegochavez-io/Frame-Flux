import cv2
import random

def condense_video(input_video_path, output_video_path, target_duration, fps=30):
    """
    Condense a video into a shorter version by extracting frames and stitching them together.

    Args:
        input_video_path (str): Path to the input video file.
        output_video_path (str): Path to the output video file.
        target_duration (int): Target duration of the condensed video in seconds.
        fps (int): Frames per second for the output video (default: 30).

    Returns:
        None
    """
    # Open the input video
    cap = cv2.VideoCapture(input_video_path)

    # Get the input video properties
    input_fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    input_duration = total_frames / input_fps
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f"Input video duration: {input_duration} seconds")
    print(f"Input video resolution: {width}x{height}")

    # Calculate the number of frames to extract
    num_frames = int(target_duration * fps)
    print(f"Number of frames to extract: {num_frames}")

    # Randomly select frame indices to extract
    frame_indices = sorted(random.sample(range(total_frames), num_frames))

    # Create a list to store the extracted frames
    frames = []

    # Extract frames from the input video
    for frame_idx in frame_indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = cap.read()
        if ret:
            frames.append(frame)

    # Release the video capture object
    cap.release()

    # Create a video writer object for the output video
    fourcc = cv2.VideoWriter_fourcc(*'X264')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    # Write the frames to the output video
    for frame in frames:
        out.write(frame)

    # Release the video writer object
    out.release()

    print(f"Video condensed and saved to {output_video_path}")

# Example usage
input_video_path = "/Users/agi/Desktop/EDIT_Hydra.mp4"
output_video_path = "/Users/agi/Desktop/EDIT_Hydra_8sec_043.mp4"
target_duration = 8  # Target duration of the condensed video in seconds
fps = 15  # Frames per second for the output video

condense_video(input_video_path, output_video_path, target_duration, fps)
