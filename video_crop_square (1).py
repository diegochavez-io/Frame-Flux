
import subprocess

def crop_video(input_video, output_video, crop_width=512, crop_height=512):
    """
    Crops the input video to the specified dimensions and saves the output video.
    Requires FFmpeg.

    :param input_video: Path to the input video file.
    :param output_video: Path to the output video file.
    :param crop_width: Width of the crop area, default is 512.
    :param crop_height: Height of the crop area, default is 512.
    """

    # Construct the FFmpeg command to crop the video
    command = (
        f'ffmpeg -i "{input_video}" -vf '
        f'"crop={crop_width}:{crop_height}:(in_w/2-{crop_width/2}):(in_h/2-{crop_height/2})" '
        f'-c:a copy "{output_video}"'
    )

    # Print the command for verification
    print("Executing command:", command)

    # Run the command and capture output and errors
    process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print(process.stdout)
    print(process.stderr)

    # Confirmation message
    if process.returncode == 0:
        print(f"Video successfully cropped and saved to: {output_video}")
    else:
        print(f"Error occurred while cropping the video. Return code: {process.returncode}")

# Example usage
input_video = r"C:\Users\diego\Desktop\Gen-2_1262907519.mov"
output_video = r"C:\Users\diego\repos\warpFusion\v23\int\Gen-2_1262907519_512.mp4"


crop_video(input_video, output_video)





