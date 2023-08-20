import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

all_stages_garmin=pd.read_csv('./transformed_data/all_stages_garmin.csv')
all_stages_project=pd.read_csv('./transformed_data/all_stages_project.csv')
measured_data=pd.read_csv('./transformed_data/measured_data.csv')

ljoin = all_stages_project.merge(all_stages_garmin, on=['PR', 'PK'], how='left')

points_missed = len(ljoin.loc[ljoin.Longitude_y.isnull()])
df_missing_points = ljoin.loc[ljoin.Longitude_y.isnull()]
avg_dist = round(
    np.sqrt((ljoin.Longitude_x - ljoin.Longitude_y) ** 2 + (ljoin.Latitude_x - ljoin.Latitude_y) ** 2).mean(), 2)

all_stages_garmin.sort_values(['PR', 'PK'], inplace=True)
all_stages_garmin = all_stages_garmin.merge(measured_data, on=['PR', 'PK'], how='left')
all_stages_garmin.fillna(method='bfill', inplace=True)
# all_stages_garmin.to_csv('Шамян сличение 1-3.csv',float_format='%.1f',index=False)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

ax1.scatter(df_missing_points.Longitude_x, df_missing_points.Latitude_x, s=5, marker='x', c='r',zorder=0)
resist = ax1.scatter(all_stages_garmin.Longitude, all_stages_garmin.Latitude, c=all_stages_garmin.Resistivity, cmap='viridis_r', s=2.5)
polar = ax2.scatter(all_stages_garmin.Longitude, all_stages_garmin.Latitude, c=all_stages_garmin.Polarization, cmap='seismic', s=2.5,vmin=-3,vmax=3)
for elem in (ax1, ax2):
    elem.set_xlabel('Longitude')
    elem.set_ylabel('Latitude')
    elem.tick_params(axis='x', labelrotation=45)
    elem.xaxis.set_major_formatter(FormatStrFormatter('%.0f'))
    elem.yaxis.set_major_formatter(FormatStrFormatter('%.0f'))
    elem.grid(alpha=0.5)
    elem.set_facecolor('lavender')
    elem.set_box_aspect(1)
    elem.set_xlim(20512000,20521000)
    elem.label_outer()
ax2.set_title('Apparent polarization, %')
ax1.set_title('Apparent resistivity, Ohm*m')

all_stages_garmin_unique = all_stages_garmin.drop_duplicates(subset=['PR'], ignore_index=True)
for el in range(len(all_stages_garmin_unique)):
    ax1.text(all_stages_garmin_unique.iloc[el, 2] - 55, all_stages_garmin_unique.iloc[el, 3] + 50, int(all_stages_garmin_unique.at[el, 'PR']), size=6)
    ax2.text(all_stages_garmin_unique.iloc[el, 2] - 55, all_stages_garmin_unique.iloc[el, 3] + 50, int(all_stages_garmin_unique.at[el, 'PR']), size=6)
plt.figtext(0.07, 0.17, 'Average GPS error: {}m\nPoints missing: {} out of {}'.format(avg_dist, points_missed, len(all_stages_project)),
            bbox={'facecolor': 'oldlace', 'alpha': 0.9, 'pad': 3}, fontsize=9)
plt.tight_layout()

plt.colorbar(resist,fraction=0.035)
plt.colorbar(polar,fraction=0.035)
plt.suptitle('Survey  areas № 1-3')
plt.show()
