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
tempu=180
mf.addTempo(track, time, tempu)

channel = 0
volume = 100
k=0

offset = [
    5,
    15,
    10,
    20
]
scade = -20

for i in range(0,4):
    if i%4==0:
        for x in range (0, 4):
            pitch = 65 + offset[x]
            time = (i*4 + x)       
            duration = 2 
            mf.addNote(track, channel, pitch, time, duration, 100)   
    elif i%4==1:
        for x in range (0, 4):
            pitch = 36 + offset[x]
            time = (i*4 + x)
            duration = 2
            mf.addNote(track, channel, pitch, time, duration, 100)  
    if i%4==2:
        for x in range (0, 4):
            pitch = 48 + offset[x]
            time = (i*4 + x)
            duration = 2
            mf.addNote(track, channel, pitch, time, duration, 100)   
    elif i%4==3:
        for x in range (0, 4):
            pitch = 41 + offset[x]
            time = (i*4 + x)         
            duration = 4 
            mf.addNote(track, channel, pitch, time, duration, 100)
       

# for i in range(0,2000):
#     if i%2==0:
#         pitch = 30         
#         time = i             
#         duration = 20       
#         mf.addNote(track, channel, pitch, time, duration, 100)
#         for j in range(1,21):
#             if j%2==0:
#                 pitch = 50         
#                 time = i+j             
#                 duration = 1      
#                 mf.addNote(track, channel, pitch, time, duration, 50)
#             else:
#                 pitch = 60         
#                 time = i+j             
#                 duration = 1      
#                 mf.addNote(track, channel, pitch, time, duration, 50)
#     else:
#         pitch = 40         
#         time = i             
#         duration = 20       
#         mf.addNote(track, channel, pitch, time, duration, 100)
#         for j in range(1,21):
#             if j%2==0:
#                 pitch = 50         
#                 time = i+j             
#                 duration = 1      
#                 mf.addNote(track, channel, pitch, time, duration, 50)
#             else:
#                 pitch = 60         
#                 time = i+j             
#                 duration = 1      
#                 mf.addNote(track, channel, pitch, time, duration, 50)


"""
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
            volume+=1"""
        



# write it to disk
with open("output.mid", 'wb') as outf:
    mf.writeFile(outf)

midis=[]
midis.append(midi_file(path='output.mid',soundfont='Piano_Paradise.sf2'))
make_wav(midis,'out.wav')
change_vol('out.wav','out.wav',20)

def image2AddNote(frame:cv2.numpy.ndarray,midis:list):
    back_tempo=alpha*sat
    for i in range(0,len(frame)):
        for j in range(0,len(frame[0])):
            return


def video2wav(video_path:str,out_path:str):
    midis=[]

    cam = cv2.VideoCapture(video_path)
    
    
    #check fps
    #video_fps=cam.get(cv2.CAP_PROP_FPS)
    #print(video_fps)
    
    flag, frame = cam.read()
    while flag:
        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        image2AddNote()
        flag, image = cam.read()

    make_wav(midis,out_path)

video2wav("MVI_2939.MP4","orionnebula.wav")




    


