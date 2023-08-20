import pandas as pd
import numpy as np
import os
pd.options.display.float_format = '{:.3f}'.format
np.set_printoptions(suppress=True, precision=2)
baza=pd.ExcelFile('.\Исходные данные\База Шамян+доп.xlsx')
stage1_project=pd.read_excel(baza, 'gph_200_50_stage', usecols = [0,1,3,4])
stage2_project=pd.read_excel(baza, "SM_200_50_pirit_WGS84", usecols = [0, 1, 3, 4])
stage3_project=pd.read_excel(baza, 'gph_200_50_stage_3', usecols = [0,1,3,4])
all_stages_project=pd.concat([stage1_project,stage3_project]) #,stage2

garmin=pd.read_excel('.\Исходные данные\Гармин Shamyan_Pl_01_80_s_pulkovo.xlsx',usecols=[3,4])

garmin_coord=np.array(garmin)


def compare_garmin_project(project_stage, garmin_coord):
    project_stage=np.array(project_stage)
    stage = []
    for row in garmin_coord:
        stage.append([*project_stage[(abs(project_stage[:, 2] - row[0]) < 8) &
                                     (abs(project_stage[:, 3] - row[1]) < 8)][:, 0:2].flatten(),
                                     row[0], row[1]])
        if len(stage[-1]) == 2:
            stage.pop()
        elif len(stage[-1]) == 6:
            stage[-1].pop(0)
            stage[-1].pop(0)
    stage=pd.DataFrame(stage, columns=['PR', 'PK', 'Longitude', 'Latitude'])
    stage.drop_duplicates(subset=['PR', 'PK'], inplace=True, ignore_index=True)
    return stage
stage1_garmin=compare_garmin_project(stage1_project,garmin_coord)
stage2_garmin=compare_garmin_project(stage2_project,garmin_coord)
stage3_garmin=compare_garmin_project(stage3_project,garmin_coord)
all_stages_garmin=compare_garmin_project(all_stages_project,garmin_coord)

stage1_garmin.to_csv('./transformed_data/stage1_garmin.csv',index=False)
stage2_garmin.to_csv('./transformed_data/stage2_garmin.csv',index=False)
stage3_garmin.to_csv('./transformed_data/stage3_garmin.csv',index=False)
all_stages_garmin.to_csv('./transformed_data/all_stages_garmin.csv',index=False)

for df in stage1_project,stage2_project,stage3_project,all_stages_project:
    df.rename(columns={'X_42':'Longitude','Y_42':'Latitude'},inplace=True)
stage1_project.to_csv('./transformed_data/stage1_project.csv',index=False)
stage2_project.to_csv('./transformed_data/stage2_project.csv',index=False)
stage3_project.to_csv('./transformed_data/stage3_project.csv',index=False)
all_stages_project.to_csv('./transformed_data/all_stages_project.csv',index=False)



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
measured_data.to_csv('./transformed_data/measured_data.csv',index=False)
