import moviepy.editor as mp
import os
import subprocess

def convert_video_to_gifs(input_video, output_folder, clip_duration, max_size=15, max_width=800, compression_scale=100):
    os.makedirs(output_folder, exist_ok=True)
    video = mp.VideoFileClip(input_video)
    num_clips = int(video.duration // clip_duration)
    
    for i in range(num_clips):
        start_time = i * clip_duration
        end_time = (i + 1) * clip_duration
        clip = video.subclip(start_time, end_time)
        
        temp_video_path = os.path.join(output_folder, f"temp_clip_{i+1}.mp4")
        clip.write_videofile(temp_video_path, codec="libx264")
        
        gif_path = os.path.join(output_folder, f"clip_{i+1}.gif")
        
        # Resize video if necessary
        if clip.w > max_width:
            scale_filter = f"scale={max_width}:-1"
        else:
            scale_filter = "scale=iw:ih"
        
        # Generate palette for better color management
        palette_path = os.path.join(output_folder, f"palette_{i+1}.png")
        subprocess.run([
            "ffmpeg", "-y", "-i", temp_video_path,
            "-vf", f"{scale_filter},palettegen",
            palette_path
        ])
        
        # Convert to GIF using palette and compression scale
        subprocess.run([
            "ffmpeg", "-y", "-i", temp_video_path, "-i", palette_path,
            "-lavfi", f"{scale_filter},paletteuse=dither=bayer:bayer_scale={compression_scale}",
            "-fs", f"{max_size}M", gif_path
        ])
        
        os.remove(temp_video_path)
        os.remove(palette_path)
        print(f"Processed clip {i+1}/{num_clips}")
    
    video.close()

# Main execution
if __name__ == "__main__":
    input_video = "/Users/agi/Dropbox/Portfolio/DeepDreem/Gen-2 16s, 418308199, cam_R 64.mp4"  # Replace with your video path
    output_folder = "/Users/agi/Dropbox/Portfolio/DeepDreem/"  # Replace with your desired output folder
    clip_duration = 5  # Duration of each clip in seconds
    max_size = 15  # Maximum size of each GIF in MB
    max_width = 800  # Maximum width of the GIFs in pixels
    compression_scale = 100  # Compression scale (0-200)

    convert_video_to_gifs(input_video, output_folder, clip_duration, max_size, max_width, compression_scale)
    print("Conversion completed!")
