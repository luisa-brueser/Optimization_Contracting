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


output_file_path = Path(__file__).parent / "data_output_one_year_30_household_3_cars_140kWh_scenario1.csv"


# output_file_path_comparison = Path(__file__).parent / "data_output_one_year_30_household_3_cars_140kWh_scenario1_85%_inv_cost.csv"
# output_file_path_comparison_2 = Path(__file__).parent / "data_output_one_year_30_household_3_cars_140kWh_scenario1_60%_inv_cost.csv"
output_file_path_comparison = Path(__file__).parent /  "data_output_one_year_30_household_3_cars_140kWh_scenario1_CO_70_HP.csv"
output_file_path_comparison_2 =Path(__file__).parent /  "data_output_one_year_30_household_3_cars_140kWh_scenario1_CO_115_HP.csv"
output_file_path_comparison_3 = Path(__file__).parent / "data_output_one_year_30_household_3_cars_140kWh_scenario1_CO_200_HP.csv"
output_file_path_comparison_4 = Path(__file__).parent / "data_output_one_year_30_household_3_cars_140kWh_scenario1_CO_250_HP.csv"

# output_file_path_comparison = Path(__file__).parent /  "data_output_one_year_30_household_3_cars_140kWh_scenario1_CO_70_no_HP.csv"
# output_file_path_comparison_2 =Path(__file__).parent /  "data_output_one_year_30_household_3_cars_140kWh_scenario1_CO_115_no_HP.csv"
# output_file_path_comparison_3 = Path(__file__).parent / "data_output_one_year_30_household_3_cars_140kWh_scenario1_CO_200_no_HP.csv"
# output_file_path_comparison_4 = Path(__file__).parent / "data_output_one_year_30_household_3_cars_140kWh_scenario1_CO_250_no_HP.csv"


# output_file_path_comparison_DH = Path(__file__).parent / "data_output_one_year_30_household_3_cars_140kWh_scenario1_DH.csv"

dir_name='C:\\Users\\Thomas\\OneDrive\\Desktop\\DA\\Bilder_Ergebnisse\\'
folder_path='Scenario_1_no_title'



df = py.IamDataFrame(output_file_path)
df_comparison = py.IamDataFrame(output_file_path_comparison)
df_comparison_2 = py.IamDataFrame(output_file_path_comparison_2)
df_comparison_3 = py.IamDataFrame(output_file_path_comparison_3)
df_comparison_4 = py.IamDataFrame(output_file_path_comparison_4)
# df_comparison_DH = py.IamDataFrame(output_file_path_comparison_DH)
# df = py.IamDataFrame(df_all_results)
# # print(df)

model, scenario = "Contracting_model", "Scenario 1"

# model_comparison, scenario_comparison = "Contracting_model", "Scenario 1 85% inv cost"
# model_comparison_2, scenario_comparison_2 = "Contracting_model", "Scenario 1 60% inv cost"
model_comparison, scenario_comparison = "Contracting_model", "Scenario 1 CO 70 HP"
model_comparison_2, scenario_comparison_2 = "Contracting_model", "Scenario 1 CO 115 HP"
model_comparison_3, scenario_comparison_3 = "Contracting_model", "Scenario 1 CO 200 HP"
model_comparison_4, scenario_comparison_4 = "Contracting_model", "Scenario 1 CO 250 HP"
# model_comparison, scenario_comparison = "Contracting_model", "Scenario 1 CO 70 no HP"
# model_comparison_2, scenario_comparison_2 = "Contracting_model", "Scenario 1 CO 115 no HP"
# model_comparison_3, scenario_comparison_3 = "Contracting_model", "Scenario 1 CO 200 no HP"
# model_comparison_4, scenario_comparison_4 = "Contracting_model", "Scenario 1 CO 250 no HP"
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


####### new capacities stacked bar plot
# data_capacitiy_new = df.filter(
#     model=model,
#     scenario=scenario,
#     variable=["Capacity|Self financed|*", "Capacity|Contractor|*","Reduction Heating Demand|*"],
# )

# variables_new_tech = data_capacitiy_new.filter(
#     variable="Capacity|Self financed|*"
# ).variable
# x_labels = [string.split("|")[2] for string in variables_new_tech] + ["Reduction \n Heating Demand" ]
# x_labels[1]="Charging \n Station" 


# y_self_financed = data_capacitiy_new.filter(variable="Capacity|Self financed|*").data["value"]
# y_self_financed_insulation = data_capacitiy_new.filter(variable=["Reduction Heating Demand|Self financed"]).data["value"]
# y_self_financed.loc[len(y_self_financed.index)] = 0
# y_self_financed_insu= y_self_financed.copy()
# y_self_financed_insu.loc[1:4] = 0 
# y_self_financed_insu[5]=y_self_financed_insulation


# y_contractor = data_capacitiy_new.filter(variable="Capacity|Contractor|*").data["value"]
# y_contractor_insulation = data_capacitiy_new.filter(variable=["Reduction Heating Demand|Contractor"]).data["value"]

# y_contractor.loc[len(y_contractor.index)] = 0
# y_contractor_insu= y_contractor.copy()
# y_contractor_insu.loc[1:4] = 0 
# y_contractor_insu[5]=y_contractor_insulation

# # y_contractor[2] = 5
# # y_contractor[3] = 5
# width =0.35  # the width of the bars: can also be len(x) sequence
# # plt.style.use("science")

# fig, ax = plt.subplots()
# ax2 = ax.twinx() 
# ax.set_ylim(0, 50)
# ax2.set_ylim(0, 100)
# ax.set_ylabel('New capacities in kW/kWh/pcs.')
# ax2.set_ylabel('Reduction heating demand in %')
# x = np.arange(len(x_labels))

# p1 = ax.bar(x , y_self_financed, width=width, align='center', color=colors_self_finance,  label='financed without contractor')
# p2 = ax.bar(x, y_contractor, width=width, align='center' ,bottom=y_self_financed, color=colors_contractor, label='financed by contractor')
# p3 = ax2.bar(x, y_self_financed_insu, width=width, align='center', color=colors_self_finance)
# p4 = ax2.bar(x, y_contractor_insu, width=width, align='center', bottom=y_self_financed_insu, color=colors_contractor)

# # # lns = [p1,p2,p3,p4]
# ax.legend(loc=(0.02, 0.55)) #(handles=lns) #, loc='best')

# ax.set_xticks(x)
# ax.set_xticklabels(x_labels)

# ax.annotate("15% of the original heating demand \n remains after insulation", xy=(4.6, 41), xytext=(2.4,45),
#         arrowprops=dict(arrowstyle="->"))
#             #arrowprops=dict(facecolor='black', shrink=0.6))


# # ax.set_title("New Investments Scenario 1")

# name_figure=folder_path+'_new_capacities.eps'
# fig.savefig(os.path.join(dir_name,folder_path+"\\"+name_figure))


######### bar plot for showing costs
# data_costs_revenue= df.filter(variable=["Cost|*","Revenue"])
# variables_cost= data_costs_revenue.filter(variable="Cost|*").variable
# x_labels_cost = [string.split("|")[1] for string in variables_cost]+['Revenue']
# total=x_labels_cost[3]
# x_labels_cost[3]=x_labels_cost[5]
# x_labels_cost[5]=total
# print('x_labels_cost: ', x_labels_cost)
# y_cost = data_costs_revenue.data["value"]

# total=y_cost[3]
# y_cost[3]=y_cost[5]
# y_cost[5]=total
# print('y_cost: ', y_cost)



# width = 0.35  # the width of the bars: can also be len(x) sequence
# # plt.style.use("science")
# fig, ax = plt.subplots()
# # colors = ['tab:blue', 'tab:cyan', 'tab:gray', 'tab:orange', 'tab:red']
# ax.bar(x_labels_cost, y_cost, width)#, color=colors_default)
# # ax.legend()
# ax.axhline(0, 0,1, linestyle="--",color='k',linewidth=0.8)
# # ax.set_title("Annual costs for tenants")
# ax.bar_label(ax.containers[0])

# name_figure=folder_path+'_with_HP_costs.eps'
# fig.savefig(os.path.join(dir_name,folder_path+"\\"+name_figure))




###### new capacities comparison stacked bar plot
# data_capacitiy_new = df.filter(
#     model=model,
#     scenario=scenario,
#     variable=["Capacity|Self financed|*", "Capacity|Contractor|*","Reduction Heating Demand|*"],
# )

# data_capacitiy_comparison = df_comparison.filter(
#     model=model_comparison,
#     scenario=scenario_comparison,
#     variable=["Capacity|Self financed|*", "Capacity|Contractor|*","Reduction Heating Demand|*"],
# )

# data_capacitiy_comparison_2= df_comparison_2.filter(
#     model=model_comparison_2,
#     scenario=scenario_comparison_2,
#     variable=["Capacity|Self financed|*", "Capacity|Contractor|*","Reduction Heating Demand|*"],
# )
# variables_new_tech = data_capacitiy_new.filter(
#     variable="Capacity|Self financed|*"
# ).variable
# x_labels = [string.split("|")[2] for string in variables_new_tech] + ["Reduction \n Heating Demand" ]
# x_labels[1]="Charging \n Station" 


# y_self_financed = data_capacitiy_new.filter(variable="Capacity|Self financed|*").data["value"]
# y_self_financed_insulation = data_capacitiy_new.filter(variable=["Reduction Heating Demand|Self financed"]).data["value"]
# y_self_financed.loc[len(y_self_financed.index)] = 0
# y_self_financed_insu= y_self_financed.copy()
# y_self_financed_insu.loc[1:4] = 0 
# y_self_financed_insu[5]=y_self_financed_insulation

# y_self_financed_comparison = data_capacitiy_comparison.filter(variable="Capacity|Self financed|*").data["value"]
# y_self_financed_comparison_insulation = data_capacitiy_comparison.filter(variable=["Reduction Heating Demand|Self financed"]).data["value"]

# y_self_financed_comparison.loc[len(y_self_financed_comparison.index)] = 0
# y_self_financed_comparison_insu= y_self_financed_comparison.copy()
# y_self_financed_comparison_insu.loc[1:4] = 0 
# y_self_financed_comparison_insu[5]=y_self_financed_comparison_insulation



# y_self_financed_comparison_2 = data_capacitiy_comparison_2.filter(variable="Capacity|Self financed|*").data["value"]
# y_self_financed_comparison_insulation_2 = data_capacitiy_comparison_2.filter(variable=["Reduction Heating Demand|Self financed"]).data["value"]

# y_self_financed_comparison_2.loc[len(y_self_financed_comparison_2.index)] = 0
# y_self_financed_comparison_insu_2= y_self_financed_comparison_2.copy()
# y_self_financed_comparison_insu_2.loc[1:4] = 0 
# y_self_financed_comparison_insu_2[5]=y_self_financed_comparison_insulation_2



# y_contractor = data_capacitiy_new.filter(variable="Capacity|Contractor|*").data["value"]
# y_contractor_insulation = data_capacitiy_new.filter(variable=["Reduction Heating Demand|Contractor"]).data["value"]

# y_contractor.loc[len(y_contractor.index)] = 0
# y_contractor_insu= y_contractor.copy()
# y_contractor_insu.loc[1:4] = 0 
# y_contractor_insu[5]=y_contractor_insulation

# y_contractor_comparison = data_capacitiy_comparison.filter(variable="Capacity|Contractor|*").data["value"]
# y_contractor_insulation_comparison = data_capacitiy_comparison.filter(variable=["Reduction Heating Demand|Contractor"]).data["value"]

# y_contractor_comparison.loc[len(y_contractor_comparison.index)] = 0
# y_contractor_comparison_insu= y_contractor_comparison.copy()
# y_contractor_comparison_insu.loc[1:4] = 0 
# y_contractor_comparison_insu[5]=y_contractor_insulation_comparison

# y_contractor_comparison_2 = data_capacitiy_comparison_2.filter(variable="Capacity|Contractor|*").data["value"]
# y_contractor_insulation_comparison_2 = data_capacitiy_comparison_2.filter(variable=["Reduction Heating Demand|Contractor"]).data["value"]

# y_contractor_comparison_2.loc[len(y_contractor_comparison_2.index)] = 0
# y_contractor_comparison_insu_2= y_contractor_comparison_2.copy()
# y_contractor_comparison_insu_2.loc[1:4] = 0 
# y_contractor_comparison_insu_2[5]=y_contractor_insulation_comparison_2


# # # y_contractor[2] = 5
# # # y_contractor[3] = 5
# width = 0.3  # the width of the bars: can also be len(x) sequence
# # # plt.style.use("science")

# fig, ax = plt.subplots()
# ax2 = ax.twinx() 
# ax.set_ylim(0, 50)
# ax2.set_ylim(0, 100)
# ax.set_ylabel('New capacities in kW/kWh/pcs.')
# ax2.set_ylabel('Reduction heating demand in %')
# x = np.arange(len(x_labels))

# p1 = ax.bar(x- width , y_self_financed, width=width, align='center', color= 'steelblue', hatch = '--')
# p2 = ax.bar(x -width, y_contractor, width=width, align='center' ,bottom=y_self_financed, color='steelblue',   hatch = '\\\\')
# p3 = ax2.bar(x - width, y_self_financed_insu, width=width, align='center', color='steelblue', hatch = '--')
# p4 = ax2.bar(x - width, y_contractor_insu, width=width, align='center' ,bottom=y_self_financed_insu, color= 'steelblue',  hatch = '\\\\')

# p5 = ax.bar(x, y_self_financed_comparison, width=width, align='center', color="mediumslateblue",  hatch = '--')
# p6 = ax.bar(x, y_contractor_comparison, width=width, align='center' ,bottom=y_self_financed_comparison, color="mediumslateblue",  hatch = '\\\\')
# p7 = ax2.bar(x, y_self_financed_comparison_insu, width=width, align='center', color="mediumslateblue",  hatch = '--')
# p8 = ax2.bar(x, y_contractor_comparison_insu, width=width, align='center' ,bottom=y_self_financed_comparison_insu, color="mediumslateblue",  hatch = '\\\\')

# p9 = ax.bar(x + width, y_self_financed_comparison_2, width=width, align='center', color="royalblue", hatch = '--')
# p10 = ax.bar(x + width, y_contractor_comparison_2, width=width, align='center' ,bottom=y_self_financed_comparison_2, color="royalblue",  hatch = '\\\\')
# p11 = ax2.bar(x + width, y_self_financed_comparison_insu_2, width=width, align='center', color="royalblue",  hatch = '--')
# p12 = ax2.bar(x + width, y_contractor_comparison_insu_2, width=width, align='center' ,bottom=y_self_financed_comparison_insu_2, color="royalblue",  hatch = '\\\\')






# ax.set_xticks(x)
# ax.set_xticklabels(x_labels)


# ax.annotate("15% of the original heating demand \n remains after insulation", xy=(4.5, 41), xytext=(2.4,45),
#         arrowprops=dict(arrowstyle="->"))
#             #arrowprops=dict(facecolor='black', shrink=0.6))

# patch1 = mpatches.Patch(color='steelblue', label='same investment costs')
# patch2 = mpatches.Patch(color='mediumslateblue', label='contractor 85% inv costs')
# patch3 = mpatches.Patch(color='royalblue', label='contractor 60% inv costs')
# patch4 = mpatches.Patch(facecolor='ghostwhite', label='financed without contractor', hatch = '--')
# patch5 = mpatches.Patch(facecolor='ghostwhite', label='financed by contractor', hatch = '\\\\')
# plt.legend(handles=[patch1,patch2,patch3,patch4,patch5], loc=(0.02, 0.55))

# # ax.set_title("Comparsion new investments Scenario 1")

# name_figure=folder_path+'_new_capacities_comparison_inv_cost.eps'
# fig.savefig(os.path.join(dir_name,folder_path+"\\"+name_figure))


## new capacities comparison CO2 stacked bar plot
data_capacitiy_new = df.filter(
    model=model,
    scenario=scenario,
    variable=["Capacity|Self financed|*", "Capacity|Contractor|*","Reduction Heating Demand|*"],
)

data_capacitiy_comparison = df_comparison.filter(
    model=model_comparison,
    scenario=scenario_comparison,
    variable=["Capacity|Self financed|*", "Capacity|Contractor|*","Reduction Heating Demand|*"],
)

data_capacitiy_comparison_2= df_comparison_2.filter(
    model=model_comparison_2,
    scenario=scenario_comparison_2,
    variable=["Capacity|Self financed|*", "Capacity|Contractor|*","Reduction Heating Demand|*"],
)

data_capacitiy_comparison_3= df_comparison_3.filter(
    model=model_comparison_3,
    scenario=scenario_comparison_3,
    variable=["Capacity|Self financed|*", "Capacity|Contractor|*","Reduction Heating Demand|*"],
)

data_capacitiy_comparison_4= df_comparison_4.filter(
    model=model_comparison_4,
    scenario=scenario_comparison_4,
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

y_self_financed_comparison = data_capacitiy_comparison.filter(variable="Capacity|Self financed|*").data["value"]
y_self_financed_comparison_insulation = data_capacitiy_comparison.filter(variable=["Reduction Heating Demand|Self financed"]).data["value"]

y_self_financed_comparison.loc[len(y_self_financed_comparison.index)] = 0
y_self_financed_comparison_insu= y_self_financed_comparison.copy()
y_self_financed_comparison_insu.loc[1:4] = 0 
y_self_financed_comparison_insu[5]=y_self_financed_comparison_insulation



y_self_financed_comparison_2 = data_capacitiy_comparison_2.filter(variable="Capacity|Self financed|*").data["value"]
y_self_financed_comparison_insulation_2 = data_capacitiy_comparison_2.filter(variable=["Reduction Heating Demand|Self financed"]).data["value"]

y_self_financed_comparison_2.loc[len(y_self_financed_comparison_2.index)] = 0
y_self_financed_comparison_insu_2= y_self_financed_comparison_2.copy()
y_self_financed_comparison_insu_2.loc[1:4] = 0 
y_self_financed_comparison_insu_2[5]=y_self_financed_comparison_insulation_2

y_self_financed_comparison_3 = data_capacitiy_comparison_3.filter(variable="Capacity|Self financed|*").data["value"]
y_self_financed_comparison_insulation_3 = data_capacitiy_comparison_3.filter(variable=["Reduction Heating Demand|Self financed"]).data["value"]

y_self_financed_comparison_3.loc[len(y_self_financed_comparison_3.index)] = 0
y_self_financed_comparison_insu_3= y_self_financed_comparison_3.copy()
y_self_financed_comparison_insu_3.loc[1:4] = 0 
y_self_financed_comparison_insu_3[5]=y_self_financed_comparison_insulation_3


y_self_financed_comparison_4 = data_capacitiy_comparison_4.filter(variable="Capacity|Self financed|*").data["value"]
y_self_financed_comparison_insulation_4 = data_capacitiy_comparison_4.filter(variable=["Reduction Heating Demand|Self financed"]).data["value"]

y_self_financed_comparison_4.loc[len(y_self_financed_comparison_4.index)] = 0
y_self_financed_comparison_insu_4= y_self_financed_comparison_4.copy()
y_self_financed_comparison_insu_4.loc[1:4] = 0 
y_self_financed_comparison_insu_4[5]=y_self_financed_comparison_insulation_4




y_contractor = data_capacitiy_new.filter(variable="Capacity|Contractor|*").data["value"]
y_contractor_insulation = data_capacitiy_new.filter(variable=["Reduction Heating Demand|Contractor"]).data["value"]

y_contractor.loc[len(y_contractor.index)] = 0
y_contractor_insu= y_contractor.copy()
y_contractor_insu.loc[1:4] = 0 
y_contractor_insu[5]=y_contractor_insulation

y_contractor_comparison = data_capacitiy_comparison.filter(variable="Capacity|Contractor|*").data["value"]
y_contractor_insulation_comparison = data_capacitiy_comparison.filter(variable=["Reduction Heating Demand|Contractor"]).data["value"]

y_contractor_comparison.loc[len(y_contractor_comparison.index)] = 0
y_contractor_comparison_insu= y_contractor_comparison.copy()
y_contractor_comparison_insu.loc[1:4] = 0 
y_contractor_comparison_insu[5]=y_contractor_insulation_comparison

y_contractor_comparison_2 = data_capacitiy_comparison_2.filter(variable="Capacity|Contractor|*").data["value"]
y_contractor_insulation_comparison_2 = data_capacitiy_comparison_2.filter(variable=["Reduction Heating Demand|Contractor"]).data["value"]

y_contractor_comparison_2.loc[len(y_contractor_comparison_2.index)] = 0
y_contractor_comparison_insu_2= y_contractor_comparison_2.copy()
y_contractor_comparison_insu_2.loc[1:4] = 0 
y_contractor_comparison_insu_2[5]=y_contractor_insulation_comparison_2

y_contractor_comparison_3 = data_capacitiy_comparison_3.filter(variable="Capacity|Contractor|*").data["value"]
y_contractor_insulation_comparison_3 = data_capacitiy_comparison_3.filter(variable=["Reduction Heating Demand|Contractor"]).data["value"]

y_contractor_comparison_3.loc[len(y_contractor_comparison_3.index)] = 0
y_contractor_comparison_insu_3= y_contractor_comparison_3.copy()
y_contractor_comparison_insu_3.loc[1:4] = 0 
y_contractor_comparison_insu_3[5]=y_contractor_insulation_comparison_3

y_contractor_comparison_4 = data_capacitiy_comparison_4.filter(variable="Capacity|Contractor|*").data["value"]
y_contractor_insulation_comparison_4 = data_capacitiy_comparison_4.filter(variable=["Reduction Heating Demand|Contractor"]).data["value"]

y_contractor_comparison_4.loc[len(y_contractor_comparison_4.index)] = 0
y_contractor_comparison_insu_4= y_contractor_comparison_4.copy()
y_contractor_comparison_insu_4.loc[1:4] = 0 
y_contractor_comparison_insu_4[5]=y_contractor_insulation_comparison_4



# # y_contractor[2] = 5
# # y_contractor[3] = 5
width = 0.15 # the width of the bars: can also be len(x) sequence
# # plt.style.use("science")

fig, ax = plt.subplots()
ax2 = ax.twinx() 
ax.set_ylim(0, 90)
ax2.set_ylim(0, 100)
ax.set_ylabel('New capacities in kW/kWh/pcs.')
ax2.set_ylabel('Reduction heating demand in %')
x = np.arange(len(x_labels))
# print('x: ', x)
# print(len(x_labels))
p1 = ax.bar(x- 2*width , y_self_financed, width=width, align='center', color= 'steelblue', hatch = '--')
p2 = ax.bar(x -2*width, y_contractor, width=width, align='center' ,bottom=y_self_financed, color='steelblue',   hatch = '\\\\')
p3 = ax2.bar(x - 2*width, y_self_financed_insu, width=width, align='center', color='steelblue', hatch = '--')
p4 = ax2.bar(x - 2*width, y_contractor_insu, width=width, align='center' ,bottom=y_self_financed_insu, color= 'steelblue',  hatch = '\\\\')

p5 = ax.bar(x- 1*width, y_self_financed_comparison, width=width, align='center', color="mediumslateblue",  hatch = '--')
p6 = ax.bar(x- 1*width, y_contractor_comparison, width=width, align='center' ,bottom=y_self_financed_comparison, color="mediumslateblue",  hatch = '\\\\')
p7 = ax2.bar(x- 1*width, y_self_financed_comparison_insu, width=width, align='center', color="mediumslateblue",  hatch = '--')
p8 = ax2.bar(x- 1*width, y_contractor_comparison_insu, width=width, align='center' ,bottom=y_self_financed_comparison_insu, color="mediumslateblue",  hatch = '\\\\')

p9 = ax.bar(x, y_self_financed_comparison_2, width=width, align='center', color="royalblue", hatch = '--')
p10 = ax.bar(x, y_contractor_comparison_2, width=width, align='center' ,bottom=y_self_financed_comparison_2, color="royalblue",  hatch = '\\\\')
p11 = ax2.bar(x, y_self_financed_comparison_insu_2, width=width, align='center', color="royalblue",  hatch = '--')
p12 = ax2.bar(x, y_contractor_comparison_insu_2, width=width, align='center' ,bottom=y_self_financed_comparison_insu_2, color="royalblue",  hatch = '\\\\')


p13 = ax.bar(x +1*width, y_self_financed_comparison_3, width=width, align='center', color="slategrey", hatch = '--')
p14 = ax.bar(x + 1*width, y_contractor_comparison_3, width=width, align='center' ,bottom=y_self_financed_comparison_3, color="slategrey",  hatch = '\\\\')
p15 = ax2.bar(x + 1*width, y_self_financed_comparison_insu_3, width=width, align='center', color="slategrey",  hatch = '--')
p16 = ax2.bar(x + 1*width, y_contractor_comparison_insu_3, width=width, align='center' ,bottom=y_self_financed_comparison_insu_3, color="slategrey",  hatch = '\\\\')

p17 = ax.bar(x + 2*width, y_self_financed_comparison_4, width=width, align='center', color="darkorchid", hatch = '--')
p18 = ax.bar(x + 2*width, y_contractor_comparison_4, width=width, align='center' ,bottom=y_self_financed_comparison_4, color="royalblue",  hatch = '\\\\')
p19 = ax2.bar(x + 2*width, y_self_financed_comparison_insu_4, width=width, align='center', color="darkorchid",  hatch = '--')
p20 = ax2.bar(x + 2*width, y_contractor_comparison_insu_4, width=width, align='center' ,bottom=y_self_financed_comparison_insu_4, color="royalblue",  hatch = '\\\\')





ax.set_xticks(x)
ax.set_xticklabels(x_labels)


ax.annotate("15% of the original heating demand \n remains after insulation", xy=(4.5, 75), xytext=(2.4,80),
        arrowprops=dict(arrowstyle="->"))
            #arrowprops=dict(facecolor='black', shrink=0.6))


ax.annotate('no HP installed', xy=(1.76,0), xytext=(0.45,15), arrowprops=dict(arrowstyle="->"))
        

# ax.annotate('no HP installed', xy=(2.3,0), xytext=(0.5,20), arrowprops=dict(arrowstyle="->"))


patch1 = mpatches.Patch(color='steelblue', label='default price')
patch2 = mpatches.Patch(color='mediumslateblue', label='70€/tCO2')
patch3 = mpatches.Patch(color='royalblue', label='115€/tCO2')
patch4 = mpatches.Patch(color="slategrey", label='200€/tCO2')
patch5 = mpatches.Patch(color="darkorchid", label='250€/tCO2')
patch6 = mpatches.Patch(facecolor='ghostwhite', label='financed \n without contractor', hatch = '--')
patch7 = mpatches.Patch(facecolor='ghostwhite', label='financed \n by contractor', hatch = '\\\\')
plt.legend(handles=[patch1,patch2,patch3,patch4,patch5,patch6,patch7], loc=(0.02, 0.4))

# ax.set_title("Comparsion new investments Scenario 1 depending on CO2 price")

name_figure=folder_path+'_new_capacities_comparison_CO2_HP.eps'
fig.savefig(os.path.join(dir_name,folder_path+"\\"+name_figure))


# ##### new capacities comparison CO2 stacked bar plot - without HP
# data_capacitiy_new = df.filter(
#     model=model,
#     scenario=scenario,
#     variable=["Capacity|Self financed|*", "Capacity|Contractor|*","Reduction Heating Demand|*"],
# )

# data_capacitiy_comparison = df_comparison.filter(
#     model=model_comparison,
#     scenario=scenario_comparison,
#     variable=["Capacity|Self financed|*", "Capacity|Contractor|*","Reduction Heating Demand|*"],
# )

# data_capacitiy_comparison_2= df_comparison_2.filter(
#     model=model_comparison_2,
#     scenario=scenario_comparison_2,
#     variable=["Capacity|Self financed|*", "Capacity|Contractor|*","Reduction Heating Demand|*"],
# )

# data_capacitiy_comparison_3= df_comparison_3.filter(
#     model=model_comparison_3,
#     scenario=scenario_comparison_3,
#     variable=["Capacity|Self financed|*", "Capacity|Contractor|*","Reduction Heating Demand|*"],
# )

# data_capacitiy_comparison_4= df_comparison_4.filter(
#     model=model_comparison_4,
#     scenario=scenario_comparison_4,
#     variable=["Capacity|Self financed|*", "Capacity|Contractor|*","Reduction Heating Demand|*"],
# )

# variables_new_tech = data_capacitiy_new.filter(
#     variable="Capacity|Self financed|*"
# ).variable
# x_labels = [string.split("|")[2] for string in variables_new_tech] + ["Reduction \n Heating Demand" ]
# x_labels[1]="Charging \n Station" 


# y_self_financed = data_capacitiy_new.filter(variable="Capacity|Self financed|*").data["value"]
# y_self_financed_insulation = data_capacitiy_new.filter(variable=["Reduction Heating Demand|Self financed"]).data["value"]
# y_self_financed.loc[len(y_self_financed.index)] = 0
# y_self_financed_insu= y_self_financed.copy()
# y_self_financed_insu.loc[1:4] = 0 
# y_self_financed_insu[5]=y_self_financed_insulation

# y_self_financed_comparison = data_capacitiy_comparison.filter(variable="Capacity|Self financed|*").data["value"]
# y_self_financed_comparison_insulation = data_capacitiy_comparison.filter(variable=["Reduction Heating Demand|Self financed"]).data["value"]

# y_self_financed_comparison.loc[len(y_self_financed_comparison.index)] = 0
# y_self_financed_comparison_insu= y_self_financed_comparison.copy()
# y_self_financed_comparison_insu.loc[1:4] = 0 
# y_self_financed_comparison_insu[5]=y_self_financed_comparison_insulation



# y_self_financed_comparison_2 = data_capacitiy_comparison_2.filter(variable="Capacity|Self financed|*").data["value"]
# y_self_financed_comparison_insulation_2 = data_capacitiy_comparison_2.filter(variable=["Reduction Heating Demand|Self financed"]).data["value"]

# y_self_financed_comparison_2.loc[len(y_self_financed_comparison_2.index)] = 0
# y_self_financed_comparison_insu_2= y_self_financed_comparison_2.copy()
# y_self_financed_comparison_insu_2.loc[1:4] = 0 
# y_self_financed_comparison_insu_2[5]=y_self_financed_comparison_insulation_2

# y_self_financed_comparison_3 = data_capacitiy_comparison_3.filter(variable="Capacity|Self financed|*").data["value"]
# y_self_financed_comparison_insulation_3 = data_capacitiy_comparison_3.filter(variable=["Reduction Heating Demand|Self financed"]).data["value"]

# y_self_financed_comparison_3.loc[len(y_self_financed_comparison_3.index)] = 0
# y_self_financed_comparison_insu_3= y_self_financed_comparison_3.copy()
# y_self_financed_comparison_insu_3.loc[1:4] = 0 
# y_self_financed_comparison_insu_3[5]=y_self_financed_comparison_insulation_3


# y_self_financed_comparison_4 = data_capacitiy_comparison_4.filter(variable="Capacity|Self financed|*").data["value"]
# y_self_financed_comparison_insulation_4 = data_capacitiy_comparison_4.filter(variable=["Reduction Heating Demand|Self financed"]).data["value"]

# y_self_financed_comparison_4.loc[len(y_self_financed_comparison_4.index)] = 0
# y_self_financed_comparison_insu_4= y_self_financed_comparison_4.copy()
# y_self_financed_comparison_insu_4.loc[1:4] = 0 
# y_self_financed_comparison_insu_4[5]=y_self_financed_comparison_insulation_4




# y_contractor = data_capacitiy_new.filter(variable="Capacity|Contractor|*").data["value"]
# y_contractor_insulation = data_capacitiy_new.filter(variable=["Reduction Heating Demand|Contractor"]).data["value"]

# y_contractor.loc[len(y_contractor.index)] = 0
# y_contractor_insu= y_contractor.copy()
# y_contractor_insu.loc[1:4] = 0 
# y_contractor_insu[5]=y_contractor_insulation

# y_contractor_comparison = data_capacitiy_comparison.filter(variable="Capacity|Contractor|*").data["value"]
# y_contractor_insulation_comparison = data_capacitiy_comparison.filter(variable=["Reduction Heating Demand|Contractor"]).data["value"]

# y_contractor_comparison.loc[len(y_contractor_comparison.index)] = 0
# y_contractor_comparison_insu= y_contractor_comparison.copy()
# y_contractor_comparison_insu.loc[1:4] = 0 
# y_contractor_comparison_insu[5]=y_contractor_insulation_comparison

# y_contractor_comparison_2 = data_capacitiy_comparison_2.filter(variable="Capacity|Contractor|*").data["value"]
# y_contractor_insulation_comparison_2 = data_capacitiy_comparison_2.filter(variable=["Reduction Heating Demand|Contractor"]).data["value"]

# y_contractor_comparison_2.loc[len(y_contractor_comparison_2.index)] = 0
# y_contractor_comparison_insu_2= y_contractor_comparison_2.copy()
# y_contractor_comparison_insu_2.loc[1:4] = 0 
# y_contractor_comparison_insu_2[5]=y_contractor_insulation_comparison_2

# y_contractor_comparison_3 = data_capacitiy_comparison_3.filter(variable="Capacity|Contractor|*").data["value"]
# y_contractor_insulation_comparison_3 = data_capacitiy_comparison_3.filter(variable=["Reduction Heating Demand|Contractor"]).data["value"]

# y_contractor_comparison_3.loc[len(y_contractor_comparison_3.index)] = 0
# y_contractor_comparison_insu_3= y_contractor_comparison_3.copy()
# y_contractor_comparison_insu_3.loc[1:4] = 0 
# y_contractor_comparison_insu_3[5]=y_contractor_insulation_comparison_3

# y_contractor_comparison_4 = data_capacitiy_comparison_4.filter(variable="Capacity|Contractor|*").data["value"]
# y_contractor_insulation_comparison_4 = data_capacitiy_comparison_4.filter(variable=["Reduction Heating Demand|Contractor"]).data["value"]

# y_contractor_comparison_4.loc[len(y_contractor_comparison_4.index)] = 0
# y_contractor_comparison_insu_4= y_contractor_comparison_4.copy()
# y_contractor_comparison_insu_4.loc[1:4] = 0 
# y_contractor_comparison_insu_4[5]=y_contractor_insulation_comparison_4



# # # y_contractor[2] = 5
# # # y_contractor[3] = 5
# width = 0.15 # the width of the bars: can also be len(x) sequence
# # # plt.style.use("science")

# fig, ax = plt.subplots()
# ax2 = ax.twinx() 
# ax.set_ylim(0, 90)
# ax2.set_ylim(0, 100)
# ax.set_ylabel('New capacities in kW/kWh/pcs.')
# ax2.set_ylabel('Reduction heating demand in %')
# x = np.arange(len(x_labels))
# # print('x: ', x)
# # print(len(x_labels))
# p1 = ax.bar(x- 2*width , y_self_financed, width=width, align='center', color= 'steelblue', hatch = '--')
# p2 = ax.bar(x -2*width, y_contractor, width=width, align='center' ,bottom=y_self_financed, color='steelblue',   hatch = '\\\\')
# p3 = ax2.bar(x - 2*width, y_self_financed_insu, width=width, align='center', color='steelblue', hatch = '--')
# p4 = ax2.bar(x - 2*width, y_contractor_insu, width=width, align='center' ,bottom=y_self_financed_insu, color= 'steelblue',  hatch = '\\\\')

# p5 = ax.bar(x- 1*width, y_self_financed_comparison, width=width, align='center', color="mediumslateblue",  hatch = '--')
# p6 = ax.bar(x- 1*width, y_contractor_comparison, width=width, align='center' ,bottom=y_self_financed_comparison, color="mediumslateblue",  hatch = '\\\\')
# p7 = ax2.bar(x- 1*width, y_self_financed_comparison_insu, width=width, align='center', color="mediumslateblue",  hatch = '--')
# p8 = ax2.bar(x- 1*width, y_contractor_comparison_insu, width=width, align='center' ,bottom=y_self_financed_comparison_insu, color="mediumslateblue",  hatch = '\\\\')

# p9 = ax.bar(x, y_self_financed_comparison_2, width=width, align='center', color="royalblue", hatch = '--')
# p10 = ax.bar(x, y_contractor_comparison_2, width=width, align='center' ,bottom=y_self_financed_comparison_2, color="royalblue",  hatch = '\\\\')
# p11 = ax2.bar(x, y_self_financed_comparison_insu_2, width=width, align='center', color="royalblue",  hatch = '--')
# p12 = ax2.bar(x, y_contractor_comparison_insu_2, width=width, align='center' ,bottom=y_self_financed_comparison_insu_2, color="royalblue",  hatch = '\\\\')


# p13 = ax.bar(x +1*width, y_self_financed_comparison_3, width=width, align='center', color="slategrey", hatch = '--')
# p14 = ax.bar(x + 1*width, y_contractor_comparison_3, width=width, align='center' ,bottom=y_self_financed_comparison_3, color="slategrey",  hatch = '\\\\')
# p15 = ax2.bar(x + 1*width, y_self_financed_comparison_insu_3, width=width, align='center', color="slategrey",  hatch = '--')
# p16 = ax2.bar(x + 1*width, y_contractor_comparison_insu_3, width=width, align='center' ,bottom=y_self_financed_comparison_insu_3, color="slategrey",  hatch = '\\\\')

# p17 = ax.bar(x + 2*width, y_self_financed_comparison_4, width=width, align='center', color="darkorchid", hatch = '--')
# p18 = ax.bar(x + 2*width, y_contractor_comparison_4, width=width, align='center' ,bottom=y_self_financed_comparison_4, color="royalblue",  hatch = '\\\\')
# p19 = ax2.bar(x + 2*width, y_self_financed_comparison_insu_4, width=width, align='center', color="darkorchid",  hatch = '--')
# p20 = ax2.bar(x + 2*width, y_contractor_comparison_insu_4, width=width, align='center' ,bottom=y_self_financed_comparison_insu_4, color="royalblue",  hatch = '\\\\')





# ax.set_xticks(x)
# ax.set_xticklabels(x_labels)


# ax.annotate("15% of the original heating demand \n remains after insulation", xy=(4.5, 75), xytext=(2.4,80),
#         arrowprops=dict(arrowstyle="->"))
#             #arrowprops=dict(facecolor='black', shrink=0.6))


# # ax.annotate('no HP installed', xy=(1.76,0), xytext=(0.5,15), arrowprops=dict(arrowstyle="->"))
        

# # ax.annotate('no HP installed', xy=(2.3,0), xytext=(0.5,20), arrowprops=dict(arrowstyle="->"))


# patch1 = mpatches.Patch(color='steelblue', label='default price')
# patch2 = mpatches.Patch(color='mediumslateblue', label='70€/tCO2')
# patch3 = mpatches.Patch(color='royalblue', label='115€/tCO2')
# patch4 = mpatches.Patch(color="slategrey", label='200€/tCO2')
# patch5 = mpatches.Patch(color="darkorchid", label='250€/tCO2')
# patch6 = mpatches.Patch(facecolor='ghostwhite', label='financed \n without contractor', hatch = '--')
# patch7 = mpatches.Patch(facecolor='ghostwhite', label='financed \n by contractor', hatch = '\\\\')
# plt.legend(handles=[patch1,patch2,patch3,patch4,patch5,patch6,patch7], loc=(0.02, 0.4))

# # ax.set_title("Comparsion new investments Scenario 1 depending on CO2 price")

# name_figure=folder_path+'_new_capacities_comparison_CO2_no_HP.eps'
# fig.savefig(os.path.join(dir_name,folder_path+"\\"+name_figure))


####### pie plot default  no HP
# data_sum_supply_default = df.filter(
#     model=model, scenario=scenario, variable=["Sum supply default|Self financed|*"]
# )
# data_sum_supply_default_comparison = df_comparison.filter(
#     model=model_comparison, scenario=scenario_comparison, variable=["Sum supply default|Self financed|*"]
# )
# data_sum_supply_default_comparison_2 = df_comparison_2.filter(
#     model=model_comparison_2, scenario=scenario_comparison_2, variable=["Sum supply default|Self financed|*"]
# )
# data_sum_supply_default_comparison_3= df_comparison_3.filter(
#     model=model_comparison_3, scenario=scenario_comparison_3, variable=["Sum supply default|Self financed|*"]
# )
# data_sum_supply_default_comparison_4= df_comparison_4.filter(
#     model=model_comparison_4, scenario=scenario_comparison_4, variable=["Sum supply default|Self financed|*"]
# )


# values_default = data_sum_supply_default.data["value"]
# values_default_comparison  = data_sum_supply_default_comparison.data["value"]
# values_default_comparison_2 = data_sum_supply_default_comparison_2.data["value"]
# values_default_comparison_3 = data_sum_supply_default_comparison_3.data["value"]
# values_default_comparison_4 = data_sum_supply_default_comparison_4.data["value"]
# print('values_default_comparison_4: ', values_default_comparison_4)

# variables_default = data_sum_supply_default.filter( 
#     variable="Sum supply default|Self financed|*"
# ).variable


# x_labels_default = [string.split("Sum supply default|Self financed|")[1] for string in variables_default]


# fig, axs = plt.subplots(1, 2)


# def func(pct, allvals):
#     absolute = int(round(pct / 100.0 * np.sum(allvals)))
#     if pct > 0:
#         return "{:.1f}%({:d} kWh)".format(pct, absolute)
#     else:
#         return ""


# patches, texts, autotexts = axs[0].pie(
#     values_default,
#     autopct=lambda pct: func(pct, values_default),
#     pctdistance=0.5,
#     colors=colors_all,
#     labeldistance=1.1,
# )

# axs[0].set_title("Default price and 70,115,200€/tCO2 ",fontsize=10)


# patches, texts, autotexts = axs[1].pie(
#     values_default_comparison_4,
#     autopct=lambda pct: func(pct, values_default_comparison_4),
#     pctdistance=0.5,
#     colors=colors_all,
#     labeldistance=1.1,
# )

# axs[1].set_title("250€/tCO2",fontsize=10)



# for patch, txt in zip(patches, autotexts):
#     # the angle at which the text is located
#     ang = (patch.theta2 + patch.theta1) / 2.0
#     # new coordinates of the text, 0.7 is the distance from the center
#     x = patch.r * 1.2 * np.cos(ang * np.pi / 180)
#     y = patch.r * 1.2 * np.sin(ang * np.pi / 180)
#     # if patch is narrow enough, move text to new coordinates
#     if (patch.theta2 - patch.theta1) < 1:
#         txt.set_position((x, y))


# fig.legend(labels=x_labels_default,   # The labels for each line
#             loc=(0.4, 0.15),
#            #loc="right",   # Position of legend
#            borderaxespad=0.1,    # Small spacing around legend box
#            title="Supply from grid"  # Title for the legend
#            )




# name_figure=folder_path+'_supply_default_comparison_CO2_no_HP.eps'
# fig.savefig(os.path.join(dir_name,folder_path+"\\"+name_figure))



####### pie plot default  with HP
# data_sum_supply_default = df.filter(
#     model=model, scenario=scenario, variable=["Sum supply default|Self financed|*"]
# )
# data_sum_supply_default_comparison = df_comparison.filter(
#     model=model_comparison, scenario=scenario_comparison, variable=["Sum supply default|Self financed|*"]
# )
# data_sum_supply_default_comparison_2 = df_comparison_2.filter(
#     model=model_comparison_2, scenario=scenario_comparison_2, variable=["Sum supply default|Self financed|*"]
# )
# data_sum_supply_default_comparison_3= df_comparison_3.filter(
#     model=model_comparison_3, scenario=scenario_comparison_3, variable=["Sum supply default|Self financed|*"]
# )
# data_sum_supply_default_comparison_4= df_comparison_4.filter(
#     model=model_comparison_4, scenario=scenario_comparison_4, variable=["Sum supply default|Self financed|*"]
# )


# values_default = data_sum_supply_default.data["value"]
# values_default_comparison  = data_sum_supply_default_comparison.data["value"]
# values_default_comparison_2 = data_sum_supply_default_comparison_2.data["value"]
# values_default_comparison_3 = data_sum_supply_default_comparison_3.data["value"]
# values_default_comparison_4 = data_sum_supply_default_comparison_4.data["value"]

# variables_default = data_sum_supply_default.filter( 
#     variable="Sum supply default|Self financed|*"
# ).variable


# x_labels_default = [string.split("Sum supply default|Self financed|")[1] for string in variables_default]


# fig, axs = plt.subplots(2, 2)


# def func(pct, allvals):
#     absolute = int(round(pct / 100.0 * np.sum(allvals)))
#     if pct > 0:
#         return "{:.1f}%({:d} kWh)".format(pct, absolute)
#     else:
#         return ""


# patches, texts, autotexts = axs[0,0].pie(
#     values_default,
#     autopct=lambda pct: func(pct, values_default),
#     pctdistance=0.5,
#     colors=colors_all,
#     labeldistance=1.1,
# )

# axs[0,0].set_title("Default price ",fontsize=10)

# patches, texts, autotexts = axs[0,1].pie(
#     values_default_comparison,
#     autopct=lambda pct: func(pct, values_default_comparison),
#     pctdistance=0.5,
#     colors=colors_all,
#     labeldistance=1.1,
# )


# axs[0,1].set_title("70€/tCO2",fontsize=10)

# patches, texts, autotexts = axs[1,0].pie(
#     values_default_comparison_2  ,
#     autopct=lambda pct: func(pct, values_default_comparison_2),
#     pctdistance=0.5,
#     colors=colors_all,
#     labeldistance=1.1,
# )

# axs[1,0].set_title("115 and 200€/tCO2",fontsize=10)

# patches, texts, autotexts = axs[1,1].pie(
#     values_default_comparison_4,
#     autopct=lambda pct: func(pct, values_default_comparison_4),
#     pctdistance=0.5,
#     colors=colors_all,
#     labeldistance=1.1,
# )

# axs[1,1].set_title("250€/tCO2",fontsize=10)

# # patches, texts, autotexts = axs[1].pie(
# #     values_default_comparison_4,
# #     autopct=lambda pct: func(pct, values_default),
# #     pctdistance=0.5,
# #     colors=colors_all,
# #     labeldistance=1.1,
# # )

# # axs[1].set_title("250€/tCO2",fontsize=10)




# # axs[0,0].legend(
# #     patches,
# #     x_labels_default,
# #     title="Sum Supply",
# #     loc="center left",
# #     bbox_to_anchor=(1, 0, 0.5, 1),
# # )

# for patch, txt in zip(patches, autotexts):
#     # the angle at which the text is located
#     ang = (patch.theta2 + patch.theta1) / 2.0
#     # new coordinates of the text, 0.7 is the distance from the center
#     x = patch.r * 1.2 * np.cos(ang * np.pi / 180)
#     y = patch.r * 1.2 * np.sin(ang * np.pi / 180)
#     # if patch is narrow enough, move text to new coordinates
#     if (patch.theta2 - patch.theta1) < 1:
#         txt.set_position((x, y))

# # axs[0,0].set_title("Sum supply from Grid")

# # plt.legend(x_labels_default, loc = 'lower center',  bbox_to_anchor=(0.5, 0),
# #             bbox_transform = plt.gcf().transFigure )

# # plt.legend(x_labels_default, loc='upper center', bbox_to_anchor=(0.5, 0), bbox_transform=plt.gcf().transFigur)

# fig.legend(labels=x_labels_default,   # The labels for each line
#             loc=(0.4, 0.4),
#            #loc="right",   # Position of legend
#            borderaxespad=0.1,    # Small spacing around legend box
#            title="Supply from grid"  # Title for the legend
#            )




# name_figure=folder_path+'_supply_default_comparison_CO2_HP.eps'
# fig.savefig(os.path.join(dir_name,folder_path+"\\"+name_figure))

############## comparing costs of DH and default

# data_costs_revenue = df.filter(
#     model=model,
#     scenario=scenario,
#     variable=["Cost|*","Revenue"])

# data_costs_revenue_comparison_DH= df_comparison_DH.filter(
#     model=model_comparison_DH,
#     scenario=scenario_comparison_DH,
#     variable=["Cost|*","Revenue"])
# # data_costs_revenue_min_CO2 = df_comparison_2.filter(
# #     model=model_comparison_2,
# #     scenario=scenario_comparison_2,
# #     variable=["Cost|*","Revenue"])



# variables_cost= data_costs_revenue.filter(variable="Cost|*").variable
# x_labels_cost = [string.split("|")[1] for string in variables_cost]+['Revenue']
# total=x_labels_cost[3]
# x_labels_cost[3]=x_labels_cost[5]
# x_labels_cost[5]=total

# y_comparison = data_costs_revenue_comparison_DH.data["value"]
# total=y_comparison[3]
# y_comparison[3]=y_comparison[5]
# y_comparison[5]=total

# # y_min_CO = data_costs_revenue_min_CO2.data["value"]

# y_value = data_costs_revenue.data["value"]
# total=y_value[3]
# y_value[3]=y_value[5]
# y_value[5]=total
# # y_self_financed[2] = 5
# # y_self_financed[3] = 20
# x = np.arange(len(x_labels_cost))
# width = 0.2  # the width of the bars: can also be len(x) sequence

# # plt.style.use("science")
# fig, ax = plt.subplots()
# rects1 = ax.bar(
#     x+ width/2, y_comparison, width, label="DH without HP",
# )
# rects2 =ax.bar(x - width/2,y_value,width,label="default Gas connection",
# )
# # rects3 =ax.bar(x - width,y_min_CO,width,label="Min CO2 scenario",color="cornflowerblue",
# # )

# ax.set_ylabel('Yealy costs in €')
# # ax.set_title('Cost difference depending on HP')
# ax.set_xticks(x)
# ax.set_xticklabels(x_labels_cost)
# ax.legend()

# ax.bar_label(rects1, padding= 1)
# ax.bar_label(rects2, padding=1, label_type='center')
# # ax.bar_label(rects3, padding=3)

# name_figure=folder_path+'_comparison_costs_DH.eps'
# fig.savefig(os.path.join(dir_name,folder_path+"\\"+name_figure))






plt.tight_layout()
plt.show()
