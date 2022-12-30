#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pretty_midi, glob, re
from pathlib import Path
from scipy.io import wavfile
from mockData import imgFeatures
from numpy.random import randint


def defineInstrument(instrument_name):
    INSTRUMENT = pretty_midi.instrument_name_to_program(instrument_name)
    inst = pretty_midi.Instrument(program=INSTRUMENT)
    return inst


def bassAppend(bass, note_num, bass_time):
    BASE_NOTE_LIST = ["C3", "D3", "E3", "F3", "G3", "A3", "B3", "C3"]
    bass_note_num = note_num if note_num < 2 else 2

    note_name = BASE_NOTE_LIST[bass_note_num]
    note_number = pretty_midi.note_name_to_number(note_name)
    bass.notes.append(
        pretty_midi.Note(
            velocity=75, pitch=note_number, start=bass_time, end=(bass_time + 1)
        )
    )
    note_name = BASE_NOTE_LIST[bass_note_num + 2]
    note_number = pretty_midi.note_name_to_number(note_name)
    bass.notes.append(
        pretty_midi.Note(
            velocity=75, pitch=note_number, start=bass_time, end=(bass_time + 1)
        )
    )
    note_name = BASE_NOTE_LIST[bass_note_num + 4]
    note_number = pretty_midi.note_name_to_number(note_name)
    bass.notes.append(
        pretty_midi.Note(
            velocity=75, pitch=note_number, start=bass_time, end=(bass_time + 1)
        )
    )


def create_music(path, movdata):
    OUTPUT_FILE_EXT = ".wav"
    CURRENT_DIR = str(Path(__file__).resolve().parent)
    OUTPUT_DIR = str(Path(__file__).resolve().parent) + "/output"
    SF_DATA = CURRENT_DIR + "/sf/GeneralUser GS v1.471.sf2"
    new_music = pretty_midi.PrettyMIDI()
    piano = defineInstrument("Acoustic Grand Piano")
    bass = defineInstrument("Electric Bass (pick)")
    NOTE_lIST = [
        "C5",
        "D5",
        "E5",
        "F5",
        "G5",
        "A5",
        "B5",
        "C6",
        "D6",
        "E6",
        "F6",
        "G6",
        "A6",
        "B6",
        "C7",
    ]

    time = 0.0
    bass_time = 0.0

    # 画像のframeが4秒4分割なので、2で0.5秒ずつ、1で0.25秒ずつでテンポ調整できる。
    # ３拍子は一旦諦める…。
    note_num = 0
    repeat_flg = False
    current_frame = 0
    # for i in list(range(0, len(movdata["vectors"]), 1)):
    while current_frame < len(movdata["vectors"]):
        if movdata["vectors"][current_frame] < 1000:
            speed = 1.0
        elif movdata["vectors"][current_frame] < 10000:
            speed = 0.5
        else:
            speed = 0.25

        upJudge = movdata["upFlg"][current_frame]
        if note_num == 0 and upJudge == -1:
            note_num = randint(len(NOTE_lIST) - 1)
        elif upJudge == 0:
            if not repeat_flg:
                note_num = note_num + upJudge * 2
                repeat_flg = True
            else:
                note_num = note_num + randint(-3, 3)
                repeat_flg = False
        else:
            note_num = note_num + upJudge * 2

        if note_num < 0:
            note_num = note_num + randint(2, len(NOTE_lIST) - note_num - 2)
        elif note_num >= len(NOTE_lIST):
            note_num = note_num - randint(
                len(NOTE_lIST) - (note_num / 2), len(NOTE_lIST)
            )
        note_name = NOTE_lIST[note_num]
        note_number = pretty_midi.note_name_to_number(note_name)
        piano.notes.append(
            pretty_midi.Note(
                velocity=100, pitch=note_number, start=time, end=(time + speed)
            )
        )

        if current_frame % 4 == 0:
            bassAppend(bass, note_num, bass_time)
            bass_time = bass_time + 1

        time = time + speed

        if movdata["vectors"][current_frame] < 1000:
            current_frame = current_frame + 4
        elif movdata["vectors"][current_frame] < 10000:
            current_frame = current_frame + 2
        else:
            current_frame = current_frame + 1

    new_music.instruments.append(piano)
    new_music.instruments.append(bass)

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
        numbering_file_list = [i for i in files if re.search(r"\(\d*\)+", i)]
        number_list = [
            int(re.search(r"\d+", re.search(r"\(\d*\)+", i).group()).group())
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
