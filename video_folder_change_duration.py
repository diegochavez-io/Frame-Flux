import moviepy.editor as mp
import os

def change_video_duration(input_folder, new_duration):
    # Iterate through all files in the input folder
    for filename in os.listdir(input_folder):
        # Skip hidden files or system files
        if filename.startswith('.'):
            continue
        
        # Create the full path to the file
        input_path = os.path.join(input_folder, filename)
        
        # Check if the file is a video file (you can add more extensions if needed)
        if filename.lower().endswith(('.mp4', '.mov', '.avi', '.mkv', '.flv')):
            try:
                # Load the video
                video = mp.VideoFileClip(input_path)
                
                # Calculate the speed factor
                speed_factor = video.duration / new_duration
                
                # Modify the video speed
                modified_video = video.fx(mp.vfx.speedx, speed_factor)
                
                # Create output file name based on input file name and new duration
                base_name, ext = os.path.splitext(filename)
                output_path = os.path.join(input_folder, f"{base_name}_{new_duration}_seconds.mp4")
                
                # Write the output video with specified codec and quality settings
                modified_video.write_videofile(
                    output_path,
                    codec='libx264',
                    preset='veryslow',
                    ffmpeg_params=[
                        '-crf', '18',
                        '-profile:v', 'high'
                    ]
                )
                print(f"Processed {filename} successfully.")
            except Exception as e:
                print(f"Failed to process {filename}: {e}")

# Input folder
input_folder = '/Volumes/Celeste/_ComfyUI_PC-Backup/_Colab/2024-06-08/interpolated'  # Change this to your input folder path
# New duration in seconds
new_duration = 5  # Change this to the desired duration

# Change the video duration for all videos in the folder
change_video_duration(input_folder, new_duration)
