import pandas as pd
from pathlib import Path
import numpy as np
import pyam
from pyam.plotting import OUTSIDE_LEGEND
import matplotlib.pyplot as plt
from pv_optimizer_contracting.new_model import model
from pprint import pprint 

output_file_path = Path(__file__).parent / 'data_output.csv'

data_capacity_contractor = [
    model.capacity["Contractor", "PV"].value,
    model.capacity["Contractor", "ST"].value,
    model.capacity["Contractor", "HP"].value,
    model.capacity["Contractor", "Charging Station"].value
]
data_capacity_self_financed  = [
    model.capacity["Self financed", "PV"].value,
    model.capacity["Self financed", "ST"].value,
    model.capacity["Self financed", "HP"].value,
    model.capacity["Self financed", "Charging Station"].value,
]
labels = ["PV", "ST", "HP", "Charging Stations"]
x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars
fig2, ax2 = plt.subplots()
rects1 = ax2.bar(x - width / 2, data_capacity_contractor , width, label="Capacity Contractor")
rects2 = ax2.bar(
    x + width / 2, data_capacity_self_financed , width, label="Capacity Self financed"
)

# Add some text for labels, title and custom x-axis tick labels, etc.
ax2.set_ylabel("kW/m²/psc")
ax2.set_title("New Technology investments")
ax2.set_xticks(x)
ax2.set_xticklabels(labels)
ax2.legend()

ax2.bar_label(rects1, padding=3)
ax2.bar_label(rects2, padding=3)

fig2.tight_layout()




results_demand = dict.fromkeys(model.set_demand)



data_template = {
    "Model": "Contracting_model",
    "Scenario": "Contracting_1",
    "Region": None,
    "Variable": None,
    "Unit": "kW",
}




for key in results_demand.keys():
    results_demand[key] = data_template.copy()
    results_demand[key]["Region"] = key
    results_demand[key]["Variable"] = "Demand"


for option in results_demand.keys():
    for time in model.set_time:
        d = {time: model.demand[time,option]}
        results_demand[option].update(d)


# new = {**data_template, **results_demand}

df = pd.DataFrame.from_dict(data=results_demand).T
pprint(df)
pd.concat([df]).to_csv(str(output_file_path),index=False)


df = pyam.IamDataFrame(output_file_path)


model, scenario = 'Contracting_model', 'Contracting_1'

data = df.filter(model=model, scenario=scenario)
# # data_demand = df_demand.filter(model=model, scenario=scenario)

# # data = (
# #     df.filter(model=model, scenario=scenario, variable='Supply_PV')
# #     .filter(region='Vienna')
# # )

fig, ax = plt.subplots()
df.plot(ax=ax, legend=True, color='region',title='Supply by grid, PV and HP',linewidth=2.5)
a = ax.get_lines()




plt.show()


