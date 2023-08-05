import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from Read import stage2, garn

prn=np.array(stage2)

st2=[]

for row in garn:
    st2.append([*prn[(abs(prn[:,2]-row[0])<8)&(abs(prn[:,3]-row[1])<8)][:,0:2].flatten(),row[0],row[1]])
    if len(st2[-1])==2:
        st2.pop()
    elif len(st2[-1])==6:
        st2[-1].pop(0)
        st2[-1].pop(0)

st2=pd.DataFrame(st2,columns=['PR','PK','Longitude','Latitude'])
st2.drop_duplicates(subset=['PR','PK'],inplace=True,ignore_index=True)
prn=pd.DataFrame(prn,columns=['PR','PK','Longitude','Latitude'])
ljoin=prn.merge(st2,on=['PR','PK'],how='left')

points_missed=len(ljoin.loc[ljoin.Longitude_y.isnull()])
avg_dist=round(np.sqrt((ljoin.Longitude_x-ljoin.Longitude_y)**2+(ljoin.Latitude_x-ljoin.Latitude_y)**2).mean(),2)

st2.sort_values(['PR','PK'],inplace=True)
#st2.to_csv('Шамян сличение 2.csv',float_format='%.1f',index=False)


fig,ax=plt.subplots()

plt.scatter(st2.Longitude,st2.Latitude,s=0.6)

plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.xticks(rotation=45,rotation_mode='anchor',ha='right')
ax.xaxis.set_major_formatter(FormatStrFormatter('%.0f'))
ax.yaxis.set_major_formatter(FormatStrFormatter('%.0f'))

plt.title('Second surveyed area')
plt.legend(['Garmin coordinates','Missing points'])
st2_unique=st2.drop_duplicates(subset=['PR'],ignore_index=True)
for el in range(len(st2_unique)):
    ax.text(st2_unique.iloc[el,2]-50,st2_unique.iloc[el,3]+50,int(st2_unique.at[el,'PR']),size=6)
plt.figtext(0.65,0.3,'Average GPS error: {}m\nPoints missing: {} out of {}'.format(avg_dist,points_missed,len(prn)),bbox = {'facecolor': 'oldlace', 'alpha': 0.8, 'pad': 3})
plt.grid()
plt.tight_layout()

plt.show()