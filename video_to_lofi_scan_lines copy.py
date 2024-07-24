import os
import numpy as np
from moviepy.editor import VideoFileClip, AudioFileClip
import moviepy.video.fx.all as vfx
from PIL import Image, ImageOps, ImageEnhance, ImageDraw

def apply_dithering(image, dither_amount):
    """
    Apply dithering to the image with a specified dither amount.
    """
    dithered = image.convert('1')
    if dither_amount < 100:
        blended = Image.blend(image.convert('L'), dithered.convert('L'), dither_amount / 100.0)
        return blended.convert('RGB')
    return dithered.convert('RGB')

def add_noise(image, noise_amount=5):
    """
    Add noise to the image.
    """
    np_image = np.array(image)
    noise = np.random.randint(-noise_amount, noise_amount, np_image.shape, dtype='int16')
    noisy_image = np_image.astype('int16') + noise
    noisy_image = np.clip(noisy_image, 0, 255).astype('uint8')
    return Image.fromarray(noisy_image)

def add_scan_lines(image, line_thickness=1, line_opacity=0.3, horizontal=True, vertical=False):
    """
    Add CRT-like scan lines to the image, with options for horizontal and vertical lines.
    """
    width, height = image.size
    scan_lines = Image.new('L', (width, height), 255)
    draw = ImageDraw.Draw(scan_lines)
    
    if horizontal:
        for y in range(0, height, line_thickness * 2):
            draw.line([(0, y), (width, y)], fill=0, width=line_thickness)
    
    if vertical:
        for x in range(0, width, line_thickness * 2):
            draw.line([(x, 0), (x, height)], fill=0, width=line_thickness)
    
    scan_lines = ImageEnhance.Brightness(scan_lines).enhance(1 - line_opacity)
    return Image.composite(image, Image.new('RGB', image.size, 'black'), scan_lines)

def process_frame(frame, dither=False, dither_amount=100, add_noise_amount=0, add_scan_lines_effect=False, scan_line_thickness=1, scan_line_opacity=0.3, horizontal_lines=True, vertical_lines=False):
    """
    Process a single frame with optional dithering, noise addition, and scan lines.
    """
    pil_image = Image.fromarray(frame).convert('L')

    if dither:
        pil_image = apply_dithering(pil_image, dither_amount)

    if add_noise_amount > 0:
        pil_image = add_noise(pil_image, add_noise_amount)

    pil_image = pil_image.convert('RGB')

    if add_scan_lines_effect:
        pil_image = add_scan_lines(pil_image, scan_line_thickness, scan_line_opacity, horizontal_lines, vertical_lines)

    return np.array(pil_image)

def video_to_mp4(input_video_path, output_video_path, fps=None, resize=None, black_and_white=False, dither=False, dither_amount=100, add_noise_amount=0, add_scan_lines_effect=False, scan_line_thickness=1, scan_line_opacity=0.3, horizontal_lines=True, vertical_lines=False, full_video=True, duration=5):
    """
    Convert a video to MP4 with optional dithering, noise effects, and CRT-like scan lines, including audio.

    Parameters:
    input_video_path (str): Path to the input video file.
    output_video_path (str): Path to save the output MP4 file.
    fps (int, optional): Frames per second for the video.
    resize (tuple, optional): Resize the video (width, height).
    black_and_white (bool, optional): Convert video to black and white if True.
    dither (bool, optional): Apply dithering effect for a lo-fi look.
    dither_amount (int, optional): Percentage of dithering (0-100).
    add_noise_amount (int, optional): Amount of noise to add to each frame.
    add_scan_lines_effect (bool, optional): Add CRT-like scan lines to the video.
    scan_line_thickness (int, optional): Thickness of scan lines.
    scan_line_opacity (float, optional): Opacity of scan lines (0.0 to 1.0).
    horizontal_lines (bool, optional): Add horizontal scan lines if True.
    vertical_lines (bool, optional): Add vertical scan lines if True.
    full_video (bool, optional): Export the entire video if True, otherwise use the specified duration.
    duration (int, optional): Duration of the video to process in seconds if full_video is False.
    """
    # Ensure the output directory exists
    output_dir = os.path.dirname(output_video_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Load the video clip
    clip = VideoFileClip(input_video_path)

    # Print the duration of the video
    print(f"Video duration: {clip.duration} seconds")

    # Trim the clip if not processing the full video
    if not full_video:
        end_time = min(duration, clip.duration)
        clip = clip.subclip(0, end_time)

    # Convert to black and white if specified
    if black_and_white:
        clip = clip.fx(vfx.blackwhite)

    # Resize the clip if resize parameter is provided
    if resize is not None:
        clip = clip.resize(resize)

    # Set the fps if provided
    if fps is not None:
        clip = clip.set_fps(fps)

    # Process each frame
    processed_clip = clip.fl_image(lambda frame: process_frame(frame, dither, dither_amount, add_noise_amount, add_scan_lines_effect, scan_line_thickness, scan_line_opacity, horizontal_lines, vertical_lines))

    # Keep the audio from the original clip
    processed_clip = processed_clip.set_audio(clip.audio)

    # Write the result to an output MP4 file
    processed_clip.write_videofile(output_video_path, codec='libx264', fps=fps or clip.fps, audio_codec='aac')

# Example usage
video_to_mp4(
    input_video_path="/Users/agi/Dropbox/Runway/Gen-3/Gen-3 Alpha 1560884746, iridescent, chromati.mp4",
    output_video_path="/Users/agi/Dropbox/Portfolio/VIdeo/Gen-3 Alpha 1560884746_.mp4",
    fps=12,
    # resize=(640, 480),  # Example resize value
    black_and_white=True,
    dither=True,
    dither_amount=40,
    add_noise_amount=5,
    add_scan_lines_effect=True,
    scan_line_thickness=1,
    scan_line_opacity=0.1,
    horizontal_lines=True,
    vertical_lines=False,
    full_video=False,  # Process only a portion of the video
    # duration=5  # Duration in seconds to process
)
