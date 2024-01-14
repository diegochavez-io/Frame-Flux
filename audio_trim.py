from pydub import AudioSegment
import os

# User Input Parameters
folder_path = r"D:\Dropbox\_MAKE\Tidalcycles\_Samples\tidalclub\jog_bass"  # Folder containing the audio files
duration_in_seconds = 1.5  # Duration of the audio in seconds
fade_in_length = 10  # Fade in duration in milliseconds
fade_out_length = 300  # Fade out duration in milliseconds


def trim_and_fade_audio(
    folder_path, duration_in_seconds, fade_in_length, fade_out_length
):
    target_length = duration_in_seconds * 1000  # Convert seconds to milliseconds
    for filename in os.listdir(folder_path):
        if filename.endswith(".wav"):  # Adjust the extension for different file formats
            file_path = os.path.join(folder_path, filename)

            # Load the audio file
            audio = AudioSegment.from_file(file_path)

            # Trim the audio to the target length
            trimmed_audio = audio[:target_length]

            # Apply fade in and fade out
            faded_audio = trimmed_audio.fade_in(fade_in_length).fade_out(
                fade_out_length
            )

            # Define the new file's name
            new_filename = f"{os.path.splitext(filename)[0]}_trimmed_faded.wav"
            new_file_path = os.path.join(folder_path, "trimmed_faded", new_filename)

            # Create the 'trimmed_faded' folder if it doesn't exist
            os.makedirs(os.path.dirname(new_file_path), exist_ok=True)

            # Export the file with the fades
            faded_audio.export(new_file_path, format="wav")


# Usage
trim_and_fade_audio(folder_path, duration_in_seconds, fade_in_length, fade_out_length)
