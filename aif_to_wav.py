import os
from pydub import AudioSegment

bpm = 30
bar_length = (4 * 60 / bpm) * 1000
fade_duration = 25

dir_path = "/Users/agi/Desktop/samples"
files = os.listdir(dir_path)

print("Files in directory:", files)  # Debugging line

for filename in files:
    if filename.endswith((".wav", ".aif")):  # Check for both .wav and .aif files
        file_path = os.path.join(dir_path, filename)
        print("Processing file:", filename)  # Debugging line

        song = AudioSegment.from_file(file_path, filename[-3:])

        filename_no_ext = os.path.splitext(filename)[0]
        num_bars = int(len(song) / bar_length) + 1

        for i in range(1, num_bars + 1):
            start_time = (i - 1) * bar_length
            end_time = start_time + bar_length
            bar = song[start_time:end_time]

            bar = bar.fade_in(fade_duration).fade_out(fade_duration)

            folder = os.path.join(dir_path, f"{filename_no_ext}_{'1' if i <= 12 else '2'}")
            if not os.path.exists(folder):
                os.makedirs(folder)

            output_filename = f"{filename_no_ext}_{str(i).zfill(2)}.wav"
            output_path = os.path.join(folder, output_filename)

            print("Saving to:", output_path)  # Debugging line
            bar.export(output_path, format="wav")
