import os
from PIL import Image

def rotate_images(folder_path, angle):
    """
    Rotates all images in the specified folder by the given angle.
    
    :param folder_path: Path to the folder containing images
    :param angle: Rotation angle in degrees (clockwise)
    """
    # Ensure the output folder exists
    output_folder = os.path.join(folder_path, "rotated")
    os.makedirs(output_folder, exist_ok=True)
    
    # Supported image formats
    supported_formats = ('.png', '.jpg', '.jpeg', '.gif', '.bmp')
    
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(supported_formats):
            # Open the image
            img_path = os.path.join(folder_path, filename)
            with Image.open(img_path) as img:
                # Rotate the image
                rotated_img = img.rotate(angle, expand=True)
                
                # Save the rotated image
                output_path = os.path.join(output_folder, f"rotated_{filename}")
                rotated_img.save(output_path)
                print(f"Rotated and saved: {output_path}")

# Example usage
folder_path = "/Users/agi/Dropbox/ComfyUI_Output/2024-07-31/FLIP"
rotation_angle = 90  # Degrees clockwise

rotate_images(folder_path, rotation_angle)