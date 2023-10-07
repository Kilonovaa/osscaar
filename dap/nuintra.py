import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
f=2#frequency sine wave
A=1#Amplitude of sine wave
x=np.arange(-np.pi, np.pi, 0.01)
y=A*np.sin(f*x)
fig=plt.figure()
plt.plot(x, y)
plt.xlabel('x')
plt.ylabel('y')
plt.show()
