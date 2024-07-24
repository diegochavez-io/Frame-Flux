import cv2
import numpy as np
from moviepy.editor import VideoFileClip
from tqdm import tqdm

def dither_frame(frame, palette, dither_amount, add_noise_amount, contrast_amount, saturation_amount):
    frame = frame.astype(np.float32) / 255.0
    frame = np.clip((frame - 0.5) * contrast_amount / 100 + 0.5, 0, 1)
    frame = np.clip(frame * saturation_amount / 100, 0, 1)

    if add_noise_amount > 0:
        noise = np.random.normal(0, add_noise_amount / 255.0, frame.shape)
        frame = np.clip(frame + noise, 0, 1)

    h, w, _ = frame.shape
    palette = np.array(palette, dtype=np.float32) / 255.0
    
    for y in range(h):
        for x in range(w):
            old_pixel = frame[y, x]
            closest_color = palette[np.sum((palette - old_pixel) ** 2, axis=1).argmin()]
            quant_error = old_pixel - closest_color
            frame[y, x] = closest_color + quant_error * (1 - dither_amount / 100)
            
            if x + 1 < w:
                frame[y, x + 1] += quant_error * 7 / 16
            if y + 1 < h:
                if x > 0:
                    frame[y + 1, x - 1] += quant_error * 3 / 16
                frame[y + 1, x] += quant_error * 5 / 16
                if x + 1 < w:
                    frame[y + 1, x + 1] += quant_error * 1 / 16
    
    return (frame * 255).astype(np.uint8)

def process_video(input_path, output_path, palette1, palette2, test_duration=None, **kwargs):
    clip = VideoFileClip(input_path)
    
    if test_duration:
        clip = clip.subclip(0, test_duration)
    
    def process_frame(get_frame, t):
        frame = get_frame(t)
        frame_index = int(t * clip.fps)
        palette = palette1 if frame_index % 2 == 0 else palette2
        return dither_frame(frame, palette, **kwargs)
    
    processed_clip = clip.fl(process_frame)
    
    processed_clip.write_videofile(output_path, codec='libx264', audio=False)
    clip.close()
    processed_clip.close()

    input_file = "/Volumes/ML 5TB/Warp/Output/aaa_readme_00023_prob3_prob3.mov"
    output_file = "/Users/agi/Dropbox/Portfolio/VIdeo/aaa_readme_00023_processed_video.mp4"

palette1 = [(220, 27, 60), (4, 80, 160)]  # Red and Blue
palette2 = [(238, 106, 159), (249, 159, 33)]  # Pink and Orange

process_video(
    input_path,
    output_path,
    palette1,
    palette2,
    test_duration=1,  # Process only the first 1 second for testing
    dither_amount=75,
    add_noise_amount=5,
    contrast_amount=60,
    saturation_amount=100
)