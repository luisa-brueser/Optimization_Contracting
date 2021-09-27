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
from trial import model
from pprint import pprint

# output_file_path = Path(__file__).parent / "data_output_trial.csv"


output_file_path = Path(__file__).parent / "data_output_30HH_3cars_altbau_needs_contractor.csv"



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
    "Scenario": "Needs Contractor",
    "Region": "Vienna City Center",
    "Variable": None,
    "Unit": "kW",
}
results_cost = dict() 

results_cost["Investment"] = None
results_cost["Investment"] = data_template.copy()
results_cost["Investment"]["Variable"] = "Cost|" + "Investment"
d = {0: round(model.investment_costs_total.value)}
results_cost["Investment"].update(d)

results_cost["Service"] = None
results_cost["Service"] = data_template.copy()
results_cost["Service"]["Variable"] = "Cost|" + "Service"
d = {0: round(model.service_costs_total.value)}
results_cost["Service"].update(d)

results_cost["Connection"] = None
results_cost["Connection"] = data_template.copy()
results_cost["Connection"]["Variable"] = "Cost|" + "Connection"
d = {0: round(model.connection_costs_total.value)}
results_cost["Connection"].update(d)

results_cost["Variable"] = None
results_cost["Variable"] = data_template.copy()
results_cost["Variable"]["Variable"] = "Cost|" + "Variable"
d = {0: round(model.variable_cost_total.value)}
results_cost["Variable"].update(d)

results_cost["Revenue"] = None
results_cost["Revenue"] = data_template.copy()
results_cost["Revenue"]["Variable"] = "Revenue"
d = {0: - round(model.revenue.value)}
results_cost["Revenue"].update(d)

results_cost["Total"] = None
results_cost["Total"] = data_template.copy()
results_cost["Total"]["Variable"] = "Cost|" + "Total"
d = {0: round(model.obj())}
results_cost["Total"].update(d)

df_results_cost = pd.DataFrame.from_dict(data=results_cost).T
# print('df_results_cost: ', df_results_cost)


results_demand = dict.fromkeys(model.set_demand)
for key in results_demand.keys():
    results_demand[key] = data_template.copy()
    # results_demand[key]["Region"] = 'Vienna'
    results_demand[key]["Variable"] = "Demand|" + str(key)


for option in results_demand.keys():
    for time in model.set_time:
        d = {time: model.demand[time, option]}
        results_demand[option].update(d)


# adding shifted demand
results_demand["Shifted Demand"] = None
results_demand["Shifted Demand"] = data_template.copy()
results_demand["Shifted Demand"]["Variable"] = "Demand|" + "Shifted Demand"

for time in model.set_time:
    d = {time: model.shifted_demand[time].value}
    results_demand["Shifted Demand"].update(d)

df_results_demand = pd.DataFrame.from_dict(data=results_demand).T
# print("df_results_demand: ", df_results_demand)

results_capacity_default = dict.fromkeys(model.set_default_technologies)
for key in results_capacity_default.keys():
    results_capacity_default[key] = data_template.copy()
    # results_capacity_new_contractor[key]["Region"] = 'Vienna'
    results_capacity_default[key]["Variable"] = "Connection Capacity|" + str(key)

for option in results_capacity_default.keys():
    d = {
        0: round(
            model.connection_capacity_default[option]
            * model.binary_default_technologies[option].value
        )
    }
    results_capacity_default[option].update(d)

df_results_capacity_default = pd.DataFrame.from_dict(data=results_capacity_default).T

results_supply_default = dict.fromkeys(model.set_default_technologies)
for key in results_supply_default.keys():
    results_supply_default[key] = data_template.copy()
    # results_capacity_new_contractor[key]["Region"] = 'Vienna'
    results_supply_default[key]["Variable"] = "Supply default|" + str(key)

for option in results_supply_default.keys():
    for time in model.set_time:
        d = {time: (model.supply_default[time, option].value)}
        results_supply_default[option].update(d)
df_results_supply_default = pd.DataFrame.from_dict(data=results_supply_default).T


results_sum_supply_default = dict.fromkeys(model.set_default_technologies)
for key in results_sum_supply_default.keys():
    results_sum_supply_default[key] = data_template.copy()
    # results_capacity_new_contractor[key]["Region"] = 'Vienna'
    results_sum_supply_default[key]["Variable"] = "Sum supply default|" + str(key)

for option in results_sum_supply_default.keys():
    d = {
        0: round(
            sum(model.supply_default[time, option].value for time in model.set_time)
        )
    }
    results_sum_supply_default[option].update(d)
df_results_sum_supply_default = pd.DataFrame.from_dict(
    data=results_sum_supply_default
).T

# # pprint(df_results_supply_default)
# show = df_results_supply_default.iloc[:, :5]
# # pprint(show)
# test = DataFrame(df_results_supply_default.iloc[:, 6:].sum(axis=1), columns=["0"])


# # .groupby(
# #     ["Model", "Scenario", "Region", "Variable", "Unit"], as_index=False
# # )


# # pprint(df_results_sum_supply_default)

# # new = show.add(df_results_sum_supply_default)
# df_results_sum_supply_default = pd.concat([show, test], axis=1)
# # pprint(new)

results_capacity_new_contractor = dict.fromkeys(model.set_new_technologies)
for key in results_capacity_new_contractor.keys():
    results_capacity_new_contractor[key] = data_template.copy()
    # results_capacity_new_contractor[key]["Region"] = 'Vienna'
    results_capacity_new_contractor[key]["Variable"] = "Capacity|Contractor|" + str(key)

for option in results_capacity_new_contractor.keys():
    d = {0: round(model.capacity["Contractor", option].value)}
    results_capacity_new_contractor[option].update(d)
df_results_capacity_new_contractor = pd.DataFrame.from_dict(
    data=results_capacity_new_contractor
).T

results_capacity_new_self_financed = dict.fromkeys(model.set_new_technologies)
for key in results_capacity_new_self_financed.keys():
    results_capacity_new_self_financed[key] = data_template.copy()
    # results_capacity_new_self_financed[key]["Region"] = 'Vienna'
    results_capacity_new_self_financed[key][
        "Variable"
    ] = "Capacity|Self financed|" + str(key)

for option in results_capacity_new_self_financed.keys():
    d = {0: round(model.capacity["Self financed", option].value)}
    results_capacity_new_self_financed[option].update(d)
df_results_capacity_new_self_financed = pd.DataFrame.from_dict(
    data=results_capacity_new_self_financed
).T


results_supply_contractor = dict.fromkeys(model.set_new_technologies)
for key in results_supply_contractor.keys():
    results_supply_contractor[key] = data_template.copy()
    # results_supply_contractor[key]["Region"] = 'Vienna'
    results_supply_contractor[key]["Variable"] = "Supply|Contractor|" + str(key)

for option in results_supply_contractor.keys():
    for time in model.set_time:
        d = {time: round(model.supply_new[time, "Contractor", option].value)}
        results_supply_contractor[option].update(d)
df_results_supply_contractor = pd.DataFrame.from_dict(data=results_supply_contractor).T

results_supply_self_financed = dict.fromkeys(model.set_new_technologies)
for key in results_supply_self_financed.keys():
    results_supply_self_financed[key] = data_template.copy()
    # results_supply_self_financed[key]["Region"] = key
    results_supply_self_financed[key]["Variable"] = "Supply|Self financed|" + str(key)

for option in results_supply_self_financed.keys():
    for time in model.set_time:
        d = {time: round(model.supply_new[time, "Self financed", option].value)}
        results_supply_self_financed[option].update(d)
df_results_supply_self_financed = pd.DataFrame.from_dict(
    data=results_supply_self_financed
).T

results_sum_supply_contractor = dict.fromkeys(model.set_new_technologies)
for key in results_sum_supply_contractor.keys():
    results_sum_supply_contractor[key] = data_template.copy()
    # results_capacity_new_contractor[key]["Region"] = 'Vienna'
    results_sum_supply_contractor[key]["Variable"] = "Sum supply new|Contractor|" + str(
        key
    )


for option in results_sum_supply_contractor.keys():
    d = {
        0: round(
            sum(
                model.supply_new[time, "Contractor", option].value
                for time in model.set_time
            )
        )
    }
    results_sum_supply_contractor[option].update(d)
df_results_sum_supply_contractor = pd.DataFrame.from_dict(
    data=results_sum_supply_contractor
).T


results_sum_supply_self_financed = dict.fromkeys(model.set_new_technologies)
for key in results_sum_supply_self_financed.keys():
    results_sum_supply_self_financed[key] = data_template.copy()
    # results_capacity_new_contractor[key]["Region"] = 'Vienna'
    results_sum_supply_self_financed[key][
        "Variable"
    ] = "Sum supply new|Self financed|" + str(key)


for option in results_sum_supply_self_financed.keys():
    d = {
        0: round(
            sum(
                model.supply_new[time, "Self financed", option].value
                for time in model.set_time
            )
        )
    }
    results_sum_supply_self_financed[option].update(d)
df_results_sum_supply_self_financed = pd.DataFrame.from_dict(
    data=results_sum_supply_self_financed
).T


results_supply_from_PV_self_financed = dict.fromkeys(model.set_PV2)
for key in results_supply_from_PV_self_financed.keys():
    results_supply_from_PV_self_financed[key] = data_template.copy()
    # results_supply_from_PV_self_financed[key]["Region"] = key
    results_supply_from_PV_self_financed[key][
        "Variable"
    ] = "Supply from PV|Self financed|" + str(key)

for option in results_supply_from_PV_self_financed.keys():
    for time in model.set_time:
        d = {time: round(model.supply_from_PV[time, "Self financed", option].value)}
        results_supply_from_PV_self_financed[option].update(d)
df_results_supply_from_PV_self_financed = pd.DataFrame.from_dict(
    data=results_supply_from_PV_self_financed
).T

results_sum_supply_from_PV_self_financed = dict.fromkeys(model.set_PV2)
for key in results_sum_supply_from_PV_self_financed.keys():
    results_sum_supply_from_PV_self_financed[key] = data_template.copy()
    # results_supply_from_PV_contractor[key]["Region"] = 'Vienna'
    results_sum_supply_from_PV_self_financed[key][
        "Variable"
    ] = "Sum supply from PV|Self financed|" + str(key)

for option in results_sum_supply_from_PV_self_financed.keys():
    d = {
        0: round(
            sum(
                model.supply_from_PV[time, "Self financed", option].value
                for time in model.set_time
            )
        )
    }
    results_sum_supply_from_PV_self_financed[option].update(d)
df_results_sum_supply_from_PV_self_financed = pd.DataFrame.from_dict(
    data=results_sum_supply_from_PV_self_financed
).T


results_supply_from_PV_contractor = dict.fromkeys(model.set_PV2)
for key in results_supply_from_PV_contractor.keys():
    results_supply_from_PV_contractor[key] = data_template.copy()
    # results_supply_from_PV_contractor[key]["Region"] = 'Vienna'
    results_supply_from_PV_contractor[key][
        "Variable"
    ] = "Supply from PV|Contractor|" + str(key)

for option in results_supply_from_PV_contractor.keys():
    for time in model.set_time:
        d = {time: round(model.supply_from_PV[time, "Contractor", option].value)}
        results_supply_from_PV_contractor[option].update(d)
df_results_supply_from_PV_contractor = pd.DataFrame.from_dict(
    data=results_supply_from_PV_contractor
).T

results_sum_supply_from_PV_contractor = dict.fromkeys(model.set_PV2)
for key in results_sum_supply_from_PV_contractor.keys():
    results_sum_supply_from_PV_contractor[key] = data_template.copy()
    # results_supply_from_PV_contractor[key]["Region"] = 'Vienna'
    results_sum_supply_from_PV_contractor[key][
        "Variable"
    ] = "Sum supply from PV|Contractor|" + str(key)

for option in results_sum_supply_from_PV_contractor.keys():
    d = {
        0: round(
            sum(
                model.supply_from_PV[time, "Contractor", option].value
                for time in model.set_time
            )
        )
    }
    results_sum_supply_from_PV_contractor[option].update(d)
df_results_sum_supply_from_PV_contractor = pd.DataFrame.from_dict(
    data=results_sum_supply_from_PV_contractor
).T

results_supply_from_ST_self_financed = dict.fromkeys(model.set_ST2)
for key in results_supply_from_ST_self_financed.keys():
    results_supply_from_ST_self_financed[key] = data_template.copy()
    # results_supply_from_ST_self_financed[key]["Region"] = key
    results_supply_from_ST_self_financed[key][
        "Variable"
    ] = "Supply from ST|Self financed|" + str(key)

for option in results_supply_from_ST_self_financed.keys():
    for time in model.set_time:
        d = {time: round(model.supply_from_ST[time, "Self financed", option].value)}
        results_supply_from_ST_self_financed[option].update(d)
df_results_supply_from_ST_self_financed = pd.DataFrame.from_dict(
    data=results_supply_from_ST_self_financed
).T

results_sum_supply_from_ST_self_financed = dict.fromkeys(model.set_ST2)
for key in results_sum_supply_from_ST_self_financed.keys():
    results_sum_supply_from_ST_self_financed[key] = data_template.copy()
    # results_supply_from_ST_contractor[key]["Region"] = 'Vienna'
    results_sum_supply_from_ST_self_financed[key][
        "Variable"
    ] = "Sum supply from ST|Self financed|" + str(key)

for option in results_sum_supply_from_ST_self_financed.keys():
    d = {
        0: round(
            sum(
                model.supply_from_ST[time, "Self financed", option].value
                for time in model.set_time
            )
        )
    }
    results_sum_supply_from_ST_self_financed[option].update(d)
df_results_sum_supply_from_ST_self_financed = pd.DataFrame.from_dict(
    data=results_sum_supply_from_ST_self_financed
).T


results_supply_from_ST_contractor = dict.fromkeys(model.set_ST2)
for key in results_supply_from_ST_contractor.keys():
    results_supply_from_ST_contractor[key] = data_template.copy()
    # results_supply_from_ST_contractor[key]["Region"] = 'Vienna'
    results_supply_from_ST_contractor[key][
        "Variable"
    ] = "Supply from ST|Contractor|" + str(key)

for option in results_supply_from_ST_contractor.keys():
    for time in model.set_time:
        d = {time: round(model.supply_from_ST[time, "Contractor", option].value)}
        results_supply_from_ST_contractor[option].update(d)
df_results_supply_from_ST_contractor = pd.DataFrame.from_dict(
    data=results_supply_from_ST_contractor
).T

results_sum_supply_from_ST_contractor = dict.fromkeys(model.set_ST2)
for key in results_sum_supply_from_ST_contractor.keys():
    results_sum_supply_from_ST_contractor[key] = data_template.copy()
    # results_supply_from_ST_contractor[key]["Region"] = 'Vienna'
    results_sum_supply_from_ST_contractor[key][
        "Variable"
    ] = "Sum supply from ST|Contractor|" + str(key)

for option in results_sum_supply_from_ST_contractor.keys():
    d = {
        0: round(
            sum(
                model.supply_from_ST[time, "Contractor", option].value
                for time in model.set_time
            )
        )
    }
    results_sum_supply_from_ST_contractor[option].update(d)
df_results_sum_supply_from_ST_contractor = pd.DataFrame.from_dict(
    data=results_sum_supply_from_ST_contractor
).T

# results_supply_from_HP_self_financed = dict.fromkeys(model.set_HP2)
# for key in results_supply_from_HP_self_financed.keys():
#     results_supply_from_HP_self_financed[key] = data_template.copy()
#     # results_supply_from_HP_self_financed[key]["Region"] = key
#     results_supply_from_HP_self_financed[key][
#         "Variable"
#     ] = "Supply from HP|Self financed|" + str(key)

# for option in results_supply_from_HP_self_financed.keys():
#     for time in model.set_time:
#         d = {time: round(model.supply_from_HP[time, "Self financed", option].value)}
#         results_supply_from_HP_self_financed[option].update(d)
# df_results_supply_from_HP_self_financed = pd.DataFrame.from_dict(
#     data=results_supply_from_HP_self_financed
# ).T

# results_sum_supply_from_HP_self_financed = dict.fromkeys(model.set_HP2)
# for key in results_sum_supply_from_HP_self_financed.keys():
#     results_sum_supply_from_HP_self_financed[key] = data_template.copy()
#     # results_supply_from_HP_contractor[key]["Region"] = 'Vienna'
#     results_sum_supply_from_HP_self_financed[key][
#         "Variable"
#     ] = "Sum supply from HP|Self financed|" + str(key)

# for option in results_sum_supply_from_HP_self_financed.keys():
#     d = {
#         0: round(
#             sum(
#                 model.supply_from_HP[time, "Self financed", option].value
#                 for time in model.set_time
#             )
#         )
#     }
#     results_sum_supply_from_HP_self_financed[option].update(d)
# df_results_sum_supply_from_HP_self_financed = pd.DataFrame.from_dict(
#     data=results_sum_supply_from_HP_self_financed
# ).T


# results_supply_from_HP_contractor = dict.fromkeys(model.set_HP2)
# for key in results_supply_from_HP_contractor.keys():
#     results_supply_from_HP_contractor[key] = data_template.copy()
#     # results_supply_from_HP_contractor[key]["Region"] = 'Vienna'
#     results_supply_from_HP_contractor[key][
#         "Variable"
#     ] = "Supply from HP|Contractor|" + str(key)

# for option in results_supply_from_HP_contractor.keys():
#     for time in model.set_time:
#         d = {time: round(model.supply_from_HP[time, "Contractor", option].value)}
#         results_supply_from_HP_contractor[option].update(d)
# df_results_supply_from_HP_contractor = pd.DataFrame.from_dict(
#     data=results_supply_from_HP_contractor
# ).T

# results_sum_supply_from_HP_contractor = dict.fromkeys(model.set_HP2)
# for key in results_sum_supply_from_HP_contractor.keys():
#     results_sum_supply_from_HP_contractor[key] = data_template.copy()
#     # results_supply_from_HP_contractor[key]["Region"] = 'Vienna'
#     results_sum_supply_from_HP_contractor[key][
#         "Variable"
#     ] = "Sum supply from HP|Contractor|" + str(key)

# for option in results_sum_supply_from_HP_contractor.keys():
#     d = {
#         0: round(
#             sum(
#                 model.supply_from_HP[time, "Contractor", option].value
#                 for time in model.set_time
#             )
#         )
#     }
#     results_sum_supply_from_HP_contractor[option].update(d)
# df_results_sum_supply_from_HP_contractor = pd.DataFrame.from_dict(
#     data=results_sum_supply_from_HP_contractor
# ).T


results_supply_from_grid = dict.fromkeys(model.set_elec_grid2)
for key in results_supply_from_grid.keys():
    results_supply_from_grid[key] = data_template.copy()
    # results_supply_from_PV_self_financed[key]["Region"] = key
    results_supply_from_grid[key]["Variable"] = "Supply from Grid|" + str(key)

for option in results_supply_from_grid.keys():
    for time in model.set_time:
        d = {time: round(model.supply_from_elec_grid[time, option].value)}
        results_supply_from_grid[option].update(d)
df_results_supply_from_grid = pd.DataFrame.from_dict(data=results_supply_from_grid).T

results_sum_supply_from_grid = dict.fromkeys(model.set_elec_grid2)
for key in results_sum_supply_from_grid.keys():
    results_sum_supply_from_grid[key] = data_template.copy()
    # results_supply_from_PV_self_financed[key]["Region"] = key
    results_sum_supply_from_grid[key]["Variable"] = "Sum supply from Grid|" + str(key)

for option in results_sum_supply_from_grid.keys():
    for time in model.set_time:
        d = {
            0: round(
                sum(
                    model.supply_from_elec_grid[time, option].value
                    for time in model.set_time
                )
            )
        }
        results_sum_supply_from_grid[option].update(d)
df_results_sum_supply_from_grid = pd.DataFrame.from_dict(
    data=results_sum_supply_from_grid
).T


results_binary_variables_new_self_financed = dict.fromkeys(model.set_new_technologies)
for key in results_binary_variables_new_self_financed.keys():
    results_binary_variables_new_self_financed[key] = data_template.copy()
    results_binary_variables_new_self_financed[key][
        "Variable"
    ] = "Binary_New_Technology|Self financed|" + str(key)

for option in results_binary_variables_new_self_financed.keys():
    for time in model.set_time:
        d = {0: round(model.binary_new_technologies["Self financed", option].value)}
        results_binary_variables_new_self_financed[option].update(d)
df_results_binary_variables_new_self_financed = pd.DataFrame.from_dict(
    data=results_binary_variables_new_self_financed
).T

results_binary_variables_new_contractor = dict.fromkeys(model.set_new_technologies)
for key in results_binary_variables_new_contractor.keys():
    results_binary_variables_new_contractor[key] = data_template.copy()
    results_binary_variables_new_contractor[key][
        "Variable"
    ] = "Binary_New_Technology|Contractor|" + str(key)

for option in results_binary_variables_new_contractor.keys():
    for time in model.set_time:
        d = {0: model.binary_new_technologies["Contractor", option].value}
        results_binary_variables_new_contractor[option].update(d)
df_results_binary_variables_new_contractor = pd.DataFrame.from_dict(
    data=results_binary_variables_new_contractor
).T

results_sum_supply_to_car = dict.fromkeys(model.set_2car)
for key in results_sum_supply_to_car.keys():
    results_sum_supply_to_car[key] = data_template.copy()
    # results_capacity_new_contractor[key]["Region"] = 'Vienna'
    results_sum_supply_to_car[key]["Variable"] = "Sum supply to Car|" + str(key)


for option in results_sum_supply_to_car.keys():
    d = {
        0: round(
            sum(model.supply_to_car[time, option].value for time in model.set_time)
        )
    }
    results_sum_supply_to_car[option].update(d)
df_results_sum_supply_to_car = pd.DataFrame.from_dict(data=results_sum_supply_to_car).T


df_all_results = pd.concat(
    [
        df_results_cost,
        df_results_demand,
        df_results_capacity_default,
        df_results_supply_default,
        df_results_sum_supply_default,
        df_results_supply_contractor,
        df_results_supply_self_financed,
        df_results_sum_supply_contractor,
        df_results_sum_supply_self_financed,
        df_results_capacity_new_contractor,
        df_results_capacity_new_self_financed,
        df_results_supply_from_PV_self_financed,
        df_results_sum_supply_from_PV_self_financed,
        df_results_supply_from_PV_contractor,
        df_results_sum_supply_from_PV_contractor,
        df_results_supply_from_ST_self_financed,
        df_results_sum_supply_from_ST_self_financed,
        df_results_supply_from_ST_contractor,
        df_results_sum_supply_from_ST_contractor,
        # df_results_supply_from_HP_self_financed,
        # df_results_sum_supply_from_HP_self_financed,
        # df_results_supply_from_HP_contractor,
        # df_results_sum_supply_from_HP_contractor,
        df_results_supply_from_grid,
        df_results_sum_supply_from_grid,
        df_results_binary_variables_new_self_financed,
        df_results_binary_variables_new_contractor,
        df_results_sum_supply_to_car,
    ]
)

pd.concat([df_all_results]).to_csv(str(output_file_path), index=False)  # ,mode='a')

# df = py.IamDataFrame(output_file_path)
# df = py.IamDataFrame(df_all_results)
# # print(df)

# model, scenario = "Contracting_model", "Trial"
###### created aggreated plot
# data = df.filter(model=model, scenario=scenario,variable='Supply|*')

# # df.aggregate_region("Supply*")
# data.plot.stack(stack="region")

### creates bar plot

### creates pie plot


# data_capacity_contractor = df.filter(variable="Capacity|Contractor|*")
# print("data_capacity_contractor: ", data_capacity_contractor)
# data_capacity_contractor.plot.bar(title="Installed Capacities by Contractor")
# plt.legend(loc=1)
# plt.tight_layout()
# plt.xlabel("Installed technologies")

# data_capacity_self_financed = df.filter(variable="Capacity|Self financed|*")
# print("data_capacity_self_financed: ", data_capacity_self_financed)
# data_capacity_self_financed.plot.bar(title="Installed Capacities Self financed")
# plt.legend(loc=1)
# plt.tight_layout()
# plt.xlabel("Installed technologies")


# data_supply_contractor = df.filter(
#     model=model, scenario=scenario, variable="Supply|Contractor|*"
# )
# data_supply_contractor.plot(
#     # ax=ax,
#     legend=True,
#     color="variable",
#     title="Supply by various technologies by Contractor",
#     linewidth=2.5,
# )
# plt.xlabel("time [h]")

# data_supply_self_financed = df.filter(
#     model=model, scenario=scenario, variable="Supply|Self financed|*"
# )
# data_supply_self_financed.plot(
#     # ax=ax,
#     legend=True,
#     color="variable",
#     title="Supply by various technologies Self financed",
#     linewidth=2.5,
# )
# plt.xlabel("time [h]")

# data_supply_from_PV_contractor = df.filter(
#     model=model, scenario=scenario, variable="Supply from PV|Contractor|*"
# )
# data_supply_from_PV_contractor.plot(
#     # ax=ax,
#     legend=True,
#     color="variable",
#     title="Supply from PV Contractor",
#     linewidth=2.5,
# )
# plt.xlabel("time [h]")


# data_supply_from_PV_self_financed = df.filter(
#     model=model, scenario=scenario, variable="Supply from PV|Self financed|*"
# )
# data_supply_from_PV_self_financed.plot(
#     # ax=ax,
#     legend=True,
#     color="variable",
#     title="Supply from PV Self financed",
#     linewidth=2.5,
# )
# plt.xlabel("time [h]")
# a = ax.get_lines()
# # a[2].set_color(color)
# a[3].set_linestyle('dotted')
# a[5].set_linestyle('dashed')

# fig, ax = plt.subplots()
# data_demand = df.filter(model=model, scenario=scenario, variable="Demand|*")
# data_demand.plot(ax=ax, legend=True, color="variable", title="Demand", linewidth=2.5)
# plt.xlabel("time [h]")
# a = ax.get_lines()
# a[2].set_color(color)
# a[3].set_linestyle("dotted")
# a[4].set_linestyle("dashed")


# data_binary_new = df.filter(variable="Binary_New_Technology|Contractor|*")
# data_binary_new.plot.bar(title="Installed Capacities by Contractor Binary Variable")
# plt.legend(loc=1)
# plt.tight_layout()
# plt.xlabel("Installed technologies")

# data_binary_new = df.filter(variable="Binary_New_Technology|Self financed|*")
# data_binary_new.plot.bar(title="Installed Capacities self financed Binary Variable")
# plt.legend(loc=1)
# plt.tight_layout()
# plt.xlabel("Installed technologies")


# values_supply_to_car = df.filter(variable="Supply default|*").data["value"]
# values_supply_to_car.aggregate("sum", components="value")
# print(values_supply_to_car)
# print(py.cumulative(values_supply_to_car["DH"], 0, 742))


# print(values_supply_to_car)
# values_supply_to_car.sum(axis=0)
