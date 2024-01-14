from mido import MidiFile


def note_number_to_name(note_number):
    # Using 's' for sharps to align with TidalCycles notation
    notes = ["c", "cs", "d", "ds", "e", "f", "fs", "g", "gs", "a", "as", "b"]
    octave = (note_number // 12) - 1
    return f"{notes[note_number % 12]}'{octave}"


def extract_chords(midi_file_path):
    midi_file = MidiFile(midi_file_path)
    chords = []
    current_chord = []
    last_time = 0

    for track in midi_file.tracks:
        for msg in track:
            if not msg.is_meta and msg.type in ["note_on", "note_off"]:
                if msg.time != last_time and current_chord:
                    chords.append(current_chord)
                    current_chord = []
                last_time = msg.time

                if msg.type == "note_on" and msg.velocity > 0:
                    current_chord.append(msg.note)

    if current_chord:
        chords.append(current_chord)

    return chords


def convert_to_tidal(chords):
    formatted_chords = " ".join(
        f"[{' '.join(note_number_to_name(note) for note in chord)}]" for chord in chords
    )
    return formatted_chords


# Usage
midi_file_path = r"D:\Dropbox\MIDI\Chordify_Alberto-Balsalm_Quantized_at_94_BPM.mid"
output_file_path = "D:\Dropbox\MIDI\Alberto.tidal"

chords = extract_chords(midi_file_path)
tidal_chords = convert_to_tidal(chords)

# Write to .tidal file
with open(output_file_path, "w") as file:
    file.write(f'd1 $ n "{tidal_chords}" # s "superpiano"\n')

print(f"Chords written to {output_file_path}")
