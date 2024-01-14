# pip install pydub in terminal

import os
from pydub import AudioSegment

# we'll assume you know the BPM and it's 120
bpm = 30

# calculate the length of a bar (4 beats) in milliseconds
bar_length = (4 * 60 / bpm) * 1000

# the fade duration in milliseconds
fade_duration = 25  # 50ms, adjust as needed

# directory where you have your wav files
dir_path = r"D:\Dropbox\_MAKE\Tidalcycles\_Samples\tidalclub\harp_harm_s"
# replace this with your actual path

# list all files in the directory
files = os.listdir(dir_path)

# process each file
for filename in files:
    # only process .wav files
    if filename.endswith(".wav"):
        # full path to the file
        file_path = os.path.join(dir_path, filename)

        # load the song
        song = AudioSegment.from_file(file_path)

        # extract filename without extension
        filename_no_ext = filename.split(".")[0]

        # number of bars in the song
        num_bars = int(len(song) / bar_length) + 1  # Added 1 to include the final bar

        # chop up the song, add fade in and out, and export each bar
        for i in range(1, num_bars + 1):
            start_time = (i - 1) * bar_length
            end_time = start_time + bar_length
            bar = song[start_time:end_time]

            # add fade in and out
            bar = bar.fade_in(fade_duration).fade_out(fade_duration)

            # determine which folder this bar should go in
            if i <= 12:
                folder = os.path.join(dir_path, f"{filename_no_ext}_1")
            else:
                folder = os.path.join(dir_path, f"{filename_no_ext}_2")

            # create the folder if it doesn't exist
            if not os.path.exists(folder):
                os.makedirs(folder)

            # save the bar to the appropriate folder
            output_filename = f"{filename_no_ext}_{str(i).zfill(2)}.wav"
            output_path = os.path.join(folder, output_filename)

            print("Saving to:", output_path)
            bar.export(output_path, format="wav")
