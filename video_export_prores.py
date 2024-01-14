from moviepy.editor import VideoFileClip

# Parameters
input_file = r"C:\Users\diego\Desktop\_CAT_CONVERT\10837_B-Roll_Cat-Machines_after_Rain_15.mov"  # Input file path
output_file = r"E:\CAT_2308\1. Media\1280x720"  # Output file path (changed to .mov for ProRes)
start_frame = 1000  # Start frame
video_length = 2400  # Video length in frames
output_resolution = (720, 1280)  # Output resolution

# Load the video
clip = VideoFileClip(input_file)

# Calculate start and end time in seconds
frame_rate = clip.fps  # frames per second
start_time = start_frame / frame_rate
end_time = start_time + (video_length / frame_rate)

# Determine the aspect ratio of the input and target videos
input_aspect_ratio = clip.size[0] / clip.size[1]
target_aspect_ratio = output_resolution[0] / output_resolution[1]

# Crop to maintain aspect ratio
if input_aspect_ratio > target_aspect_ratio:
    # Input video is wider than target. Crop horizontally.
    new_width = int(clip.size[1] * target_aspect_ratio)
    offset = (clip.size[0] - new_width) / 2
    clip_cropped = clip.crop(x_center=clip.size[0]/2, width=new_width)
else:
    # Input video is taller than target. Crop vertically.
    new_height = int(clip.size[0] / target_aspect_ratio)
    offset = (clip.size[1] - new_height) / 2
    clip_cropped = clip.crop(y_center=clip.size[1]/2, height=new_height)

# Trim, resize, and write to the output file
clip_cropped.subclip(start_time, end_time).resize(output_resolution).write_videofile(output_file, codec='prores_ks')

print(f"Video has been processed and saved as {output_file}")
