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


# from pv_optimizer_contracting.new_model_copy import model
# from trial import model
from pprint import pprint
# from create_dataframe import output_file_path 
# print(output_file_path)
# output_file_path = Path(__file__).parent / "data_output_trial.csv"

# output_file_path = Path(__file__).parent / "data_output_30HH_3cars_altbau.csv"
# output_file_path = Path(__file__).parent / "data_output_30HH_3cars_altbau_default.csv"

output_file_path = Path(__file__).parent / "data_output_30HH_3cars_altbau_base.csv"
df = py.IamDataFrame(output_file_path)
# df = py.IamDataFrame(df_all_results)
# print(df)

# model, scenario = "Contracting_model", "Base 30HH 3cars rent"
model, scenario = "Contracting_model", "Base"
#################### defining colors
colors_default = ["tab:blue", "tab:cyan", "darkgrey"]
colors_new = [
    "forestgreen",
    "orange",
    "fuchsia",
    "crimson",
    "k",
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
    "k",
    "limegreen",
    "burlywood",
    "violet",
    "indianred",
    "dimgray",
]

########## bar plot for showing costs
data_costs_revenue= df.filter(variable=["Cost|*","Revenue"])
variables_cost= data_costs_revenue.filter(variable="Cost|*").variable
x_labels_cost = [string.split("|")[1] for string in variables_cost]+['Revenue']
y_cost = data_costs_revenue.data["value"]

width = 0.35  # the width of the bars: can also be len(x) sequence
# plt.style.use("science")
fig, ax = plt.subplots()
# colors = ['tab:blue', 'tab:cyan', 'tab:gray', 'tab:orange', 'tab:red']
ax.bar(x_labels_cost, y_cost, width)#, color=colors_default)
# ax.legend()
ax.axhline(0, 0,1, linestyle="--",color='k')
ax.set_title("Costs")
ax.bar_label(ax.containers[0])

########## new capacities stacked bar plot
data_capacitiy_new = df.filter(
    model=model,
    scenario=scenario,
    variable=["Capacity|Self financed|*", "Capacity|Contractor|*"],
)
variables_new_tech = data_capacitiy_new.filter(
    variable="Capacity|Self financed|*"
).variable
x_labels = [string.split("|")[2] for string in variables_new_tech]
y_self_financed = data_capacitiy_new.filter(variable="Capacity|Self financed|*").data[
    "value"
]
y_contractor = data_capacitiy_new.filter(variable="Capacity|Contractor|*").data["value"]
# y_self_financed[2] = 5
# y_self_financed[3] = 20
width = 0.35  # the width of the bars: can also be len(x) sequence
# plt.style.use("science")
fig, ax = plt.subplots()
rects1 = ax.bar(
    x_labels, y_self_financed, width, label="Self financed", color=colors_self_finance
)

rects2 =ax.bar(
    x_labels,
    y_contractor,
    width,
    bottom=y_self_financed,
    label="Contractor",
    color=colors_contractor,
)
ax.legend()
ax.set_title("New Capacities")
# ax.bar_label(rects1, padding=3,label_type='center')
# ax.bar_label(rects2, padding=3,label_type='center')

############# default capacities bar plot
data_capacity_default = df.filter(variable="Connection Capacity|*")
variables_default = data_capacity_default.filter(
    variable="Connection Capacity|*"
).variable

x_labels_default = [string.split("|")[1] for string in variables_default]

y_default = data_capacity_default.filter(variable="Connection Capacity|*").data["value"]
width = 0.35  # the width of the bars: can also be len(x) sequence
# plt.style.use("science")
fig, ax = plt.subplots()
# colors = ['tab:blue', 'tab:cyan', 'tab:gray', 'tab:orange', 'tab:red']
ax.bar(x_labels_default, y_default, width, color=colors_default)
# ax.legend()
ax.set_title("Default Connection Capacities")
ax.bar_label(ax.containers[0])


########## pie plot default  (this needs to be from default scenario)
data_sum_supply_default = df.filter(
    model=model, scenario=scenario, variable="Sum supply default|*"
)
values_default = data_sum_supply_default.filter(variable="Sum supply default|*").data[
    "value"
]

fig, ax = plt.subplots()


def func(pct, allvals):
    absolute = int(round(pct / 100.0 * np.sum(allvals)))
    if pct > 0:
        return "{:.1f}%({:d} kWh)".format(pct, absolute)
    else:
        return ""


patches, texts, autotexts = ax.pie(
    values_default,
    autopct=lambda pct: func(pct, values_default),
    pctdistance=0.5,
    colors=colors_default,
    labeldistance=1.1,
)

ax.legend(
    patches,
    x_labels_default,
    title="Sum Supply",
    loc="center left",
    bbox_to_anchor=(1, 0, 0.5, 1),
)

for patch, txt in zip(patches, autotexts):
    # the angle at which the text is located
    ang = (patch.theta2 + patch.theta1) / 2.0
    # new coordinates of the text, 0.7 is the distance from the center
    x = patch.r * 1.2 * np.cos(ang * np.pi / 180)
    y = patch.r * 1.2 * np.sin(ang * np.pi / 180)
    # if patch is narrow enough, move text to new coordinates
    if (patch.theta2 - patch.theta1) < 1:
        txt.set_position((x, y))

ax.set_title("Sum supply default")

########## pie plot supply all
data_sum_supply_all = df.filter(
    model=model,
    scenario=scenario,
    variable=[
        "Sum supply default|*",
        "Sum supply new|Contractor|*",
        "Sum supply new|Self financed|*",
    ],
)
values_supply_all = data_sum_supply_all.filter(
    variable=[
        "Sum supply default|*",
        "Sum supply new|Contractor|*",
        "Sum supply new|Self financed|*",
    ]
).data["value"]

variables_new_tech_all_finance = data_capacitiy_new.filter(
    variable="Capacity|*"
).variable

labels_all = [string.split("|")[1] for string in variables_default] + [
    string.split("Capacity|")[1] for string in variables_new_tech_all_finance
]

fig, ax = plt.subplots()


patches, texts, autotexts = ax.pie(
    values_supply_all,
    autopct=lambda pct: func(pct, values_supply_all),
    pctdistance=0.5,
    colors=colors_all,
    labeldistance=1.1,
)

ax.legend(
    patches,
    labels_all,
    # title="Sum Supply all",
    loc="center left",
    bbox_to_anchor=(1, 0, 0.5, 1),
)

for patch, txt in zip(patches, autotexts):
    # the angle at which the text is located
    ang = (patch.theta2 + patch.theta1) / 2.0
    # new coordinates of the text, 0.7 is the distance from the center
    x = patch.r * 1.8 * np.cos(ang * np.pi / 180)
    y = patch.r * 1.8 * np.sin(ang * np.pi / 180)
    # if patch is narrow enough, move text to new coordinates
    if (patch.theta2 - patch.theta1) < 1:
        txt.set_position((x, y))

ax.set_title("Sum supply all")

############## Supply to Car Pie Chart
data_sum_supply_to_car = df.filter(
    model=model,
    scenario=scenario,
    variable=[
        "Sum supply to Car|*",
    ],
)

values_supply_to_car = data_sum_supply_to_car.filter(
    variable=[
        "Sum supply to Car|*",
    ]
).data["value"]

variables_to_car = data_sum_supply_to_car.filter(
    variable="Sum supply to Car|*"
).variable

labels_to_car = [string.split("|")[1] for string in variables_to_car]


fig, ax = plt.subplots()


patches, texts, autotexts = ax.pie(
    values_supply_to_car,
    autopct=lambda pct: func(pct, values_supply_to_car),
    pctdistance=0.5,
    colors=["forestgreen","tab:blue","crimson"],
    labeldistance=1.1,
    # normalize=False,
)

ax.legend(
    patches,
    labels_to_car,
    # title="Sum Supply all",
    loc="center left",
    bbox_to_anchor=(1, 0, 0.5, 1),
)

for patch, txt in zip(patches, autotexts):
    # the angle at which the text is located
    ang = (patch.theta2 + patch.theta1) / 2.0
    # new coordinates of the text, 0.7 is the distance from the center
    x = patch.r * 0.9 * np.cos(ang * np.pi / 180)
    y = patch.r * 0.9 * np.sin(ang * np.pi / 180)
    # if patch is narrow enough, move text to new coordinates
    if (patch.theta2 - patch.theta1) < 1:
        txt.set_position((x, y))

ax.set_title("Sum supply to car")

############## Supply to House Household Electricity
data_sum_supply_to_household = df.filter(
    model=model,
    scenario=scenario,
    variable=[
        "Sum supply from PV|Self financed|Household",
        "Sum supply from PV|Contractor|Household",
        "Sum supply from Grid|Household",
    ],
)

values_supply_to_household = data_sum_supply_to_household.data["value"]

variables_to_household = data_sum_supply_to_household.variable

labels_to_household = [
    string.split("|Household")[0] for string in variables_to_household
]

fig, ax = plt.subplots()

patches, texts, autotexts = ax.pie(
    values_supply_to_household,
    autopct=lambda pct: func(pct, values_supply_to_household),
    pctdistance=0.5,
    colors=["tab:blue","crimson",
    "indianred"],
    labeldistance=1.1,
    # normalize=False,
)

ax.legend(
    patches,
    labels_to_household,
    # title="Sum Supply all",
    loc="center left",
    bbox_to_anchor=(1, 0, 0.5, 1),
)

for patch, txt in zip(patches, autotexts):
    # the angle at which the text is located
    ang = (patch.theta2 + patch.theta1) / 2.0
    # new coordinates of the text, 0.7 is the distance from the center
    x = patch.r * 0.9 * np.cos(ang * np.pi / 180)
    y = patch.r * 0.9 * np.sin(ang * np.pi / 180)
    # if patch is narrow enough, move text to new coordinates
    if (patch.theta2 - patch.theta1) < 1:
        txt.set_position((x, y))

ax.set_title("Electricity to Household")

############## Supply to House Household Electricity
data_sum_supply_thermal_to_household = df.filter(
    model=model,
    scenario=scenario,
    variable=[
        "Sum supply from ST|Self financed|Household",
        "Sum supply from ST|Contractor|Household",
        "Sum supply new|Self financed|HP",
        "Sum supply new|Contractor|HP",
        "Sum supply default|Gas",
        "Sum supply default|DH",
    ],
)

values_sum_supply_thermal_to_household = data_sum_supply_thermal_to_household.data[
    "value"
]

variables_thermal_to_household_2 = data_sum_supply_thermal_to_household.filter(
    variable=["Sum supply new|Contractor|HP","Sum supply new|Self financed|HP", ]
).variable
variables_thermal_to_household_3 = data_sum_supply_thermal_to_household.filter(
    variable=["Sum supply default|DH","Sum supply default|Gas"]
).variable


labels_to_household_thermal = (
    [string.split("|")[1] for string in variables_thermal_to_household_3]
    + ["Contractor|ST","Self financed|ST"]
    + [
        string.split("Sum supply new|")[1]
        for string in variables_thermal_to_household_2
    ]
)

fig, ax = plt.subplots()


patches, texts, autotexts = ax.pie(
    values_sum_supply_thermal_to_household,
    autopct=lambda pct: func(pct, values_sum_supply_thermal_to_household),
    pctdistance=0.5,
    colors=[
    "tab:blue",
    "darkgrey",
    "k",
    "dimgray",
    "fuchsia",
    "orange",
    "violet",
],
    labeldistance=1.1,
    # normalize=False,
)

ax.legend(
    patches,
    labels_to_household_thermal,
    # title="Sum Supply all",
    loc="center left",
    bbox_to_anchor=(1, 0, 0.5, 1),
)

for patch, txt in zip(patches, autotexts):
    # the angle at which the text is located
    ang = (patch.theta2 + patch.theta1) / 2.0
    # new coordinates of the text, 0.7 is the distance from the center
    x = patch.r * 0.9 * np.cos(ang * np.pi / 180)
    y = patch.r * 0.9 * np.sin(ang * np.pi / 180)
    # if patch is narrow enough, move text to new coordinates
    if (patch.theta2 - patch.theta1) < 1:
        txt.set_position((x, y))

ax.set_title("Thermal supply to Household")


plt.tight_layout()

plt.show()
