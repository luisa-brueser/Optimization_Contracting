import pandas as pd
from pathlib import Path
import numpy as np
import pyam
from pyam.plotting import OUTSIDE_LEGEND
import matplotlib.pyplot as plt
# from pv_optimizer_contracting.new_model_copy import model
from new_model import model
from pprint import pprint

output_file_path = Path(__file__).parent / "data_output.csv"

######### created bar plot that shows newly installed capacities

# data_capacity_contractor = [
#     model.capacity["Contractor", "PV"].value,
#     model.capacity["Contractor", "ST"].value,
#     model.capacity["Contractor", "HP"].value,
#     model.capacity["Contractor", "Charging Station"].value,
# ]
# data_capacity_self_financed = [
#     model.capacity["Self financed", "PV"].value,
#     model.capacity["Self financed", "ST"].value,
#     model.capacity["Self financed", "HP"].value,
#     model.capacity["Self financed", "Charging Station"].value,
# ]
# labels = ["PV", "ST", "HP", "Charging Stations"]
# x = np.arange(len(labels))  # the label locations
# width = 0.35  # the width of the bars
# fig2, ax2 = plt.subplots()
# rects1 = ax2.bar(
#     x - width / 2, data_capacity_contractor, width, label="Capacity Contractor"
# )
# rects2 = ax2.bar(
#     x + width / 2, data_capacity_self_financed, width, label="Capacity Self financed"
# )

# ax2.set_ylabel("kW/m²/psc")
# ax2.set_title("New Technology investments")
# ax2.set_xticks(x)
# ax2.set_xticklabels(labels)
# ax2.legend()

# ax2.bar_label(rects1, padding=3)
# ax2.bar_label(rects2, padding=3)
# fig2.tight_layout()


data_template = {
    "Model": "Contracting_model",
    "Scenario": "Extreme 1",
    "Region": None,
    "Variable": None,
    "Unit": "kW",
}

results_demand = dict.fromkeys(model.set_demand)
for key in results_demand.keys():
    results_demand[key] = data_template.copy()
    results_demand[key]["Region"] = 'Vienna'
    results_demand[key]["Variable"] = ("Demand|"+str(key))

for option in results_demand.keys():
    for time in model.set_time:
        d = {time: model.demand[time, option]}
        results_demand[option].update(d)
df_results_demand = pd.DataFrame.from_dict(data=results_demand).T

results_capacity_new_contractor = dict.fromkeys(model.set_new_technologies)
for key in results_capacity_new_contractor.keys():
    results_capacity_new_contractor[key] = data_template.copy()
    results_capacity_new_contractor[key]["Region"] = 'Vienna'
    results_capacity_new_contractor[key]["Variable"] = ("Capacity|Contractor|"+str(key))

for option in results_capacity_new_contractor.keys():
    d = {0:model.capacity['Contractor',option].value}
    results_capacity_new_contractor[option].update(d)
df_results_capacity_new_contractor = pd.DataFrame.from_dict(data=results_capacity_new_contractor).T

results_capacity_new_self_financed = dict.fromkeys(model.set_new_technologies)
for key in results_capacity_new_self_financed.keys():
    results_capacity_new_self_financed[key] = data_template.copy()
    results_capacity_new_self_financed[key]["Region"] = 'Vienna'
    results_capacity_new_self_financed[key]["Variable"] = ("Capacity|Self financed|"+str(key))

for option in results_capacity_new_self_financed.keys():
    d = {0:model.capacity['Self financed',option].value}
    results_capacity_new_self_financed[option].update(d)
df_results_capacity_new_self_financed = pd.DataFrame.from_dict(data=results_capacity_new_self_financed).T


results_supply_contractor = dict.fromkeys(model.set_new_technologies)
for key in results_supply_contractor.keys():
    results_supply_contractor[key] = data_template.copy()
    results_supply_contractor[key]["Region"] = 'Vienna'
    results_supply_contractor[key]["Variable"] = ("Supply|Contractor|"+str(key))

for option in results_supply_contractor.keys():
    for time in model.set_time:
        d = {time: model.supply_new[time,'Contractor', option].value}
        results_supply_contractor[option].update(d)
df_results_supply_contractor = pd.DataFrame.from_dict(data=results_supply_contractor).T

results_supply_self_financed = dict.fromkeys(model.set_new_technologies)
for key in results_supply_self_financed.keys():
    results_supply_self_financed[key] = data_template.copy()
    results_supply_self_financed[key]["Region"] = key
    results_supply_self_financed[key]["Variable"] = ("Supply|Self financed|"+str(key))

for option in results_supply_self_financed.keys():
    for time in model.set_time:
        d = {time: model.supply_new[time,'Self financed', option].value}
        results_supply_self_financed[option].update(d)
df_results_supply_self_financed = pd.DataFrame.from_dict(data=results_supply_self_financed).T

results_supply_from_PV_self_financed = dict.fromkeys(model.set_PV2)
for key in results_supply_from_PV_self_financed.keys():
    results_supply_from_PV_self_financed[key] = data_template.copy()
    results_supply_from_PV_self_financed[key]["Region"] = key
    results_supply_from_PV_self_financed[key]["Variable"] = ("Supply from PV|Self financed|"+str(key))

for option in results_supply_from_PV_self_financed.keys():
    for time in model.set_time:
        d = {time: model.supply_from_PV[time,'Self financed',option].value}
        results_supply_from_PV_self_financed[option].update(d)
df_results_supply_from_PV_self_financed = pd.DataFrame.from_dict(data=results_supply_from_PV_self_financed).T

results_supply_from_PV_contractor = dict.fromkeys(model.set_PV2)
for key in results_supply_from_PV_contractor.keys():
    results_supply_from_PV_contractor[key] = data_template.copy()
    results_supply_from_PV_contractor[key]["Region"] = 'Vienna'
    results_supply_from_PV_contractor[key]["Variable"] = ("Supply from PV|Contractor|"+str(key))

for option in results_supply_from_PV_contractor.keys():
    for time in model.set_time:
        d = {time: model.supply_from_PV[time,'Contractor',option].value}
        results_supply_from_PV_contractor[option].update(d)
df_results_supply_from_PV_contractor = pd.DataFrame.from_dict(data=results_supply_from_PV_contractor).T







# all_results= {**results_supply_self_financed, **results_demand,}
#print('all_results: ', all_results)



df_all_results = pd.concat([df_results_demand,df_results_supply_contractor,\
    df_results_supply_self_financed,df_results_capacity_new_contractor,\
        df_results_capacity_new_self_financed,df_results_supply_from_PV_self_financed,df_results_supply_from_PV_contractor])

pd.concat([df_all_results]).to_csv(str(output_file_path), index=False) #mode='a'

# df = pyam.IamDataFrame(output_file_path)
df = pyam.IamDataFrame(df_all_results)
# print(df)

model, scenario = "Contracting_model", "Extreme 1"
###### created aggreated plot
# data = df.filter(model=model, scenario=scenario,variable='Supply|*')

# # df.aggregate_region("Supply*")
# data.plot.stack(stack="region")

### creates bar plot 
data_capacity = df.filter(variable="Capacity|*")

data_capacity.plot.bar(title="Installed Capacity")
plt.legend(loc=1)
plt.tight_layout()
# plt.show()

# fig, ax = plt.subplots()
data_supply = df.filter(model=model, scenario=scenario,variable='Supply|*')
data_supply.plot(
    #ax=ax, 
    legend=True, color="variable", title="Supply by grid, PV and HP", linewidth=2.5
)

data_supply_from_PV = df.filter(model=model, scenario=scenario,variable='Supply from PV|*')
data_supply_from_PV.plot(
    #ax=ax, 
    legend=True, color="variable", title="Supply from PV", linewidth=2.5
)


data_demand = df.filter(model=model, scenario=scenario,variable='Demand|*')
data_demand.plot(
    #ax=ax, 
    legend=True, color="variable", title="Demand", linewidth=2.5
)

# a = ax.get_lines()

plt.show()
