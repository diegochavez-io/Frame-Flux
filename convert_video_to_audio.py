from moviepy.editor import *

def convert_video_to_audio(video_path, audio_path):
    """
    Convert a video file to an audio file.

    Parameters:
    - video_path (str): Path to the input video file.
    - audio_path (str): Path to save the output audio file.
    """
    video = VideoFileClip(video_path)
    audio = video.audio

    # Check if the video has an audio track
    if audio:
        audio.write_audiofile(audio_path, codec='pcm_s16le')  # codec='pcm_s16le' ensures .wav format
        audio.close()
    else:
        print("The video does not have an audio track.")

    video.close()

if __name__ == "__main__":
    # Example usage:
    video_path = r"C:\Users\diego\Desktop\music_rip\Doomsday (Instrumental).mp4"
    audio_path = r"C:\Users\diego\Desktop\music_rip\Doomsday (Instrumental).wav"
    
    convert_video_to_audio(video_path, audio_path)
    print(f"Audio saved to {audio_path}")
