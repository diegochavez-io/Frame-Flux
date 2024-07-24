import os
import subprocess

def duplicate_frames(input_file, output_file, num_duplicates, temp_dir):
    """
    Extracts frames from a video, duplicates them, and encodes into a ProRes output.

    Args:
        input_file: Path to the input video file.
        output_file: Path to the desired output video file.
        num_duplicates: Number of times to duplicate each frame.
        temp_dir: Directory to store the extracted and duplicated frames.
    """
    
    # Specify absolute path to your ffmpeg binary
    ffmpeg_path = "/Users/agi/miniforge3/envs/audio/bin/ffmpeg"

    # Debugging: Print the temp directory for verification
    print("Temp Directory:", temp_dir)

    # Extract frames into the temporary directory
    subprocess.call([ffmpeg_path, "-i", input_file, 
                     os.path.join(temp_dir, "frame_%0d.jpg")])  

    # Duplicate frames in place 
    for filename in os.listdir(temp_dir):
        if filename.endswith(".jpg"):
            filepath = os.path.join(temp_dir, filename)
            for _ in range(num_duplicates):
                new_filename = os.path.join(temp_dir, f"{filename[:-4]}_{os.urandom(4).hex()}.jpg")
                os.copy(filepath, new_filename) 

    # Combine the duplicated frames into ProRes output (replace <framerate> with actual value)
    subprocess.call([ffmpeg_path, "-framerate",  "<framerate>", 
                     "-f",  "image2", 
                     "-i", os.path.join(temp_dir, "%d.jpg"),
                     "-c:v", "prores_ks", "-pix_fmt", "yuv422p10le",
                     output_file]) 

# ============== Usage Example ==============
input_file = "/Volumes/Apus/Catalyst/Working_Files/cocoon_dup_frames-fix.mov"
output_file = "/Volumes/Apus/Catalyst/Working_Files/output.mov"
num_duplicates = 2  # Duplicate each frame twice
temp_dir = "/path/to/temp/directory"  # Make sure this directory exists 

duplicate_frames(input_file, output_file, num_duplicates, temp_dir)
