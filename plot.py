import seaborn as sns
import matplotlib.pyplot as plt
from Сличение import fil, prn
sns.set_style("darkgrid")
plt.scatter(fil.Longitude,fil.Latitude,s=0.1)
plt.scatter(prn[:,2],prn[:,3],s=0.1,marker='x')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Шамянская площадь')
plt.legend(['Garmin coordinates','Project coordinates'])
plt.show()
