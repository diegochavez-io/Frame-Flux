from pydub import AudioSegment
import os

# Configuration
file_path = '/Users/agi/Dropbox/_AM/10. Touch Docs/Sights-&-Sound/Spring 24 STEMS/Hydra/hydra -  ALL VOX.wav' # Add your file extension, e.g., '.mp3'
output_dir = '/Users/agi/Desktop/hydra_vox'
bpm = 111
beats_per_slice = 4 # Change this to chop into different lengths (e.g., 0.5 for half-beat slices)
fade_duration = 1 # Milliseconds of fade in/out

# Calculate slice duration in milliseconds
bpm_to_milliseconds = 60000 / bpm
slice_duration_ms = bpm_to_milliseconds * beats_per_slice

# Load the song
song = AudioSegment.from_file(file_path)

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Chop and export slices
total_slices = len(song) // slice_duration_ms
for i in range(int(total_slices)):
    start = i * slice_duration_ms
    end = start + slice_duration_ms
    slice = song[start:end]
    
    # Apply a quick fade in and out to prevent pops
    slice = slice.fade_in(fade_duration).fade_out(fade_duration)
    
    # Export slice
    slice.export(f"{output_dir}/slice_{i}.wav", format="wav")

print(f"Exported {total_slices} slices to {output_dir}.")
