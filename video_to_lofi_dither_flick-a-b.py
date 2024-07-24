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

def apply_threshold(image, threshold, invert=False):
    """
    Apply a binary threshold to the image.
    """
    grayscale_image = image.convert('L')
    if invert:
        binary_image = grayscale_image.point(lambda p: 255 if p < threshold else 0, '1')
    else:
        binary_image = grayscale_image.point(lambda p: 255 if p > threshold else 0, '1')
    return binary_image.convert('RGB')

def apply_two_tone_threshold(image, threshold, color1, color2, invert=False):
    """
    Apply a two-tone threshold to the image.
    """
    grayscale_image = image.convert('L')
    if invert:
        binary_image = grayscale_image.point(lambda p: 255 if p < threshold else 0, '1')
    else:
        binary_image = grayscale_image.point(lambda p: 255 if p > threshold else 0, '1')
    rgb_image = binary_image.convert('RGB')
    data = np.array(rgb_image)

    r1, g1, b1 = color1
    r2, g2, b2 = color2

    if invert:
        data[(data == [0, 0, 0]).all(axis=-1)] = [r1, g1, b1]
        data[(data == [255, 255, 255]).all(axis=-1)] = [r2, g2, b2]
    else:
        data[(data == [255, 255, 255]).all(axis=-1)] = [r1, g1, b1]
        data[(data == [0, 0, 0]).all(axis=-1)] = [r2, g2, b2]

    return Image.fromarray(data, 'RGB')

def process_frame(frame, frame_index, black_and_white=False, invert_bw=False, dither=False, dither_amount=100, add_noise_amount=0, contrast_amount=100, saturation_amount=100, threshold=None, two_tone_threshold=None, color1=(255, 0, 0), color2=(0, 0, 0), invert=False, frame_algorithm=(1, 1)):
    """
    Process a single frame, alternating between two effects for each frame (1,1 pattern).
    Includes debug output.
    """
    original_image = Image.fromarray(frame)

    # Determine which set of effects to apply based on the frame index
    if frame_index % 2 == 0:  # Even frames (including 0)
        print(f"Frame {frame_index}: Applying first effect set")
        if black_and_white:
            original_image = original_image.convert('L').convert('RGB')
        if invert_bw:
            original_image = ImageOps.invert(original_image.convert('L')).convert('RGB')
    else:  # Odd frames
        print(f"Frame {frame_index}: Applying second effect set")
        if dither:
            dithered_image = apply_dithering(original_image.convert('L'), dither_amount)
            original_image = Image.blend(original_image, dithered_image, 0.5)
        if add_noise_amount > 0:
            original_image = add_noise(original_image, add_noise_amount)
        if contrast_amount != 100:
            original_image = adjust_contrast(original_image, contrast_amount)
        if saturation_amount != 100:
            original_image = adjust_saturation(original_image, saturation_amount)
        if threshold is not None:
            original_image = apply_threshold(original_image, threshold, invert)
        if two_tone_threshold is not None:
            original_image = apply_two_tone_threshold(original_image, two_tone_threshold, color1, color2, invert)

    return np.array(original_image)

def video_to_mp4(input_video_path, output_video_path, start_time=None, end_time=None, resize=None, fps=None, black_and_white=False, invert_bw=False, dither=False, dither_amount=100, add_noise_amount=0, contrast_amount=100, saturation_amount=100, threshold=None, two_tone_threshold=None, color1=(255, 0, 0), color2=(0, 0, 0), invert=False, frame_algorithm=(1, 1)):
    """
    Convert a video to MP4 with optional effects, including audio. Includes debug output.
    """
    # Ensure the output directory exists
    output_dir = os.path.dirname(output_video_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Load the video clip
    clip = VideoFileClip(input_video_path)

    # Print the duration and FPS of the video
    print(f"Video duration: {clip.duration} seconds")
    print(f"Original FPS: {clip.fps}")

    # Trim the clip if start_time and end_time are provided
    if start_time is not None and end_time is not None:
        clip = clip.subclip(start_time, end_time)

    # Resize the clip if resize parameter is provided
    if resize is not None:
        clip = clip.resize(resize)

    # Set the fps if provided
    if fps is not None:
        clip = clip.set_fps(fps)
    
    print(f"Processing FPS: {clip.fps}")

    # Process each frame
    frame_count = 0
    def process_and_count(get_frame, t):
        nonlocal frame_count
        frame = process_frame(get_frame(t), frame_count, black_and_white, invert_bw, dither, dither_amount, add_noise_amount, contrast_amount, saturation_amount, threshold, two_tone_threshold, color1, color2, invert, frame_algorithm)
        frame_count += 1
        return frame

    processed_clip = clip.fl(process_and_count)

    # Keep the audio from the original clip
    processed_clip = processed_clip.set_audio(clip.audio)

    # Write the result to an output MP4 file
    processed_clip.write_videofile(output_video_path, codec='libx264', fps=fps or clip.fps, audio_codec='aac')

    print(f"Total frames processed: {frame_count}")

# Example usage
if __name__ == "__main__":
    video_to_mp4(
        input_video_path="/Users/agi/Dropbox/ComfyUI_Output/2024-07-21/video_clips/0720_9843576_00002.mov",
        output_video_path="/Users/agi/Dropbox/ComfyUI_Output/2024-07-21/dither/0720_9843576_00002_debug_output_1-1_v12.mp4",
        fps=12,
        black_and_white=False,
        invert_bw=True,
        dither=True,
        dither_amount=45,
        contrast_amount=80,
        saturation_amount=150,
        threshold=None,
        two_tone_threshold=None,
        color1=(4, 102, 101),
        color2=(251, 75, 25),
        frame_algorithm=(1, 1)  # This will create a 1-1 flip pattern
    )