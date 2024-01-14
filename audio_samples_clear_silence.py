import os
import librosa
import soundfile as sf
import numpy as np


def process_audio_files(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".wav"):  # Assuming the files are .wav format
            file_path = os.path.join(folder_path, filename)
            audio, sr = librosa.load(file_path, sr=None)

            # Remove silence
            non_silent_parts = librosa.effects.split(
                audio, top_db=30
            )  # top_db might need adjustment
            audio_processed = [audio[start:end] for start, end in non_silent_parts]
            audio_processed = np.concatenate(audio_processed)

            # Apply fade in and fade out
            fade_in_length = int(sr * 0.01)  # 0.01 seconds fade-in
            fade_out_length = int(sr * 0.01)  # 0.01 seconds fade-out
            audio_processed[:fade_in_length] *= np.linspace(0, 1, fade_in_length)
            audio_processed[-fade_out_length:] *= np.linspace(1, 0, fade_out_length)

            # Save the processed file
            processed_file_path = os.path.join(folder_path, "processed", filename)
            os.makedirs(os.path.dirname(processed_file_path), exist_ok=True)
            sf.write(processed_file_path, audio_processed, sr)


# Usage
process_audio_files("D:/Dropbox/_MAKE/Tidalcycles/_Samples/tidalclub/harp_harm_c")
