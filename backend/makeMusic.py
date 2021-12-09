#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pretty_midi, glob, re
from pathlib import Path
from scipy.io import wavfile
from mockData import imgFeatures


def create_music(path, movdata):
    OUTPUT_FILE_EXT = ".wav"
    CURRENT_DIR = str(Path(__file__).resolve().parent)
    OUTPUT_DIR = str(Path(__file__).resolve().parent) + "/output"
    SF_DATA = CURRENT_DIR + "/sf/GeneralUser GS v1.471.sf2"
    CELLO_PROGRAM = pretty_midi.instrument_name_to_program("Cello")
    new_music = pretty_midi.PrettyMIDI()
    cello = pretty_midi.Instrument(program=CELLO_PROGRAM)
    time = 0.0
    NOTE_lIST = ["C5", "D5", "E5", "F5", "G5", "A5", "B5", "C6"]

    # 画像のframeが4秒4分割なので、2で0.5秒ずつ、1で0.25秒ずつでテンポ調整できる。
    # ３拍子は一旦諦める…。
    noteNum = 0
    for i in list(range(0, len(movdata["vectors"]), 2)):
        upJudge = 1 if movdata["upFlg"][i] and movdata["upFlg"][i][0] else -1
        noteNum = noteNum + upJudge
        if noteNum < 0:
            noteNum = 2
        elif noteNum > 7:
            noteNum = 5

        note_name = NOTE_lIST[noteNum]
        note_number = pretty_midi.note_name_to_number(note_name)
        note = pretty_midi.Note(
            velocity=100, pitch=note_number, start=time, end=(time + 0.5)
        )
        cello.notes.append(note)
        time = time + 0.5
    new_music.instruments.append(cello)

    INPUT_FILE_NAME = Path(path).stem
    files = [
        Path(file).stem
        for file in glob.glob(
            OUTPUT_DIR + "/" + INPUT_FILE_NAME + "*" + OUTPUT_FILE_EXT
        )
    ]

    audio_data = new_music.fluidsynth(sf2_path=SF_DATA)

    if len(files) == 0:
        output_filename = OUTPUT_DIR + "/" + INPUT_FILE_NAME + OUTPUT_FILE_EXT
        wavfile.write(output_filename, 44100, audio_data)
    else:
        numbering_file_list = [i for i in files if re.search(r"\(\d\)+", i)]
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
            + INPUT_FILE_NAME
            + "("
            + str(max_num + 1)
            + ")"
            + OUTPUT_FILE_EXT
        )

        wavfile.write(output_filename, 44100, audio_data)


create_music("./sampleFiles/sample3.mov", imgFeatures)
