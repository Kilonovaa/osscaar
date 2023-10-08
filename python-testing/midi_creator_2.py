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

def addNoteAtIndex(mf: MIDIFile, midiLength: float, timeBetweenNotes: float,
                   index: int, pitch: int, volume: int,
                   nrChannels: int = 16,
                   noteDuration: float = 40.0):
    
    time = index * timeBetweenNotes
    mf.addNote(track = index % nrChannels, channel = index % nrChannels, pitch=pitch, time=time, duration=noteDuration, volume=volume)
    return max(midiLength, time)


def postProcessing(mf: MIDIFile, midiLength: float, timeBetweenNotes: float,
                   tempo: int,
                   volumeZeroDuration: float,
                   volumeSlopeUpDuration: float,
                   volumeSlopeDownDuration: float,
                   volumeZero2Duration: float,
                   nrChannels: int = 16,
                   maxParameter: int = 127,
                   incVolumeResolution: float = 2.5,
                   decVolumeResolution: float = 3.5):
    
    volumeMaxDuration = timeBetweenNotes * nrChannels - (volumeZeroDuration + volumeSlopeUpDuration + volumeSlopeDownDuration + volumeZero2Duration)
    assert(volumeMaxDuration >= 0.0)
    for i in range(nrChannels):
        mf.addTempo(track=i, time=0, tempo=tempo) # tempo is in beats per minute
        mf.addControllerEvent(track=i, channel=i, time=0, controller_number=7, parameter=maxParameter)
        mf.addControllerEvent(track=i, channel=i, time=0, controller_number=11, parameter=0)
        j = float(i) * timeBetweenNotes
        while j <= midiLength:

            mf.addControllerEvent(track=i, channel=i, time=j, controller_number=11, parameter=0)
            j += volumeZeroDuration
            if volumeSlopeUpDuration > 0.0:
                for k in np.arange(0, maxParameter, incVolumeResolution, dtype=float):
                    mf.addControllerEvent(track=i, channel=i, time=j + (float(k) / maxParameter) * volumeSlopeUpDuration, controller_number=11, parameter=max(min(int(k), maxParameter), 0))
            j += volumeSlopeUpDuration
            mf.addControllerEvent(track=i, channel=i, time=j, controller_number=11, parameter=maxParameter)
            j += volumeMaxDuration
            if volumeSlopeDownDuration > 0.0:
                for k in np.arange(0, maxParameter, decVolumeResolution, dtype=float):
                    mf.addControllerEvent(track=i, channel=i, time=j + (float(k) / maxParameter) * volumeSlopeDownDuration, controller_number=11, parameter=max(min(maxParameter - int(k), maxParameter), 0))
            j += volumeSlopeDownDuration
            mf.addControllerEvent(track=i, channel=i, time=j, controller_number=11, parameter=0)
            j += volumeZero2Duration


# test

# mf = MIDIFile(numTracks=16, eventtime_is_ticks=False)
# currentMidiLength = 0.0
# timeBetweenNotes = 0.7

# currentMidiLength = addNoteAtIndex(mf, currentMidiLength, timeBetweenNotes, 0, 60, 90)
# currentMidiLength = addNoteAtIndex(mf, currentMidiLength, timeBetweenNotes, 1, 62, 90)
# currentMidiLength = addNoteAtIndex(mf, currentMidiLength, timeBetweenNotes, 2, 63, 90)
# currentMidiLength = addNoteAtIndex(mf, currentMidiLength, timeBetweenNotes, 3, 65, 90)
# currentMidiLength = addNoteAtIndex(mf, currentMidiLength, timeBetweenNotes, 4, 67, 90)
# currentMidiLength = addNoteAtIndex(mf, currentMidiLength, timeBetweenNotes, 5, 68, 90)
# currentMidiLength = addNoteAtIndex(mf, currentMidiLength, timeBetweenNotes, 6, 67, 90)
# currentMidiLength = addNoteAtIndex(mf, currentMidiLength, timeBetweenNotes, 7, 65, 90)
# currentMidiLength = addNoteAtIndex(mf, currentMidiLength, timeBetweenNotes, 8, 67, 90)

# postProcessing(mf, currentMidiLength, timeBetweenNotes, 120, 0.5, 2.3, 0.3, 0.2)

# from piano_convert import midi_file, make_wav

# with open("funnyout.mid", 'wb') as outf:
#     mf.writeFile(outf)

# make_wav([midi_file("funnyout.mid", "Piano_Paradise.sf2")], "funnyout.wav")
