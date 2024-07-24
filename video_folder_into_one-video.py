import os
import random
from moviepy.editor import VideoFileClip, concatenate_videoclips

def get_random_segments(video_path, num_segments=2, segment_duration=5, temp_dir="temp_segments"):
    clip = VideoFileClip(video_path)
    video_duration = clip.duration
    segments = []
    
    for i in range(num_segments):
        start_time = random.uniform(0, video_duration - segment_duration)
        end_time = start_time + segment_duration
        segment = clip.subclip(start_time, end_time)
        segment_file = os.path.join(temp_dir, f"{os.path.basename(video_path)}_segment_{i}.mp4")
        segment.write_videofile(segment_file, codec='libx264')
        segments.append(segment_file)
    
    clip.close()
    return segments

def create_video_from_folder(
    folder_path,
    output_path,
    num_segments=2,
    segment_duration=5,
    frame_rate=24,
    temp_dir="temp_segments"
):
    # Ensure output_path has a .mp4 extension
    if not output_path.lower().endswith('.mp4'):
        output_path += '.mp4'
    
    # Create temporary directory for segments
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    
    # Get list of video files
    video_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith(('mp4', 'avi', 'mov', 'mkv'))]
    video_files.sort()
    
    all_segments = []
    
    # Extract random segments from each video and save them to disk
    for video_file in video_files:
        segments = get_random_segments(video_file, num_segments, segment_duration, temp_dir)
        all_segments.extend(segments)
    
    # Load segments from disk and concatenate them into one video
    segment_clips = [VideoFileClip(segment) for segment in all_segments]
    final_clip = concatenate_videoclips(segment_clips, method='compose')
    final_clip.set_fps(frame_rate)
    final_clip.write_videofile(output_path, codec='libx264')
    
    # Clean up temporary segment files
    for segment in all_segments:
        os.remove(segment)

    # Clean up temporary directory
    os.rmdir(temp_dir)

# Usage example
create_video_from_folder(
    folder_path='/Volumes/Apus/Catalyst/AnimateDiff/_MOV/scaled',
    output_path='/Users/agi/Dropbox/Delenda/Catalyst/BTS',  # Specify a valid output file with .mp4 extension
    num_segments=2,
    segment_duration=0.15,
    frame_rate=12
)
