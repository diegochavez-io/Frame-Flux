import os
from moviepy.editor import VideoFileClip
from moviepy.video.fx.all import rotate

def process_videos(input_folder, rotation, codec, resize_factor=1):
    # Ensure the codec is in the correct format and set the appropriate file extension
    if codec.lower() == 'proreshd':
        codec = 'prores_ks'
        file_extension = '.mov'
    elif codec.lower() == 'highest_quality_mp4':
        codec = 'libx264'
        file_extension = '.mp4'
    else:
        raise ValueError("Unsupported codec. Use 'proreshd' or 'highest_quality_mp4'.")

    # Create output folder
    output_folder = f"{input_folder}_rotated_{rotation}_resized_{resize_factor}_codec_{codec}"
    os.makedirs(output_folder, exist_ok=True)

    # Process each video file
    for filename in os.listdir(input_folder):
        if filename.endswith((".mp4", ".mov")):
            video_path = os.path.join(input_folder, filename)
            with VideoFileClip(video_path) as video:
                # Rotate video
                rotated_video = rotate(video, rotation)
                
                # Resize video if resize_factor is not 1
                if resize_factor != 1:
                    rotated_video = rotated_video.resize(resize_factor)
                
                # Set output file path
                output_filename = f"{os.path.splitext(filename)[0]}_{rotation}_resized_{resize_factor}_codec_{codec}{file_extension}"
                output_path = os.path.join(output_folder, output_filename)
                
                # Write video to file
                rotated_video.write_videofile(output_path, codec=codec, audio_codec='aac')

def main():
    input_folder = '/Users/agi/Dropbox/_AM/10. Touch Docs/Stable_Hall_24_08/Video Clips/Texture'
    rotation = 90  # Rotation in degrees (clockwise)
    codec = 'highest_quality_mp4'  # Options: 'proreshd', 'highest_quality_mp4'
    resize_factor = 1  # 1 for no resizing, or a float like 0.5 for 50% size

    process_videos(input_folder, rotation, codec, resize_factor)

if __name__ == "__main__":
    main()
