import os
import subprocess

def convert_video(input_path, output_path):
    if os.path.isdir(input_path):
        print(f"Input path is a directory. Listing files in directory: {input_path}")
        filenames = [os.path.join(input_path, filename) for filename in os.listdir(input_path) if filename.endswith((".mkv", ".mp4"))]
    else:
        print(f"Input path is a file: {input_path}")
        filenames = [input_path]

    for input_file in filenames:
        if input_file.endswith((".mkv", ".mp4")):
            output_file = os.path.join(output_path, f"{os.path.splitext(os.path.basename(input_file))[0]}_converted.mp4")
            print(f"Processing file: {input_file}")
            command = [
                "ffmpeg", "-i", input_file, "-c:v", "h264", "-c:a", "aac",
                "-b:v", "10M", "-strict", "-2", output_file
            ]
            print(f"Running command: {' '.join(command)}")
            try:
                result = subprocess.run(command, check=True, capture_output=True, text=True)
                print(f"Command output: {result.stdout}")
                print(f"Successfully converted: {input_file}")
            except subprocess.CalledProcessError as e:
                print(f"Error converting file {input_file}: {e}")
                print(f"Error output: {e.stderr}")
        else:
            print(f"Skipping file: {input_file} (not a valid video file format)")

if __name__ == "__main__":
    input_path = "/Volumes/ML 5TB/_OUTPUT/epoch-120_coral-1280_226-7-s_24-0-fps_frame-000972-jpg_scale_2x_prob-3-2x-RIFE-RIFE4-0-48fps_scale_1x_alq-13.mov"
    output_path = "/Volumes/ML 5TB/_OUTPUT/"
    os.makedirs(output_path, exist_ok=True)
    convert_video(input_path, output_path)
