import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from Сличение import project_coord, garmin_coord, measured_data

all = []

for row in garmin_coord:
    all.append([*project_coord[(abs(project_coord[:, 2] - row[0]) < 8) & (abs(project_coord[:, 3] - row[1]) < 8)][:, 0:2].flatten(), row[0], row[1]])
    if len(all[-1]) == 2:
        all.pop()
    elif len(all[-1]) == 6:
        all[-1].pop(0)
        all[-1].pop(0)

all = pd.DataFrame(all, columns=['PR', 'PK', 'Longitude', 'Latitude'])
all.drop_duplicates(subset=['PR', 'PK'], inplace=True, ignore_index=True)

project_coord = pd.DataFrame(project_coord, columns=['PR', 'PK', 'Longitude', 'Latitude'])
project_coord.drop_duplicates(subset=['PR', 'PK'], inplace=True, ignore_index=True)
ljoin = project_coord.merge(all, on=['PR', 'PK'], how='left')

points_missed = len(ljoin.loc[ljoin.Longitude_y.isnull()])
df_missing_points = ljoin.loc[ljoin.Longitude_y.isnull()]
avg_dist = round(
    np.sqrt((ljoin.Longitude_x - ljoin.Longitude_y) ** 2 + (ljoin.Latitude_x - ljoin.Latitude_y) ** 2).mean(), 2)

all.sort_values(['PR', 'PK'], inplace=True)
all = all.merge(measured_data, on=['PR', 'PK'], how='left')
all.fillna(method='bfill', inplace=True)
# all.to_csv('Шамян сличение 1-3.csv',float_format='%.1f',index=False)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

#ax1.scatter(df_missing_points.Longitude_x, df_missing_points.Latitude_x, s=5, marker='x', c='r',zorder=0)
resist = ax1.scatter(all.Longitude, all.Latitude, c=all.Resistivity, cmap='viridis_r', s=2.5)
polar = ax2.scatter(all.Longitude, all.Latitude, c=all.Polarization, cmap='seismic', s=2.5,vmin=-3,vmax=3)
for elem in (ax1, ax2):
    elem.set_xlabel('Longitude')
    elem.set_ylabel('Latitude')
    elem.tick_params(axis='x', labelrotation=45)
    elem.xaxis.set_major_formatter(FormatStrFormatter('%.0f'))
    elem.yaxis.set_major_formatter(FormatStrFormatter('%.0f'))
    elem.grid(alpha=0.5)
    elem.set_facecolor('lavender')
    elem.set_box_aspect(1)
    elem.set_xlim(20512000,20522000)
ax2.set_title('Apparent polarization, %')
ax1.set_title('Apparent resistivity, Ohm*m')

all_unique = all.drop_duplicates(subset=['PR'], ignore_index=True)
for el in range(len(all_unique)):
    ax1.text(all_unique.iloc[el, 2] - 55, all_unique.iloc[el, 3] + 50, int(all_unique.at[el, 'PR']), size=6)
    ax2.text(all_unique.iloc[el, 2] - 55, all_unique.iloc[el, 3] + 50, int(all_unique.at[el, 'PR']), size=6)
plt.figtext(0.46, 0.2, 'Average GPS error: {}m\nPoints missing: {} out of {}'.format(avg_dist, points_missed, len(project_coord)),
            bbox={'facecolor': 'oldlace', 'alpha': 0.6, 'pad': 3}, fontsize=7)
plt.tight_layout()

plt.colorbar(resist,fraction=0.035)
plt.colorbar(polar,fraction=0.035)
plt.suptitle('Survey  areas № 1-3')
plt.show()
