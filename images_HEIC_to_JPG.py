from wand.image import Image
import os


def convert_heic_to_jpg(input_folder):
    # Create a new directory for processed images
    output_folder = os.path.join(input_folder, "Processed_JPG")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(".heic"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename[:-5] + ".jpg")

            # Use Wand to convert the image
            with Image(filename=input_path) as img:
                img.format = "jpg"
                img.save(filename=output_path)


# Usage
input_folder = "G:\\My Drive\\Hash-2311"
convert_heic_to_jpg(input_folder)
