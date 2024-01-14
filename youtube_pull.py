
#pip install yt-dlp

import yt_dlp
import os

def download_video(url, output_folder, quality='best', download_audio=True):
    ydl_opts = {
    'format': quality,
    'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),
    'restrictfilenames': True,
    'noplaylist' : True,
    'nocheckcertificate': True,
    'ignoreerrors': False,  # Change this to False
    'logtostderr': True,  # Change this to True
    'quiet': False,  # Change this to False
    'no_warnings': False,  # Change this to False
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}


    if not download_audio:
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }]

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

if __name__ == "__main__":
    url = 'https://www.youtube.com/watch?v=2e8tKBF_ACc'
    output_folder = './E:/Shamon Cassette/YouTube_Rip'
    quality = 'best'
    download_audio = False

    download_video(url, output_folder, quality, download_audio)
