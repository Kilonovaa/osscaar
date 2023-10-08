#create midi files for video#
#############################
import cv2
from piano_convert import *
from midiutil.MidiFile import MIDIFile
import random


#image to hsv matrix
frame = cv2.imread('blackandwhite.png')
frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)






# create your MIDI object
mf = MIDIFile(1)     # only 1 track
track = 0   # the only track
time = 0    # start at the beginning
mf.addTrackName(track, time, "Sample Track")
mf.addTempo(track, time, 120)
mf.addTempo(track, time,2000)


# add some notes
channel = 0
volume = 0
k=0
for i in range(0,int(len(frame_hsv)/10)):
    for j in range(0,len(frame_hsv[0])):
        if frame_hsv[i][j][2]==0:
            pitch = 0+random.randrange(0,120)           
            time = k             
            duration = 50       
            mf.addNote(track, channel, pitch, time, duration, volume)
            
        elif frame_hsv[i][j][2]>0:
            pitch = 50+(j%20)*3+random.randrange(0,3)           
            time = k             
            duration = 1         
            mf.addNote(track, channel, pitch, time, duration, volume)
        mf.addControllerEvent(track,channel,k,7,volume)
        k+=1
        if volume<100:
            volume+=1
        



# write it to disk
with open("output.mid", 'wb') as outf:
    mf.writeFile(outf)

midis=[]
midis.append(midi_file(path='output.mid',soundfont='Piano_Paradise.sf2'))
make_wav(midis,'out.wav')
change_vol('out.wav','out.wav',20)

def image2AddNote():
    return

def video2wav(video_path:str,out_path:str):
    cam = cv2.VideoCapture(video_path)
    flag, frame = cam.read()
    while flag:
        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        
        flag, image = cam.read()




    


