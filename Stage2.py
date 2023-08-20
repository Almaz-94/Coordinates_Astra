import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

stage2_garmin=pd.read_csv('./transformed_data/stage2_garmin.csv')
stage2_project=pd.read_csv('./transformed_data/stage2_project.csv')
measured_data=pd.read_csv('./transformed_data/measured_data.csv')

ljoin=stage2_project.merge(stage2_garmin,on=['PR','PK'],how='left')

points_missed=len(ljoin.loc[ljoin.Longitude_y.isnull()])
avg_dist=round(np.sqrt((ljoin.Longitude_x-ljoin.Longitude_y)**2+(ljoin.Latitude_x-ljoin.Latitude_y)**2).mean(),2)

stage2_garmin.sort_values(['PR','PK'],inplace=True)
#stage2_garmin.to_csv('Шамян сличение 2.csv',float_format='%.1f',index=False)


fig,ax=plt.subplots()

plt.scatter(stage2_garmin.Longitude,stage2_garmin.Latitude,s=0.6)

plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.xticks(rotation=45,rotation_mode='anchor',ha='right')
ax.xaxis.set_major_formatter(FormatStrFormatter('%.0f'))
ax.yaxis.set_major_formatter(FormatStrFormatter('%.0f'))

plt.title('Survey area №2')
plt.legend(['Garmin coordinates','Missing points'])
stage2_garmin_unique=stage2_garmin.drop_duplicates(subset=['PR'],ignore_index=True)
for el in range(len(stage2_garmin_unique)):
    ax.text(stage2_garmin_unique.iloc[el,2]-50,
            stage2_garmin_unique.iloc[el,3]+50,
            int(stage2_garmin_unique.at[el,'PR']),size=6)
plt.figtext(0.65,0.3,'Average GPS error: {}m\nPoints missing: {} out of {}'.format(avg_dist,points_missed,len(stage2_project)),
            bbox = {'facecolor': 'oldlace', 'alpha': 0.8, 'pad': 3})
plt.grid()
plt.tight_layout()

plt.show()