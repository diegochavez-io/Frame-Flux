import os
import cv2

# Set the input and output folders
input_folder = '/Users/agi/Dropbox/Midjourney/Microscopic Photography/ref'
output_folder = '/Users/agi/Dropbox/Midjourney/Microscopic Photography/ref_b&w'

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Loop through all the files in the input folder
for filename in os.listdir(input_folder):
    # Check if the file is an image
    if filename.endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
        # Read the image using OpenCV
        img = cv2.imread(os.path.join(input_folder, filename))

        # Convert the image to grayscale (black and white)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Save the grayscale image to the output folder
        cv2.imwrite(os.path.join(output_folder, filename), gray)

print("Images converted to black and white and saved to", output_folder)