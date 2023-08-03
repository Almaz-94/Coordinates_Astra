import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from Сличение import stage1, garn

prn=np.array(stage1)

st1=[]

for row in garn:
    st1.append([*prn[(abs(prn[:,2]-row[0])<8)&(abs(prn[:,3]-row[1])<8)][:,0:2].flatten(),row[0],row[1]])
    if len(st1[-1])==2:
        st1.pop()
    elif len(st1[-1])==6:
        st1[-1].pop(0)
        st1[-1].pop(0)

st1=pd.DataFrame(st1,columns=['PR','PK','Longitude','Latitude'])
st1.drop_duplicates(subset=['PR','PK'],inplace=True,ignore_index=True)
prn=pd.DataFrame(prn,columns=['PR','PK','Longitude','Latitude'])
ljoin=prn.merge(st1,on=['PR','PK'],how='left')

points_missed=len(ljoin.loc[ljoin.Longitude_y.isnull()])
df_missing_points=ljoin.loc[ljoin.Longitude_y.isnull()]
avg_dist=round(np.sqrt((ljoin.Longitude_x-ljoin.Longitude_y)**2+(ljoin.Latitude_x-ljoin.Latitude_y)**2).mean(),2)

st1.sort_values(['PR','PK'],inplace=True)
st1.to_csv('Шамян сличение 1.csv',float_format='%.1f',index=False)


fig,ax=plt.subplots()

plt.scatter(st1.Longitude,st1.Latitude,s=0.6)
plt.scatter(df_missing_points.Longitude_x,df_missing_points.Latitude_x,s=5,marker='x',c='r')


plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.xticks(rotation=45,rotation_mode='anchor',ha='right')
ax.xaxis.set_major_formatter(FormatStrFormatter('%.0f'))
ax.yaxis.set_major_formatter(FormatStrFormatter('%.0f'))

plt.title('First surveyed area')
plt.legend(['Factual GPS coordinates','Missing points'])
st1_unique=st1.drop_duplicates(subset=['PR'],ignore_index=True)
for el in range(len(st1_unique)):
    ax.text(st1_unique.iloc[el,2]-50,st1_unique.iloc[el,3]+50,int(st1_unique.at[el,'PR']),size=6)
plt.figtext(0.68,0.23,'Average GPS error: {}m\nPoints missing: {} out of {}'.format(avg_dist,points_missed,len(prn)),bbox = {'facecolor': 'oldlace', 'alpha': 0.8, 'pad': 3})
plt.grid()
plt.tight_layout()

plt.show()