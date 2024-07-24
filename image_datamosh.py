from PIL import Image
import random

# Load the image
image_path = "/Users/agi/Dropbox/Midjourney/_PYC_/2. Midjourney/ComfyUI_00147_.png"
img = Image.open(image_path)
pixels = img.load()

# Function to apply a glitch effect
def apply_glitch(img, glitch_intensity=0.1, glitch_amount=10, offset_x=0, offset_y=0, datamosh_scale=1, melt_map=1):
    width, height = img.size
    
    # Apply horizontal glitches
    for y in range(height):
        if random.random() < glitch_intensity:  # Apply glitch with a given probability
            offset = random.randint(-glitch_amount, glitch_amount)
            row = [pixels[x, y] for x in range(width)]
            row = row[offset:] + row[:offset]  # Shift row pixels by offset
            for x in range(width):
                pixels[x, y] = row[x]

    # Apply vertical glitches
    for x in range(width):
        if random.random() < glitch_intensity:  # Apply glitch with a given probability
            offset = random.randint(-glitch_amount, glitch_amount)
            column = [pixels[x, y] for y in range(height)]
            column = column[offset:] + column[:offset]  # Shift column pixels by offset
            for y in range(height):
                pixels[x, y] = column[y]
    
    # Apply datamosh scale
    for y in range(0, height, datamosh_scale):
        for x in range(width):
            pixels[x, y] = pixels[(x + offset_x) % width, (y + offset_y) % height]
    
    # Apply melt map
    for y in range(0, height, melt_map):
        for x in range(0, width, melt_map):
            if random.random() < glitch_intensity:
                pixels[x, y] = pixels[(x + offset_x) % width, (y + offset_y) % height]
    
    return img

# Apply the glitch effect with additional controls
glitched_img = apply_glitch(img, glitch_intensity=50.1, glitch_amount=20, offset_x=30, offset_y=30, datamosh_scale=5, melt_map=10)

# Save the glitched image
output_path = "/Users/agi/Desktop/_Digital_billboard"
glitched_img.save(output_path)
output_path
