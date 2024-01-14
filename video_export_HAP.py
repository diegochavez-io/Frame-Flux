import os
import subprocess

# Specify your input and output file paths here
input_file = r"G:\My Drive\AI\SGXL_Output\LookingGlass_GAN\LookignGlass_koi_pix2pix_07_apo8_prob3.mov"
output_directory = r'D:\_HAP\StyleGAN'
output_file_name = os.path.basename(input_file)
output_file = os.path.join(output_directory, output_file_name)

def convert_to_hap(input_file, output_file):
    command = [
        'ffmpeg',
        '-i', input_file,
        '-c:v', 'hap',
        output_file
    ]
    
    subprocess.run(command)

# Run the conversion
convert_to_hap(input_file, output_file)
