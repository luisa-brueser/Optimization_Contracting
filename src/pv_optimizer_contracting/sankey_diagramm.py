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
output_file_path = Path(__file__).parent / "data_output_one_year_30_household_30_cars_25kWh_scenario3_6_month.csv"


df = py.IamDataFrame(output_file_path)

sankey_mapping = {
    "Sum supply from Grid|Household": ("Electricity grid", "ELectricity demand household"),
    "Sum supply from Grid|HP": ("Electricity grid", "HP Contractor"),
    "Sum supply from Grid|Car": ("Electricity grid", "Car"),
    "Sum supply from Grid|Battery": ("Electricity grid", "Battery Contractor"),
    "Sum supply from PV|Self financed|Car": ("PV Self financed", "Car"),
    "Sum supply from PV|Self financed|Electric Grid": ("PV Self financed","Electricity grid feedin"),
    "Sum supply from PV|Self financed|Battery": ("PV Self financed", "Battery Contractor"),
    "Sum supply from PV|Self financed|Household": ("PV Self financed","ELectricity demand household"),
    "Sum supply from PV|Self financed|HP": ("PV Self financed", "HP Self financed"),
    "Sum supply from PV|Contractor|Car": ("PV Contractor", "Car"),
    "Sum supply from PV|Contractor|Electric Grid": ("PV Contractor","Electricity grid feedin"),
    "Sum supply from PV|Contractor|Battery": ("PV Contractor", "Battery Contractor"),
    "Sum supply from PV|Contractor|Household": ("PV Contractor","ELectricity demand household"),
    "Sum supply from PV|Contractor|HP": ("PV Contractor", "HP Contractor"),
    "Sum supply from ST|Contractor|DH": ("ST Contractor", "DH grid feedin"),
    "Sum supply from ST|Contractor|Household": ("ST Contractor","Thermal demand household"),
    "Sum supply from ST|Self financed|DH": ("ST Self financed", "DH grid feedin"),
    "Sum supply from ST|Self financed|Household": ("ST Self financed","Thermal demand household"),
    "Sum supply new|Contractor|HP": ("HP Contractor","Thermal demand household"),
    "Sum supply new|Self financed|HP": ("HP Self financed","Thermal demand household"),
    "Sum supply new|Contractor|Battery": ("Battery Contractor","Car"),
    "Sum supply new|Self financed|Battery": ("Battery","Car"),
    "Sum supply default|Contractor|DH": ("DH grid","Thermal demand household"),
    "Sum supply default|Contractor|Gas": ("Gas grid","Thermal demand household"),
    "Sum supply default|Self financed|DH": ("DH grid","Thermal demand household"),
    "Sum supply default|Self financed|Gas": ("Gas grid","Thermal demand household"),


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

fig = df.filter(year=0).plot.sankey(mapping=sankey_mapping)
# calling `show()` is necessary to have the thumbnail in the gallery overview
plotly.io.show(fig)
