import pickle
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
from scipy import stats

def r2(x, y):
    return stats.pearsonr(x, y)[0] ** 2

soc_ts = pickle.load(open("data/forsen/forsen_ts.p","rb"))
df = pd.DataFrame.from_dict(soc_ts,orient='index')
sns.set(color_codes=True)

df.plot(y='soc',title='forsen Social% vs Time')
plt.savefig('data/forsen/graphs/soc_time.png')
df.plot.scatter(x='rate',y='soc',title='forsen Social% vs Rate')
plt.savefig('data/forsen/graphs/soc_rate.png')
df.plot(y='n_user',title='forsen Unique Users vs Time')
plt.savefig('data/forsen/graphs/usr_time.png')
df.plot.scatter(x='rate',y='n_user',title='forsen Unique Users vs Rate')
plt.savefig('data/forsen/graphs/usr_rate.png')
df.plot.scatter(x='soc',y='n_user',title='forsen Unique Users vs Social%')
plt.savefig('data/forsen/graphs/usr_soc.png')


sns.jointplot(x="rate", y="soc", data=df,kind="reg")
plt.suptitle('Forsen Social% vs Rate')
plt.savefig('data/forsen/graphs/rate_soc_reg.png')

sns.jointplot(x="rate", y="n_user", data=df,kind="reg")
plt.suptitle('Forsen Unique Users vs Rate')
plt.savefig('data/forsen/graphs/rate_usr_reg.png')

sns.jointplot(x="soc", y="n_user", data=df,kind="reg")
plt.suptitle('Forsen Unique Users vs Social%')
plt.savefig('data/forsen/graphs/soc_usr_reg.png')