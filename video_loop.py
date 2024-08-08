import cv2
import numpy as np
from moviepy.editor import VideoFileClip, concatenate_videoclips

def process_video(input_path, output_path, loops, rotate=False, codec='h264'):
    """
    Process and loop a video file with options to rotate and choose codec.

    Parameters:
    - input_path (str): Path to the input video file.
    - output_path (str): Path to save the processed video file.
    - loops (int): Number of times to loop the video.
    - rotate (bool): Option to rotate the video 90 degrees clockwise. Default is False.
    - codec (str): Codec to use for the output video ('prores' or 'h264'). Default is 'h264'.
    """
    # Load video with OpenCV
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        raise ValueError("Error opening video file")

    # Get video properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Read frames from the video
    frames = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if rotate:
            frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        frames.append(frame)
    
    cap.release()
    
    # Create a list of repeated frames
    looped_frames = frames * loops
    
    # Create a temporary file for the concatenated video
    temp_output_path = output_path.replace(".mp4", "_temp.mp4")
    
    # Write the looped video to a temporary file using OpenCV
    out = cv2.VideoWriter(temp_output_path, fourcc, fps, (width if not rotate else height, height if not rotate else width))
    for frame in looped_frames:
        out.write(frame)
    out.release()
    
    # Load the temporary video with MoviePy
    clip = VideoFileClip(temp_output_path)
    
    # Set codec and quality options
    if codec == 'prores':
        codec_options = {'codec': 'prores_ks', 'bitrate': '200M'}
    elif codec == 'h264':
        codec_options = {'codec': 'libx264', 'bitrate': '18M'}
    else:
        raise ValueError("Unsupported codec. Choose 'prores' or 'h264'.")
    
    # Write the final output with MoviePy
    clip.write_videofile(output_path, **codec_options)
    
if __name__ == "__main__":
    # Example usage
    input_path = "/Users/agi/Dropbox/_AM/10. Touch Docs/Stable_Hall_24_08/Video Clips/Texture_rotated_90_resized_1_codec_libx264/PYC_00002_7-10_90_resized_1_codec_prores_ks_90_resized_1_codec_libx264.mp4"
    output_path = "/Users/agi/Desktop/_LOOPS/PYC_00002_7-10_loop_4.mp4"
    loops = 4
    rotate = False
    codec = 'h264'

    process_video(input_path, output_path, loops, rotate, codec)
