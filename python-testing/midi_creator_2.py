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

def addNoteAtIndex(midiFiles: list[MIDIFile], midiLength: float, timeBetweenNotes: float,
                   noteIndex: int, pitch: int, volume: int, balance: float,
                   nrChannels: int = 16) -> float:
    
    noteStart = noteIndex * timeBetweenNotes
    noteDuration = timeBetweenNotes * len(midiFiles)
    # balance: [-1, 1]
    balanceChannel = max( min( round((float(balance) + 1.0) / 2.0 * (nrChannels-1)), nrChannels-1 ), 0 )
    midiFiles[noteIndex % len(midiFiles)].addNote(track = balanceChannel, channel = balanceChannel, pitch=pitch, time=noteStart, duration=noteDuration, volume=volume)
    return max(midiLength, noteStart)

def addNoteAtTime(midiFiles: list[MIDIFile], midiLength: float, timeBetweenNotes: float,
                   noteStart: float, pitch: int, volume: int, balance: float,
                   nrChannels: int = 16) -> float:
    
    addNoteAtIndex(midiFiles, midiLength, timeBetweenNotes,
                   round(noteStart / timeBetweenNotes), pitch, volume, balance,
                   nrChannels)


def postProcessing(midiFiles: list[MIDIFile], midiLength: float, timeBetweenNotes: float,
                   tempo: int,
                   volumeZeroDuration: float,
                   volumeSlopeUpDuration: float,
                   volumeSlopeDownDuration: float,
                   volumeZero2Duration: float,
                   nrChannels: int = 16,
                   maxVolume: int = 127,
                   maxExpression: int = 127,
                   maxBalance: int = 127,
                   incVolumeResolution: float = 2.5,
                   decVolumeResolution: float = 3.5):
    
    volumeMaxDuration = timeBetweenNotes * len(midiFiles) - (volumeZeroDuration + volumeSlopeUpDuration + volumeSlopeDownDuration + volumeZero2Duration)
    assert(volumeMaxDuration >= 0.0)
    
    for i in range(len(midiFiles)):
        for ch in range(nrChannels):
            balance = max(min(round(float(ch) / (nrChannels-1) * maxBalance), maxBalance), 0)
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


# test

midiFiles = []
midiFiles.append(MIDIFile(numTracks=16, eventtime_is_ticks=False))
midiFiles.append(MIDIFile(numTracks=16, eventtime_is_ticks=False))
midiFiles.append(MIDIFile(numTracks=16, eventtime_is_ticks=False))
midiFiles.append(MIDIFile(numTracks=16, eventtime_is_ticks=False))
midiFiles.append(MIDIFile(numTracks=16, eventtime_is_ticks=False))
midiFiles.append(MIDIFile(numTracks=16, eventtime_is_ticks=False))

currentMidiLength = 0.0
timeBetweenNotes = 0.7

currentMidiLength = coolAddNote(midiFiles, currentMidiLength, timeBetweenNotes, 0, 60, 100, -1)
currentMidiLength = coolAddNote(midiFiles, currentMidiLength, timeBetweenNotes, 1, 60, 100, -0.75)
currentMidiLength = coolAddNote(midiFiles, currentMidiLength, timeBetweenNotes, 2, 60, 100, -0.5)
currentMidiLength = coolAddNote(midiFiles, currentMidiLength, timeBetweenNotes, 3, 60, 100, -0.25)
currentMidiLength = coolAddNote(midiFiles, currentMidiLength, timeBetweenNotes, 4, 60, 100, 0.0)
currentMidiLength = coolAddNote(midiFiles, currentMidiLength, timeBetweenNotes, 5, 60, 100, 0.25)
currentMidiLength = coolAddNote(midiFiles, currentMidiLength, timeBetweenNotes, 6, 60, 100, 0.5)
currentMidiLength = coolAddNote(midiFiles, currentMidiLength, timeBetweenNotes, 7, 60, 100, 0.75)
currentMidiLength = coolAddNote(midiFiles, currentMidiLength, timeBetweenNotes, 8, 60, 100, 1.0)

postProcessing(midiFiles, currentMidiLength, timeBetweenNotes, 120, 0.4, 0.5, 0.3, 0.2)

from piano_convert import midi_file, make_wav

midiPaths = []

for i in range(len(midiFiles)):
    midiPaths.append(midi_file("custom_mid_" + str(i) + ".mid", "Piano_Paradise.sf2"))
    with open("custom_mid_" + str(i) + ".mid", 'wb') as outf:
        midiFiles[i].writeFile(outf)

make_wav(midiPaths, "funnyout.wav")
