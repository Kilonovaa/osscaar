import matplotlib.pyplot as plt
import pandas as pd
import os
min_value=49
max_value=151
mypath = os.path.dirname(__file__)
df=pd.read_csv(mypath + r'\Book1.csv')
index_value = (df.Value >= min_value) & (df.Value <= max_value)
df_filt=df[index_value]
cash=len(index_value)
map = plt.imread(mypath + r'\imagine.png')
plt.imshow(map, extent=[-180,180,-90,90], alpha=0.7)
plt.plot(df_filt.Longitude, df_filt.Latitude,"o", color="red")
plt.title('Showing '+str(cash)+' locations')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()
