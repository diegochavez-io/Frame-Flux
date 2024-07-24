import os
import numpy as np
import cv2
from moviepy.editor import VideoFileClip
import moviepy.video.fx.all as vfx
import pixelsort

def apply_pixelsort(frame, randomness, lower_threshold, upper_threshold, angle=0):
    # Ensure the frame is in the correct format (uint8)
    frame = frame.astype(np.uint8)
    
    # Apply pixelsort directly to the numpy array
    sorted_frame = pixelsort.pixelsort(
        frame,
        randomness=randomness,
        lower_threshold=lower_threshold,
        upper_threshold=upper_threshold,
        angle=angle
    )
    
    return sorted_frame.astype(np.uint8)

def video_to_lossy_mp4(input_video_path, output_video_path, start_time=None, end_time=None, resize=None, fps=None, quality=10, black_and_white=False, pixel_sort=False, randomness=0, lower_threshold=0, upper_threshold=255, angle=0):
    if not os.path.exists(input_video_path):
        raise FileNotFoundError(f"Input video file not found: {input_video_path}")

    clip = VideoFileClip(input_video_path)

    if start_time is not None and end_time is not None:
        clip = clip.subclip(start_time, end_time)

    if resize is not None:
        clip = clip.resize(resize)

    if fps is not None:
        clip = clip.set_fps(fps)
    else:
        fps = clip.fps

    if black_and_white:
        clip = clip.fx(vfx.blackwhite)

    width, height = clip.size

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    try:
        for frame in clip.iter_frames(dtype="uint8"):
            if pixel_sort:
                frame = apply_pixelsort(frame, randomness, lower_threshold, upper_threshold, angle)
            
            # Ensure frame is in BGR color space for OpenCV
            if frame.shape[2] == 4:  # If RGBA
                frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)
            elif frame.shape[2] == 3:  # If RGB
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            
            out.write(frame)

    except Exception as e:
        print(f"An error occurred during video processing: {str(e)}")
    finally:
        out.release()
        clip.close()
        cv2.destroyAllWindows()

    print(f"Video processing complete. Output saved to: {output_video_path}")

# Example usage
if __name__ == "__main__":
    try:
        video_to_lossy_mp4(
            input_video_path="/Users/agi/Dropbox/Runway/Int/snake styleganxl cc_scale__clip_4.mp4",
            output_video_path="/Users/agi/Dropbox/Portfolio/Video/output_sorted.mp4",
            start_time=0,
            end_time=1,
            fps=8,
            quality=15,
            black_and_white=True,
            pixel_sort=True,
            randomness=5,
            lower_threshold=10,
            upper_threshold=245,
            angle=0
        )
    except Exception as e:
        print(f"An error occurred: {str(e)}")