import time
from pysinewave import SineWave

sinewave = SineWave(pitch=12, pitch_per_second=122)

sinewave.play()
time.sleep(2)
sinewave.set_pitch(-5)
time.sleep(3)
