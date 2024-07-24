import os
import cv2
import dlib
from imutils import face_utils
import numpy as np

# Initialize dlib's face detector (HOG-based) and then create the facial landmark predictor
detector = dlib.get_frontal_face_detector()
predictor_path = '/Users/agi/Dropbox/_AM/2023 Album Promos/1_Hydra/Midjourney Hydra Images/Hydra_Characters/shape_predictor_68_face_landmarks.dat'
predictor = dlib.shape_predictor(predictor_path)

# Set the directory paths
input_dir_path = '/Users/agi/Dropbox/_AM/2023 Album Promos/1_Hydra/Midjourney Hydra Images/Hydra_Characters/_Hydra Albino Mystic'
output_base_dir = '/Users/agi/Dropbox/_AM/2023 Album Promos/1_Hydra/Midjourney Hydra Images/Hydra_Characters'
output_dir_path = os.path.join(output_base_dir, os.path.basename(input_dir_path) + '_aligned')

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir_path):
    os.makedirs(output_dir_path)

# Define the target output size with 16:9 aspect ratio
max_output_width = 1280
max_output_height = 720

# Function to align faces
def align_face(image, gray, rect):
    shape = predictor(gray, rect)
    shape = face_utils.shape_to_np(shape)

    # Compute the bounding box that encloses all facial landmarks
    x, y, w, h = cv2.boundingRect(shape)

    # Expand the bounding box slightly
    margin = 0.2
    x -= int(w * margin)
    y -= int(h * margin)
    w += int(2 * w * margin)
    h += int(2 * h * margin)

    # Ensure the expanded bounding box stays within the image boundaries
    x = max(0, x)
    y = max(0, y)
    w = min(w, image.shape[1] - x)
    h = min(h, image.shape[0] - y)

    # Center and resize the bounding box to fit the desired output size while maintaining the aspect ratio
    desired_width = max_output_width
    desired_height = max_output_height
    aspect_ratio = desired_width / desired_height
    face_aspect_ratio = w / h

    if face_aspect_ratio > aspect_ratio:
        new_w = w
        new_h = int(w / aspect_ratio)
    else:
        new_h = h
        new_w = int(h * aspect_ratio)

    new_x = x + w // 2 - new_w // 2
    new_y = y + h // 2 - new_h // 2

    # Crop and resize the aligned face region
    aligned_face = image[new_y:new_y+new_h, new_x:new_x+new_w]
    aligned_face = cv2.resize(aligned_face, (desired_width, desired_height))

    return aligned_face



# Iterate over all the images in the directory
for filename in os.listdir(input_dir_path):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        # Read the image
        img_path = os.path.join(input_dir_path, filename)
        img = cv2.imread(img_path)

        # Convert the image to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Detect faces
        rects = detector(gray, 1)

        # Align and save the faces
        for rect in rects:
            aligned_face = align_face(img, gray, rect)
            output_filename = os.path.join(output_dir_path, f'aligned_{filename}')
            cv2.imwrite(output_filename, aligned_face)
        if not rects:
            print(f"No faces detected in the image: {filename}")
