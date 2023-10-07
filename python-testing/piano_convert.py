#function to convert pixel to midi to wav file
from midi2audio import FluidSynth
from pydub import AudioSegment

synth = FluidSynth('congas MW_1_0.SF2')

synth.midi_to_audio('deb_menu.mid',"output.wav")

song = AudioSegment.from_wav("output.wav")
song_20_db_louder = song + 20
song_20_db_louder.export("louder.wav", "wav")