#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pretty_midi, glob, re
from pathlib import Path
from scipy.io import wavfile

OUTPUT_FILE_EXT = ".wav"
CURRENT_DIR = str(Path(__file__).resolve().parent)
OUTPUT_DIR = str(Path(__file__).resolve().parent) + "/output"


def create_music(path):
    new_music = pretty_midi.PrettyMIDI()
    cello_program = pretty_midi.instrument_name_to_program("Cello")
    cello = pretty_midi.Instrument(program=cello_program)

    time = 0.0

    for note_name in ["C5", "D5", "E5", "F5", "G5", "A5", "B5", "C6"]:
        note_number = pretty_midi.note_name_to_number(note_name)
        note = pretty_midi.Note(
            velocity=100, pitch=note_number, start=time, end=(time + 0.5)
        )
        cello.notes.append(note)
        time = time + 0.5
    new_music.instruments.append(cello)

    input_filename = Path(path).stem
    files = [
        Path(file).stem
        for file in glob.glob(OUTPUT_DIR + "/" + input_filename + "*" + OUTPUT_FILE_EXT)
    ]
    numbering_file_list = [i for i in files if re.search(r"\(\d\)+", i)]

    audio_data = new_music.fluidsynth(
        sf2_path=CURRENT_DIR + "/sf/GeneralUser GS v1.471.sf2"
    )
    if len(files) == 0:

        output_filename = OUTPUT_DIR + "/" + input_filename + OUTPUT_FILE_EXT
        wavfile.write(output_filename, 44100, audio_data)

    else:
        number_list = [
            int(re.search(r"\d+", re.search(r"\(\d\)+", i).group()).group())
            for i in numbering_file_list
        ]
        max_num = 0
        if len(number_list) != 0:
            max_num = max(number_list)

        output_filename = (
            OUTPUT_DIR
            + "/"
            + input_filename
            + "("
            + str(max_num + 1)
            + ")"
            + OUTPUT_FILE_EXT
        )

        wavfile.write(output_filename, 44100, audio_data)


create_music(
    "/Users/sasakimanami/Documents/Github/movie2music/backend/sampleFiles/sample3.mov"
)
