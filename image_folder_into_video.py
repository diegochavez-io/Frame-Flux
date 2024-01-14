import cv2
import os
import random

# Parameters
input_folder = r"G:\My Drive\algo-film\delenda_algo_film_shoot_0822\extracted_frames"  # Folder containing all the image frames
output_video_path = r"G:\My Drive\algo-film\delenda_algo_film_shoot_0822\rand_output_video_all_frames.mp4"  # Path to save the output video
frame_rate = 24  # Desired frame rate for the output video
frame_hold = 5  # Number of times each frame should be repeated
random_order = True  # Set to True to randomize the order of frames

def images_to_video(input_folder, output_video_path, frame_rate, frame_hold, random_order):
    # Get all image files from the input directory
    image_files = [f for f in os.listdir(input_folder) if f.endswith(('.jpg', '.jpeg', '.png'))]
    
    # Shuffle the order if random_order is True
    if random_order:
        random.shuffle(image_files)
    else:
        image_files.sort()  # Sorting ensures frames are in order
    
    # Check if there are any images to process
    if not image_files:
        print(f"No images found in the specified directory: {input_folder}")
        return

    # Read the first image to get the dimensions
    frame = cv2.imread(os.path.join(input_folder, image_files[0]))
    h, w, layers = frame.shape
    size = (w, h)
    
    # Create a video writer object
    out = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'mp4v'), frame_rate, size)

    for image_file in image_files:
        image_path = os.path.join(input_folder, image_file)
        image = cv2.imread(image_path)
        
        # Repeat the image for frame_hold times
        for _ in range(frame_hold):
            out.write(image)

    out.release()
    print(f"Video saved to {output_video_path}")

if __name__ == "__main__":
    images_to_video(input_folder, output_video_path, frame_rate, frame_hold, random_order)
