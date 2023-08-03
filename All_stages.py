import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from Сличение import prn, garn, measured_data

all=[]

for row in garn:
    all.append([*prn[(abs(prn[:,2]-row[0])<8)&(abs(prn[:,3]-row[1])<8)][:,0:2].flatten(),row[0],row[1]])
    if len(all[-1])==2:
        all.pop()
    elif len(all[-1])==6:
        all[-1].pop(0)
        all[-1].pop(0)

all=pd.DataFrame(all,columns=['PR','PK','Longitude','Latitude'])
all.drop_duplicates(subset=['PR','PK'],inplace=True,ignore_index=True)
prn=pd.DataFrame(prn,columns=['PR','PK','Longitude','Latitude'])
prn.drop_duplicates(subset=['PR','PK'],inplace=True,ignore_index=True)
ljoin=prn.merge(all,on=['PR','PK'],how='left')

points_missed=len(ljoin.loc[ljoin.Longitude_y.isnull()])
df_missing_points=ljoin.loc[ljoin.Longitude_y.isnull()]
avg_dist=round(np.sqrt((ljoin.Longitude_x-ljoin.Longitude_y)**2+(ljoin.Latitude_x-ljoin.Latitude_y)**2).mean(),2)

all.sort_values(['PR','PK'],inplace=True)
all=all.merge(measured_data, on=['PR','PK'],how='left' )
#all.to_csv('Шамян сличение 1-3.csv',float_format='%.1f',index=False)

#plt.figure(figsize=(10, 10))
fig,ax=plt.subplots()


f=plt.scatter(all.Longitude,all.Latitude,c=all.Resistivity,cmap='viridis_r', s=2.5)
plt.scatter(df_missing_points.Longitude_x,df_missing_points.Latitude_x,s=5,marker='x',c='r')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.xticks(rotation=45,rotation_mode='anchor',ha='right')
ax.xaxis.set_major_formatter(FormatStrFormatter('%.0f'))
ax.yaxis.set_major_formatter(FormatStrFormatter('%.0f'))

plt.title('Survey  areas № 1-3')
plt.legend(['Missing points'])
all_unique=all.drop_duplicates(subset=['PR'],ignore_index=True)
for el in range(len(all_unique)):
    ax.text(all_unique.iloc[el,2]-55,all_unique.iloc[el,3]+50,int(all_unique.at[el,'PR']),size=6)
plt.figtext(0.6,0.23,'Average GPS error: {}m\nPoints missing: {} out of {}'.format(avg_dist,points_missed,len(prn)),bbox = {'facecolor': 'oldlace', 'alpha': 0.8, 'pad': 3},fontsize=7)
plt.grid(alpha=0.5)
plt.tight_layout()
plt.axis('equal')
plt.colorbar(f)
plt.clim(0,3)

plt.show()