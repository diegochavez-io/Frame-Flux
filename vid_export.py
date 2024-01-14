#pip install moviepy

from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import VideoFileClip

# Parameters
input_file = "G:/My Drive/AI/SGXL_Output/LookigGlass_JellyPix_02.mp4"  # Input file path
output_file = "G:/My Drive/AI/SGXL_Output/LookigGlass_RNML_1.mp4"  # Output file path
start_frame = 1000  # Start frame
video_length = 2400  # Video length in frames
output_format = ".mp4"  # Output format
output_resolution = (512, 512)  # Output resolution

# Get frame rate
clip = VideoFileClip(input_file)
frame_rate = clip.fps  # frames per second

# Convert frames to time (seconds)
start_time = start_frame / frame_rate
end_time = start_time + (video_length / frame_rate)

# Process video
ffmpeg_extract_subclip(input_file, start_time, end_time, targetname=output_file)
clip_sub = VideoFileClip(output_file)
clip_resized = clip_sub.resize(output_resolution)
clip_resized.write_videofile(output_file, codec='libx264')

print(f"Video has been processed and saved as {output_file}")

