#function to convert pixel to midi to wav file
from midi2audio import FluidSynth
from pydub import AudioSegment


congas = 'congas MW_1_0.SF2'
piano = 'Piano_Paradise.sf2'

class midi_file:
  def __init__(self, path, soundfont):
    self.path = ""
    self.soundfont = ""

FluidSynth('congas MW_1_0.SF2').midi_to_audio('deb_menu.mid',"output.wav")
FluidSynth('Piano_Paradise.sf2').midi_to_audio('mond_1.mid',"output_beet.wav")





sound1 = AudioSegment.from_file("output.wav")
sound2 = AudioSegment.from_file("output_beet.wav")

combined = sound1.overlay(sound2)

combined.export("combined.wav", format='wav')




song = AudioSegment.from_wav("combined.wav")
song_20_db_louder = song + 40
song_20_db_louder.export("louder.wav", "wav")





def make_wav(midis: list):
    assert(len(midis) > 0)
    
    FluidSynth(midis[0].path).midi_to_audio(midis[0].soundfont,"combined.wav".format(index))
    if len(midis) > 1:
        for index in range(1, len(midis)):
            FluidSynth(midis[index].path).midi_to_audio(midis[index].soundfont,"{index}.wav".format(index))
            wav0 = AudioSegment.from_file("combined.wav")
            wavi = AudioSegment.from_file("{index}.wav".format(index))
            wavi.overlay(wav0).export("combined.wav", format='wav')
        
    
