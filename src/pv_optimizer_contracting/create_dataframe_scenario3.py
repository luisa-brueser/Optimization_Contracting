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
from model import model
from pprint import pprint

# output_file_path = Path(__file__).parent / "data_output_trial.csv"


output_file_path = Path(__file__).parent / "data_output_one_year_30_household_30_cars_25kWh_scenario3_new.csv"



data_template = {
    "Model": "Contracting_model",
    "Scenario": "Scenario 3",
    "Region": "Vienna City Border",
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
d = {0: - round(model.revenue_total.value)}
results_cost["Revenue"].update(d)

results_cost["Total"] = None
results_cost["Total"] = data_template.copy()
results_cost["Total"]["Variable"] = "Cost|" + "Total"
d = {0: round(model.obj())}
results_cost["Total"].update(d)

df_results_cost = pd.DataFrame.from_dict(data=results_cost).T

results_cost_contractor = dict() 

results_cost_contractor["Investment"] = None
results_cost_contractor["Investment"] = data_template.copy()
results_cost_contractor["Investment"]["Variable"] = "Cost Contractor|" + "Investment"
d = {0: round(model.investment_costs_total_contractor.value)}
results_cost_contractor["Investment"].update(d)

results_cost_contractor["Service"] = None
results_cost_contractor["Service"] = data_template.copy()
results_cost_contractor["Service"]["Variable"] = "Cost Contractor|" + "Service"
d = {0: round(model.service_costs_total_contractor.value)}
results_cost_contractor["Service"].update(d)

results_cost_contractor["Connection"] = None
results_cost_contractor["Connection"] = data_template.copy()
results_cost_contractor["Connection"]["Variable"] = "Cost Contractor|" + "Connection"
d = {0: round(model.connection_costs_total_contractor.value)}
results_cost_contractor["Connection"].update(d)

results_cost_contractor["Variable"] = None
results_cost_contractor["Variable"] = data_template.copy()
results_cost_contractor["Variable"]["Variable"] = "Cost Contractor|" + "Variable"
d = {0: round(model.variable_cost_total_contractor.value)}
results_cost_contractor["Variable"].update(d)

results_cost_contractor["Revenue"] = None
results_cost_contractor["Revenue"] = data_template.copy()
results_cost_contractor["Revenue"]["Variable"] = "Revenue Contractor"
d = {0: - round(model.revenue_total_contractor.value)}
results_cost_contractor["Revenue"].update(d)

results_cost_contractor["Total"] = None
results_cost_contractor["Total"] = data_template.copy()
results_cost_contractor["Total"]["Variable"] = "Cost Contractor|" + "Total"
d = {0: round(model.total_costs_contractor.value)}
results_cost_contractor["Total"].update(d)

df_results_cost_contractor = pd.DataFrame.from_dict(data=results_cost_contractor).T



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

# reduction_heating_demand = dict() 

# reduction_heating_demand["Contractor"] = None
# reduction_heating_demand["Contractor"] = data_template.copy()
# reduction_heating_demand["Contractor"]["Variable"] = "Reduction Heating Demand|Contractor"
# d = {0: round(sum(model.demand[time, "Heating"] for time in model.set_time)*(
#             0.1 * model.binary_insulation['Contractor', "Insulation 10%"].value
#         + 0.3 * model.binary_insulation['Contractor', "Insulation 30%"].value
#         + 0.85 * model.binary_insulation['Contractor', "Insulation 85%"].value)/sum(model.demand[time, "Heating"] for time in model.set_time)*100)}

# reduction_heating_demand["Contractor"].update(d)

# reduction_heating_demand["Self financed"] = None
# reduction_heating_demand["Self financed"] = data_template.copy()
# reduction_heating_demand["Self financed"]["Variable"] = "Reduction Heating Demand|Self financed"
# d = {0: round(sum(model.demand[time, "Heating"] for time in model.set_time)*(
#             0.1 * model.binary_insulation['Self financed', "Insulation 10%"].value
#         + 0.3 * model.binary_insulation['Self financed', "Insulation 30%"].value
#         + 0.85 * model.binary_insulation['Self financed', "Insulation 85%"].value)/sum(model.demand[time, "Heating"] for time in model.set_time)*100)}

# reduction_heating_demand["Self financed"].update(d)


# df_reduction_heating_demand= pd.DataFrame.from_dict(data=reduction_heating_demand).T
# print('df_reduction_heating_demand: ', df_reduction_heating_demand)

results_capacity_default = dict.fromkeys(model.set_default_technologies)
for key in results_capacity_default.keys():
    results_capacity_default[key] = data_template.copy()
    # results_capacity_new_contractor[key]["Region"] = 'Vienna'
    results_capacity_default[key]["Variable"] = "Connection Capacity|" + str(key)

for option in results_capacity_default.keys():
    d = {
        0: round(
            model.connection_capacity_default[option]
            * (model.binary_default_technologies['Contractor',option].value + model.binary_default_technologies['Self financed',option].value)
        )
    }
    results_capacity_default[option].update(d)

df_results_capacity_default = pd.DataFrame.from_dict(data=results_capacity_default).T

results_supply_default_contractor = dict.fromkeys(model.set_default_technologies)
for key in results_supply_default_contractor.keys():
    results_supply_default_contractor[key] = data_template.copy()
    # results_capacity_new_contractor[key]["Region"] = 'Vienna'
    results_supply_default_contractor[key]["Variable"] = "Supply default|Contractor|" + str(key)

for option in results_supply_default_contractor.keys():
    for time in model.set_time:
        d = {time: (model.supply_default[time,'Contractor', option].value)}
        results_supply_default_contractor[option].update(d)
df_results_supply_default_contractor = pd.DataFrame.from_dict(data=results_supply_default_contractor).T

results_supply_default_self = dict.fromkeys(model.set_default_technologies)
for key in results_supply_default_self.keys():
    results_supply_default_self[key] = data_template.copy()
    # results_capacity_new_contractor[key]["Region"] = 'Vienna'
    results_supply_default_self[key]["Variable"] = "Supply default|Self financed|" + str(key)

for option in results_supply_default_self.keys():
    for time in model.set_time:
        d = {time: (model.supply_default[time,'Self financed', option].value)}
        results_supply_default_self[option].update(d)
df_results_supply_default_self = pd.DataFrame.from_dict(data=results_supply_default_self).T





results_sum_supply_default_contractor = dict.fromkeys(model.set_default_technologies)
for key in results_sum_supply_default_contractor.keys():
    results_sum_supply_default_contractor[key] = data_template.copy()
    # results_capacity_new_contractor[key]["Region"] = 'Vienna'
    results_sum_supply_default_contractor[key]["Variable"] = "Sum supply default|Contractor|" + str(key)

for option in results_sum_supply_default_contractor.keys():
    d = {
        0: round(
            sum(model.supply_default[time,'Contractor', option].value for time in model.set_time)
        )
    }
    results_sum_supply_default_contractor[option].update(d)
df_results_sum_supply_default_contractor = pd.DataFrame.from_dict(
    data=results_sum_supply_default_contractor
).T


results_sum_supply_default_self = dict.fromkeys(model.set_default_technologies)
for key in results_sum_supply_default_self.keys():
    results_sum_supply_default_self[key] = data_template.copy()
    # results_capacity_new_contractor[key]["Region"] = 'Vienna'
    results_sum_supply_default_self[key]["Variable"] = "Sum supply default|Self financed|" + str(key)

for option in results_sum_supply_default_self.keys():
    d = {
        0: round(
            sum(model.supply_default[time,'Self financed', option].value for time in model.set_time)
        )
    }
    results_sum_supply_default_self[option].update(d)
df_results_sum_supply_default_self= pd.DataFrame.from_dict(
    data=results_sum_supply_default_self
).T

results_contractor_npv = dict.fromkeys(model.set_new_technologies)
for key in results_contractor_npv.keys():
    results_contractor_npv[key] = data_template.copy()
    # results_capacity_new_contractor[key]["Region"] = 'Vienna'
    results_contractor_npv[key]["Variable"] = "NPV Contractor|" + str(key)

for option in results_contractor_npv.keys():
    d = {0: model.npv[option].value}
    results_contractor_npv[option].update(d)


results_contractor_npv["Insulation"] = None
results_contractor_npv["Insulation"] = data_template.copy()
results_contractor_npv["Insulation"]["Variable"] = "NPV Contractor|" + "Insulation"


d = {0: model.npv_insulation.value}
results_contractor_npv["Insulation"].update(d)

df_results_contractor_npv = pd.DataFrame.from_dict(data=results_contractor_npv).T


results_annual_costs_contractor= dict.fromkeys(model.set_new_technologies)
for key in results_annual_costs_contractor.keys():
    results_annual_costs_contractor[key] = data_template.copy()
    # results_capacity_new_contractor[key]["Region"] = 'Vienna'
    results_annual_costs_contractor[key]["Variable"] = "Costs Contractor|" + str(key)

for option in results_annual_costs_contractor.keys():
    d = {0: model.annual_costs_contractor[option].value}
    results_annual_costs_contractor[option].update(d)

results_annual_costs_contractor["Insulation"] = None
results_annual_costs_contractor["Insulation"] = data_template.copy()
results_annual_costs_contractor["Insulation"]["Variable"] = "Costs Contractor|" + "Insulation"


d = {0: model.annual_costs_contractor_insulation.value}
results_annual_costs_contractor["Insulation"].update(d)

df_results_annual_costs_contractor = pd.DataFrame.from_dict(data=results_annual_costs_contractor).T

results_revenue_contractor= dict.fromkeys(model.set_new_technologies)
for key in results_revenue_contractor.keys():
    results_revenue_contractor[key] = data_template.copy()
    # results_capacity_new_contractor[key]["Region"] = 'Vienna'
    results_revenue_contractor[key]["Variable"] = "Revenue Contractor|" + str(key)

for option in results_revenue_contractor.keys():
    d = {0: model.revenue_contractor[option].value}
    results_revenue_contractor[option].update(d)

results_revenue_contractor["Insulation"] = None
results_revenue_contractor["Insulation"] = data_template.copy()
results_revenue_contractor["Insulation"]["Variable"] = "Revenue Contractor|" + "Insulation"


d = {0: model.revenue_contractor_insulation.value}
results_revenue_contractor["Insulation"].update(d)

df_results_revenue_contractor = pd.DataFrame.from_dict(data=results_revenue_contractor).T

results_contractor_rate= dict.fromkeys(model.set_new_technologies)
for key in results_contractor_rate.keys():
    results_contractor_rate[key] = data_template.copy()
    # results_capacity_new_contractor[key]["Region"] = 'Vienna'
    results_contractor_rate[key]["Variable"] = "Contractor Rate|" + str(key)

for option in results_contractor_rate.keys():
    d = {0: model.contractorrate[option].value}
    results_contractor_rate[option].update(d)

results_contractor_rate["Insulation"] = None
results_contractor_rate["Insulation"] = data_template.copy()
results_contractor_rate["Insulation"]["Variable"] = "Contractor Rate|" + "Insulation"


d = {0: model.contractorrate_insulation.value}
results_contractor_rate["Insulation"].update(d)

df_results_contractor_rate = pd.DataFrame.from_dict(data=results_contractor_rate).T

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


# results_supply_from_HP_contractor = dict()
# results_supply_from_HP_contractor["Household"] = None 
# results_supply_from_HP_contractor["Household"]= data_template.copy()
# results_supply_from_HP_contractor["Household"]["Variable"] = "Supply from HP|Contractor|" 


# for time in model.set_time:
#     d = {time: round(model.supply_from_HP[time, "Contractor", "Household"].value)}
#     results_supply_from_HP_contractor["Household"].update(d)
# df_results_supply_from_HP_contractor= pd.DataFrame.from_dict(
#     data=results_supply_from_HP_contractor
# ).T

# print('df_results_supply_from_HP_contractor: ', df_results_supply_from_HP_contractor)

# results_supply_from_HP_self_financed = dict.fromkeys(model.set_HP2)
# for key in results_supply_from_HP_self_financed.keys():
#     results_supply_from_HP_self_financed[key] = data_template.copy()
#     # results_supply_from_ST_contractor[key]["Region"] = 'Vienna'
#     results_supply_from_HP_self_financed[key][
#         "Variable"
#     ] = "Supply from HP|Self financed|" + str(key)


# for time in model.set_time:
#     d = {time: round(model.supply_from_HP[time, "Self financed", "Household"].value)}
#     results_supply_from_HP_self_financed.update(d)
# df_results_supply_from_HP_self_financed= pd.DataFrame.from_dict(
#     data=results_supply_from_HP_self_financed
# ).T




# results_sum_supply_from_HP_self_financed = dict.fromkeys(model.set_HP2)
# for key in results_sum_supply_from_HP_self_financed.keys():
#     results_sum_supply_from_HP_self_financed[key] = data_template.copy()
#     # results_supply_from_HP_contractor[key]["Region"] = 'Vienna'
#     results_sum_supply_from_HP_self_financed[key][
#         "Variable"
#     ] = "Sum supply from HP|Self financed|" + str(key)


# d = {
#     0: round(
#         sum(
#             model.supply_from_HP[time, "Self financed", 'Household'].value
#             for time in model.set_time
#         )
#     )
# }
# results_sum_supply_from_HP_self_financed.update(d)
# df_results_sum_supply_from_HP_self_financed = pd.DataFrame.from_dict(
#     data=results_sum_supply_from_HP_self_financed
# ).T


# results_sum_supply_from_HP_contractor = dict.fromkeys(model.set_HP2)
# for key in results_sum_supply_from_HP_contractor.keys():
#     results_sum_supply_from_HP_contractor[key] = data_template.copy()
#     # results_supply_from_HP_contractor[key]["Region"] = 'Vienna'
#     results_sum_supply_from_HP_contractor[key][
#         "Variable"
#     ] = "Sum supply from HP|Contractor|" + str(key)

# d = {
#     0: round(
#         sum(
#             model.supply_from_HP[time, "Contractor", 'Household'].value
#             for time in model.set_time
#         )
#     )
# }
# results_sum_supply_from_HP_contractor.update(d)
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

results_binary_insulation_self = dict.fromkeys(model.set_insulation_options)
for key in results_binary_insulation_self.keys():
    results_binary_insulation_self[key] = data_template.copy()
    results_binary_insulation_self[key][
        "Variable"
    ] = "Binary Insulation|Self financed|" + str(key)

for option in results_binary_insulation_self.keys():
    for time in model.set_time:
        d = {0: round(model.binary_insulation["Self financed", option].value)}
        results_binary_insulation_self[option].update(d)
df_results_binary_insulation_self = pd.DataFrame.from_dict( 
    data=results_binary_insulation_self
).T


results_binary_insulation_contractor = dict.fromkeys(model.set_insulation_options)
for key in results_binary_insulation_contractor.keys():
    results_binary_insulation_contractor[key] = data_template.copy()
    results_binary_insulation_contractor[key][
        "Variable"
    ] = "Binary Insulation|Contractor|" + str(key)

for option in results_binary_insulation_contractor.keys():
    for time in model.set_time:
        d = {0: round(model.binary_insulation["Contractor", option].value)}
        results_binary_insulation_contractor[option].update(d)
df_results_binary_insulation_contractor = pd.DataFrame.from_dict( 
    data=results_binary_insulation_contractor
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
        df_results_cost_contractor,
        df_results_demand,
        df_results_capacity_default,
        df_results_supply_default_self,
        df_results_supply_default_contractor,
        df_results_sum_supply_default_contractor,
        df_results_sum_supply_default_self,
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
        df_results_contractor_npv,
        df_results_annual_costs_contractor,
        df_results_revenue_contractor,   
        df_results_contractor_rate,
        df_results_binary_insulation_self, 
        df_results_binary_insulation_contractor,
        # df_reduction_heating_demand,
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
