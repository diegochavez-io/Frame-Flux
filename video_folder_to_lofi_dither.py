import os
import numpy as np
from moviepy.editor import VideoFileClip, AudioFileClip
import moviepy.video.fx.all as vfx
from PIL import Image, ImageOps, ImageEnhance

def apply_dithering(image, dither_amount):
    """
    Apply dithering to the image with a specified dither amount.
    """
    dithered = image.convert('1')
    if dither_amount < 100:
        blended = Image.blend(image.convert('L'), dithered.convert('L'), dither_amount / 100)
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

def adjust_contrast(image, contrast_amount):
    """
    Adjust the contrast of the image by directly manipulating pixel values.
    """
    contrast_factor = (259 * (contrast_amount + 255)) / (255 * (259 - contrast_amount))
    def contrast(c):
        return 128 + contrast_factor * (c - 128)
    return image.point(contrast)

def adjust_saturation(image, saturation_amount):
    """
    Adjust the saturation of the image.
    """
    enhancer = ImageEnhance.Color(image)
    return enhancer.enhance(saturation_amount / 100.0)

def process_frame(frame, black_and_white=False, dither=False, dither_amount=100, add_noise_amount=0, contrast_amount=100, saturation_amount=100):
    """
    Process a single frame with optional dithering, noise addition, contrast, and saturation adjustment.
    """
    original_image = Image.fromarray(frame)
    pil_image = original_image.convert('L') if black_and_white else original_image.copy()

    if dither:
        dithered_image = apply_dithering(pil_image, dither_amount)
        pil_image = Image.blend(original_image.convert('RGB'), dithered_image, 0.5)

    if add_noise_amount > 0:
        pil_image = add_noise(pil_image, add_noise_amount)

    if contrast_amount != 100:
        pil_image = adjust_contrast(pil_image, contrast_amount)

    if saturation_amount != 100:
        pil_image = adjust_saturation(pil_image, saturation_amount)

    return np.array(pil_image)

def video_to_mp4(input_video_path, output_video_path, start_time=None, end_time=None, resize=None, fps=None, black_and_white=False, dither=False, dither_amount=100, add_noise_amount=0, contrast_amount=100, saturation_amount=100):
    """
    Convert a video to MP4 with optional dithering, noise, contrast, and saturation effects, including audio.

    Parameters:
    input_video_path (str): Path to the input video file.
    output_video_path (str): Path to save the output MP4 file.
    start_time (float, optional): Start time in seconds to begin the video.
    end_time (float, optional): End time in seconds to end the video.
    resize (tuple, optional): Resize the video (width, height).
    fps (int, optional): Frames per second for the video.
    black_and_white (bool, optional): Convert video to black and white if True.
    dither (bool, optional): Apply dithering effect for a lo-fi look.
    dither_amount (int, optional): Percentage of dithering (0-100).
    add_noise_amount (int, optional): Amount of noise to add to each frame.
    contrast_amount (int, optional): Amount of contrast adjustment (0-100).
    saturation_amount (int, optional): Amount of saturation adjustment (0-100).
    """
    # Ensure the output directory exists
    output_dir = os.path.dirname(output_video_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Load the video clip
    clip = VideoFileClip(input_video_path)

    # Print the duration of the video
    print(f"Processing {input_video_path}, duration: {clip.duration} seconds")

    # Trim the clip if start_time and end_time are provided
    if start_time is not None and end_time is not None:
        clip = clip.subclip(start_time, end_time)

    # Resize the clip if resize parameter is provided
    if resize is not None:
        clip = clip.resize(resize)

    # Set the fps if provided
    if fps is not None:
        clip = clip.set_fps(fps)

    # Process each frame
    processed_clip = clip.fl_image(lambda frame: process_frame(frame, black_and_white, dither, dither_amount, add_noise_amount, contrast_amount, saturation_amount))

    # Keep the audio from the original clip
    processed_clip = processed_clip.set_audio(clip.audio)

    # Write the result to an output MP4 file
    processed_clip.write_videofile(output_video_path, codec='libx264', fps=fps or clip.fps, audio_codec='aac')

def process_folder(input_folder, output_folder, **kwargs):
    """
    Process all video files in the input folder and save them to the output folder with _dither suffix.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.mp4', '.mov', '.avi', '.mkv')):
            input_video_path = os.path.join(input_folder, filename)
            output_video_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}_dither.mp4")
            video_to_mp4(input_video_path, output_video_path, **kwargs)

# Example usage
process_folder(
    input_folder="/Users/agi/Dropbox/ComfyUI_Output/2024-07-21/scale",
    output_folder="/Users/agi/Dropbox/ComfyUI_Output/2024-07-21/dither",
    # start_time=0,  # start at 0 seconds
    # end_time=5,    # end at 5 seconds
    # resize=(320, 240),  # resize to 320x240 (commented out)
    fps=12,  # set frames per second to 12
    black_and_white=False,  # Do not convert video to black and white
    dither=True,  # apply dithering effect for a lo-fi look
    dither_amount=85,  # set dithering amount to 45%
    # add_noise_amount=5,  # add noise to each frame for lossy effect
    contrast_amount=80,  # adjust contrast to make dithering pop (0-100 scale)
    saturation_amount=150  # boost saturation to compensate for color loss (0-100 scale)
)
