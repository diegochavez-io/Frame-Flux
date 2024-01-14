import subprocess
import shlex

def convert_mp4_to_avi(input_file, output_file):
    input_file = shlex.quote(input_file)
    output_file = shlex.quote(output_file)
    command = f"ffmpeg -i {input_file} {output_file}"
    subprocess.call(command, shell=True)

# specify your mp4 file
mp4_file = "E:/_OUTPUT/TPPP-liquid-chrome-BLUR.mov"
# specify the output avi file
avi_file = "E:/_OUTPUT/TPPP-liquid-chrome-BLUR.avi"

convert_mp4_to_avi(mp4_file, avi_file)
