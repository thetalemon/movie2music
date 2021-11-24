#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pretty_midi, os, glob, re
from pathlib import Path

output_file_ext = ".mid"


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

    filename = Path(path).stem
    files = [
        Path(file).stem
        for file in glob.glob(
            os.path.dirname(__file__) + "/output/" + filename + "*" + output_file_ext
        )
    ]
    numbering_file_list = [i for i in files if re.search(r"(\d)+", i)]

    print(files)

    print(os.path.dirname(__file__) + "/output/" + filename + ".mid")

    if len(files) == 0:
        new_music.write(os.path.dirname(__file__) + "/output/" + filename + ".mid")
    else:
        number_list = [int(re.search(r"\d+", i).group()) for i in numbering_file_list]
        print(len(number_list))
        print(number_list)
        max_num = 0
        if len(number_list) != 0:
            max_num = max(number_list)

        new_music.write(
            os.path.dirname(__file__)
            + "/output/"
            + filename
            + "("
            + str(max_num + 1)
            + ").mid"
        )
