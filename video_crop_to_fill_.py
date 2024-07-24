import cv2
import argparse

def fill_video_dimensions(source_file, output_file, target_width, target_height, crop_width, crop_height, resized_width, method):

    cap = cv2.VideoCapture(source_file)

    original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    out = cv2.VideoWriter(output_file, 
                          cv2.VideoWriter_fourcc(*'mp4v'), 
                          cap.get(cv2.CAP_PROP_FPS), 
                          (target_width, target_height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Resize the original frame if needed (independent of filling dimensions)
        if resized_width: 
            frame = cv2.resize(frame, (resized_width, int(resized_width * original_height / original_width)))

        # ... (Rest of the filling logic remains the same) ...      

# Example usage - you can modify these values
source_file = r"E:\Delenda Warp\02065280_runpod_8x_upscale.mov" 
output_file = "filled_video.mp4"
target_width = 1920
target_height = 1080
crop_width = 1280  # Example crop
crop_height = 720  # Example crop
resized_width = 1280  

fill_video_dimensions(source_file, output_file, target_width, target_height, crop_width, crop_height, resized_width, 'blur')  # Choose your method
