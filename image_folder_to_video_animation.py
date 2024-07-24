import cv2
import os
import numpy as np

def create_video_from_images(input_folder, output_file, video_size=(1920, 1080), bg_color=(0, 0, 0), 
                             fps=30, frame_hold=1, video_duration=None):
    # Get list of image files
    image_files = [f for f in os.listdir(input_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
    image_files.sort()  # Sort files to ensure correct order

    # Calculate total frames
    total_frames = len(image_files) * frame_hold
    if video_duration:
        total_frames = min(total_frames, int(video_duration * fps))

    # Create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_file, fourcc, fps, video_size)

    for i in range(total_frames):
        # Create a blank frame with the specified background color
        frame = np.full((video_size[1], video_size[0], 3), bg_color, dtype=np.uint8)

        # Load and resize image
        img_index = i // frame_hold
        if img_index < len(image_files):
            img_path = os.path.join(input_folder, image_files[img_index])
            img = cv2.imread(img_path)
            
            if img is not None:
                # Calculate scaling factor to fit image within video frame
                h, w = img.shape[:2]
                scale = min(video_size[0] / w, video_size[1] / h)
                new_size = (int(w * scale), int(h * scale))
                
                # Resize image
                resized_img = cv2.resize(img, new_size)
                
                # Calculate position to center the image
                top = (video_size[1] - new_size[1]) // 2
                left = (video_size[0] - new_size[0]) // 2
                
                # Place the resized image onto the frame
                frame[top:top+new_size[1], left:left+new_size[0]] = resized_img

        # Write the frame
        out.write(frame)

    # Release the VideoWriter
    out.release()

    print(f"Video created: {output_file}")

# Example usage
input_folder = "/Users/agi/Library/CloudStorage/GoogleDrive-diegovchavez@gmail.com/My Drive/dataset-footage/delenda/algo_warp_frames"
output_file = "/Users/agi/Dropbox/Delenda/Catalyst/BTS/algo_warp_frames_catalyst_.mp4"
create_video_from_images(input_folder, output_file, video_size=(1920, 1080), bg_color=(0, 0, 0), 
                         fps=30, frame_hold=2, video_duration=10)