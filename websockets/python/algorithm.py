import time
import midi_creator_2
from piano_convert import midi_file, make_wav
import cv2


def createDirIfNotExists(path):
    import os
    if not os.path.exists(path):
        os.makedirs(path)


def removeDirAndFilesInsideIfNotEmpty(path):
    import os
    if os.path.exists(path):
        for file in os.listdir(path):
            os.remove(path+"/"+file)
        os.removedirs(path)


def processAudio(user_id, video_data, callback):
    callable(0)

    createDirIfNotExists("./tmp/"+user_id+"/")

    with open("./tmp/"+user_id+"/"+"orionnebula.mp4", 'wb') as outf:
        outf.write(video_data)

    audio_file_name = midi_creator_2.getMidisFromVideo(
        "./tmp/"+user_id+"/"+"orionnebula.mp4", "./tmp/"+user_id+"/", callback)

    audio_data = open(audio_file_name, "rb").read()

    # cleanup
    removeDirAndFilesInsideIfNotEmpty("./tmp/"+user_id+"/")

    return audio_data
