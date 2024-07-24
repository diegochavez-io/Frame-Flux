import cv2
import dlib
import numpy as np

# Load the images
image1_path = '/Users/agi/Dropbox/Midjourney/_PYC_/2. Midjourney/ComfyUI_00136_.png'
image2_path = '/Users/agi/Dropbox/Midjourney/_PYC_/2. Midjourney/ComfyUI_00142_.png'

image1 = cv2.imread(image1_path)
image2 = cv2.imread(image2_path)

# Initialize dlib's face detector and shape predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

def get_landmarks(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    rects = detector(gray)
    
    if len(rects) > 0:
        shape = predictor(gray, rects[0])
        coords = np.zeros((68, 2), dtype=int)
        for i in range(68):
            coords[i] = (shape.part(i).x, shape.part(i).y)
        return coords
    else:
        return None

# Get the landmarks
landmarks1 = get_landmarks(image1)
landmarks2 = get_landmarks(image2)

if landmarks1 is None or landmarks2 is None:
    print("Could not detect landmarks in one or both images.")
else:
    # Continue with triangulation and morphing
    pass
