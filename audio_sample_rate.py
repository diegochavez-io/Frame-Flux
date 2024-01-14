from pydub import AudioSegment
import os


def convert_audio_properties(
    folder_path, target_bitrate="320k", target_sample_rate=44100
):
    for filename in os.listdir(folder_path):
        if filename.endswith(
            ".wav"
        ):  # Change the extension if your files are in a different format
            file_path = os.path.join(folder_path, filename)

            # Load the audio file
            audio = AudioSegment.from_file(file_path)

            # Change the sample rate
            audio = audio.set_frame_rate(target_sample_rate)

            # Define the new file's name
            new_filename = f"{os.path.splitext(filename)[0]}_converted.wav"
            new_file_path = os.path.join(folder_path, "converted", new_filename)

            # Create the 'converted' folder if it doesn't exist
            os.makedirs(os.path.dirname(new_file_path), exist_ok=True)

            # Export the file with the new bitrate and sample rate
            audio.export(new_file_path, format="wav", bitrate=target_bitrate)


# Usage
convert_audio_properties(
    "D:/Dropbox/_MAKE/Tidalcycles/_Samples/tidalclub/harp_harm_c/processed"
)
