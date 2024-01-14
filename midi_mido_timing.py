from mido import MidiFile

def extract_notes_and_timing(midi_file_path):
    mid = MidiFile(midi_file_path)

    # Data structure to store note information: [(note, start_time, duration), ...]
    notes_info = []

    # Iterate through all tracks in the MIDI file
    for track in mid.tracks:
        current_time = 0  # Track the current time in the MIDI file
        note_start_times = {}  # Dictionary to track when notes start

        for msg in track:
            current_time += msg.time  # Update the current time

            if msg.type == 'note_on' and msg.velocity > 0:
                # Record the start time of the note
                note_start_times[msg.note] = current_time
            elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                # Note end: calculate the duration and store the note info
                start_time = note_start_times.pop(msg.note, None)
                if start_time is not None:  # If the note start time was recorded
                    duration = current_time - start_time
                    notes_info.append((msg.note, start_time, duration))

    return notes_info

# Replace with your MIDI file path
midi_file_path = r"D:\Dropbox\MIDI\Chordify_Alberto-Balsalm_Quantized_at_94_BPM.mid"

# Extract notes and timing
notes_and_timing = extract_notes_and_timing(midi_file_path)
print(notes_and_timing[:10])  # Print first 10 notes for brevity
