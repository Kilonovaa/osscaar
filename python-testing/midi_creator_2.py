# list of controllers: http://midi.teragonaudio.com/tech/midispec/ctllist.htm

# 0   Bank Select (coarse)
# 1   Modulation Wheel (coarse)
# 2   Breath controller (coarse)
# 4   Foot Pedal (coarse)
# 5   Portamento Time (coarse)
# 6   Data Entry (coarse)
# 7   Volume (coarse)
# 8   Balance (coarse)
# 10  Pan position (coarse)
# 11  Expression (coarse)
# 12  Effect Control 1 (coarse)
# 13  Effect Control 2 (coarse)
# 16  General Purpose Slider 1
# 17  General Purpose Slider 2
# 18  General Purpose Slider 3
# 19  General Purpose Slider 4
# 32  Bank Select (fine)
# 33  Modulation Wheel (fine)
# 34  Breath controller (fine)
# 36  Foot Pedal (fine)
# 37  Portamento Time (fine)
# 38  Data Entry (fine)
# 39  Volume (fine)
# 40  Balance (fine)
# 42  Pan position (fine)
# 43  Expression (fine)
# 44  Effect Control 1 (fine)
# 45  Effect Control 2 (fine)
# 64  Hold Pedal (on/off)
# 65  Portamento (on/off)
# 66  Sustenuto Pedal (on/off)
# 67  Soft Pedal (on/off)
# 68  Legato Pedal (on/off)
# 69  Hold 2 Pedal (on/off)
# 70  Sound Variation
# 71  Sound Timbre
# 72  Sound Release Time
# 73  Sound Attack Time
# 74  Sound Brightness
# 75  Sound Control 6
# 76  Sound Control 7
# 77  Sound Control 8
# 78  Sound Control 9
# 79  Sound Control 10
# 80  General Purpose Button 1 (on/off)
# 81  General Purpose Button 2 (on/off)
# 82  General Purpose Button 3 (on/off)
# 83  General Purpose Button 4 (on/off)
# 91  Effects Level
# 92  Tremulo Level
# 93  Chorus Level
# 94  Celeste Level
# 95  Phaser Level
# 96  Data Button increment
# 97  Data Button decrement
# 98  Non-registered Parameter (fine)
# 99  Non-registered Parameter (coarse)
# 100 Registered Parameter (fine)
# 101 Registered Parameter (coarse)
# 120 All Sound Off
# 121 All Controllers Off
# 122 Local Keyboard (on/off)
# 123 All Notes Off
# 124 Omni Mode Off
# 125 Omni Mode On
# 126 Mono Operation
# 127 Poly Operation

from midiutil.MidiFile import MIDIFile
import numpy as np
import cv2

def getChannelFromBalance(balance: int) -> int:
    return max( min( round(float(balance) / 127.0 * 15.0), 15 ), 0 )

def getBalanceFromChannel(channel: int) -> int:
    return max( min( round(float(channel) / 15.0 * 127.0), 127 ), 0 )

def addNoteAtIndex(midiFiles, timeBetweenNotes: float,
                   noteIndex: int, pitch: int, volume: int, balance: int) -> float:
    
    noteStart = noteIndex * timeBetweenNotes
    noteDuration = timeBetweenNotes * len(midiFiles)
    balanceChannel = getChannelFromBalance(balance)
    print(str(noteIndex % len(midiFiles)) + " " + str(noteStart) + " " + str(noteDuration))
    midiFiles[noteIndex % len(midiFiles)].addNote(track = balanceChannel, channel = balanceChannel, pitch=pitch, time=noteStart, duration=noteDuration, volume=volume)


def addNoteAtTime(midiFiles, timeBetweenNotes: float,
                   noteStart: float, pitch: int, volume: int, balance: int) -> float:
    
    addNoteAtIndex(midiFiles, timeBetweenNotes,
                   round(noteStart / timeBetweenNotes), pitch, volume, balance)


def postProcessing(midiFiles, midiLength: float, timeBetweenNotes: float,
                   tempo: int,
                   volumeZeroDuration: float,
                   volumeSlopeUpDuration: float,
                   volumeSlopeDownDuration: float,
                   volumeZero2Duration: float,
                   maxVolume: int = 127,
                   maxExpression: int = 127,
                   incVolumeResolution: float = 2.5,
                   decVolumeResolution: float = 3.5):
    
    volumeMaxDuration = timeBetweenNotes * len(midiFiles) - (volumeZeroDuration + volumeSlopeUpDuration + volumeSlopeDownDuration + volumeZero2Duration)
    assert(volumeMaxDuration >= 0.0)

    for i in range(1, len(midiFiles)):
        midiFiles[i].addNote(track=7, channel=7, pitch=1, time=0, duration=0.01, volume=1)
    
    for i in range(len(midiFiles)):
        for ch in range(16):
            balance = getBalanceFromChannel(ch)
            midiFiles[i].addControllerEvent(track=ch, channel=ch, time=0, controller_number=8, parameter=balance)
            midiFiles[i].addTempo(track=ch, time=0, tempo=tempo) # tempo is in beats per minute
            
            midiFiles[i].addControllerEvent(track=ch, channel=ch, time=0, controller_number=7, parameter=maxVolume)
            midiFiles[i].addControllerEvent(track=ch, channel=ch, time=0, controller_number=11, parameter=0)
            j = float(i) * timeBetweenNotes
            while j <= midiLength:

                midiFiles[i].addControllerEvent(track=ch, channel=ch, time=j, controller_number=11, parameter=0)
                j += volumeZeroDuration
                if volumeSlopeUpDuration > 0.0:
                    for k in np.arange(0, maxExpression, incVolumeResolution, dtype=float):
                        midiFiles[i].addControllerEvent(track=ch, channel=ch, time=j + (float(k) / maxExpression) * volumeSlopeUpDuration, controller_number=11, parameter=max(min(round(k), maxExpression), 0))
                j += volumeSlopeUpDuration
                midiFiles[i].addControllerEvent(track=ch, channel=ch, time=j, controller_number=11, parameter=maxExpression)
                j += volumeMaxDuration
                if volumeSlopeDownDuration > 0.0:
                    for k in np.arange(0, maxExpression, decVolumeResolution, dtype=float):
                        midiFiles[i].addControllerEvent(track=ch, channel=ch, time=j + (float(k) / maxExpression) * volumeSlopeDownDuration, controller_number=11, parameter=max(min(maxExpression - round(k), maxExpression), 0))
                j += volumeSlopeDownDuration
                midiFiles[i].addControllerEvent(track=ch, channel=ch, time=j, controller_number=11, parameter=0)
                j += volumeZero2Duration


def getPitchFromHSV(hue: int, saturation: int, value: int, thresh: int, minPitch: int, maxPitch: int) -> (bool, int):
    if value < thresh: return False, 0
    return True, max( min( round(minPitch + (float(value) / 255.0) * (maxPitch - minPitch)), maxPitch ), minPitch )

def getVolumeFromPercentage(percent: float, thresh: float, minVolume: int, maxVolume: int) -> (bool, int):
    if percent < thresh: return False, 0
    return True, max( min( round(minVolume + 5.0 * percent * (maxVolume - minVolume)), maxVolume ), minVolume )


def addNotesFromFrame(midiFiles, frame: np.ndarray, timeBetweenNotes: float, noteIndex: int,
                      threshPitch: int = 40, minPitch: int = 30, maxPitch: int = 100,
                      threshVolume: int = 25, minVolume: int = 15, maxVolume: int = 120):
    height, width, _ = frame.shape
    frArray = np.zeros((128, 16), dtype=float)
    frame = cv2.convertScaleAbs(frame, alpha = float(maxPitch - minPitch) / 255.0, beta = minPitch)

    for i in range(height):
        for j in range(width):
            pitch = frame[i][j][2]
            balanceIndex = getChannelFromBalance(round(float(j) / (width-1) * 127.0))
            frArray[pitch][balanceIndex] += 1

    def frArrayModifyVertical(x):
        y = np.convolve(x, [1.0] * 15, mode='full')
        y = np.roll(y, -7)
        return y

    def frArrayModifyHorizontal(x):
        y = np.convolve(x, [0.5, 1.0, 0.5], mode='full')
        y = np.roll(y, -1)
        return y
    
    frArray = np.apply_along_axis(frArrayModifyVertical, 0, frArray) # vertical
    frArray = np.apply_along_axis(frArrayModifyHorizontal, 1, frArray) # orizontal

    frArray *= (maxVolume - minVolume) / float(height * width / 16.0)
    frArray += minVolume

    for i in range(threshPitch, 128):
        for j in range(16):
            if round(frArray[i][j]) > threshVolume:
                volume = max( min( round(frArray[i][j]), maxVolume), minVolume)
                addNoteAtIndex(midiFiles, timeBetweenNotes, noteIndex, i, volume, j)


def getMidisFromVideo(cap: cv2.VideoCapture, timeBetweenNotes: float, callback):
    videoLength = float(cap.get(cv2.CAP_PROP_FRAME_COUNT)) / cap.get(cv2.CAP_PROP_FPS)

    midiFiles = []
    for i in range(15):
        midiFiles.append(MIDIFile(numTracks=16, adjust_origin=False, eventtime_is_ticks=False))

    lastIndex = -1
    frameNumber = -1

    frameExists, frame = cap.read()
    timestamp = float(cap.get(cv2.CAP_PROP_POS_MSEC)) / 1000.0
    frameNumber += 1
    callback(float(frameNumber) / cap.get(cv2.CAP_PROP_FRAME_COUNT))
    while frameExists:
        index = round(timestamp / timeBetweenNotes)
        if index != lastIndex:
            lastIndex = index
            height, width, _ = frame.shape
            scaleFactor = min(256.0 / float(height), 256.0 / float(width))
            if scaleFactor < 1.0:
                frame = cv2.resize(frame, (round(width * scaleFactor), round(height * scaleFactor)))
            hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            addNotesFromFrame(midiFiles, hsvFrame, timeBetweenNotes, lastIndex)
        frameExists, frame = cap.read()
        timestamp = float(cap.get(cv2.CAP_PROP_POS_MSEC)) / 1000.0
        frameNumber += 1
        callback(float(frameNumber) / cap.get(cv2.CAP_PROP_FRAME_COUNT))

    postProcessing(midiFiles, videoLength + 3.0, timeBetweenNotes, 60, 0.20, 1.0, 0.05, 0.05)
    return midiFiles


# test

from piano_convert import midi_file, make_wav

def processingCallback(status: float):
    print("Loading:  " + str(status * 100.0) + " %")

midiFiles = getMidisFromVideo(cv2.VideoCapture("MVI_2939.MP4"), 1.0, processingCallback)

midiPaths = []

for i in range(len(midiFiles)):
    midiPaths.append(midi_file("custom_mid_" + str(i) + ".mid", "Piano_Paradise.sf2"))
    with open("custom_mid_" + str(i) + ".mid", 'wb') as outf:
        midiFiles[i].writeFile(outf)

make_wav(midiPaths, "funnyout.wav")