import os
import random
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

    # Create slices of the video
    for i in range(num_slices):
        output_file = os.path.join(output_dir, f"slice_{i}.mp4")
        x_offset = i * slice_width

        cmd = (
            ffmpeg.input(input_file, ss=time_offset)
            .filter("crop", slice_width, height, x_offset, 0)
            .output(output_file, vcodec="libx264", crf=23, preset="medium")
            .overwrite_output()
        )
        print(f"Creating slice {i}: {cmd.get_cmd()}")

        ffmpeg.run(cmd)


def create_mosaic(input_dir, output_file, input_width, input_height, num_slices, time_offset):
    # Get the paths to the sliced videos in order
    sliced_paths = [os.path.join(input_dir, f"slice_{i}.mp4") for i in range(num_slices)]

    # Create a list of input streams with staggered time offsets
    inputs = []
    for i, path in enumerate(sliced_paths):
        input_stream = ffmpeg.input(path)
        input_stream = input_stream.filter("setpts", f"PTS-STARTPTS+{i * time_offset}/TB")
        inputs.append(input_stream)

    # Concatenate the sliced videos horizontally
    concat = ffmpeg.concat(*inputs, v=1, a=0)
    scaled = concat.filter("scale", input_width, input_height)
    output = ffmpeg.output(scaled, output_file, vcodec="libx264", crf=23, preset="medium")

    print(f"Creating mosaic: {output.get_cmd()}")
    ffmpeg.run(output)


# Set the directory and file paths
directory = r'G:\My Drive\AI\StableWarpFusion\images_out\_ffmpeg_test'
input_file = os.path.join(directory, 'GettyImages-544164044.mp4')
output_dir = os.path.join(directory, 'slices')
output_file = os.path.join(directory, 'GettyImages-544164044_mosaic.mp4')

# Specify the number of vertical slices
num_slices = 12

# Specify the time offset (in seconds)
time_offset = 1

# Create the slices of the video
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
create_mosaic(output_dir, output_file, input_width, input_height, num_slices, time)