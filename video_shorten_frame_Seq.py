import os
import random
import time
from moviepy.editor import VideoFileClip, concatenate_videoclips, CompositeVideoClip, vfx
from scipy.signal import find_peaks
import numpy as np

def detect_scenes(video, min_scene_length=15):
    frame_diffs = []
    prev_frame = None
    for frame in video.iter_frames(fps=video.fps):
        if prev_frame is not None:
            diff = np.mean(np.abs(frame.astype(float) - prev_frame.astype(float)))
            frame_diffs.append(diff)
        prev_frame = frame

    if len(frame_diffs) > 0:
        peaks, _ = find_peaks(frame_diffs, height=np.mean(frame_diffs) + np.std(frame_diffs), distance=min_scene_length)
        scene_changes = list(peaks)
    else:
        scene_changes = []
    
    return [change / video.fps for change in scene_changes]  # Convert to seconds

def select_clips(video, scene_changes, target_duration, grain_size_frames, overlap_frames, random_factor):
    clips = []
    video_duration = video.duration
    total_frames = int(video.fps * video_duration)
    target_frames = int(target_duration * video.fps)
    
    effective_grain_size = grain_size_frames - overlap_frames
    num_grains = target_frames // effective_grain_size if effective_grain_size > 0 else target_frames

    for i in range(num_grains):
        # Calculate the ideal start frame to cover the whole video
        ideal_start_frame = int(i * total_frames / num_grains)
        
        # Find the nearest scene change
        if scene_changes:
            nearest_scene = min(scene_changes, key=lambda x: abs(x * video.fps - ideal_start_frame))
            start_frame = int(nearest_scene * video.fps)
        else:
            start_frame = ideal_start_frame
        
        # Apply random factor
        max_offset = int(random_factor * total_frames / 100)
        random_offset = random.randint(-max_offset, max_offset)
        start_frame = max(0, min(total_frames - grain_size_frames, start_frame + random_offset))
        
        start_time = start_frame / video.fps
        end_time = (start_frame + grain_size_frames) / video.fps
        clip = video.subclip(start_time, min(end_time, video_duration))
        clips.append(clip)
    
    return clips

def apply_crossfade(clip1, clip2, overlap_frames):
    if overlap_frames == 0:
        return concatenate_videoclips([clip1, clip2])
    overlap_duration = overlap_frames / clip1.fps
    return CompositeVideoClip([clip1, clip2.set_start(clip1.duration - overlap_duration).crossfadein(overlap_duration)])

def condense_video(input_video_path, output_dir, target_duration, output_fps=60, grain_size_frames=3, overlap_frames=0, random_factor=0, speed_factor=1):
    os.makedirs(output_dir, exist_ok=True)

    try:
        video = VideoFileClip(input_video_path)
        input_duration = video.duration
        print(f"Input video duration: {input_duration} seconds")
        print(f"Input video FPS: {video.fps}")

        scene_changes = detect_scenes(video)
        print(f"Detected {len(scene_changes)} scene changes")

        clips = select_clips(video, scene_changes, target_duration, grain_size_frames, overlap_frames, random_factor)
        print(f"Selected {len(clips)} clips")

        # Apply crossfades between clips
        if overlap_frames > 0:
            crossfaded_clips = [clips[0]]
            for i in range(1, len(clips)):
                crossfaded_clip = apply_crossfade(crossfaded_clips[-1], clips[i], overlap_frames)
                crossfaded_clips.append(crossfaded_clip)
            condensed_video = concatenate_videoclips(crossfaded_clips, method="compose")
        else:
            condensed_video = concatenate_videoclips(clips, method="compose")

        # Apply speed factor
        if speed_factor != 1:
            condensed_video = condensed_video.fx(vfx.speedx, speed_factor)

        # Ensure the final duration matches the target duration
        if condensed_video.duration != target_duration:
            condensed_video = condensed_video.set_duration(target_duration)

        # Set the output FPS
        if output_fps != video.fps:
            condensed_video = condensed_video.set_fps(output_fps)

        output_video_filename = f"condensed_video_{int(time.time())}.mp4"
        output_video_file_path = os.path.join(output_dir, output_video_filename)

        condensed_video.write_videofile(output_video_file_path, codec='libx264', fps=output_fps, preset='slow', bitrate='12000k')
        
        print(f"Video condensed and saved to {output_video_file_path}")
        print(f"Output video duration: {condensed_video.duration} seconds")
        print(f"Output video FPS: {condensed_video.fps}")
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    
    finally:
        if 'video' in locals():
            video.close()
        if 'condensed_video' in locals():
            condensed_video.close()

# User inputs
input_video_path = "/Users/agi/Desktop/EDIT_Hydra.mp4"
output_dir = "/Users/agi/Desktop/EDIT_Hydra_output"
target_duration = 8  # Target duration of the condensed video in seconds
output_fps = 30  # Frames per second for the output video
grain_size_frames = 3  # Size of each grain in frames
overlap_frames = 0  # Overlap between grains in frames
random_factor = 25  # Percentage of randomness to apply to frame selection (0-100), 0 for no randomness
speed_factor = 1  # Speed factor to apply to the final video (e.g., 2 for 2x speed), 1 for normal speed

condense_video(input_video_path, output_dir, target_duration, output_fps, grain_size_frames, overlap_frames, random_factor, speed_factor)