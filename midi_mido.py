from mido import MidiFile

def extract_chords_and_timing(midi_file_path):
    mid = MidiFile(midi_file_path)

    # You'll need to process each track in the MIDI file
    for track in mid.tracks:
        # Initialize variables to store note start times, durations, etc.

        for msg in track:
            # Analyze note_on and note_off messages
            if msg.type == 'note_on':
                # Store the start time of the note
                pass
            elif msg.type == 'note_off':
                # Calculate the duration and end time of the note
                pass

            # Add logic to group notes into chords based on their start times
            # Add logic to analyze the rhythm based on start times and durations

    # Return the extracted chord and rhythm information
    return chords, rhythms

midi_file_path = r"D:\Dropbox\MIDI\Chordify_Alberto-Balsalm_Quantized_at_94_BPM.mid"
chords, rhythms = extract_chords_and_timing(midi_file_path)


