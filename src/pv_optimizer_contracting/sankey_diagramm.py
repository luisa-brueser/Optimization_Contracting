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
# output_file_path = Path(__file__).parent / "data_output_trial.csv"


df = py.IamDataFrame(output_file_path)

sankey_mapping = {
    "Supply from Grid|Household": ("Electricity grid", "ELectricity demand household"),
    "Supply from Grid|HP": ("Electricity grid", "HP"),
    "Supply from Grid|Car": ("Electricity grid", "ELectricity demand car charging"),
    "Supply from Grid|Battery": ("Electricity grid", "Battery"),
    "Supply from PV|Self financed|Car": ("PV Self financed", "Car"),
    "Supply from PV|Self financed|Electric Grid": ("PV Self financed","Electricity grid feedin"),
    "Supply from PV|Self financed|Battery": ("PV Self financed", "Battery"),
    "Supply from PV|Self financed|Household": ("PV Self financed","ELectricity demand household"),
    "Supply from PV|Self financed|HP": ("PV Self financed", "HP"),
    "Supply from PV|Contractor|Car": ("PV Contractor", "Car"),
    "Supply from PV|Contractor|Electric Grid": ("PV Contractor","Electricity grid feedin"),
    "Supply from PV|Contractor|Battery": ("PV Contractor", "Battery"),
    "Supply from PV|Contractor|Household": ("PV Contractor","ELectricity demand household"),
    "Supply from PV|Contractor|HP": ("PV Contractor", "HP"),
    "Supply from ST|Contractor|DH": ("ST Contractor", "DH grid feedin"),
    "Supply from ST|Contractor|Household": ("ST Contractor","Thermal demand household"),
    "Supply from ST|Self financed|DH": ("ST Self financed", "DH grid feedin"),
    "Supply from ST|Self financed|Household": ("ST Self financed","Thermal demand household"),
    "Supply|Contractor|HP": ("HP","Thermal demand household"),
    "Supply|Self financed|HP": ("HP","Thermal demand household"),
    "Supply|Contractor|Battery": ("Battery","Thermal demand household"),
    "Supply|Self financed|Battery": ("Battery","Thermal demand household"),


    # "Primary Energy|Gas": ("Natural Gas Extraction", "Gas Network & Power Generation"),
    # "Secondary Energy|Electricity|Non-Biomass Renewables": (
    #     "Non-Biomass Renewables",
    #     "Electricity Grid",
    # ),
    # "Secondary Energy|Electricity|Nuclear": ("Nuclear", "Electricity Grid"),
    # "Secondary Energy|Electricity|Coal": (
    #     "Coal Trade & Power Generation",
    #     "Electricity Grid",
    # ),
    # "Secondary Energy|Electricity|Gas": (
    #     "Gas Network & Power Generation",
    #     "Electricity Grid",
    # ),
    # "Final Energy|Electricity": ("Electricity Grid", "Electricity Demand"),
    # "Final Energy|Solids|Coal": (
    #     "Coal Trade & Power Generation",
    #     "Non-Electricity Coal Demand",
    # ),
    # "Final Energy|Gases": ("Gas Network & Power Generation", "Gas Demand"),
}

fig = df.filter(year=31).plot.sankey(mapping=sankey_mapping)
# calling `show()` is necessary to have the thumbnail in the gallery overview
plotly.io.show(fig)
