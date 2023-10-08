#function to convert midis to wav file and ajunts volume#
#########################################################
from midi2audio import FluidSynth
from pydub import AudioSegment
import os

#Font database
congas = 'congas MW_1_0.SF2'
piano = 'Piano_Paradise.sf2'


class midi_file:
  def __init__(self, path: str, soundfont: str):
    self.path = path
    self.soundfont = soundfont


def make_wav(midis: list,wav_out_path):
    assert(len(midis) > 0)

    FluidSynth(midis[0].path).midi_to_audio(midis[0].soundfont,wav_out_path)
    if len(midis) > 1:
        for index in range(1, len(midis)):
            FluidSynth(midis[index].path).midi_to_audio(midis[index].soundfont,"{}.wav".format(index))
            wav0 = AudioSegment.from_file(wav_out_path)
            wavi = AudioSegment.from_file("{}.wav".format(index))
            wavi.overlay(wav0).export(wav_out_path, format='wav')

def change_vol(wav_in_path, wav_out_path, db_change):
   (AudioSegment.from_wav(wav_in_path) + db_change).export(wav_out_path, "wav")



#test
# midis=[]
# midis.append(midi_file('deb_menu.mid','congas MW_1_0.SF2'))
# midis.append(midi_file('mond_1.mid','Piano_Paradise.sf2'))
# midis.append(midi_file('deb_menu.mid','congas MW_1_0.SF2'))

# make_wav(midis,"combined.wav")
# change_vol("combined.wav","combined.wav",40)
        
    
