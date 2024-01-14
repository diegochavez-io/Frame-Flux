import os
import subprocess

def run_ffmpeg(input_file, output_file, x, y, count):
    # Ensure the output directory exists
    output_dir = os.path.dirname(output_file)
    os.makedirs(output_dir, exist_ok=True)
    
    command = f'ffmpeg -i "{input_file}" -vf "crop=240:240:{x}:{y}" "{output_file}-crop-{count}.mp4"'
    subprocess.call(command, shell=True)

input_file = "G:\My Drive\AI\StableWarpFusion\images_out\_ffmpeg_test\output2.mp4"
output_file = "G:\My Drive\AI\StableWarpFusion\images_out\_ffmpeg_test"

count = 0
for y in range(3):
    y = 240*y
    for x in range(3):
        x = 240*x
        run_ffmpeg(input_file, output_file, x, y, count)
        count +=1
