from mido import MidiFile
import music21 as m21  # Requires music21 library

def midi_to_chord_name(notes):
    # Create a music21 chord object from MIDI notes
    chord = m21.chord.Chord(notes)
    # Analyze the chord to get intervals
    intervals = chord.closedPosition().semiClosedPosition().normalOrderString
    # Mapping to TidalCycles chord names (this will need to be extended based on requirements)
    chord_mapping = {
        # Add mappings here based on intervals
        # Example: '024' : 'maj', '036' : 'min'
    }
    return chord_mapping.get(intervals, "unknown")

def extract_chords(midi_file_path):
    midi_file = MidiFile(midi_file_path)
    chords = []
    current_chord = []
    last_time = 0

    for track in midi_file.tracks:
        for msg in track:
            if not msg.is_meta and msg.type in ['note_on', 'note_off']:
                if msg.time != last_time and current_chord:
                    chords.append(current_chord)
                    current_chord = []
                last_time = msg.time

                if msg.type == 'note_on' and msg.velocity > 0:
                    current_chord.append(msg.note)

    if current_chord:
        chords.append(current_chord)

    return chords

def convert_to_tidal(chords):
    formatted_chords = []
    for chord in chords:
        chord_name = midi_to_chord_name(chord)
        formatted_chords.append(chord_name)
    return ' '.join(formatted_chords)

# Usage
midi_file_path = '/Users/ekeko/Library/CloudStorage/Dropbox/MIDI/Chordify_Hermanos-Gutierrez-Tres-Hermanos_Time_Aligned_94_BPM.mid'
output_file_path = '/Users/ekeko/Desktop/output_chords_6.tidal'

chords = extract_chords(midi_file_path)
tidal_chords = convert_to_tidal(chords)

# Write to .tidal file
with open(output_file_path, 'w') as file:
    file.write(f"d1 $ n \"{tidal_chords}\" # s \"superpiano\"\n")

print(f"Chords written to {output_file_path}")
