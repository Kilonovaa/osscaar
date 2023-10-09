from midi_creator_2 import *
import os


def shorthandGetMidisFromVideo(fileName: str):
    getMidisFromVideo("../video-stash/" + fileName + ".mp4", "../video-stash/" + fileName, emptyCallback)

shorthandGetMidisFromVideo("Animation of Comet 2I_Borisov")
shorthandGetMidisFromVideo("Cosmic Reef_ NGC 2014 & NGC 2020")
shorthandGetMidisFromVideo("Flight Through the Orion Nebula in Infrared Light")
