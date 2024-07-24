import os
import numpy as np
import imageio
from moviepy.editor import VideoFileClip
import moviepy.video.fx.all as vfx
from PIL import Image, ImageOps

def apply_dithering(image, dither_amount):
    """
    Apply dithering to the image with a specified dither amount.
    """
    if dither_amount == 100:
        return image.convert('1')  # Full dithering
    else:
        # Blend the dithered image with the original to control dither amount
        dithered = image.convert('1')
        return Image.blend(image.convert('L'), dithered.convert('L'), dither_amount / 100).convert('L')

def apply_halftone(image, dot_size=1):
    """
    Apply halftone effect to the image with specified dot size.
    """
    # Convert to grayscale
    image = image.convert('L')
    
    # Create halftone pattern using a custom approach
    width, height = image.size
    halftone_image = Image.new('L', (width, height))
    
    for x in range(0, width, dot_size):
        for y in range(0, height, dot_size):
            box = (x, y, x + dot_size, y + dot_size)
            region = image.crop(box)
            average = int(np.mean(region))
            fill_color = 255 if average > 127 else 0
            halftone_image.paste(fill_color, box)

    return halftone_image

def video_to_gif(input_video_path, output_gif_path, start_time=None, end_time=None, resize=None, fps=None, quality=10, black_and_white=False, dither=False, dither_amount=100, halftone=False, dot_size=1):
    """
    Convert a video to GIF with compression settings and optional dithering and halftone effects.

    Parameters:
    input_video_path (str): Path to the input video file.
    output_gif_path (str): Path to save the output GIF file.
    start_time (float, optional): Start time in seconds to begin the GIF.
    end_time (float, optional): End time in seconds to end the GIF.
    resize (tuple, optional): Resize the video (width, height).
    fps (int, optional): Frames per second for the GIF.
    quality (int, optional): Compression quality for the GIF (0-100, lower is more compressed).
    black_and_white (bool, optional): Convert video to black and white if True.
    dither (bool, optional): Apply dithering effect for a lo-fi look.
    dither_amount (int, optional): Percentage of dithering (0-100).
    halftone (bool, optional): Apply halftone dotted effect if True.
    dot_size (int, optional): Size of the dots for halftone effect.
    """
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

    # Write the result to a temporary file using moviepy
    temp_gif_path = "temp.gif"
    clip.write_gif(temp_gif_path, fps=fps)

    # Ensure the output path includes a file name
    if not output_gif_path.endswith('.gif'):
        output_gif_path = os.path.join(output_gif_path, "output.gif")

    # Read the temporary GIF and apply lo-fi compression
    reader = imageio.get_reader(temp_gif_path, format='gif')
    writer = imageio.get_writer(output_gif_path, format='gif', mode='I', quality=quality)

    for frame in reader:
        # Convert frame to PIL image
        pil_image = Image.fromarray(frame)

        # Apply dithering effect if specified
        if dither:
            pil_image = apply_dithering(pil_image, dither_amount)

        # Apply halftone effect if specified
        if halftone:
            pil_image = apply_halftone(pil_image, dot_size)

        # Append the processed frame to the output GIF
        writer.append_data(np.array(pil_image))

    writer.close()

    # Remove the temporary file
    os.remove(temp_gif_path)

# Example usage
video_to_gif(
    input_video_path="//Users/agi/Dropbox/Runway/Int/snake styleganxl cc_scale__clip_4.mp4",
    output_gif_path="/Users/agi/Dropbox/Portfolio/GIF/output_7.gif",
    start_time=0,  # start at 0 seconds
    end_time=5,    # end at 5 seconds
    # resize=(320, 240),  # resize to 320x240 (commented out)
    fps=8,  # set frames per second to 8
    quality=15,  # set compression quality for a lo-fi effect
    black_and_white=True,  # convert video to black and white
    dither=True,  # apply dithering effect for a lo-fi look
    dither_amount=80,  # set dithering amount to 80%
    halftone=True,  # apply halftone effect
    dot_size=2  # set dot size for halftone effect
)
