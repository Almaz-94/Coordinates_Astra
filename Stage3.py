import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from Сличение import stage3, garn

prn=np.array(stage3)

st3=[]

for row in garn:
    st3.append([*prn[(abs(prn[:,2]-row[0])<8)&(abs(prn[:,3]-row[1])<8)][:,0:2].flatten(),row[0],row[1]])
    if len(st3[-1])==2:
        st3.pop()
    elif len(st3[-1])==6:
        st3[-1].pop(0)
        st3[-1].pop(0)

st3=pd.DataFrame(st3,columns=['PR','PK','Longitude','Latitude'])
st3.drop_duplicates(subset=['PR','PK'],inplace=True,ignore_index=True)
prn=pd.DataFrame(prn,columns=['PR','PK','Longitude','Latitude'])
ljoin=prn.merge(st3,on=['PR','PK'],how='left')

points_missed=len(ljoin.loc[ljoin.Longitude_y.isnull()])
df_missing_points=ljoin.loc[ljoin.Longitude_y.isnull()]
avg_dist=round(np.sqrt((ljoin.Longitude_x-ljoin.Longitude_y)**2+(ljoin.Latitude_x-ljoin.Latitude_y)**2).mean(),2)

st3.sort_values(['PR','PK'],inplace=True)
#st3.to_csv('Шамян сличение 3.csv',float_format='%.1f',index=False)


fig,ax=plt.subplots()

plt.scatter(st3.Longitude,st3.Latitude,s=0.6)
plt.scatter(df_missing_points.Longitude_x,df_missing_points.Latitude_x,s=5,marker='x',c='r')

plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.xticks(rotation=45,rotation_mode='anchor',ha='right')
ax.xaxis.set_major_formatter(FormatStrFormatter('%.0f'))
ax.yaxis.set_major_formatter(FormatStrFormatter('%.0f'))

plt.title('Third surveyed area')
plt.legend(['Garmin coordinates','Missing points'])

st3_unique=st3.drop_duplicates(subset=['PR'],ignore_index=True)
for el in range(len(st3_unique)):
    ax.text(st3_unique.iloc[el,2]-50,st3_unique.iloc[el,3]+50,int(st3_unique.at[el,'PR']),size=6)

plt.figtext(0.01,0.01,'Average GPS error: {}m\nPoints missing: {} out of {}'.format(avg_dist,points_missed,len(prn)),bbox = {'facecolor': 'oldlace', 'alpha': 0.8, 'pad': 3})
plt.grid()
plt.tight_layout()

plt.show()
