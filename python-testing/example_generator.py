from midi_creator_2 import *
import os

for file in os.listdir("../video-stash"):
    if file.lower().endswith(".mp4"):
        fileName = file[0:-4]
        print(fileName)
        getMidisFromVideo("../video-stash/" + fileName + ".mp4", "../video-stash/" + fileName, emptyCallback)
        
