import pandas as pd
from pathlib import Path
import numpy as np
from pandas.core.frame import DataFrame
from pandas.io.formats.format import TextAdjustment
import pyam as py
from pyam.plotting import OUTSIDE_LEGEND
import matplotlib.pyplot as plt
import plotly
from collections import Counter
import matplotlib.ticker as mtick
import os
import matplotlib.patches as mpatches

from pprint import pprint



output_file_path = Path(__file__).parent / "data_output_one_month_30_household_30_cars_25kWh_scenario3_test.csv"

# output_file_path = Path(__file__).parent / "data_output_one_month_30_household_30_cars_25kWh_scenario3_no_DSM.csv"
# output_file_path = Path(__file__).parent / "data_output_one_year_30_household_30_cars_25kWh_scenario3_24h.csv"
# output_file_path_2=Path(__file__).parent / "data_output_one_year_30_household_30_cars_25kWh_scenario3_24h_summer.csv"

# output_file_path_comparison = Path(__file__).parent / "data_output_one_year_30_household_3_cars_140kWh_scenario1_85%_inv_cost.csv"
# output_file_path_comparison_2 = Path(__file__).parent / "data_output_one_year_30_household_3_cars_140kWh_scenario1_60%_inv_cost.csv"
# output_file_path_comparison = Path(__file__).parent /  "data_output_one_year_30_household_3_cars_140kWh_scenario1_CO_70_HP.csv"
# output_file_path_comparison_2 =Path(__file__).parent /  "data_output_one_year_30_household_3_cars_140kWh_scenario1_CO_115_HP.csv"
# output_file_path_comparison_3 = Path(__file__).parent / "data_output_one_year_30_household_3_cars_140kWh_scenario1_CO_200_HP.csv"
# output_file_path_comparison_4 = Path(__file__).parent / "data_output_one_year_30_household_3_cars_140kWh_scenario1_CO_250_HP.csv"
# output_file_path_comparison_DH = Path(__file__).parent / "data_output_one_year_30_household_3_cars_140kWh_scenario1_DH.csv"

dir_name='C:\\Users\\Thomas\\OneDrive\\Desktop\\DA\\Bilder_Ergebnisse\\'
folder_path='Scenario_3'



df = py.IamDataFrame(output_file_path)
# df_comparison = py.IamDataFrame(output_file_path_comparison)
# df_comparison_2 = py.IamDataFrame(output_file_path_comparison_2)
# df_comparison_3 = py.IamDataFrame(output_file_path_comparison_3)
# df_comparison_4 = py.IamDataFrame(output_file_path_comparison_4)
# df_comparison_DH = py.IamDataFrame(output_file_path_comparison_DH)
# df = py.IamDataFrame(df_all_results)
# # print(df)

model, scenario = "Contracting_model", "Scenario 3 no DSM"
# model, scenario = "Contracting_model", "Scenario 3 24h"
# model_2, scenario_2 = "Contracting_model", "Scenario 3 24h summer"
# model_comparison, scenario_comparison = "Contracting_model", "Scenario 1 85% inv cost"
# model_comparison_2, scenario_comparison_2 = "Contracting_model", "Scenario 1 60% inv cost"
# model_comparison, scenario_comparison = "Contracting_model", "Scenario 1 CO 70 HP"
# model_comparison_2, scenario_comparison_2 = "Contracting_model", "Scenario 1 CO 115 HP"
# model_comparison_3, scenario_comparison_3 = "Contracting_model", "Scenario 1 CO 200 HP"
# model_comparison_4, scenario_comparison_4 = "Contracting_model", "Scenario 1 CO 250 HP"
# model_comparison_DH, scenario_comparison_DH = "Contracting_model", "Scenario 1 force DH"
#################### defining colors
colors_default = ["tab:blue", "tab:cyan", "darkgrey"]
colors_new = [
    "forestgreen",
    "orange",
    "fuchsia",
    "crimson",
    "tab:gray",
    "limegreen",
    "burlywood",
    "violet",
    "indianred",
    "dimgray",
]
colors_self_finance = "tab:purple"
colors_contractor = "mediumblue"
colors_all = [
    "tab:blue",
    "tab:cyan",
    "darkgrey",
    "forestgreen",
    "orange",
    "fuchsia",
    "crimson",
    "tab:gray",
    "limegreen",
    "burlywood",
    "violet",
    "indianred",
    "dimgray",
]

#### line plot showing demand and shifted demand

# data_demand= df.filter(
#     model=model,
#     scenario=scenario,
#     variable=["Demand|*"],
# )


# data_supply_default= df.filter(
#     model=model,
#     scenario=scenario,
#     variable=["Supply default|Self financed|*"],
# )

# data_supply_PV= df.filter(
#     model=model,
#     scenario=scenario,
#     variable=["Supply|Contractor|PV"], 
# )


# x=np.arange(24)



# y_demand_car = data_demand.filter(variable="Demand|Car").data["value"]
# y_demand_car=y_demand_car.to_numpy()
# y_demand_shifted = data_demand.filter(variable="Demand|Shifted Demand").data["value"]
# y_demand_shifted=y_demand_shifted.to_numpy()
# y_demand_electricity_household = data_demand.filter(variable="Demand|Electricity household").data["value"]
# y_demand_electricity_household=y_demand_electricity_household.to_numpy()
# y_supply_electricity_grid = data_supply_default.filter(variable="Supply default|Self financed|Electricity").data["value"]
# y_supply_electricity_grid=y_supply_electricity_grid.to_numpy()
# y_supply_PV = data_supply_PV.filter(variable="Supply|Contractor|PV").data["value"]
# # y_supply_PV=y_supply_PV.to_numpy()
# print('y_supply_PV: ', y_supply_PV)


# y_demand_car  = df.filter(model=model, scenario=scenario, variable="Demand|Car")
# y_demand_shifted  = df.filter(model=model, scenario=scenario, variable="Demand|Shifted Demand")
# y_demand_electricity_household  = df.filter(model=model, scenario=scenario, variable="Demand|Electricity household")
# y_supply_electricity_grid  = df.filter(model=model, scenario=scenario, variable="Supply default|Self financed|Electricity")
# y_supply_PV  = df.filter(model=model, scenario=scenario, variable="Supply|Contractor|PV")

# y_demand_car.plot(label = "Car demand")
# y_demand_shifted.plot(label = "Shifted demand")
# y_demand_electricity_household.plot( label = "Electricity household")
# y_supply_electricity_grid.plot(label = "Electricity grid")
# y_supply_PV.plot(label = "Supply PV")

# fig, ax = plt.subplots()

# ax.plot(x, y_demand_car, label = "Car demand")
# ax.plot(x, y_demand_shifted, label = "Shifted demand")
# ax.plot(x, y_demand_electricity_household, label = "Electricity household")
# ax.plot(x, y_supply_electricity_grid, label = "Electricity grid")
# ax.plot(x, y_supply_PV, label = "Supply PV")
# ax.legend()

# name_figure=folder_path+'_shifted_demand.eps'
# fig.savefig(os.path.join(dir_name,folder_path+"\\"+name_figure))




# plt.show()


# model, scenario = "REMIND-MAgPIE 1.7-3.0", "CD-LINKS_INDCi"

# data = df.filter(model=model, scenario=scenario, variable="Supply|Contractor|PV").data["value"]
# # df_new = py.IamDataFrame(data)
# print('df_new: ', df_new)
# print('data: ', data)

# data=df.filter(model=model, scenario=scenario, variable=["Demand|Car","Demand|Shifted Demand","Demand|Electricity household","Supply default|Self financed|Electricity","Supply|Contractor|PV"])

# fig, ax = plt.subplots()

# data.plot(ax=ax, legend=True, color="variable")
# ax.set_title(None)
# ax.set_ylabel('Supply in kW')
# ax.set_xlabel('Hour')
# name_figure=folder_path+'_24h_DSM.eps'
# fig.savefig(os.path.join(dir_name,folder_path+"\\"+name_figure))


# data_summer=df.filter(model=model_2, scenario=scenario_2, variable=["Demand|Car","Demand|Shifted Demand","Demand|Electricity household","Supply default|Self financed|Electricity","Supply|Contractor|PV"])

# fig, ax = plt.subplots()

# data.plot(ax=ax, legend=True, color="variable")
# ax.set_title(None)
# ax.set_ylabel('Supply in kW')
# ax.set_xlabel('Hour')
# name_figure=folder_path+'_24h_DSM_summer.eps'
# fig.savefig(os.path.join(dir_name,folder_path+"\\"+name_figure))


################

################ comparing costs contractor and tenants

# data_costs_revenue = df.filter(
#     model=model,
#     scenario=scenario,
#     variable=["Cost|*","Revenue"])

# data_costs_revenue_contractor = df.filter(
#     model=model,
#     scenario=scenario,
#     variable=["Cost Contractor|*","Revenue Contractor"])


# variables_cost= data_costs_revenue.filter(variable="Cost|*").variable
# x_labels_cost = [string.split("|")[1] for string in variables_cost]+['Revenue']
# total=x_labels_cost[3]
# x_labels_cost[3]=x_labels_cost[5]
# x_labels_cost[5]=total
# # y_comparison = data_costs_revenue_comparison.data["value"]
# # # y_min_CO = data_costs_revenue_min_CO2.data["value"]

# y_value_tenant = data_costs_revenue.data["value"]
# total=y_value_tenant[3]
# y_value_tenant[3]=y_value_tenant[5]
# y_value_tenant[5]=total


# y_value_contractor = data_costs_revenue_contractor.data["value"]
# total=y_value_contractor[3]
# y_value_contractor[3]=y_value_contractor[5]
# y_value_contractor[5]=total

# investment=52000-y_value_contractor[1]
# initial_investment= [0,investment,0,0,0,0]


# #y_value_contractor[1]=52000

# # # y_self_financed[2] = 5
# # # y_self_financed[3] = 20
# x = np.arange(len(x_labels_cost))
# width = 0.3  # the width of the bars: can also be len(x) sequence

# # # plt.style.use("science")
# fig, ax = plt.subplots()
# rects1 = ax.bar(
#     x- width/2, y_value_tenant , width, label="Costs/Revenues tenants",
# )
# rects2 =ax.bar(x + width/2, y_value_contractor, width, label="Costs/Revenues contractor",
# )
# rects3 =ax.bar(x + width/2, initial_investment, width, bottom=y_value_contractor, label="Total investment", color='lightsalmon'
# )


# ax.annotate("Annuity", xy=(1.1, 10), xytext=(0.3,11000),
#         arrowprops=dict(arrowstyle="->"))
#             #arrowprops=dict(facecolor='black', shrink=0.6))



# # rects3 =ax.bar(x - width,y_min_CO,width,label="Min CO2 scenario",color="cornflowerblue",
# # )
# ax.axhline(0, 0,1, linestyle="--",color='k')
# ax.set_ylabel('Yealy costs in €')
# # ax.set_title('Yearly costs for contractor and tenants')
# ax.set_xticks(x)
# ax.set_xticklabels(x_labels_cost)
# ax.legend(loc=(0.02, 0.55))
# ax.set_ylim(-20000, 60000)

# ax.text(0.91,52300,'52000')
# ax.bar_label(rects1, padding=1)
# ax.bar_label(rects2, padding=1)
# # ax.bar_label(rects3, padding=1)
# # ax.bar_label(rects3, padding=3)

# name_figure=folder_path+'_comparison_costs_tenants_contractor.eps'
# fig.savefig(os.path.join(dir_name,folder_path+"\\"+name_figure), bbox_inches='tight')


#### new capacities stacked bar plot
data_capacitiy_new = df.filter(
    model=model,
    scenario=scenario,
    variable=["Capacity|Self financed|*", "Capacity|Contractor|*","Reduction Heating Demand|*"],
)

variables_new_tech = data_capacitiy_new.filter(
    variable="Capacity|Self financed|*"
).variable
x_labels = [string.split("|")[2] for string in variables_new_tech] + ["Reduction \n Heating Demand" ]
x_labels[1]="Charging \n Station" 


y_self_financed = data_capacitiy_new.filter(variable="Capacity|Self financed|*").data["value"]
y_self_financed_insulation = data_capacitiy_new.filter(variable=["Reduction Heating Demand|Self financed"]).data["value"]
y_self_financed.loc[len(y_self_financed.index)] = 0
y_self_financed_insu= y_self_financed.copy()
y_self_financed_insu.loc[1:4] = 0 
y_self_financed_insu[5]=y_self_financed_insulation


y_contractor = data_capacitiy_new.filter(variable="Capacity|Contractor|*").data["value"]
y_contractor_insulation = data_capacitiy_new.filter(variable=["Reduction Heating Demand|Contractor"]).data["value"]

y_contractor.loc[len(y_contractor.index)] = 0
y_contractor_insu= y_contractor.copy()
y_contractor_insu.loc[1:4] = 0 
y_contractor_insu[5]=y_contractor_insulation

# y_contractor[2] = 5
# y_contractor[3] = 5
width =0.35  # the width of the bars: can also be len(x) sequence
# plt.style.use("science")

fig, ax = plt.subplots()
ax2 = ax.twinx() 
# ax.set_ylim(0, 50)
ax2.set_ylim(0, 100)
ax.set_ylabel('New capacities in kW/kWh/psc.')
ax2.set_ylabel('Reduction heating demand in %')
x = np.arange(len(x_labels))

p1 = ax.bar(x , y_self_financed, width=width, align='center', color=colors_self_finance,  label='financed without contractor')
p2 = ax.bar(x, y_contractor, width=width, align='center' ,bottom=y_self_financed, color=colors_contractor, label='financed by contractor')
p3 = ax2.bar(x, y_self_financed_insu, width=width, align='center', color=colors_self_finance)
p4 = ax2.bar(x, y_contractor_insu, width=width, align='center', bottom=y_self_financed_insu, color=colors_contractor)

# # lns = [p1,p2,p3,p4]
ax.legend(loc='best')

ax.set_xticks(x)
ax.set_xticklabels(x_labels)



# ax.set_title("New Investments Scenario 2")

name_figure=folder_path+'_new_capacities.eps'
fig.savefig(os.path.join(dir_name,folder_path+"\\"+name_figure))

plt.tight_layout()

plt.show()