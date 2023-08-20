import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import matplotlib.tri as tri
from mplcursors import cursor


all_stages_garmin=pd.read_csv('./transformed_data/all_stages_garmin.csv')
all_stages_project=pd.read_csv('./transformed_data/all_stages_project.csv')
measured_data=pd.read_csv('./transformed_data/measured_data.csv')

all_stages_garmin.sort_values(['PR', 'PK'], inplace=True)
all_stages_garmin = all_stages_garmin.merge(measured_data, on=['PR', 'PK'], how='left')
all_stages_garmin.fillna(method='bfill', inplace=True)
# all_stages_garmin.to_csv('Шамян сличение 1-3.csv',float_format='%.1f',index=False)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))


x = np.array(all_stages_garmin.Longitude)
y = np.array(all_stages_garmin.Latitude)
z_resist=np.array(all_stages_garmin.Resistivity)
z_polar=np.array(all_stages_garmin.Polarization)
triang = tri.Triangulation(x, y)

def apply_mask(triang, alpha=400):
    triangles = triang.triangles
    xtri = x[triangles] - np.roll(x[triangles], 1, axis=1)
    ytri = y[triangles] - np.roll(y[triangles], 1, axis=1)
    maxi = np.max(np.sqrt(xtri**2 + ytri**2), axis=1)
    triang.set_mask(maxi > alpha)
apply_mask(triang, alpha=300)

#ax1.scatter(df_missing_points.Longitude_x, df_missing_points.Latitude_x, s=5, marker='x', c='r',zorder=0)
resist = ax1.tricontourf(triang, z_resist,  cmap="gist_earth_r",vmax=3000,levels=40)
resist_points=ax1.scatter(x=all_stages_garmin.Longitude,
                          y=all_stages_garmin.Latitude,
                          s=0.3,c='k',alpha=0.6)

polar = ax2.tricontourf(triang, z_polar,  cmap="coolwarm",vmin=-2.6,vmax=2.6,levels=40)
polar_points=ax2.scatter(x=all_stages_garmin.Longitude,
                         y=all_stages_garmin.Latitude,
                         s=0.3,c='k',alpha=0.6)

cursor(resist_points, hover=True).connect(
        "add", lambda sel: sel.annotation.set_text(
            'PR {:.0f}\nPK {:.0f}\nRk={:.1f}Ohm*m'.format(all_stages_garmin.iloc[sel.index].PR,
                                                          all_stages_garmin.iloc[sel.index].PK,
                                                          all_stages_garmin.iloc[sel.index].Resistivity)))
cursor(polar_points, hover=True).connect(
        "add", lambda sel: sel.annotation.set_text(
            'PR {:.0f}\nPK {:.0f}\nPol-n={:.1f}%'.format(all_stages_garmin.iloc[sel.index].PR,
                                                         all_stages_garmin.iloc[sel.index].PK,
                                                         all_stages_garmin.iloc[sel.index].Polarization)))

for elem in (ax1, ax2):
    elem.set_xlabel('Longitude')
    elem.set_ylabel('Latitude')
    elem.tick_params(axis='x', labelrotation=45)
    elem.xaxis.set_major_formatter(FormatStrFormatter('%.0f'))
    elem.yaxis.set_major_formatter(FormatStrFormatter('%.0f'))
    elem.grid(alpha=0.5)
    elem.set_facecolor('lavender')
    elem.set_box_aspect(1)
    elem.set_ylim(5522000, 5532500)
    elem.set_xlim(20512000,20522000)
    elem.label_outer()

ax2.set_title('Apparent polarization, %',pad=5)
ax1.set_title('Apparent resistivity, Ohm*m',pad=5)

all_stages_garmin_unique = all_stages_garmin.drop_duplicates(subset=['PR'], ignore_index=True)
for el in range(len(all_stages_garmin_unique)):

    ax1.text(all_stages_garmin_unique.iloc[el, 2] - 55,
             all_stages_garmin_unique.iloc[el, 3] + 50,
             int(all_stages_garmin_unique.at[el, 'PR']), size=6)

    ax2.text(all_stages_garmin_unique.iloc[el, 2] - 55,
             all_stages_garmin_unique.iloc[el, 3] + 50,
             int(all_stages_garmin_unique.at[el, 'PR']), size=6)

plt.tight_layout()
plt.colorbar(resist,fraction=0.035)
plt.colorbar(polar,fraction=0.035)
plt.suptitle('Survey  areas № 1,3',fontsize=18)
plt.show()
