import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
stage3_garmin=pd.read_csv('./transformed_data/stage3_garmin.csv')
stage3_project=pd.read_csv('./transformed_data/stage3_project.csv')
measured_data=pd.read_csv('./transformed_data/measured_data.csv')


ljoin = stage3_project.merge(stage3_garmin, on=['PR', 'PK'], how='left')
points_missed = len(ljoin.loc[ljoin.Longitude_y.isnull()])
df_missing_points = ljoin.loc[ljoin.Longitude_y.isnull()]
avg_dist = round(
    np.sqrt((ljoin.Longitude_x - ljoin.Longitude_y) ** 2 + (ljoin.Latitude_x - ljoin.Latitude_y) ** 2).mean(), 2)

stage3_garmin.sort_values(['PR', 'PK'], inplace=True)
stage3_garmin = stage3_garmin.merge(measured_data, on=['PR', 'PK'], how='left')
stage3_garmin.fillna(method='bfill', inplace=True)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

ax1.scatter(df_missing_points.Longitude_x, df_missing_points.Latitude_x, s=10, marker='x', c='r',zorder=0)
ax2.scatter(df_missing_points.Longitude_x, df_missing_points.Latitude_x, s=10, marker='x', c='r',zorder=0)
resist = ax1.scatter(stage3_garmin.Longitude, stage3_garmin.Latitude, c=stage3_garmin.Resistivity, cmap='viridis_r', s=2.5)
polar = ax2.scatter(stage3_garmin.Longitude, stage3_garmin.Latitude, c=stage3_garmin.Polarization, cmap='seismic', s=2.5,vmin=-3,vmax=3)
for elem in (ax1, ax2):
    elem.set_xlabel('Longitude')
    elem.set_ylabel('Latitude')
    elem.tick_params(axis='x', labelrotation=45)
    elem.xaxis.set_major_formatter(FormatStrFormatter('%.0f'))
    elem.yaxis.set_major_formatter(FormatStrFormatter('%.0f'))
    elem.grid(alpha=0.5)
    elem.set_facecolor('lavender')
    elem.set_box_aspect(1)
    elem.set_ylim(5522000,5527000)

ax2.set_title('Apparent polarization, %')
ax1.set_title('Apparent resistivity, Ohm*m')

all_unique = stage3_garmin.drop_duplicates(subset=['PR'], ignore_index=True)
for el in range(len(all_unique)):
    ax1.text(all_unique.iloc[el, 2] - 55, all_unique.iloc[el, 3] + 50, int(all_unique.at[el, 'PR']), size=6)
    ax2.text(all_unique.iloc[el, 2] - 55, all_unique.iloc[el, 3] + 50, int(all_unique.at[el, 'PR']), size=6)
plt.figtext(0.46, 0.2, 'Average GPS error: {}m\nPoints missing: {} out of {}'.format(avg_dist, points_missed, len(stage3_project)),
            bbox={'facecolor': 'oldlace', 'alpha': 0.6, 'pad': 3}, fontsize=7)
plt.tight_layout()

plt.colorbar(resist,fraction=0.035)
plt.colorbar(polar,fraction=0.035)
plt.suptitle('Survey  area №3')
plt.show()
