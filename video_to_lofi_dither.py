import os
import numpy as np
from moviepy.editor import VideoFileClip, AudioFileClip
import moviepy.video.fx.all as vfx
from PIL import Image, ImageEnhance, ImageOps

def apply_contrast(image, contrast_amount):
    """
    Apply contrast enhancement to the image.
    """
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(contrast_amount)

def apply_dithering(image, dither_amount):
    """
    Apply dithering to the image with a specified dither amount.
    """
    dithered = image.convert('1')
    if dither_amount < 100:
        blended = Image.blend(image.convert('L'), dithered.convert('L'), dither_amount / 100)
        return blended
    return dithered

def add_noise(image, noise_amount=5):
    """
    Add noise to the image.
    """
    np_image = np.array(image)
    noise = np.random.randint(-noise_amount, noise_amount, np_image.shape, dtype='int16')
    noisy_image = np_image.astype('int16') + noise
    noisy_image = np.clip(noisy_image, 0, 255).astype('uint8')
    return Image.fromarray(noisy_image)

def process_frame(frame, contrast=False, contrast_amount=1.0, dither=False, dither_amount=100, add_noise_amount=0):
    """
    Process a single frame with optional contrast enhancement, dithering, and noise addition.
    """
    pil_image = Image.fromarray(frame).convert('L')

    if contrast:
        pil_image = apply_contrast(pil_image, contrast_amount)

    if dither:
        pil_image = apply_dithering(pil_image, dither_amount)

    if add_noise_amount > 0:
        pil_image = add_noise(pil_image, add_noise_amount)

    return np.array(pil_image.convert('RGB'))

def video_to_mp4(input_video_path, output_video_path, start_time=None, end_time=None, resize=None, fps=None, black_and_white=False, contrast=False, contrast_amount=1.0, dither=False, dither_amount=100, add_noise_amount=0):
    """
    Convert a video to MP4 with optional contrast enhancement, dithering, and noise effects, including audio.

    Parameters:
    input_video_path (str): Path to the input video file.
    output_video_path (str): Path to save the output MP4 file.
    start_time (float, optional): Start time in seconds to begin the video.
    end_time (float, optional): End time in seconds to end the video.
    resize (tuple, optional): Resize the video (width, height).
    fps (int, optional): Frames per second for the video.
    black_and_white (bool, optional): Convert video to black and white if True.
    contrast (bool, optional): Apply contrast enhancement if True.
    contrast_amount (float, optional): Contrast level (0.0-2.0).
    dither (bool, optional): Apply dithering effect for a lo-fi look.
    dither_amount (int, optional): Percentage of dithering (0-100).
    add_noise_amount (int, optional): Amount of noise to add to each frame.
    """
    # Ensure the output directory exists
    output_dir = os.path.dirname(output_video_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Load the video clip
    clip = VideoFileClip(input_video_path)

    # Trim the clip if start_time and end_time are provided
    if start_time is not None and end_time is not None:
        clip = clip.subclip(start_time, end_time)

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
    processed_clip = clip.fl_image(lambda frame: process_frame(frame, contrast, contrast_amount, dither, dither_amount, add_noise_amount))

    # Keep the audio from the original clip
    processed_clip = processed_clip.set_audio(clip.audio)

    # Write the result to an output MP4 file
    processed_clip.write_videofile(output_video_path, codec='libx264', fps=fps or clip.fps, audio_codec='aac')

# Example usage
video_to_mp4(
    input_video_path="/Users/agi/Dropbox/Portfolio/VIdeo/AD_00006_5_seconds_prob4_ahq12_dither_16_aion1.mp4",
    output_video_path="/Users/agi/Dropbox/Portfolio/VIdeo/AD_00006_5_seconds_prob4_ahq12_dither_16_aion1_dith-2.mp4",
    start_time=0,  # start at 0 seconds
    # end_time=5,    # end at 5 seconds
    # resize=(320, 240),  # resize to 320x240 (commented out)
    fps=8,  # set frames per second to 8
    black_and_white=True,  # convert video to black and white
    contrast=True,  # apply contrast enhancement
    # contrast_amount=1.5,  # set contrast amount (0.0-2.0)
    dither=True,  # apply dithering effect for a lo-fi look
    dither_amount=75,  # set dithering amount to 75% (0-100)
    add_noise_amount=0  # add noise to each frame for lossy effect
)
