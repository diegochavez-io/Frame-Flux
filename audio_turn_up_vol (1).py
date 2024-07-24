from pydub import AudioSegment
import os


def amplify_volume(folder_path, volume_increase_dB=5.0):
    for filename in os.listdir(folder_path):
        if filename.endswith(
            ".wav"
        ):  # Change the extension if your files are in a different format
            file_path = os.path.join(folder_path, filename)

            # Load the audio file
            audio = AudioSegment.from_file(file_path)

            # Increase the volume
            louder_audio = audio + volume_increase_dB

            # Define the new file's name
            new_filename = f"{os.path.splitext(filename)[0]}_amplified.wav"
            new_file_path = os.path.join(folder_path, "amplified", new_filename)

            # Create the 'amplified' folder if it doesn't exist
            os.makedirs(os.path.dirname(new_file_path), exist_ok=True)

            # Export the file with the increased volume
            louder_audio.export(new_file_path, format="wav")


# Usage
amplify_volume("D:/Dropbox/_MAKE/Tidalcycles/_Samples/tidalclub/harp_harm_c/converted")
