import pandas as pd
from pathlib import Path
import numpy as np
import pyam
from pyam.plotting import OUTSIDE_LEGEND
import matplotlib.pyplot as plt
from pv_optimizer_contracting.new_model import model
from pprint import pprint 

output_file_path = Path(__file__).parent / 'data_output_new_model.csv'
#output_file_path_demand = Path(__file__).parent / 'data_output_demand.csv'

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




# data_supply_PV_contractor={'Model':['Contracting_model'],'Scenario':['Contracting_1'],'Region':'Supply PV Contractor','Variable':['Supply'],'Unit':['kW'],
# '1':[model.supply_new[1,'Contractor','PV'].value],'2':[model.supply_new[2,'Contractor','PV'].value],'3':[model.supply_new[3,'Contractor','PV'].value],'4':[model.supply_new[4,'Contractor','PV'].value],'5':[model.supply_new[5,'Contractor','PV'].value],'6':[model.supply_new[6,'Contractor','PV'].value],'7':[model.supply_new[7,'Contractor','PV'].value],'8':[model.supply_new[8,'Contractor','PV'].value],
# '9':[model.supply_new[9,'Contractor','PV'].value],'10':[model.supply_new[10,'Contractor','PV'].value],'11':[model.supply_new[11,'Contractor','PV'].value],'12':[model.supply_new[12,'Contractor','PV'].value],'13':[model.supply_new[13,'Contractor','PV'].value],'14':[model.supply_new[14,'Contractor','PV'].value],'15':[model.supply_new[15,'Contractor','PV'].value],
# '16':[model.supply_new[16,'Contractor','PV'].value],'17':[model.supply_new[17,'Contractor','PV'].value],'18':[model.supply_new[18,'Contractor','PV'].value],'19':[model.supply_new[19,'Contractor','PV'].value],'20':[model.supply_new[20,'Contractor','PV'].value],'21':[model.supply_new[21,'Contractor','PV'].value],'22':[model.supply_new[22,'Contractor','PV'].value],'23':[model.supply_new[23,'Contractor','PV'].value],'24':[model.supply_new[24,'Contractor','PV'].value]}

# data_supply_PV_to_HP={'Model':['Contracting_model'],'Scenario':['Contracting_1'],'Region':'Supply PV to HP','Variable':['Supply'],'Unit':['kW'],
# '1':[model.supply_from_PV[1,'Contractor','HP'].value],'2':[model.supply_from_PV[2,'Contractor','HP'].value],'3':[model.supply_from_PV[3,'Contractor','HP'].value],'4':[model.supply_from_PV[4,'Contractor','HP'].value],'5':[model.supply_from_PV[5,'Contractor','HP'].value],'6':[model.supply_from_PV[6,'Contractor','HP'].value],'7':[model.supply_from_PV[7,'Contractor','HP'].value],'8':[model.supply_from_PV[8,'Contractor','HP'].value],
# '9':[model.supply_from_PV[9,'Contractor','HP'].value],'10':[model.supply_from_PV[10,'Contractor','HP'].value],'11':[model.supply_from_PV[11,'Contractor','HP'].value],'12':[model.supply_from_PV[12,'Contractor','HP'].value],'13':[model.supply_from_PV[13,'Contractor','HP'].value],'14':[model.supply_from_PV[14,'Contractor','HP'].value],'15':[model.supply_from_PV[15,'Contractor','HP'].value],
# '16':[model.supply_from_PV[16,'Contractor','HP'].value],'17':[model.supply_from_PV[17,'Contractor','HP'].value],'18':[model.supply_from_PV[18,'Contractor','HP'].value],'19':[model.supply_from_PV[19,'Contractor','HP'].value],'20':[model.supply_from_PV[20,'Contractor','HP'].value],'21':[model.supply_from_PV[21,'Contractor','HP'].value],'22':[model.supply_from_PV[22,'Contractor','HP'].value],'23':[model.supply_from_PV[23,'Contractor','HP'].value],'24':[model.supply_from_PV[24,'Contractor','HP'].value]}

# data_supply_Grid_to_HP={'Model':['Contracting_model'],'Scenario':['Contracting_1'],'Region':'Supply Grid to HP','Variable':['Supply'],'Unit':['kW'],
# '1':[model.supply_to_HP[1,'Self financed','Electric Grid'].value],'2':[model.supply_to_HP[2,'Self financed','Electric Grid'].value],'3':[model.supply_to_HP[3,'Self financed','Electric Grid'].value],'4':[model.supply_to_HP[4,'Self financed','Electric Grid'].value],'5':[model.supply_to_HP[5,'Self financed','Electric Grid'].value],'6':[model.supply_to_HP[6,'Self financed','Electric Grid'].value],'7':[model.supply_to_HP[7,'Self financed','Electric Grid'].value],'8':[model.supply_to_HP[8,'Self financed','Electric Grid'].value],
# '9':[model.supply_to_HP[9,'Self financed','Electric Grid'].value],'10':[model.supply_to_HP[10,'Self financed','Electric Grid'].value],'11':[model.supply_to_HP[11,'Self financed','Electric Grid'].value],'12':[model.supply_to_HP[12,'Self financed','Electric Grid'].value],'13':[model.supply_to_HP[13,'Self financed','Electric Grid'].value],'14':[model.supply_to_HP[14,'Self financed','Electric Grid'].value],'15':[model.supply_to_HP[15,'Self financed','Electric Grid'].value],
# '16':[model.supply_to_HP[16,'Self financed','Electric Grid'].value],'17':[model.supply_to_HP[17,'Self financed','Electric Grid'].value],'18':[model.supply_to_HP[18,'Self financed','Electric Grid'].value],'19':[model.supply_to_HP[19,'Self financed','Electric Grid'].value],'20':[model.supply_to_HP[20,'Self financed','Electric Grid'].value],'21':[model.supply_to_HP[21,'Self financed','Electric Grid'].value],'22':[model.supply_to_HP[22,'Self financed','Electric Grid'].value],'23':[model.supply_to_HP[23,'Self financed','Electric Grid'].value],'24':[model.supply_to_HP[24,'Self financed','Electric Grid'].value]}

# data_supply_HP_Selffinanced={'Model':['Contracting_model'],'Scenario':['Contracting_1'],'Region':'Supply HP Self-financed','Variable':['Supply'],'Unit':['kW'],
# '1':[model.supply_new[1,'Self financed','HP'].value],'2':[model.supply_new[2,'Self financed','HP'].value],'3':[model.supply_new[3,'Self financed','HP'].value],'4':[model.supply_new[4,'Self financed','HP'].value],'5':[model.supply_new[5,'Self financed','HP'].value],'6':[model.supply_new[6,'Self financed','HP'].value],'7':[model.supply_new[7,'Self financed','HP'].value],'8':[model.supply_new[8,'Self financed','HP'].value],
# '9':[model.supply_new[9,'Self financed','HP'].value],'10':[model.supply_new[10,'Self financed','HP'].value],'11':[model.supply_new[11,'Self financed','HP'].value],'12':[model.supply_new[12,'Self financed','HP'].value],'13':[model.supply_new[13,'Self financed','HP'].value],'14':[model.supply_new[14,'Self financed','HP'].value],'15':[model.supply_new[15,'Self financed','HP'].value],
# '16':[model.supply_new[16,'Self financed','HP'].value],'17':[model.supply_new[17,'Self financed','HP'].value],'18':[model.supply_new[18,'Self financed','HP'].value],'19':[model.supply_new[19,'Self financed','HP'].value],'20':[model.supply_new[20,'Self financed','HP'].value],'21':[model.supply_new[21,'Self financed','HP'].value],'22':[model.supply_new[22,'Self financed','HP'].value],'23':[model.supply_new[23,'Self financed','HP'].value],'24':[model.supply_new[24,'Contractor','PV'].value]}


data_demand_charging={'Model':['Contracting_model'],'Scenario':['Contracting_1'],'Region':'Demand','Variable':['Demand - Charging'],'Unit':['kW'],
'1':[model.demand[1,'Car']],'2':[model.demand[2,'Car']],'3':[model.demand[3,'Car']],'4':[model.demand[4,'Car']],'5':[model.demand[5,'Car']],'6':[model.demand[6,'Car']],'7':[model.demand[7,'Car']],'8':[model.demand[8,'Car']],'9':[model.demand[9,'Car']],'10':[model.demand[10,'Car']],'11':[model.demand[11,'Car']],'12':[model.demand[12,'Car']],
'13':[model.demand[13,'Car']],'14':[model.demand[14,'Car']],'15':[model.demand[15,'Car']],'16':[model.demand[16,'Car']],'17':[model.demand[17,'Car']],'18':[model.demand[18,'Car']],'19':[model.demand[19,'Car']],'20':[model.demand[20,'Car']],'21':[model.demand[21,'Car']],'22':[model.demand[22,'Car']],'23':[model.demand[23,'Car']],'24':[model.demand[24,'Car']]}

data_demand_heating={'Model':['Contracting_model'],'Scenario':['Contracting_1'],'Region':'Demand','Variable':['Demand - Heating'],'Unit':['kW'],
'1':[model.demand[1,'Heating']],'2':[model.demand[2,'Heating']],'3':[model.demand[3,'Heating']],'4':[model.demand[4,'Heating']],'5':[model.demand[5,'Heating']],'6':[model.demand[6,'Heating']],'7':[model.demand[7,'Heating']],'8':[model.demand[8,'Heating']],'9':[model.demand[9,'Heating']],'10':[model.demand[10,'Heating']],'11':[model.demand[11,'Heating']],'12':[model.demand[12,'Heating']],
'13':[model.demand[13,'Heating']],'14':[model.demand[14,'Heating']],'15':[model.demand[15,'Heating']],'16':[model.demand[16,'Heating']],'17':[model.demand[17,'Heating']],'18':[model.demand[18,'Heating']],'19':[model.demand[19,'Heating']],'20':[model.demand[20,'Heating']],'21':[model.demand[21,'Heating']],'22':[model.demand[22,'Heating']],'23':[model.demand[23,'Heating']],'24':[model.demand[24,'Heating']]}

data_demand_DHW={'Model':['Contracting_model'],'Scenario':['Contracting_1'],'Region':'Demand','Variable':['Demand - DHW'],'Unit':['kW'],
'1':[model.demand[1,'Heating']],'2':[model.demand[2,'DHW']],'3':[model.demand[3,'DHW']],'4':[model.demand[4,'DHW']],'5':[model.demand[5,'DHW']],'6':[model.demand[6,'DHW']],'7':[model.demand[7,'DHW']],'8':[model.demand[8,'DHW']],'9':[model.demand[9,'DHW']],'10':[model.demand[10,'DHW']],'11':[model.demand[11,'DHW']],'12':[model.demand[12,'DHW']],
'13':[model.demand[13,'DHW']],'14':[model.demand[14,'DHW']],'15':[model.demand[15,'DHW']],'16':[model.demand[16,'DHW']],'17':[model.demand[17,'DHW']],'18':[model.demand[18,'DHW']],'19':[model.demand[19,'DHW']],'20':[model.demand[20,'DHW']],'21':[model.demand[21,'DHW']],'22':[model.demand[22,'DHW']],'23':[model.demand[23,'DHW']],'24':[model.demand[24,'DHW']]}

data_demand_electricity={'Model':['Contracting_model'],'Scenario':['Contracting_1'],'Region':'Demand','Variable':['Demand - Electricity'],'Unit':['kW'],
'1':[model.demand[1,'Electricity household']],'2':[model.demand[2,'Electricity household']],'3':[model.demand[3,'Electricity household']],'4':[model.demand[4,'Electricity household']],'5':[model.demand[5,'Electricity household']],'6':[model.demand[6,'Electricity household']],'7':[model.demand[7,'Electricity household']],'8':[model.demand[8,'Electricity household']],'9':[model.demand[9,'Electricity household']],'10':[model.demand[10,'Electricity household']],'11':[model.demand[11,'Electricity household']],'12':[model.demand[12,'Electricity household']],
'13':[model.demand[13,'Electricity household']],'14':[model.demand[14,'Electricity household']],'15':[model.demand[15,'Electricity household']],'16':[model.demand[16,'Electricity household']],'17':[model.demand[17,'Electricity household']],'18':[model.demand[18,'Electricity household']],'19':[model.demand[19,'Electricity household']],'20':[model.demand[20,'Electricity household']],'21':[model.demand[21,'Electricity household']],'22':[model.demand[22,'Electricity household']],'23':[model.demand[23,'Electricity household']],'24':[model.demand[24,'Electricity household']]}





# data_shifted_demand={'Model':['Contracting_model'],'Scenario':['Contracting_1'],'Region':[model.shifted_demand],'Variable':['Shifted Demand'],'Unit':['kW'],
# '1':[model.shifted_demand[1].value],'2':[model.shifted_demand[2].value],'3':[model.shifted_demand[3].value],'4':[model.shifted_demand[4].value],'5':[model.shifted_demand[5].value],'6':[model.shifted_demand[6].value],'7':[model.shifted_demand[7].value],'8':[model.shifted_demand[8].value],'9':[model.shifted_demand[9].value],'10':[model.shifted_demand[10].value],'11':[model.shifted_demand[11].value],'12':[model.shifted_demand[12].value],
# '13':[model.shifted_demand[13].value],'14':[model.shifted_demand[14].value],'15':[model.shifted_demand[15].value],'16':[model.shifted_demand[16].value],'17':[model.shifted_demand[17].value],'18':[model.shifted_demand[18].value],'19':[model.shifted_demand[19].value],'20':[model.shifted_demand[20].value],'21':[model.shifted_demand[21].value],'22':[model.shifted_demand[22].value],'23':[model.shifted_demand[23].value],'24':[model.shifted_demand[24].value]}

# data_irradiation={'Model':['Contracting_model'],'Scenario':['Contracting_1'],'Region':[model.irradiation_full_pv_area],'Variable':['Irradiation'],'Unit':['kW'],
# '1':[model.irradiation_full_pv_area[1]],'2':[model.irradiation_full_pv_area[2]],'3':[model.irradiation_full_pv_area[3]],'4':[model.irradiation_full_pv_area[4]],'5':[model.irradiation_full_pv_area[5]],'6':[model.irradiation_full_pv_area[6]],'7':[model.irradiation_full_pv_area[7]],'8':[model.irradiation_full_pv_area[8]],'9':[model.irradiation_full_pv_area[9]],'10':[model.irradiation_full_pv_area[10]],'11':[model.irradiation_full_pv_area[11]],'12':[model.irradiation_full_pv_area[12]],
# '13':[model.irradiation_full_pv_area[13]],'14':[model.irradiation_full_pv_area[14]],'15':[model.irradiation_full_pv_area[15]],'16':[model.irradiation_full_pv_area[16]],'17':[model.irradiation_full_pv_area[17]],'18':[model.irradiation_full_pv_area[18]],'19':[model.irradiation_full_pv_area[19]],'20':[model.irradiation_full_pv_area[20]],'21':[model.irradiation_full_pv_area[21]],'22':[model.irradiation_full_pv_area[22]],'23':[model.irradiation_full_pv_area[23]],'24':[model.demand[24]]}


# df_supply_PV_contractor= pd.DataFrame(data=data_supply_PV_contractor)
# df_supply_HP_Selffinanced=pd.DataFrame(data=data_supply_HP_Selffinanced)
# df_supply_PV_to_HP=pd.DataFrame(data=data_supply_PV_to_HP)
# df_supply_Grid_to_HP=pd.DataFrame(data=data_supply_Grid_to_HP)
df_demand_heating=pd.DataFrame(data=data_demand_heating)
df_demand_charging= pd.DataFrame(data=data_demand_charging)
df_demand_DHW=pd.DataFrame(data=data_demand_DHW)
df_demand_electricity=pd.DataFrame(data=data_demand_electricity)
# df_demand_shifted=pd.DataFrame(data=data_shifted_demand)
# df_irradiation=pd.DataFrame(data=data_irradiation)

#pd.concat([df_supply_grid,df_supply_contracting,df_supply_PV,df_demand,df_demand_shifted,df_irradiation]).to_csv(str(output_file_path),index=False)
#pd.concat([df_supply_PV_contractor,df_demand_charging,df_supply_PV_to_HP,df_supply_Grid_to_HP,df_demand_heating,df_supply_HP_Selffinanced,df_demand_DHW,df_demand_electricity]).to_csv(str(output_file_path),index=False)
pd.concat([df_demand_charging,df_demand_heating,df_demand_DHW,df_demand_electricity]).to_csv(str(output_file_path),index=False)


df = pyam.IamDataFrame(output_file_path)

# df_demand= pd.DataFrame(data=data_demand).to_csv(str(output_file_path_demand),index=False)
# df_demand = pyam.IamDataFrame(output_file_path_demand)

model, scenario = 'Contracting_model', 'Contracting_1'

data = df.filter(model=model, scenario=scenario)
# # data_demand = df_demand.filter(model=model, scenario=scenario)

# # data = (
# #     df.filter(model=model, scenario=scenario, variable='Supply_PV')
# #     .filter(region='Vienna')
# # )

# fig, ax = plt.subplots()
# df.plot(ax=ax, legend=True, color='region', title='Contracting model with DSM, shifting limited to 5kW',linewidth=2.5)
# a = ax.get_lines()
# #a[2].set_color(color)

# #a[6].set_linestyle('dotted')
# #a[5].set_linestyle('dashed')


# # df.plot(color='region', title='Test',ylabel='Time')#,legend=OUTSIDE_LEGEND['bottom'])
# # # df_demand.plot(color='region', title='Test',dashes=[6, 2])
# # #df.plot(color='region', title='Test', dashes=[6, 2])
# plt.xlabel('time [h]')
# plt.show()

# print(data.timeseries())

# args = dict(model='Contracting_model', scenario='Contracting_1')
# data = df.filter(**args, variable="'Demand - *", region="World")

data.plot.bar(stacked=True, title="Primary energy mix")
plt.legend(loc=1)
plt.tight_layout()
plt.show()
