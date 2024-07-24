import moviepy.editor as mp
import os
import math
import subprocess

def run_ffmpeg_command(command):
    result = subprocess.run(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    if result.returncode != 0:
        print(f"Error running command: {' '.join(command)}")
        print(result.stderr.decode())
        raise RuntimeError(f"ffmpeg command failed with error code {result.returncode}")

def convert_video_to_gifs(input_video, output_folder, clip_duration, max_size=15, max_width=800, num_colors=12):
    os.makedirs(output_folder, exist_ok=True)
    video = mp.VideoFileClip(input_video)
    num_clips = math.ceil(video.duration / clip_duration)
    
    for i in range(num_clips):
        start_time = i * clip_duration
        end_time = min((i + 1) * clip_duration, video.duration)
        clip = video.subclip(start_time, end_time)
        
        temp_video_path = os.path.join(output_folder, f"temp_clip_{i+1}.mp4")
        
        if clip.w > max_width:
            clip = clip.resize(width=max_width)
        
        clip.write_videofile(temp_video_path, codec="libx264")

        gif_path = os.path.join(output_folder, f"clip_{i+1}.gif")
        
        # Resize video if necessary
        if clip.w > max_width:
            scale_filter = f"scale={max_width}:-1"
        else:
            scale_filter = "scale=iw:ih"
        
        # Generate palette for better color management
        palette_path = os.path.join(output_folder, f"palette_{i+1}.png")
        run_ffmpeg_command([
            "ffmpeg", "-y", "-i", temp_video_path,
            "-vf", f"{scale_filter},palettegen=max_colors={num_colors}",
            palette_path
        ])
        
        # Convert to GIF using palette and dithering
        run_ffmpeg_command([
            "ffmpeg", "-y", "-i", temp_video_path, "-i", palette_path,
            "-lavfi", f"{scale_filter},paletteuse=dither=floyd_steinberg",
            "-fs", f"{max_size}M", gif_path
        ])
        
        os.remove(temp_video_path)
        os.remove(palette_path)
        print(f"Processed clip {i+1}/{num_clips}")
    
    video.close()

# Main execution
if __name__ == "__main__":
    input_video = "/Users/agi/Dropbox/Portfolio/DeepDreem/Gen-2 16s, 418308199, cam_R 64.mp4"
    output_folder = "/Users/agi/Dropbox/Portfolio/DeepDreem/"
    clip_duration = 5  # Duration of each clip in seconds
    max_size = 14  # Maximum size of each GIF in MB
    max_width = 800  # Maximum width of the GIFs in pixels
    num_colors = 48  # Number of colors for the GIF (2-256)

    convert_video_to_gifs(input_video, output_folder, clip_duration, max_size, max_width, num_colors)
    print("Conversion completed!")
