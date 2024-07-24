import torch
import numpy as np
import imageio
from PIL import Image

from comfy.utils import ProgressBar

class LofiVaporwaveGIF:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "video_frames": ("IMAGE",),
                "output_path": ("STRING", {"default": "output.gif"}),
                "resize": ("STRING", {"default": "800x800"}),
                "fps": ("INT", {"default": 8, "min": 1, "max": 30, "step": 1}),
                "quality": ("INT", {"default": 100, "min": 1, "max": 100, "step": 1}),
                "dither_amount": ("INT", {"default": 80, "min": 0, "max": 100, "step": 1}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("output_path",)
    FUNCTION = "process_video"
    CATEGORY = "🏵️Fill Nodes/VFX"

    def apply_dithering(self, image, dither_amount):
        if dither_amount == 100:
            return image.convert('1')  # Full dithering
        else:
            dithered = image.convert('1')
            return Image.blend(image.convert('L'), dithered.convert('L'), dither_amount / 100)

    def apply_halftone(self, image, dot_size=1):
        image = image.convert('L')
        width, height = image.size
        halftone_image = Image.new('L', (width, height))
        pixels = halftone_image.load()
        
        for x in range(0, width, dot_size):
            for y in range(0, height, dot_size):
                box = (x, y, x + dot_size, y + dot_size)
                region = image.crop(box)
                average = int(np.mean(region))
                for i in range(x, x + dot_size):
                    for j in range(y, y + dot_size):
                        if i < width and j < height:
                            pixels[i, j] = average
        
        return halftone_image

    def process_video(self, video_frames, output_path, resize="800x800", fps=8, quality=100, dither_amount=80):
        frames = []
        total_frames = video_frames.shape[0]
        width, height = map(int, resize.split('x'))
        pbar = ProgressBar(total_frames)

        for i in range(total_frames):
            frame = video_frames[i].cpu().numpy()
            pil_image = Image.fromarray(np.uint8(frame * 255))
            pil_image = pil_image.resize((width, height))
            pil_image = self.apply_dithering(pil_image, dither_amount)
            pil_image = self.apply_halftone(pil_image, dot_size=1)
            frames.append(np.array(pil_image.convert('RGB')))
            pbar.update_absolute(i + 1)

        imageio.mimsave(output_path, frames, format='GIF', fps=fps, quantizer='nq', palettesize=256)
        return (output_path,)

# Node mappings
NODE_CLASS_MAPPINGS = {
    "LofiVaporwaveGIF": LofiVaporwaveGIF
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "LofiVaporwaveGIF": "Lofi Vaporwave GIF"
}
