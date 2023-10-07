#function to convert pixel to midi to wav file
from midi2audio import FluidSynth

synth = FluidSynth('congas MW_1_0.SF2')
synth.midi_to_audio('deb_menu.mid',"output.wav", gain=2)