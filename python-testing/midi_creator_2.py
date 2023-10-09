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
from pydub import AudioSegment
from midi2audio import FluidSynth
import math
import random
from datetime import datetime


class CompleteMidiFile:
  def __init__(self, path: str, soundfont: str):
    self.path = path
    self.soundfont = soundfont


majorPitches = []
minorPitches = []

for pitch in range(12, 24):
    majorPitch = [pitch]
    while majorPitch[-1] <= 127:
        majorPitch.append(majorPitch[-1] + 4)
        majorPitch.append(majorPitch[-1] + 3)
        majorPitch.append(majorPitch[-1] + 5)
    majorPitches.append(majorPitch)
    minorPitch = [pitch]
    while minorPitch[-1] <= 127:
        minorPitch.append(minorPitch[-1] + 3)
        minorPitch.append(minorPitch[-1] + 4)
        minorPitch.append(minorPitch[-1] + 5)
    minorPitches.append(minorPitch)

currentChord = majorPitches[0]

def getRandomChord():
    mm = random.randint(0, 1)
    if mm == 0:
        return majorPitches[random.randint(0, len(majorPitches)-1)]
    return minorPitches[random.randint(0, len(minorPitches)-1)]


callback = lambda x: x
lastCompletion = 0.0
nrFrames = 1


verticalKernel = np.array([0.5, 0.7, 0.9, 1.0, 1.0, 1.0, 0.9, 0.7, 0.5], dtype=float)
verticalKernel *= 0.38

horizontalKernel = np.array([0.35, 0.85, 1.0, 0.85, 0.35], dtype=float)
horizontalKernel *= 0.48


def getChannelFromBalance(balance: int) -> int:
    return max( min( round(float(balance) / 127.0 * 15.0), 15 ), 0 )

def getBalanceFromChannel(channel: int) -> int:
    return max( min( round(float(channel) / 15.0 * 127.0), 127 ), 0 )

def addNoteAtIndex(midiFiles, timeBetweenNotes: float,
                   noteIndex: int, pitch: int, volume: int, balanceChannel: int) -> float:
    
    noteStart = noteIndex * timeBetweenNotes
    noteDuration = timeBetweenNotes * len(midiFiles) - 0.02
    midiFiles[noteIndex % len(midiFiles)].addNote(track = balanceChannel, channel = balanceChannel, pitch=pitch, time=noteStart, duration=noteDuration, volume=volume)



def postProcessing(midiFiles, midiLength: float, timeBetweenNotes: float,
                   tempo: int,
                   volumeZeroDuration: float,
                   volumeSlopeUpDuration: float,
                   volumeMaxDuration: float,
                   volumeSlopeDownDuration: float,
                   maxVolume: int = 127,
                   maxExpression: int = 127,
                   incVolumeResolution: float = 2.5,
                   decVolumeResolution: float = 3.5):
    
    global callback, lastCompletion, nrFrames

    callback(lastCompletion, "Applying post processing (attack-removal volume + expression trick, L-R stereo distribution)", nrFrames)
    
    volumeZero2Duration = timeBetweenNotes * len(midiFiles) - (volumeZeroDuration + volumeSlopeUpDuration + volumeMaxDuration + volumeSlopeDownDuration)
    assert(volumeZero2Duration >= 0.0)
    
    for i in range(len(midiFiles)):
        for ch in range(16):
            balance = getBalanceFromChannel(ch)
            midiFiles[i].addControllerEvent(track=ch, channel=ch, time=0, controller_number=125, parameter=0)
            midiFiles[i].addControllerEvent(track=ch, channel=ch, time=0, controller_number=127, parameter=0)
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



def addNotesFromFrame(midiFiles, frame: np.ndarray, lowerHsv: np.ndarray, upperHsv: np.ndarray,
                      timeBetweenNotes: float, noteIndex: int,
                      threshPitch: int = 35, minPitch: int = 30, maxPitch: int = 120,
                      threshVolume: int = 20, minVolume: int = 15, maxVolume: int = 100):
    
    global callback, lastCompletion, nrFrames

    callback(lastCompletion, "Applying HSV masks", nrFrames)
    mask = 0
    if (lowerHsv[0] > upperHsv[0]):
        mask1 = cv2.inRange(frame, lowerHsv, np.array([179, upperHsv[1], upperHsv[2]]))
        mask2 = cv2.inRange(frame, np.array([0, lowerHsv[1], lowerHsv[2]]), upperHsv)
        mask = cv2.bitwise_or(mask1, mask2)
        frame = cv2.bitwise_and(frame, frame, mask = mask)
    else:
        mask = cv2.inRange(frame, lowerHsv, upperHsv)
        frame = cv2.bitwise_and(frame, frame, mask = mask)

    callback(lastCompletion, "Calculating pitch - balance frequency matrix", nrFrames)
    height, width, _ = frame.shape
    frArray = np.zeros((128, 16), dtype=float)
    maskArray = np.zeros((16), dtype=float)
    frame = cv2.convertScaleAbs(frame, alpha = float(maxPitch - minPitch) / 255.0, beta = minPitch)

    for i in range(height):
        for j in range(width):
            pitch = frame[i][j][2]
            balanceIndex = getChannelFromBalance(round(float(j) / (width-1) * 127.0))
            frArray[pitch][balanceIndex] += mask[i][j]
            maskArray[balanceIndex] += mask[i][j]

    callback(lastCompletion, "Normalizing frequency matrix by mask per-balance density", nrFrames)
    for i in range(0, 128):
        for j in range(0, 16):
            frArray[i][j] /= (maskArray[j] + 2.0 * 255)

    callback(lastCompletion, "Computing fast convolution between frequency matrix and custom vertical/horizontal kernel", nrFrames)

    global verticalKernel, horizontalKernel

    def frArrayModifyVertical(x):
        y = np.convolve(x, verticalKernel, mode='full')
        y = np.roll(y, - (len(verticalKernel) // 2))
        return y

    def frArrayModifyHorizontal(x):
        y = np.convolve(x, horizontalKernel, mode='full')
        y = np.roll(y, - (len(horizontalKernel) // 2))
        return y
    
    frArray = np.apply_along_axis(frArrayModifyVertical, 0, frArray) # vertical
    frArray = np.apply_along_axis(frArrayModifyHorizontal, 1, frArray) # orizontal

    frArray *= (maxVolume - minVolume)
    frArray += minVolume

    callback(lastCompletion, "Creating notes as part of a chord", nrFrames)

    global currentChord

    for i in currentChord:
        if i < threshPitch:
            continue
        if i > maxPitch:
            break
        for j in range(0, 16, 1):
            if frArray[i][j] > threshVolume:
                volume = max( min( round(frArray[i][j] - i / 8.0), maxVolume), minVolume)
                addNoteAtIndex(midiFiles, timeBetweenNotes, noteIndex, i, volume, j)



def getMidisFromVideo(videoPath: str, idString: str, myCallback):
    global callback, lastCompletion, nrFrames
    callback = myCallback

    cap = cv2.VideoCapture(videoPath)

    timeBetweenNotes = 0.4
    videoNewSize = 256

    nrFrames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    videoLength = float(nrFrames) / cap.get(cv2.CAP_PROP_FPS)

    callback(0, "Starting the magic...", nrFrames)

    violinSF = 'Levi_s_Violin.sf2'
    pianoSF = 'Piano_Paradise.sf2'
    harpSF = 'Open_Diapason_Pipe_Organ.sf2.sf2'
    guitarSF = 'Pianoteq_8_Classical_Guitar.sf2'
    fluteSF = 'Mell Flutes.SF2'
    bassSF = 'BassLong.sf2'

    lowerViolin = np.array([165, 35, 35])
    upperViolin = np.array([15, 255, 220])
    lowerPiano = np.array([15, 35, 35])
    upperPiano = np.array([35, 255, 220])
    lowerPiano2 = np.array([0, 0, 192])
    upperPiano2 = np.array([179, 255, 255])
    lowerHarp = np.array([35, 35, 35])
    upperHarp = np.array([85, 255, 220])
    lowerGuitar = np.array([85, 35, 35])
    upperGuitar = np.array([100, 255, 220])
    lowerFlute = np.array([100, 35, 35])
    upperFlute = np.array([135, 255, 220])
    lowerBass = np.array([135, 35, 35])
    upperBass = np.array([165, 255, 220])
    

    violinMidiFiles = []
    pianoMidiFiles = []
    harpMidiFiles = []
    guitarMidiFiles = []
    fluteMidiFiles = []
    bassMidiFiles = []
    for i in range(15):
        violinMidiFiles.append(MIDIFile(numTracks=16, adjust_origin=False, eventtime_is_ticks=False))
        pianoMidiFiles.append(MIDIFile(numTracks=16, adjust_origin=False, eventtime_is_ticks=False))
        harpMidiFiles.append(MIDIFile(numTracks=16, adjust_origin=False, eventtime_is_ticks=False))
        guitarMidiFiles.append(MIDIFile(numTracks=16, adjust_origin=False, eventtime_is_ticks=False))
        fluteMidiFiles.append(MIDIFile(numTracks=16, adjust_origin=False, eventtime_is_ticks=False))
        bassMidiFiles.append(MIDIFile(numTracks=16, adjust_origin=False, eventtime_is_ticks=False))

    lastIndex = -1
    frameNumber = -1

    lastCompletion = 0.0

    global currentChord

    random.seed(datetime.now().timestamp())

    currentChord = getRandomChord()
    lastRandomizationTimestamp = 0.0
    randomDuration = random.random() * 5.0 + 11.0

    frameExists, frame = cap.read()
    timestamp = float(cap.get(cv2.CAP_PROP_POS_MSEC)) / 1000.0
    frameNumber += 1
    lastCompletion = float(frameNumber) / nrFrames / 2.0
    callback(lastCompletion, "Processing frame " + str(frameNumber) + " of " + str(nrFrames), nrFrames)
    while frameExists:
        if timestamp - lastRandomizationTimestamp >= randomDuration:
            currentChord = getRandomChord()
            lastRandomizationTimestamp = timestamp
            randomDuration = random.random() * 5.0 + 10.0
        index = round(timestamp / timeBetweenNotes)
        if index != lastIndex:
            lastIndex = index
            hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            height, width, _ = hsvFrame.shape
            scaleFactor = min(float(videoNewSize) / float(height), float(videoNewSize) / float(width))
            if scaleFactor < 1.0:
                hsvFrame = cv2.resize(hsvFrame, (round(width * scaleFactor), round(height * scaleFactor)))
            addNotesFromFrame(violinMidiFiles, hsvFrame, lowerViolin, upperViolin, timeBetweenNotes, lastIndex)
            addNotesFromFrame(pianoMidiFiles, hsvFrame, lowerPiano, upperPiano, timeBetweenNotes, lastIndex)
            addNotesFromFrame(pianoMidiFiles, hsvFrame, lowerPiano2, upperPiano2, timeBetweenNotes, lastIndex, minVolume=40, maxVolume=110, threshVolume=45)
            addNotesFromFrame(harpMidiFiles, hsvFrame, lowerHarp, upperHarp, timeBetweenNotes, lastIndex)
            addNotesFromFrame(guitarMidiFiles, hsvFrame, lowerGuitar, upperGuitar, timeBetweenNotes, lastIndex)
            addNotesFromFrame(fluteMidiFiles, hsvFrame, lowerFlute, upperFlute, timeBetweenNotes, lastIndex)
            addNotesFromFrame(bassMidiFiles, hsvFrame, lowerBass, upperBass, timeBetweenNotes, lastIndex)
            
        frameExists, frame = cap.read()
        timestamp = float(cap.get(cv2.CAP_PROP_POS_MSEC)) / 1000.0
        frameNumber += 1
        lastCompletion = float(frameNumber) / nrFrames / 2.0
        callback(lastCompletion, "Processing frame " + str(frameNumber) + " of " + str(nrFrames), nrFrames)
    
    lastCompletion = 0.5

    postProcessing(violinMidiFiles, videoLength + 3.5, timeBetweenNotes, 60, 0.3, 0.8, 2.2, 0.8, maxVolume=78)
    postProcessing(pianoMidiFiles, videoLength + 3.5, timeBetweenNotes, 60, 0.3, 0.8, 2.2, 0.8)
    postProcessing(harpMidiFiles, videoLength + 3.5, timeBetweenNotes, 60, 0.3, 0.8, 2.2, 0.8)
    postProcessing(guitarMidiFiles, videoLength + 3.5, timeBetweenNotes, 60, 0.3, 0.8, 2.2, 0.8)
    postProcessing(fluteMidiFiles, videoLength + 3.5, timeBetweenNotes, 60, 0.3, 0.8, 2.2, 0.8)
    postProcessing(bassMidiFiles, videoLength + 3.5, timeBetweenNotes, 60, 0.3, 0.8, 2.2, 0.8)

    violinMidiPath = idString + "_violin.mid"
    pianoMidiPath = idString + "_piano.mid"
    harpMidiPath = idString + "_harp.mid"
    guitarMidiPath = idString + "_guitar.mid"
    fluteMidiPath = idString + "_flute.mid"
    bassMidiPath = idString + "_bass.mid"
    
    violinWavPath = idString + "_violin.wav"
    pianoWavPath = idString + "_piano.wav"
    harpWavPath = idString + "_harp.wav"
    guitarWavPath = idString + "_guitar.wav"
    fluteWavPath = idString + "_flute.wav"
    bassWavPath = idString + "_bass.wav"
    

    callback(lastCompletion, "Creating violin .wav number 0", nrFrames)
    with open(violinMidiPath, "wb") as outf:
        violinMidiFiles[0].writeFile(outf)
    FluidSynth(violinMidiPath).midi_to_audio(violinSF, violinWavPath)
    if len(violinMidiFiles) > 1:
        wav0 = AudioSegment.from_file(violinWavPath)
        for index in range(1, len(violinMidiFiles)):
            callback(lastCompletion + float(index) / len(violinMidiFiles) / 12.0, "Creating violin .wav number " + str(index), nrFrames)
            with open(violinMidiPath, "wb") as outf:
                violinMidiFiles[index].writeFile(outf)
            FluidSynth(violinMidiPath).midi_to_audio(violinSF, violinWavPath)
            wavi = AudioSegment.from_file(violinWavPath)
            wav0 = wav0.overlay(wavi)
        wav0.export(violinWavPath, "wav")
    lastCompletion += 1.0 / 12.0
    
    callback(lastCompletion, "Creating piano .wav number 0", nrFrames)
    with open(pianoMidiPath, "wb") as outf:
        pianoMidiFiles[0].writeFile(outf)
    FluidSynth(pianoMidiPath).midi_to_audio(pianoSF, pianoWavPath)
    if len(pianoMidiFiles) > 1:
        wav0 = AudioSegment.from_file(pianoWavPath)
        for index in range(1, len(pianoMidiFiles)):
            callback(lastCompletion + float(index) / len(pianoMidiFiles) / 12.0, "Creating piano .wav number " + str(index), nrFrames)
            with open(pianoMidiPath, "wb") as outf:
                pianoMidiFiles[index].writeFile(outf)
            FluidSynth(pianoMidiPath).midi_to_audio(pianoSF, pianoWavPath)
            wavi = AudioSegment.from_file(pianoWavPath)
            wav0 = wav0.overlay(wavi)
        wav0.export(pianoWavPath, "wav")
    lastCompletion += 1.0 / 12.0
    
    callback(lastCompletion, "Creating harp .wav number 0", nrFrames)
    with open(harpMidiPath, "wb") as outf:
        harpMidiFiles[0].writeFile(outf)
    FluidSynth(harpMidiPath).midi_to_audio(harpSF, harpWavPath)
    if len(harpMidiFiles) > 1:
        wav0 = AudioSegment.from_file(harpWavPath)
        for index in range(1, len(harpMidiFiles)):
            callback(lastCompletion + float(index) / len(harpMidiFiles) / 12.0, "Creating harp .wav number " + str(index), nrFrames)
            with open(harpMidiPath, "wb") as outf:
                harpMidiFiles[index].writeFile(outf)
            FluidSynth(harpMidiPath).midi_to_audio(harpSF, harpWavPath)
            wavi = AudioSegment.from_file(harpWavPath)
            wav0 = wav0.overlay(wavi)
        wav0.export(harpWavPath, "wav")
    lastCompletion += 1.0 / 12.0
    
    callback(lastCompletion, "Creating guitar .wav number 0", nrFrames)
    with open(guitarMidiPath, "wb") as outf:
        guitarMidiFiles[0].writeFile(outf)
    FluidSynth(guitarMidiPath).midi_to_audio(guitarSF, guitarWavPath)
    if len(guitarMidiFiles) > 1:
        wav0 = AudioSegment.from_file(guitarWavPath)
        for index in range(1, len(guitarMidiFiles)):
            callback(lastCompletion + float(index) / len(guitarMidiFiles) / 12.0, "Creating guitar .wav number " + str(index), nrFrames)
            with open(guitarMidiPath, "wb") as outf:
                guitarMidiFiles[index].writeFile(outf)
            FluidSynth(guitarMidiPath).midi_to_audio(guitarSF, guitarWavPath)
            wavi = AudioSegment.from_file(guitarWavPath)
            wav0 = wav0.overlay(wavi)
        wav0.export(guitarWavPath, "wav")
    lastCompletion += 1.0 / 12.0
    
    callback(lastCompletion, "Creating flute .wav number 0", nrFrames)
    with open(fluteMidiPath, "wb") as outf:
        fluteMidiFiles[0].writeFile(outf)
    FluidSynth(fluteMidiPath).midi_to_audio(fluteSF, fluteWavPath)
    if len(fluteMidiFiles) > 1:
        wav0 = AudioSegment.from_file(fluteWavPath)
        for index in range(1, len(fluteMidiFiles)):
            callback(lastCompletion + float(index) / len(fluteMidiFiles) / 12.0, "Creating flute .wav number " + str(index), nrFrames)
            with open(fluteMidiPath, "wb") as outf:
                fluteMidiFiles[index].writeFile(outf)
            FluidSynth(fluteMidiPath).midi_to_audio(fluteSF, fluteWavPath)
            wavi = AudioSegment.from_file(fluteWavPath)
            wav0 = wav0.overlay(wavi)
        wav0.export(fluteWavPath, "wav")
    lastCompletion += 1.0 / 12.0
    
    callback(lastCompletion, "Creating bass .wav number 0", nrFrames)
    with open(bassMidiPath, "wb") as outf:
        bassMidiFiles[0].writeFile(outf)
    FluidSynth(bassMidiPath).midi_to_audio(bassSF, bassWavPath)
    if len(bassMidiFiles) > 1:
        wav0 = AudioSegment.from_file(bassWavPath)
        for index in range(1, len(bassMidiFiles)):
            callback(lastCompletion + float(index) / len(bassMidiFiles) / 12.0, "Creating bass .wav number " + str(index), nrFrames)
            with open(bassMidiPath, "wb") as outf:
                bassMidiFiles[index].writeFile(outf)
            FluidSynth(bassMidiPath).midi_to_audio(bassSF, bassWavPath)
            wavi = AudioSegment.from_file(bassWavPath)
            wav0 = wav0.overlay(wavi)
        wav0.export(bassWavPath, "wav")
    lastCompletion += 1.0 / 12.0
    

    segmViolin = AudioSegment.from_file(violinWavPath)
    segmPiano = AudioSegment.from_file(pianoWavPath)
    segmHarp = AudioSegment.from_file(harpWavPath)
    segmGuitar = AudioSegment.from_file(guitarWavPath)
    segmFlute = AudioSegment.from_file(fluteWavPath)
    segmBass = AudioSegment.from_file(bassWavPath)

    segmAll = segmViolin.overlay(segmPiano).overlay(segmHarp).overlay(segmGuitar).overlay(segmFlute).overlay(segmBass)
    segmAll.export(idString + "_all.wav", "wav")

    lastCompletion = 1.0

    callback(lastCompletion, "Done!", nrFrames)
    
    return idString + "_all.wav"


def emptyCallback(a, b, c):
    return

# test

def processingCallback(status: float, msg: str, nrFrames):
    print("Loading:  " + str(status * 100.0) + " %")

getMidisFromVideo("orionnebula.mp4", "the_dawn_of_mankind", processingCallback)
