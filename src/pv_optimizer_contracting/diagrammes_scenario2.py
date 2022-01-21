from re import X
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


output_file_path = Path(__file__).parent / "data_output_one_year_30_household_10_cars_50kWh_scenario2.csv"


output_file_path_comparison = Path(__file__).parent / "data_output_one_year_30_household_10_cars_50kWh_scenario2_60%_var.csv"

output_file_path_CO_200_DH = Path(__file__).parent / "data_output_one_year_30_household_10_cars_50kWh_scenario2_CO_200_new_formula.csv"
output_file_path_CO_2_times_DH = Path(__file__).parent / "data_output_one_year_30_household_10_cars_50kWh_scenario2_new_formula_HP_2_times_DH.csv"

output_file_path_ST_20 = Path(__file__).parent / "data_output_one_year_30_household_10_cars_50kWh_scenario2_ST_to_DH_20_cent.csv"
output_file_path_ST_30 = Path(__file__).parent / "data_output_one_year_30_household_10_cars_50kWh_scenario2_ST_to_DH_30_cent.csv"
output_file_path_ST_40 = Path(__file__).parent / "data_output_one_year_30_household_10_cars_50kWh_scenario2_ST_to_DH_40_cent.csv"
# output_file_path_comparison_2 = Path(__file__).parent / "data_output_one_year_30_household_3_cars_140kWh_scenario1_60%_inv_cost.csv"
# output_file_path_comparison = Path(__file__).parent /  "data_output_one_year_30_household_3_cars_140kWh_scenario1_CO_70_HP.csv"
# output_file_path_comparison_2 =Path(__file__).parent /  "data_output_one_year_30_household_3_cars_140kWh_scenario1_CO_115_HP.csv"
# output_file_path_comparison_3 = Path(__file__).parent / "data_output_one_year_30_household_3_cars_140kWh_scenario1_CO_200_HP.csv"
# output_file_path_comparison_4 = Path(__file__).parent / "data_output_one_year_30_household_3_cars_140kWh_scenario1_CO_250_HP.csv"
# output_file_path_comparison_DH = Path(__file__).parent / "data_output_one_year_30_household_3_cars_140kWh_scenario1_DH.csv"

dir_name='C:\\Users\\Thomas\\OneDrive\\Desktop\\DA\\Bilder_Ergebnisse\\'
folder_path='Scenario_2'



df = py.IamDataFrame(output_file_path)
df_comparison = py.IamDataFrame(output_file_path_comparison)
df_ST_20 =py.IamDataFrame(output_file_path_ST_20)
df_ST_30 =py.IamDataFrame(output_file_path_ST_30)
df_ST_40 =py.IamDataFrame(output_file_path_ST_40)

df_DH_200=py.IamDataFrame(output_file_path_CO_200_DH)
df_2_times_DH =py.IamDataFrame(output_file_path_CO_2_times_DH)

# df_comparison_2 = py.IamDataFrame(output_file_path_comparison_2)
# df_comparison_3 = py.IamDataFrame(output_file_path_comparison_3)
# df_comparison_4 = py.IamDataFrame(output_file_path_comparison_4)
# df_comparison_DH = py.IamDataFrame(output_file_path_comparison_DH)
# df = py.IamDataFrame(df_all_results)
# # print(df)

model, scenario = "Contracting_model", "Scenario 2"

model_comparison, scenario_comparison = "Contracting_model", "Scenario 2 60% var"
model_ST_20, scenario_ST_20 = "Contracting_model", "Scenario 2 ST to DH 20 cent no PV"
model_ST_30, scenario_ST_30 = "Contracting_model", "Scenario 2 ST to DH 30 cent no PV"
model_ST_40, scenario_ST_40 = "Contracting_model", "Scenario 2 ST to DH 40 cent no PV"

model_DH_200, scenario_DH_200 = "Contracting_model", "Scenario 2 CO 200 new formula"
model_2_times_DH, scenario_2_times_DH = "Contracting_model", "Scenario 2 new formula HP 2x DH"


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


###### new capacities stacked bar plot
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
# ax.set_ylabel('New capacities in kW/kWh/psc.')
# ax2.set_ylabel('Reduction heating demand in %')
# x = np.arange(len(x_labels))

# p1 = ax.bar(x , y_self_financed, width=width, align='center', color=colors_self_finance,  label='financed without contractor')
# p2 = ax.bar(x, y_contractor, width=width, align='center' ,bottom=y_self_financed, color=colors_contractor, label='financed by contractor')
# p3 = ax2.bar(x, y_self_financed_insu, width=width, align='center', color=colors_self_finance)
# p4 = ax2.bar(x, y_contractor_insu, width=width, align='center', bottom=y_self_financed_insu, color=colors_contractor)

# # # lns = [p1,p2,p3,p4]
# ax.legend(loc='best')

# ax.set_xticks(x)
# ax.set_xticklabels(x_labels)



# # ax.set_title("New Investments Scenario 2")

# name_figure=folder_path+'_new_capacities.eps'
# fig.savefig(os.path.join(dir_name,folder_path+"\\"+name_figure))


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
# ax.set_ylim(-10000, 60000)

# ax.text(0.91,52300,'52000')
# ax.bar_label(rects1, padding=1)
# ax.bar_label(rects2, padding=1)
# # ax.bar_label(rects3, padding=1)
# # ax.bar_label(rects3, padding=3)

# name_figure=folder_path+'_comparison_costs_tenants_contractor.eps'
# fig.savefig(os.path.join(dir_name,folder_path+"\\"+name_figure))

# # ######### pie plot default  
# data_sum_supply_default = df.filter(
#     model=model, scenario=scenario, variable=["Sum supply default|Self financed|*"]
# )
# values_default = data_sum_supply_default.data["value"]

# variables_default = data_sum_supply_default.filter( 
#     variable="Sum supply default|Self financed|*"
# ).variable


# x_labels_default = [string.split("Sum supply default|Self financed|")[1] for string in variables_default]



# fig, ax = plt.subplots()


# def func(pct, allvals):
#     absolute = int(round(pct / 100.0 * np.sum(allvals)))
#     if pct > 0:
#         return "{:.1f}%({:d} kWh)".format(pct, absolute)
#     else:
#         return ""


# patches, texts, autotexts = ax.pie(
#     values_default,
#     autopct=lambda pct: func(pct, values_default),
#     pctdistance=0.5,
#     colors=colors_all,
#     labeldistance=1.1,
# )

# ax.legend(
#     patches,
#     x_labels_default,
#     title="Sum Supply",
#     loc="center left",
#     bbox_to_anchor=(1, 0, 0.5, 1),
# )

# for patch, txt in zip(patches, autotexts):
#     # the angle at which the text is located
#     ang = (patch.theta2 + patch.theta1) / 2.0
#     # new coordinates of the text, 0.7 is the distance from the center
#     x = patch.r * 1.2 * np.cos(ang * np.pi / 180)
#     y = patch.r * 1.2 * np.sin(ang * np.pi / 180)
#     # if patch is narrow enough, move text to new coordinates
#     if (patch.theta2 - patch.theta1) < 1:
#         txt.set_position((x, y))

# # ax.set_title("Sum supply from Grid")


# name_figure=folder_path+'_supply_default_self_financed.eps'
# fig.savefig(os.path.join(dir_name,folder_path+"\\"+name_figure))


# ########## Revenue, costs,contractor rate bar plot
# data_revenues_rates = df.filter(
#     model=model,
#     scenario=scenario,
#     variable=["Revenue Contractor|*", "Contractor Rate|*"],
# )

# data_revenues_rates_var60 = df_comparison.filter(
#     model=model_comparison,
#     scenario=scenario_comparison,
#     variable=["Revenue Contractor|*", "Contractor Rate|*"],
# )

# # )
# variables_new_tech = df.filter(
#     variable="Capacity|Self financed|*"
# ).variable
# x_labels = [string.split("|")[2] for string in variables_new_tech] + ["Reduction \n Heating Demand" ]
# x_labels[1]="Charging \n Station" 


# y_contractor_rate= data_revenues_rates.filter(variable="Contractor Rate|*").data["value"]
# temp=y_contractor_rate[3]
# y_contractor_rate[3]=y_contractor_rate[4]
# y_contractor_rate[4]=temp
# print('y_contractor_rate: ', y_contractor_rate)
# y_revenues= data_revenues_rates.filter(variable="Revenue Contractor|*").data["value"]
# print('y_revenues: ', y_revenues)
# temp=y_revenues[3]
# y_revenues[3]=y_revenues[4]
# y_revenues[4]=temp
# y_var_revenues=y_revenues-y_contractor_rate
# print('y_var_revenues: ', y_var_revenues)

# y_contractor_rate_comparison= data_revenues_rates_var60.filter(variable="Contractor Rate|*").data["value"]
# temp=y_contractor_rate_comparison[3]
# y_contractor_rate_comparison[3]=y_contractor_rate_comparison[4]
# y_contractor_rate_comparison[4]=temp
# print('y_contractor_rate_comparison: ', y_contractor_rate_comparison)
# y_revenues_comparison= data_revenues_rates_var60.filter(variable="Revenue Contractor|*").data["value"]
# temp=y_revenues_comparison[3]
# y_revenues_comparison[3]=y_revenues_comparison[4]
# y_revenues_comparison[4]=temp
# y_var_revenues_comparison=y_revenues_comparison-y_contractor_rate_comparison
# print('y_var_revenues_comparison: ', y_var_revenues_comparison)


# width = 0.2  # the width of the bars: can also be len(x) sequence
# # # plt.style.use("science")

# fig, ax = plt.subplots()

# ax.set_ylabel('Revenues for Contractor in €')
# x = np.arange(len(x_labels))

# p1 = ax.bar(x-width/2, y_contractor_rate, width=width, align='center', color='blue',hatch = '.', label='Contractor rate - 80% variable cost')
# p2 = ax.bar(x-width/2,y_var_revenues, width=width, align='center' ,bottom=y_contractor_rate, color='red', hatch = '.', label='Variable renvenue - 80% variable cost')
# p3 = ax.bar(x+width/2, y_contractor_rate_comparison, width=width, align='center', color='blue', hatch = '/',label='Contractor rate - 60% variable cost')
# p4 = ax.bar(x+width/2,y_var_revenues_comparison, width=width, align='center' ,bottom=y_contractor_rate_comparison, color='red', hatch = '/',label='Variable renvenue - 60% variable cost')

# # # lns = [p1,p2,p3,p4]
# ax.legend() #(handles=lns) #, loc='best')

# ax.set_xticks(x)
# ax.set_xticklabels(x_labels)

# ax.set_title("Revenues Contractor")

# name_figure=folder_path+'_revenues_contractor_3_comparisons.eps'
# fig.savefig(os.path.join(dir_name,folder_path+"\\"+name_figure))

### Show ST capacity depending on DH feed-in

data_capacitiy_ST_20 = df_ST_20.filter(
    model=model_ST_20, 
    scenario=scenario_ST_20,
    variable=["Capacity|Contractor|ST"],
)

data_capacitiy_ST_40 = df_ST_40.filter(
    model=model_ST_40, 
    scenario=scenario_ST_40,
    variable=["Capacity|Contractor|ST"],
)
data_capacitiy_ST_30 = df_ST_30.filter(
    model=model_ST_30, 
    scenario=scenario_ST_30,
    variable=["Capacity|Contractor|ST"],
)


x_labels =[0.2,0.3,0.4]


y_value_ST_20 = data_capacitiy_ST_20.data["value"]
y_value_ST_30 = data_capacitiy_ST_30.data["value"]
y_value_ST_40 = data_capacitiy_ST_40.data["value"]


x = np.arange(len(x_labels))
width = 0.3  # the width of the bars: can also be len(x) sequence

# # plt.style.use("science")
fig, ax = plt.subplots()
rects1 = ax.bar(
    0, y_value_ST_20 , width, color= "mediumblue",
)
rects2 = ax.bar(
    1, y_value_ST_30 , width, color= "mediumblue", label="New ST capacity"
)
rects3 = ax.bar(
    2, y_value_ST_40 , width, color= "mediumblue",
)



# ax.axhline(0, 0,1, linestyle="--",color='k')
ax.set_ylabel('New capacities in kW')
# ax.set_title('Yearly costs for contractor and tenants')
ax.set_xlabel('Feedin price ST2DH in €')
ax.set_xticks(x)
ax.set_xticklabels(x_labels)
ax.legend(loc=(0.02, 0.55))
# ax.set_ylim(0,100)

# ax.text(0.91,52300,'52000')
ax.bar_label(rects1, padding=1)
ax.bar_label(rects2, padding=1)
ax.bar_label(rects3, padding=1)
# ax.bar_label(rects3, padding=3)

name_figure=folder_path+'_capacity_ST_to_DH.eps'
fig.savefig(os.path.join(dir_name,folder_path+"\\"+name_figure))


###### new capacities comparison CO2 price
# data_capacitiy_new = df.filter(
#     model=model,
#     scenario=scenario,
#     variable=["Capacity|Self financed|*", "Capacity|Contractor|*","Reduction Heating Demand|*"],
# )

# data_capacitiy_DH_200= df_DH_200.filter(
#     model=model_DH_200,
#     scenario=scenario_DH_200,
#     variable=["Capacity|Self financed|*", "Capacity|Contractor|*","Reduction Heating Demand|*"],
# )

# data_capacitiy_2_times_DH= df_2_times_DH.filter(
#     model=model_2_times_DH,
#     scenario= scenario_2_times_DH,
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

# y_self_financed_comparison = data_capacitiy_DH_200.filter(variable="Capacity|Self financed|*").data["value"]
# y_self_financed_comparison_insulation = data_capacitiy_DH_200.filter(variable=["Reduction Heating Demand|Self financed"]).data["value"]

# y_self_financed_comparison.loc[len(y_self_financed_comparison.index)] = 0
# y_self_financed_comparison_insu= y_self_financed_comparison.copy()
# y_self_financed_comparison_insu.loc[1:4] = 0 
# y_self_financed_comparison_insu[5]=y_self_financed_comparison_insulation



# y_self_financed_comparison_2 = data_capacitiy_2_times_DH.filter(variable="Capacity|Self financed|*").data["value"]
# y_self_financed_comparison_insulation_2 = data_capacitiy_2_times_DH.filter(variable=["Reduction Heating Demand|Self financed"]).data["value"]

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

# y_contractor_comparison = data_capacitiy_DH_200.filter(variable="Capacity|Contractor|*").data["value"]
# y_contractor_insulation_comparison = data_capacitiy_DH_200.filter(variable=["Reduction Heating Demand|Contractor"]).data["value"]

# y_contractor_comparison.loc[len(y_contractor_comparison.index)] = 0
# y_contractor_comparison_insu= y_contractor_comparison.copy()
# y_contractor_comparison_insu.loc[1:4] = 0 
# y_contractor_comparison_insu[5]=y_contractor_insulation_comparison

# y_contractor_comparison_2 = data_capacitiy_2_times_DH.filter(variable="Capacity|Contractor|*").data["value"]
# y_contractor_insulation_comparison_2 = data_capacitiy_2_times_DH.filter(variable=["Reduction Heating Demand|Contractor"]).data["value"]

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
# # ax.set_ylim(0, 100)
# ax2.set_ylim(0, 100)
# ax.set_ylabel('New capacities in kW/kWh/psc.')

# ax2.set_ylabel('Reduction heating demand in %')
# x = np.arange(len(x_labels))

# p1 = ax.bar(x- width , y_self_financed, width=width, align='center', color= 'blue', hatch = '--')
# p2 = ax.bar(x -width, y_contractor, width=width, align='center' ,bottom=y_self_financed, color=colors_contractor,   hatch = '\\\\')
# p3 = ax2.bar(x - width, y_self_financed_insu, width=width, align='center', color='blue', hatch = '--')
# p4 = ax2.bar(x - width, y_contractor_insu, width=width, align='center' ,bottom=y_self_financed_insu, color= 'blue',   hatch = '\\\\')

# p5 = ax.bar(x + width, y_self_financed_comparison_2, width=width, align='center', color="mediumslateblue", label='2 times DH price', hatch = '--')
# p6 = ax.bar(x  + width, y_contractor_comparison_2, width=width, align='center' ,bottom=y_self_financed_comparison_2, color="mediumslateblue",   hatch = '\\\\')
# p7 = ax2.bar(x+ width, y_self_financed_comparison_insu_2, width=width, align='center', color="mediumslateblue",  hatch = '--')
# p8 = ax2.bar(x+ width, y_contractor_comparison_insu_2, width=width, align='center' ,bottom=y_self_financed_comparison_insu_2, color="mediumslateblue",   hatch = '\\\\')

# p9 = ax.bar(x , y_self_financed_comparison, width=width, align='center', color="royalblue", label='DH price with 200 €/tCO2', hatch = '--') 
# p10 = ax.bar(x, y_contractor_comparison, width=width, align='center' ,bottom=y_self_financed_comparison, color="royalblue",   hatch = '\\\\')
# p11 = ax2.bar(x, y_self_financed_comparison_insu, width=width, align='center', color="royalblue", hatch = '--')
# p12 = ax2.bar(x, y_contractor_comparison_insu, width=width, align='center' ,bottom=y_self_financed_comparison_insu, color="royalblue",   hatch = '\\\\')


# patch1 = mpatches.Patch(color='blue', label='default CO2 price')
# patch2 = mpatches.Patch(color='mediumslateblue', label='2 times DH price')
# patch3 = mpatches.Patch(color='royalblue', label='DH price with 200 €/tCO2')
# patch4 = mpatches.Patch(facecolor='ghostwhite', label='financed without contractor', hatch = '--')
# patch5 = mpatches.Patch(facecolor='ghostwhite', label='financed by contractor', hatch = '\\\\')
# plt.legend(handles=[patch1,patch3,patch2,patch4,patch5], loc=('upper right'))



# # # lns = [p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12]
# # ax.legend(loc='upper left')#handles=lns,

# ax.set_xticks(x)
# ax.set_xticklabels(x_labels)

# # ax.set_title("Comparsion new investments")

# name_figure=folder_path+'_new_capacities_comparison_CO2.eps'
# fig.savefig(os.path.join(dir_name,folder_path+"\\"+name_figure))

plt.tight_layout()
plt.show()
