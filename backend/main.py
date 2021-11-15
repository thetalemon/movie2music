import pretty_midi
cello_c_chord = pretty_midi.PrettyMIDI()
cello_program = pretty_midi.instrument_name_to_program('Cello')
cello = pretty_midi.Instrument(program=cello_program)

time = 0.0

for note_name in ['C5', 'D5', 'E5', 'F5', 'G5', 'A5', 'B5', 'C6']:
    note_number = pretty_midi.note_name_to_number(note_name)
    note = pretty_midi.Note(
        velocity=100, pitch=note_number, start=time, end=(time + .5))
    cello.notes.append(note)
    time = time + .5
cello_c_chord.instruments.append(cello)
cello_c_chord.write('sample.mid')