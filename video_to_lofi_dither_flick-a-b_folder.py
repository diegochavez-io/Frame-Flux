import os
import numpy as np
import cv2
from moviepy.editor import VideoFileClip
from tqdm import tqdm
import time
from multiprocessing import Pool, cpu_count

def optimized_dither(frame, palette):
    h, w, _ = frame.shape
    frame_flat = frame.reshape((-1, 3))
    palette = palette.reshape((-1, 3))
    distances = np.sum((frame_flat[:, np.newaxis, :] - palette[np.newaxis, :, :]) ** 2, axis=2)
    closest_color_indices = np.argmin(distances, axis=1)
    dithered = palette[closest_color_indices].reshape((h, w, 3))
    error = frame - dithered
    
    # Apply error diffusion
    for y in range(h-1):
        for x in range(w-1):
            err = error[y, x] * 0.4375
            frame[y, x+1] += err * 7/16
            frame[y+1, x-1] += err * 3/16
            frame[y+1, x] += err * 5/16
            frame[y+1, x+1] += err * 1/16
    
    return dithered

def process_frame(args):
    frame, frame_index, dither_amount, add_noise_amount, contrast_amount, saturation_amount, color1, color2, color3, color4 = args
    
    frame = frame.astype(float) / 255.0
    frame = np.clip((frame - 0.5) * contrast_amount / 100 + 0.5, 0, 1)
    frame = np.clip(frame * saturation_amount / 100, 0, 1)

    if add_noise_amount > 0:
        noise = np.random.normal(0, add_noise_amount / 255.0, frame.shape)
        frame = np.clip(frame + noise, 0, 1)

    if frame_index % 2 == 0:
        palette = np.array([color1, color2]) / 255.0
    else:
        palette = np.array([color3, color4]) / 255.0
    
    dithered = optimized_dither(frame, palette)

    blended = cv2.addWeighted(frame, 1 - dither_amount/100, dithered, dither_amount/100, 0)

    return (blended * 255).astype(np.uint8)

def process_video_chunk(chunk_data):
    chunk, start_frame, params = chunk_data
    processed_frames = []
    for i, frame in enumerate(chunk):
        frame_index = start_frame + i
        processed_frame = process_frame((frame, frame_index, *params))
        processed_frames.append(processed_frame)
    return processed_frames

def process_video(input_path, output_path, chunk_size=100, test_duration=None, **kwargs):
    clip = VideoFileClip(input_path)
    
    if test_duration:
        clip = clip.subclip(0, min(test_duration, clip.duration))
    
    total_frames = int(clip.fps * clip.duration)
    
    writer = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), clip.fps, 
                             (int(clip.w), int(clip.h)))

    start_time = time.time()
    
    params = (kwargs['dither_amount'], kwargs['add_noise_amount'], 
              kwargs['contrast_amount'], kwargs['saturation_amount'],
              kwargs['color1'], kwargs['color2'], kwargs['color3'], kwargs['color4'])

    with Pool(processes=cpu_count()) as pool:
        chunks = []
        for t in np.arange(0, clip.duration, chunk_size/clip.fps):
            chunk_frames = list(clip.subclip(t, min(t + chunk_size/clip.fps, clip.duration)).iter_frames())
            chunks.append((chunk_frames, int(t * clip.fps), params))
        
        for processed_chunk in tqdm(pool.imap(process_video_chunk, chunks), 
                                    total=len(chunks), desc="Processing video"):
            for frame in processed_chunk:
                writer.write(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    writer.release()
    clip.close()

    # Add audio back to the video
    final_clip = VideoFileClip(output_path)
    final_clip = final_clip.set_audio(clip.audio)
    final_clip.write_videofile(output_path.replace('.mp4', '_audio.mp4'), codec='libx264', audio_codec='aac')
    final_clip.close()

    end_time = time.time()
    print(f"Total processing time: {end_time - start_time:.2f} seconds")

def process_folder(input_folder, output_folder, test_duration=None, **kwargs):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    video_extensions = ['.mp4', '.avi', '.mov', '.mkv']
    
    videos = [f for f in os.listdir(input_folder) if any(f.lower().endswith(ext) for ext in video_extensions)]
    
    for i, filename in enumerate(videos, 1):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, f"processed_{filename}")
        
        print(f"Processing video {i} of {len(videos)}: {filename}")
        process_video(input_path, output_path, test_duration=test_duration, **kwargs)
        print(f"Completed video {i} of {len(videos)}: {filename}")
        print("------------------------")

if __name__ == "__main__":
    input_folder = "/Users/agi/Dropbox/ComfyUI_Output/2024-07-21/scale/"
    output_folder = "/Users/agi/Dropbox/ComfyUI_Output/2024-07-21/flick_4-tone"
    
    process_folder(
        input_folder,
        output_folder,
        chunk_size=100,
        # test_duration=1,  # Process only the first 2 seconds for testing, comment out for full video
        dither_amount=75,
        add_noise_amount=5,
        contrast_amount=60,
        saturation_amount=100,
        color1=(35, 171, 226),   # Light Blue
        color2=(42, 179, 91),    # Green
        color3=(233, 8, 138),    # Pink
        color4=(251, 180, 31)    # Orange
    )