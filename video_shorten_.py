import cv2
import os
import math

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
    input_duration = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) / input_fps
    print(f"Input video duration: {input_duration} seconds")

    # Calculate the number of frames to extract
    num_frames = int(target_duration * fps)
    print(f"Number of frames to extract: {num_frames}")

    # Create a list to store the extracted frames
    frames = []

    # Extract frames from the input video
    for i in range(num_frames):
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(i * (input_fps * input_duration / num_frames)))
        ret, frame = cap.read()
        if ret:
            frames.append(frame)

    # Release the video capture object
    cap.release()

    # Create a video writer object for the output video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (frames[0].shape[1], frames[0].shape[0]))

    # Write the frames to the output video
    for frame in frames:
        out.write(frame)

    # Release the video writer object
    out.release()

    print(f"Video condensed and saved to {output_video_path}")

# Example usage
input_video_path = "/Users/agi/Dropbox/_AM/2023 Album Promos/Social Media Content/Production Files/AM Introduction Posts/Post #9 - Avicenna Film/Avicenna - AM Architect.mp4"
output_video_path = "/Users/agi/Dropbox/_AM/2023 Album Promos/Social Media Content/Production Files/AM Introduction Posts/Post #9 - Avicenna Film/Segments/reassembled_video_8fps.mp4"
target_duration = 5  # Target duration of the condensed video in seconds
fps = 12  # Frames per second for the output video

condense_video(input_video_path, output_video_path, target_duration, fps)
