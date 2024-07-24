import os
import subprocess
from tqdm import tqdm

# Parameters for easy configuration
input_video_file = "/Users/agi/Dropbox/Delenda/Catalyst/BTS/moth_pr.mp4" 
speed_factor = 2  # Adjust as needed
output_dir = "/Users/agi/Dropbox/Delenda/Catalyst/BTS/"

def convert_to_cfr(input_filename):
    """
    Converts a video to Constant Frame Rate (CFR) to avoid issues with variable frame rates.
    """
    print("Starting conversion to CFR...")
    cfr_filename = f"{os.path.splitext(input_filename)[0]}_cfr.mp4"
    command = [
        "ffmpeg", "-y", "-i", input_filename, "-filter:v", "fps=fps=30", cfr_filename
    ]
    try:
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        print("Conversion to CFR completed.")
        return cfr_filename
    except subprocess.CalledProcessError as e:
        print(f"Error converting to CFR: {e.output.decode()}")
        return None

def speed_up_video(input_filename, speed_factor, output_dir):
    print("Preparing to speed up video...")
    input_filename = convert_to_cfr(input_filename)  # Ensure input is CFR
    if not input_filename:
        return

    print(f"Processing video: {input_filename}")
    output_filename = f"{os.path.splitext(os.path.basename(input_filename))[0]}_x{speed_factor}.mp4"
    output_path = os.path.join(output_dir, output_filename)

    os.makedirs(output_dir, exist_ok=True)

    atempo_filters = ','.join(['atempo=0.5'] * (speed_factor // 2))
    if speed_factor % 2 != 0:  # Apply a final adjustment if there's a remainder
        atempo_filters += ',atempo=1.0' if atempo_filters == '' else ',atempo=0.707'  # Adjust based on actual need

    command = [
        "ffmpeg", "-y", "-i", input_filename, "-filter_complex",
        f"[0:v]setpts={speed_factor}*PTS[v];[0:a]{atempo_filters}[a]",
        "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "fast", "-c:a", "aac", output_path
    ]

    print("Executing ffmpeg command...")
    for i in tqdm(range(100), desc="Processing video"):
        # Ensure subprocess output is immediately visible
        process = subprocess.run(command, check=True, text=True, capture_output=True)
        print(process.stdout)
        print(f"Video sped up successfully and saved to {output_path}")
    print(f"Video processed successfully and saved to {output_path}")

# Main execution
if __name__ == "__main__":
    speed_up_video(input_video_file, speed_factor, output_dir)