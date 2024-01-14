# Script Parameters
FILE_PATH = (
    r"C:\Users\diego\Desktop\DUB_TECHNO_Selection _121.mp3"  # Path to the audio file
)
NUM_SAMPLES = 35  # Desired number of samples
SHORT_SAMPLE_LENGTH = 150  # Maximum length of each short sample in milliseconds
LONG_SAMPLE_LENGTH = 500  # Maximum length of each long sample in milliseconds

import os
import random
from pydub import AudioSegment
from pydub.utils import make_chunks
from pydub.effects import normalize


def process_audio_randomly(file_path, num_samples, max_sample_length, output_suffix):
    try:
        # Load the audio file
        audio = AudioSegment.from_file(file_path)

        # Calculate the total number of possible chunks
        total_chunks = len(audio) // max_sample_length

        # Select random start points for chunks
        start_points = sorted(random.sample(range(total_chunks), num_samples))

        # Directory for processed samples
        base_name = os.path.basename(file_path)
        sample_name = os.path.splitext(base_name)[0]
        output_dir = os.path.join(
            os.path.dirname(file_path), sample_name + output_suffix
        )
        os.makedirs(output_dir, exist_ok=True)

        # Process and save each chunk
        for i, start in enumerate(start_points):
            # Extract the chunk
            start_ms = start * max_sample_length
            chunk = audio[start_ms : start_ms + max_sample_length]

            # Normalize, apply quick fade in and fade out to avoid pops
            processed_chunk = normalize(chunk.fade_in(10).fade_out(10))

            # Save the chunk
            output_file = os.path.join(output_dir, f"{sample_name}_sample_{i+1}.wav")
            processed_chunk.export(output_file, format="wav")

        print(f"Processed samples saved in: {output_dir}")

    except Exception as e:
        print(f"An error occurred: {e}")


# Running the script for two different sample lengths with randomness
process_audio_randomly(
    FILE_PATH, NUM_SAMPLES, SHORT_SAMPLE_LENGTH, "_1_random_processed"
)  # Shorter samples
process_audio_randomly(
    FILE_PATH, NUM_SAMPLES, LONG_SAMPLE_LENGTH, "_2_random_processed"
)  # Longer samples
