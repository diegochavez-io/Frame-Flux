import subprocess
import os

def encode_to_hap(source_file, output_file, hap_type='hap'):
    ffmpeg_command = ["ffmpeg", "-i", source_file, "-c:v", "hap"]

    if hap_type == 'hap_alpha':
        ffmpeg_command.extend(["-format", "hap_alpha"])
    elif hap_type == 'hap_q':
        ffmpeg_command.extend(["-format", "hap_q"])

    ffmpeg_command.append(output_file)

    # Execute the FFmpeg command
    subprocess.run(ffmpeg_command)

# Usage example
source_file = "/Users/agi/Desktop/_Runway4TD_S02.mp4"  # Replace with your source file path
output_file = "/Users/agi/Desktop/_Runway4TD_S02_HAP.mov"  # Replace with your desired output file path

# Call the function
encode_to_hap(source_file, output_file, hap_type='hap')  # hap_type can be 'hap', 'hap_alpha', or 'hap_q'
