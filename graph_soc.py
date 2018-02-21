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

# df.plot(y='soc',title='forsen Social% vs Time')
# plt.savefig('data/forsen/graphs/soc_time.png')
# df.plot.scatter(x='rate',y='soc',title='forsen Social% vs Rate')
# plt.savefig('data/forsen/graphs/soc_rate.png')
# df.plot(y='n_user',title='forsen Unique Users vs Time')
# plt.savefig('data/forsen/graphs/usr_time.png')
# df.plot.scatter(x='rate',y='n_user',title='forsen Unique Users vs Rate')
# plt.savefig('data/forsen/graphs/usr_rate.png')
# df.plot.scatter(x='soc',y='n_user',title='forsen Unique Users vs Social%')
# plt.savefig('data/forsen/graphs/usr_soc.png')


# sns.jointplot(x="rate", y="soc", data=df,kind="reg")
# plt.suptitle('Forsen Social% vs Rate')
# plt.savefig('data/forsen/graphs/rate_soc_reg.png')

# sns.jointplot(x="rate", y="n_user", data=df,kind="reg")
# plt.suptitle('Forsen Unique Users vs Rate')
# plt.savefig('data/forsen/graphs/rate_usr_reg.png')

# sns.jointplot(x="soc", y="n_user", data=df,kind="reg")
# plt.suptitle('Forsen Unique Users vs Social%')
# plt.savefig('data/forsen/graphs/soc_usr_reg.png')

f_ts = pickle.load(open("data/forsen/forsen_ts.p","rb"))
d_ts = pickle.load(open("data/destiny/destiny_ts.p","rb"))
a_ts = pickle.load(open("data/asmongold/asmongold_ts.p","rb"))
s_ts = pickle.load(open("data/sodapoppin/sodapoppin_ts.p","rb"))

f_df = pd.DataFrame.from_dict(f_ts,orient='index')
f_df.rename(columns={'soc':'Forsen'}, inplace=True)
d_df = pd.DataFrame.from_dict(d_ts,orient='index')
d_df.rename(columns={'soc':'Destiny'}, inplace=True)
a_df = pd.DataFrame.from_dict(a_ts,orient='index')
a_df.rename(columns={'soc':'Asmon'}, inplace=True)
s_df = pd.DataFrame.from_dict(s_ts,orient='index')
s_df.rename(columns={'soc':'Soda'}, inplace=True)

DF = pd.concat([f_df,d_df,a_df,s_df], ignore_index=True)
DF.drop('n_user',axis=1,inplace=True)
#plt.figure(figsize=(12,8))
ax = DF.plot.scatter(x='rate',y='Forsen',label='Forsen',alpha=0.7,figsize=(12,8))
DF.plot.scatter(x='rate',y='Destiny',ax=ax,color="C2",label='Destiny',alpha=0.7)
DF.plot.scatter(x='rate',y='Asmon',ax=ax,color="C3",label='Asmon',alpha=0.7)
DF.plot.scatter(x='rate',y='Soda',ax=ax,color="C4",label='Soda',alpha=0.7)
plt.xlabel('Rate [msg/min]')
plt.ylabel('Soc %')

plt.savefig('data/soc_rate_all.png')