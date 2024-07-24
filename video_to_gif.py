import imageio
from PIL import Image
import numpy as np
import os

def convert_to_gif(input_video, output_gif, max_size_mb=15, initial_fps=10, initial_scale=1.0):
    # Read video file
    reader = imageio.get_reader(input_video)
    
    # Get original fps
    fps = reader.get_meta_data().get('fps', initial_fps)
    
    # Initialize parameters
    current_fps = fps
    current_scale = initial_scale
    
    while True:
        frames = []
        for frame in reader:
            # Resize frame
            pil_frame = Image.fromarray(frame).convert('RGB')
            new_size = tuple(int(dim * current_scale) for dim in pil_frame.size)
            resized_frame = np.array(pil_frame.resize(new_size, Image.LANCZOS))
            frames.append(resized_frame)
        
        # Save as GIF
        imageio.mimsave(output_gif, frames, fps=current_fps, optimize=True)
        
        # Check file size
        current_size_mb = os.path.getsize(output_gif) / (1024 * 1024)
        
        if current_size_mb <= max_size_mb:
            print(f"GIF created successfully. Size: {current_size_mb:.2f} MB")
            break
        
        # Adjust parameters if file is too large
        if current_fps > 5:
            current_fps -= 1
        elif current_scale > 0.5:
            current_scale -= 0.1
        else:
            print("Unable to reduce file size further while maintaining quality.")
            break
        
        print(f"Retrying with fps={current_fps}, scale={current_scale:.2f}")

# Example usage:
input_video = '/Users/agi/Dropbox/Portfolio/Pathetic/REVERSE_221205_5_stable_warpfusion_0-5-22_MV_REVERSE(-1)_prob3.gif'
output_gif = '/Users/agi/Dropbox/Portfolio/Pathetic/REVERSE_221205_5_stable_warpfusion_0-5-22_MV_REVERSE(-1)_prob3_v4.gif'
convert_to_gif(input_video, output_gif)