import moviepy.editor as mp
import os

def change_video_duration(input_path, new_duration, reverse=False):
    try:
        # Load the video
        print(f"Loading video: {input_path}")
        video = mp.VideoFileClip(input_path)
        
        # Print the original duration
        print(f"Original duration: {video.duration} seconds")
        
        # Reverse the video if the reverse flag is set to True
        if reverse:
            print("Reversing the video...")
            video = video.fx(mp.vfx.time_mirror)
            # Check if the video is reversed
            reversed_duration = video.duration
            print(f"Reversed duration: {reversed_duration} seconds")
        
        # Calculate the speed factor
        speed_factor = video.duration / new_duration
        print(f"Speed factor: {speed_factor}")
        
        # Modify the video speed
        print("Modifying the video speed...")
        modified_video = video.fx(mp.vfx.speedx, speed_factor)
        
        # Create output file name based on input file name and new duration
        base_name, ext = os.path.splitext(input_path)
        output_path = f"{base_name}_{new_duration}_seconds{ext}"
        
        # Write the output video with specified codec and quality settings
        print(f"Writing the output video to: {output_path}")
        modified_video.write_videofile(output_path, codec='libx264', preset='veryslow', bitrate='5000k')
    except IOError as e:
        print(f"An IOError occurred: {e}")
        print("Possible causes: corrupted file, incompatible codec, or outdated FFmpeg version.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Input file
input_file = '/Volumes/Celeste/_ComfyUI_PC-Backup/2024-06-08/interpolated/AD_00008_prob4_thf4.mov'  # Assuming ProRes format is in .mov container
# New duration in seconds
new_duration = 7  # For example, change this to the desired duration
# Reverse option
reverse = True  # Set to True to reverse the video, False to keep it normal

# Change the video duration with the reverse option
change_video_duration(input_file, new_duration, reverse)
