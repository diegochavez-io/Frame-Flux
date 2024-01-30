import music21

# Function to create a MusicXML file for a metronome mark at 150 BPM
def create_musicxml_for_metronome(bpm):
    # Create a Score and a Part
    score = music21.stream.Score()
    part = music21.stream.Part()
    score.append(part)

    # Create a MetronomeMark at 150 BPM and add it to the part
    metronome_mark = music21.tempo.MetronomeMark(number=bpm)
    part.append(metronome_mark)

    # Create a measure and add it to the part
    measure = music21.stream.Measure()
    part.append(measure)

    # Export the score to a MusicXML file
    score.write('musicxml', 'metronome_musicxml.xml')

# Create a MusicXML file for a metronome mark at 150 BPM
create_musicxml_for_metronome(150)
