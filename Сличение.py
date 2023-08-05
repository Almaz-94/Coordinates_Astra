import pandas as pd
import numpy as np
import os
pd.options.display.float_format = '{:.3f}'.format
np.set_printoptions(suppress=True, precision=2)
baza=pd.ExcelFile('.\Исходные данные\База Шамян+доп.xlsx')
stage1=pd.read_excel(baza, 'gph_200_50_stage', usecols = [0,1,3,4])
#stage2=pd.read_excel(baza, "SM_200_50_pirit_WGS84", usecols = [0, 1, 3, 4])
stage3=pd.read_excel(baza, 'gph_200_50_stage_3', usecols = [0,1,3,4])
project=pd.concat([stage1,stage3]) #,stage2

garmin=pd.read_excel('.\Исходные данные\Гармин Shamyan_Pl_01_80_s_pulkovo.xlsx',usecols=[3,4])

project_coord=np.array(project)
garmin_coord=np.array(garmin)

files=os.listdir('./Исходные данные/Планшеты 1-72')
temp=[]
for file in files:
    data=pd.read_excel('./Исходные данные/Планшеты 1-72/'+file,usecols=[0,1,4,5])
    temp.append(data)
measured_data=pd.concat(temp,ignore_index=True)

measured_data.rename(columns={"ПР":'PR' ,'ПК':'PK','Рк':'Resistivity',"Заряжаемость":'Polarization'},inplace=True)
measured_data.drop_duplicates(subset=['PR','PK'],inplace=True,ignore_index=True)
measured_data.sort_values(['PR','PK'],inplace=True)
measured_data.PR=measured_data.loc[:,'PR']/100
measured_data.PK=measured_data.loc[:,'PK']/10
#measured_data.Polarization=measured_data.loc[:,'Polarization']+2
#measured_data.to_csv('III.csv',index=False)
