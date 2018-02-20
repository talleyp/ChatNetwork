import pickle
import pandas as pd
import matplotlib.pyplot as plt

soc_ts = pickle.load(open("data/destiny/destiny_ts.p","rb"))
df = pd.DataFrame.from_dict(soc_ts,orient='index')

df.plot(y='soc')
df.plot.scatter(x='rate',y='soc')
plt.show()