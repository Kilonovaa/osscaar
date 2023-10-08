import time
import midi_creator_2
from piano_convert import midi_file, make_wav
import cv2


def processAudio(user_id, video_data, callback):
    callable(0)

    def processingCallback(status: float):
        print("Loading:  " + str(status * 100.0) + " %")

    with open("orionnebula.mp4", 'wb') as outf:
        outf.write(video_data)

    midiFiles = midi_creator_2.getMidisFromVideo(cv2.VideoCapture(
        "orionnebula.mp4"), 0.2, callback)

    midiPaths = []

    for i in range(len(midiFiles)):
        midiPaths.append(midi_file("custom_mid_" + str(i) +
                         ".mid", "Piano_Paradise.sf2"))
        with open("custom_mid_" + str(i) + ".mid", 'wb') as outf:
            midiFiles[i].writeFile(outf)

    make_wav(midiPaths, "funnyout.wav")

    audio_data = open("funnyout.wav", "rb").read()

    return audio_data
