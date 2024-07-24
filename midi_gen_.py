import pretty_midi

def create_structured_chord_midi(chord_sections, tempo_bpm, file_path):
    # Create a PrettyMIDI object
    midi = pretty_midi.PrettyMIDI()
    
    # Create an Instrument instance for a piano instrument
    piano_program = pretty_midi.instrument_name_to_program('Acoustic Grand Piano')
    piano = pretty_midi.Instrument(program=piano_program)
    
    # Define start time and chord duration
    start_time = 0
    chord_duration = 1.0  # 1 bar per chord
    
    for section in chord_sections:
        for chord in section:
            # Create a chord note for each note in the chord
            notes = []
            for note_name in chord:
                note_number = pretty_midi.note_name_to_number(note_name)
                note = pretty_midi.Note(velocity=100, pitch=note_number, start=start_time, end=start_time + chord_duration)
                notes.append(note)
            
            # Add the notes to the piano instrument
            piano.notes.extend(notes)
            
            # Increment the start time for the next chord
            start_time += chord_duration
    
    # Add the piano instrument to the PrettyMIDI object
    midi.instruments.append(piano)
    
    # Write out the MIDI data
    midi.write(file_path)

# Define the chord sections for the song
chord_sections = [
    # Intro (8 bars)
    [['D#4', 'G#4', 'A#4', 'C#5'], ['G#3', 'B3', 'D#4', 'F#4', 'A#4'], ['C#4', 'E#4', 'G#4', 'B4'], ['F#3', 'A#3', 'C#4', 'E#4']] * 2,
    # Verse 1 (8 bars)
    [['D#3', 'F#3', 'A#3', 'C4'], ['G#3', 'B3', 'D#4', 'F4'], ['A#3', 'C#4', 'E4', 'G#4'], ['C#4', 'E#4', 'G#4', 'B4']] * 2,
    # Pre-Chorus (4 bars)
    [['B3', 'D#4', 'F#4', 'A#4'], ['C#4', 'E#4', 'G#4', 'B4'], ['F#3', 'A3', 'C#4', 'E4'], ['G#3', 'B3', 'D#4', 'F#4']],
    # Chorus (8 bars)
    [['D#4', 'G#4', 'A#4', 'C#5'], ['G#3', 'B3', 'D#4', 'F#4', 'A#4'], ['A#3', 'C#4', 'E#4', 'G#4'], ['C#4', 'E#4', 'G#4', 'B4']] * 2,
    # Verse 2 (8 bars)
    [['D#3', 'F#3', 'A#3', 'C4'], ['G#3', 'B3', 'D#4', 'F4'], ['A#3', 'C#4', 'E4', 'G#4'], ['C#4', 'E#4', 'G#4', 'B4']] * 2,
    # Pre-Chorus (4 bars)
    [['B3', 'D#4', 'F#4', 'A#4'], ['C#4', 'E#4', 'G#4', 'B4'], ['F#3', 'A3', 'C#4', 'E4'], ['G#3', 'B3', 'D#4', 'F#4']],
    # Chorus (8 bars)
    [['D#4', 'G#4', 'A#4', 'C#5'], ['G#3', 'B3', 'D#4', 'F#4', 'A#4'], ['A#3', 'C#4', 'E#4', 'G#4'], ['C#4', 'E#4', 'G#4', 'B4']] * 2,
    # Bridge (8 bars)
    [['G#3', 'B3', 'D#4', 'F#4'], ['C#4', 'E#4', 'G#4', 'B4'], ['F#3', 'A#3', 'C#4', 'E#4'], ['B3', 'D#4', 'F#4', 'A#4']] * 2,
    # Final Chorus (8 bars)
    [['D#4', 'G#4', 'A#4', 'C#5'], ['G#3', 'B3', 'D#4', 'F#4', 'A#4'], ['A#3', 'C#4', 'E#4', 'G#4'], ['C#4', 'E#4', 'G#4', 'B4']] * 2,
    # Outro (4 bars)
    [['D#3', 'F#3', 'A#3', 'C4'], ['G#3', 'B3', 'D#4', 'F#4'], ['C#4', 'E#4', 'G#4', 'B4'], ['F#3', 'A#3', 'C#4', 'E#4']]
]

# File path for the MIDI file
file_path_long = '/Users/agi/Desktop/midi/midi_03.mid'

# Create the MIDI file
create_structured_chord_midi(chord_sections, 96.5, file_path_structured)
