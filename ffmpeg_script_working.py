import os
import ffmpeg

def create_slices(input_file, output_dir, num_slices, time_offset):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Get the dimensions of the input video
    probe = ffmpeg.probe(input_file)
    video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
    if not video_stream:
        raise ValueError("No video stream found in input file.")
    
    width = int(video_stream['width'])
    height = int(video_stream['height'])
    
    # Calculate the width of each slice
    slice_width = width // num_slices
    
    # Create slices of the video with offset
    for i in range(num_slices):
        output_file = os.path.join(output_dir, f"slice_{i}.mp4")
        x_offset = i * slice_width + i * time_offset
        
        ffmpeg.input(input_file, ss=time_offset, y='-y').filter('crop', slice_width, height, x_offset, 0).output(output_file).run()

def create_mosaic(input_dir, output_file, input_width, input_height):
    # Get the paths to the sliced videos
    sliced_paths = sorted([os.path.join(input_dir, f"slice_{i}.mp4") for i in range(num_slices)])
    
    # Create a list of input streams for stacking
    inputs = [ffmpeg.input(path) for path in sliced_paths]
    
    # Stack the sliced videos horizontally
    stacked = ffmpeg.filter(inputs, 'hstack', inputs=num_slices)
    
    # Apply scaling to maintain the input dimensions
    stacked = stacked.filter('scale', input_width, input_height)
    
    # Output the final mosaic video
    stacked.output(output_file).run()

# Set the directory and file paths
directory = r'G:\My Drive\AI\StableWarpFusion\images_out\_ffmpeg_test'
input_file = os.path.join(directory, 'GettyImages-544164044.mp4')
output_dir = os.path.join(directory, 'slices')
output_file = os.path.join(directory, 'GettyImages-544164044_mosaic.mp4')

# Specify the number of vertical slices
num_slices = 12

# Specify the time offset (in seconds)
time_offset = 1

# Create the slices of the video with offset
create_slices(input_file, output_dir, num_slices, time_offset)
print("Video slices created successfully!")

# Get the dimensions of the input video
probe = ffmpeg.probe(input_file)
video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
if not video_stream:
    raise ValueError("No video stream found in input file.")

input_width = int(video_stream['width'])
input_height = int(video_stream['height'])

# Create the mosaic by stacking the sliced videos horizontally
create_mosaic(output_dir, output_file, input_width, input_height)
print("Mosaic video created successfully!")
