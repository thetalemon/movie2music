import pretty_midi, os, glob, re

output_file_name = "/sample"
output_file_ext = ".mid"

def create_music():
  new_music = pretty_midi.PrettyMIDI()
  cello_program = pretty_midi.instrument_name_to_program('Cello')
  cello = pretty_midi.Instrument(program=cello_program)

  time = 0.0

  for note_name in ['C5', 'D5', 'E5', 'F5', 'G5', 'A5', 'B5', 'C6']:
    note_number = pretty_midi.note_name_to_number(note_name)
    note = pretty_midi.Note(
        velocity=100, pitch=note_number, start=time, end=(time + .5))
    cello.notes.append(note)
    time = time + .5
  new_music.instruments.append(cello)

  files = glob.glob(os.path.dirname(__file__) + '/' + output_file_name + '*' + output_file_ext)
  numbering_file_list = [i for i in files if re.search(r'\d+', i)]
  number_list = [int(re.search(r'\d+', i).group()) for i in numbering_file_list]

  max_num = max(number_list)

  if len(files) == 0:
    new_music.write(os.path.dirname(__file__) + '/sample.mid')
  else:
    new_music.write(os.path.dirname(__file__) + '/sample(' + str(max_num + 1) + ').mid')
