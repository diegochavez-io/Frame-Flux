import cv2
import os
import random
import zipfile

# Parameters
source_file = "/Users/agi/Desktop/dlnda_cyr_00054689654_00026.mov"  # Path to the video file
image_count = 50  # Number of images to extract
output_size = 512  # Desired size of the output images
zip_output = False  # Set True to zip the output folder

# Output folder
output_folder = "/Users/agi/Desktop/Processed_Images"  # Output folder path

def crop_center(img, cropx, cropy):
    y, x, _ = img.shape
    startx = x // 2 - (cropx // 2)
    starty = y // 2 - (cropy // 2)
    return img[starty:starty+cropy, startx:startx+cropx]

def extract_frames(video_path, image_count, output_size):
    vidcap = cv2.VideoCapture(video_path)
    total_frames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Adjust image_count if it's more than the total frames
    image_count = min(image_count, total_frames)

    # Randomly select unique frames with a minimum gap
    min_gap = total_frames // image_count
    frames_to_extract = sorted(random.sample(range(total_frames), image_count))
    frames_to_extract = [frame + i * min_gap for i, frame in enumerate(frames_to_extract)]
    frames_to_extract = [min(frame, total_frames - 1) for frame in frames_to_extract]  # Adjust if exceeds total frames

    # Prepare the output subfolder
    output_subfolder = os.path.join(output_folder, os.path.splitext(os.path.basename(video_path))[0])
    os.makedirs(output_subfolder, exist_ok=True)

    for frame_index in frames_to_extract:
        vidcap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
        success, image = vidcap.read()
        if success:
            cropped_image = crop_center(image, output_size, output_size)
            cv2.imwrite(os.path.join(output_subfolder, f"frame{frame_index}.jpg"), cropped_image)

    vidcap.release()
    return output_subfolder

def zip_folder(folder):
    zipf = zipfile.ZipFile(f"{folder}.zip", 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(folder):
        for file in files:
            zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(folder, '..')))
    zipf.close()

def main():
    print(f"Extracting frames from {source_file}...")
    output_subfolder = extract_frames(source_file, image_count, output_size)
    
    if zip_output:
        print(f"Zipping output folder {output_subfolder}...")
        zip_folder(output_subfolder)
    print("Processing complete.")

if __name__ == "__main__":
    main()
