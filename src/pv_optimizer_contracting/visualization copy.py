import pandas as pd
from pathlib import Path
import numpy as np
import pyam
from pyam.plotting import OUTSIDE_LEGEND
import matplotlib.pyplot as plt
from pv_optimizer_contracting.mymodel import model
from pprint import pprint

output_file_path = Path(__file__).parent / "data_output.csv"
# output_file_path_demand = Path(__file__).parent / 'data_output_demand.csv'

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

# data={'Model':['Contracting_model'],'Scenario':['Contracting_1'],'Region':['Vienna'],'Variable':['Supply_PV'],'Unit':['kW'],'0':[0],'4':[0],'8':[4],'12':[6],'16':[8],'20':[2],'24':[0]}
results_supply = dict.fromkeys(model.options)
# results["demand"] = None
# results["shifted_demand"] = None
# print("model.demand: ", model.demand)
# print("model.demand: ", model.shifted_demand)

results_demand = {
    "demand": None,
    "shifted_demand": None,
}


data_template = {
    "Model": "Contracting_model",
    "Scenario": "Contracting_1",
    "Region": None,
    "Variable": None,
    "Unit": "kW",
}

for key in results_demand.keys():
    results_demand[key] = data_template.copy()
    # results_demand["demand"]["Variable"] = "Shifted Demand"
    # results_demand["shifted_demand"]["Variable"] = "Demand"

for time in model.time:
    x = {time: model.demand[time]}
    # print("x: ", x)
    results_demand["demand"].update(x)
    


for time in model.time:
    d = {time: model.shifted_demand[time].value}
    results_demand["shifted_demand"].update(d)


for key in results_supply.keys():
    results_supply[key] = data_template
    results_supply[key]["Variable"] = "Supply"

for option in model.options:
    results_supply[option]["Region"] = option    
    for time in model.time:
        d = {time: model.supply[time, option].value}
        results_supply[option].update(d)
        

        # pprint(d)
# pprint(results_supply)

# df = pd.DataFrame.for(results_supply)

# for
new = {**results_supply, **results_demand}
df = pd.DataFrame.from_dict(data=new).T

# df_demand = pd.DataFrame.from_dict(data=demand)
# print("df: ", df)

# with open("test.csv", "w") as file:
#     # txt.write("string")
#     df.to_csv(file)

# for option in model.options:
#     for time in model.time:
#         d={time:[model.supply[time,option].value]}
# d.update(results[option])
# pd.DataFrame.from_dict(data=results[option])


# pprint(new)
# pprint(new)
##########
# for key,value in results.items():
#     results[key]=data_template
# for option in model.options:
#     for time in model.time:
#         d={time:[model.supply[time,option].value]}
#         results[option].update(d)
######

# pprint(d)
# pprint(results)

# data_results=pd.DataFrame.from_dict(data=results)
# print('data_results: ', data_results)
# pprint(data_results)


# result_supply_grid,result_supply_contracting,result_supply_PV

# results={k:v for k,v in model.options[k}


# pprint(results)
# for option in results:
#     data_results=pd.DataFrame.from_dict(data=results)


# print('data_results: ', data_results)

df = pyam.IamDataFrame(output_file_path)


model, scenario = 'Contracting_model', 'Contracting_1'

data = df.filter(model=model, scenario=scenario)

fig, ax = plt.subplots()
df.plot(ax=ax, legend=True, color='region', title='Contracting model with DSM, shifting limited to 5kW',linewidth=2.5)
# a = ax.get_lines()


# a[1].set_linestyle('dotted')
# a[2].set_linestyle('dashed')

plt.xlabel('time [h]')
# plt.show()

# print(data.timeseries())


# data_supply_grid={'Model':['Contracting_model'],'Scenario':['Contracting_1'],'Region':[model.options[1]],'Variable':['Supply'],'Unit':['kW'],
# '1':[model.supply[1,'Grid_Only'].value],'2':[model.supply[2,'Grid_Only'].value],'3':[model.supply[3,'Grid_Only'].value],'4':[model.supply[4,'Grid_Only'].value],'5':[model.supply[5,'Grid_Only'].value],'6':[model.supply[6,'Grid_Only'].value],'7':[model.supply[7,'Grid_Only'].value],'8':[model.supply[8,'Grid_Only'].value],
# '9':[model.supply[9,'Grid_Only'].value],'10':[model.supply[10,'Grid_Only'].value],'11':[model.supply[11,'Grid_Only'].value],'12':[model.supply[12,'Grid_Only'].value],'13':[model.supply[13,'Grid_Only'].value],'14':[model.supply[14,'Grid_Only'].value],'15':[model.supply[15,'Grid_Only'].value],
# '16':[model.supply[16,'Grid_Only'].value],'17':[model.supply[17,'Grid_Only'].value],'18':[model.supply[18,'Grid_Only'].value],'19':[model.supply[19,'Grid_Only'].value],'20':[model.supply[20,'Grid_Only'].value],'21':[model.supply[21,'Grid_Only'].value],'22':[model.supply[22,'Grid_Only'].value],'23':[model.supply[23,'Grid_Only'].value],'24':[model.supply[24,'Grid_Only'].value]}

# data_supply_contracting={'Model':['Contracting_model'],'Scenario':['Contracting_1'],'Region':[model.options[2]],'Variable':['Supply'],'Unit':['kW'],
# '1':[model.supply[1,'Pv_Contractor'].value],'2':[model.supply[2,'Pv_Contractor'].value],'3':[model.supply[3,'Pv_Contractor'].value],'4':[model.supply[4,'Pv_Contractor'].value],'5':[model.supply[5,'Pv_Contractor'].value],'6':[model.supply[6,'Pv_Contractor'].value],'7':[model.supply[7,'Pv_Contractor'].value],'8':[model.supply[8,'Pv_Contractor'].value],
# '9':[model.supply[9,'Pv_Contractor'].value],'10':[model.supply[10,'Pv_Contractor'].value],'11':[model.supply[11,'Pv_Contractor'].value],'12':[model.supply[12,'Pv_Contractor'].value],'13':[model.supply[13,'Pv_Contractor'].value],'14':[model.supply[14,'Pv_Contractor'].value],'15':[model.supply[15,'Pv_Contractor'].value],
# '16':[model.supply[16,'Pv_Contractor'].value],'17':[model.supply[17,'Pv_Contractor'].value],'18':[model.supply[18,'Pv_Contractor'].value],'19':[model.supply[19,'Pv_Contractor'].value],'20':[model.supply[20,'Pv_Contractor'].value],'21':[model.supply[21,'Pv_Contractor'].value],'22':[model.supply[22,'Pv_Contractor'].value],'23':[model.supply[23,'Pv_Contractor'].value],'24':[model.supply[24,'Pv_Contractor'].value]}

# data_supply_PV={'Model':['Contracting_model'],'Scenario':['Contracting_1'],'Region':[model.options[3]],'Variable':['Supply'],'Unit':['kW'],
# '1':[model.supply[1,'PV'].value],'2':[model.supply[2,'PV'].value],'3':[model.supply[3,'PV'].value],'4':[model.supply[4,'PV'].value],'5':[model.supply[5,'PV'].value],'6':[model.supply[6,'PV'].value],'7':[model.supply[7,'PV'].value],'8':[model.supply[8,'PV'].value],
# '9':[model.supply[9,'PV'].value],'10':[model.supply[10,'PV'].value],'11':[model.supply[11,'PV'].value],'12':[model.supply[12,'PV'].value],'13':[model.supply[13,'PV'].value],'14':[model.supply[14,'PV'].value],'15':[model.supply[15,'PV'].value],
# '16':[model.supply[16,'PV'].value],'17':[model.supply[17,'PV'].value],'18':[model.supply[18,'PV'].value],'19':[model.supply[19,'PV'].value],'20':[model.supply[20,'PV'].value],'21':[model.supply[21,'PV'].value],'22':[model.supply[22,'PV'].value],'23':[model.supply[23,'PV'].value],'24':[model.supply[24,'PV'].value]}

# data_demand={'Model':['Contracting_model'],'Scenario':['Contracting_1'],'Region':[model.demand],'Variable':['Demand'],'Unit':['kW'],
# '0':[model.demand[1]],'4':[model.demand[4]],'8':[model.demand[8]],'12':[model.demand[12]],'15':[model.demand[15]],
# '16':[model.demand[16]],'17':[model.demand[17]],'18':[model.demand[18]],'19':[model.demand[19]],'20':[model.demand[20]],'24':[model.demand[24]]}

# data_shifted_demand={'Model':['Contracting_model'],'Scenario':['Contracting_1'],'Region':[model.shifted_demand],'Variable':['Shifted Demand'],'Unit':['kW'],
# '0':[model.shifted_demand[1].value],'4':[model.shifted_demand[4].value],'8':[model.shifted_demand[8].value],'12':[model.shifted_demand[12].value],'15':[model.shifted_demand[15].value],
# '16':[model.shifted_demand[16].value],'17':[model.shifted_demand[17].value],'18':[model.shifted_demand[18].value],'19':[model.shifted_demand[19].value],'20':[model.shifted_demand[20].value],'24':[model.shifted_demand[24].value]}

# data_irradiation={'Model':['Contracting_model'],'Scenario':['Contracting_1'],'Region':[model.irradiation_full_pv_area],'Variable':['Irradiation'],'Unit':['kW'],
# '0':[model.irradiation_full_pv_area[1]],'4':[model.irradiation_full_pv_area[4]],'8':[model.irradiation_full_pv_area[8]],'12':[model.irradiation_full_pv_area[12]],'15':[model.irradiation_full_pv_area[15]],
# '16':[model.irradiation_full_pv_area[16]],'17':[model.irradiation_full_pv_area[17]],'18':[model.irradiation_full_pv_area[18]],'19':[model.irradiation_full_pv_area[19]],'20':[model.irradiation_full_pv_area[20]],'24':[model.irradiation_full_pv_area[24]]}

# df_supply_grid = pd.DataFrame(data=data_supply_grid)
# df_supply_contracting = pd.DataFrame(data=data_supply_contracting)
# df_supply_PV = pd.DataFrame(data=data_supply_PV)
# df_demand= pd.DataFrame(data=data_demand)
# df_demand_shifted=pd.DataFrame(data=data_shifted_demand)
# df_irradiation=pd.DataFrame(data=data_irradiation)

# pd.concat([df_supply_grid,df_supply_contracting,df_supply_PV,df_demand,df_demand_shifted,df_irradiation]).to_csv(str(output_file_path),index=False)


# df = pyam.IamDataFrame(output_file_path)

# # df_demand= pd.DataFrame(data=data_demand).to_csv(str(output_file_path_demand),index=False)
# # df_demand = pyam.IamDataFrame(output_file_path_demand)

# model, scenario = 'Contracting_model', 'Contracting_1'

# data = df.filter(model=model, scenario=scenario)
# # data_demand = df_demand.filter(model=model, scenario=scenario)

# # data = (
# #     df.filter(model=model, scenario=scenario, variable='Supply_PV')
# #     .filter(region='Vienna')
# # )

# fig, ax = plt.subplots()
# df.plot(ax=ax, legend=True, color='region', title='Contracting model',linewidth=2.5)
# a = ax.get_lines()
# #a[2].set_color(color)

# a[3].set_linestyle('dashed')
# a[5].set_linestyle('dashed')


# # df.plot(color='region', title='Test',ylabel='Time')#,legend=OUTSIDE_LEGEND['bottom'])
# # # df_demand.plot(color='region', title='Test',dashes=[6, 2])
# # #df.plot(color='region', title='Test', dashes=[6, 2])
# plt.xlabel('time [h]')
# plt.show()

# print(data.timeseries())




#