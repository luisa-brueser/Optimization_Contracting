import pandas as pd
from pathlib import Path
import numpy as np
import pyam
import matplotlib.pyplot as plt
from mymodel import *

output_file_path = Path(__file__).parent / 'data_output.csv'
#cur_dir=Path.cwd()
#csv_path=str(cur_dir)+"\\..\\Dataset\\data_output_test.csv"

# df = pyam.IamDataFrame(output_file_path)
# df

# model, scenario = 'Luisa', 'Contracting1'

# # data = (
# #     df.filter(model=model, scenario=scenario, variable='Supply_PV')
# #     .filter(region='Vienna')
# # )

# df.plot(color='region', title='Test')

# plt.show()
# print(data.timeseries())

#data={'Model':['Contracting_model'],'Scenario':['Contracting_1'],'Region':['Vienna'],'Variable':['Supply_PV'],'Unit':['kW'],'0':[0],'4':[0],'8':[4],'12':[6],'16':[8],'20':[2],'24':[0]}
data_supply_grid={'Model':['Contracting_model'],'Scenario':['Contracting_1'],'Region':[model.options[1]],'Variable':['Supply'],'Unit':['kW'],
'0':[model.supply[1,'Grid_Only'].value],'4':[model.supply[4,'Grid_Only'].value],'8':[model.supply[8,'Grid_Only'].value],'12':[model.supply[12,'Grid_Only'].value],'15':[model.supply[15,'Grid_Only'].value],
'16':[model.supply[16,'Grid_Only'].value],'17':[model.supply[17,'Grid_Only'].value],'18':[model.supply[18,'Grid_Only'].value],'19':[model.supply[19,'Grid_Only'].value],'20':[model.supply[20,'Grid_Only'].value],'24':[model.supply[24,'Grid_Only'].value]}

data_supply_contracting={'Model':['Contracting_model'],'Scenario':['Contracting_1'],'Region':[model.options[2]],'Variable':['Supply'],'Unit':['kW'],
'0':[model.supply[1,'Pv_Contractor'].value],'4':[model.supply[4,'Pv_Contractor'].value],'8':[model.supply[8,'Pv_Contractor'].value],'12':[model.supply[12,'Pv_Contractor'].value],'15':[model.supply[15,'Pv_Contractor'].value],
'16':[model.supply[16,'Pv_Contractor'].value],'17':[model.supply[17,'Pv_Contractor'].value],'18':[model.supply[18,'Pv_Contractor'].value],'19':[model.supply[19,'Pv_Contractor'].value],'20':[model.supply[20,'Pv_Contractor'].value],'24':[model.supply[24,'Pv_Contractor'].value]}

data_demand={'Model':['Contracting_model'],'Scenario':['Contracting_1'],'Region':[model.demand],'Variable':['Demand'],'Unit':['kW'],
'0':[model.demand[1]],'4':[model.demand[4]],'8':[model.demand[8]],'12':[model.demand[12]],'15':[model.demand[15]],
'16':[model.demand[16]],'17':[model.demand[17]],'18':[model.demand[18]],'19':[model.demand[19]],'20':[model.demand[20]],'24':[model.demand[24]]}

data_irradiation={'Model':['Contracting_model'],'Scenario':['Contracting_1'],'Region':[model.irradiation_full_pv_area],'Variable':['Irradiation'],'Unit':['kW'],
'0':[model.irradiation_full_pv_area[1]],'4':[model.irradiation_full_pv_area[4]],'8':[model.irradiation_full_pv_area[8]],'12':[model.irradiation_full_pv_area[12]],'15':[model.irradiation_full_pv_area[15]],
'16':[model.irradiation_full_pv_area[16]],'17':[model.irradiation_full_pv_area[17]],'18':[model.irradiation_full_pv_area[18]],'19':[model.irradiation_full_pv_area[19]],'20':[model.irradiation_full_pv_area[20]],'24':[model.irradiation_full_pv_area[24]]}



df_supply_grid = pd.DataFrame(data=data_supply_grid)
df_supply_contracting = pd.DataFrame(data=data_supply_contracting)
df_demand= pd.DataFrame(data=data_demand)
df_irradiation=pd.DataFrame(data=data_irradiation)

pd.concat([df_supply_grid,df_supply_contracting,df_demand,df_irradiation]).to_csv(str(output_file_path),index=False)




df = pyam.IamDataFrame(output_file_path)
df

model, scenario = 'Contracting_model', 'Contracting_1'

data = df.filter(model=model, scenario=scenario)


# data = (
#     df.filter(model=model, scenario=scenario, variable='Supply_PV')
#     .filter(region='Vienna')
# )

df.plot(color='region', title='Test')

plt.show()
print(data.timeseries())

