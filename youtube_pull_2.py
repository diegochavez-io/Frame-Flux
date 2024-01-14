import os
from pytube import YouTube

url = 'https://www.youtube.com/watch?v=yKYgCD3m9AU'
output_folder = r'C:\Users\diego\Desktop\music_rip'

# Ensure output folder exists
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

print(f"Starting download of {url}...")

youtube = YouTube(url)

video = youtube.streams.filter(file_extension='mp4', only_video=True).order_by('resolution').desc().first()

if video is not None:
    print(f"Video title: {video.title}")

    output_path = video.download(output_folder)

    print(f"Downloaded video to: {output_path}")
else:
    print("No matching video stream found.")
