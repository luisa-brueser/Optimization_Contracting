from datetime import datetime
from os import supports_follow_symlinks
from pprint import pprint

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from pyomo.environ import *
from pyomo.gdp import Disjunct, Disjunction

# from disjunction import *
from input_new_model import *

model = ConcreteModel()

# Loading all variables from input data
(
    set_time,
    set_day,
    set_finance_options,
    set_technologies,
    set_default_technologies,
    set_costs,
    set_costs_default,
    set_demand,
    set_PV2,
    set_ST2,
    set_elec_grid2,
    set_Car2,
    set_2Car,
    set_Battery2,
    set_2Battery,
    set_HP2,
    set_2HP,
) = read_set_data()
(dict_general_parameters) = read_general_data()
(annuity_factor) = calculate_annuity_factor()
(dict_cost_new, dict_cost_default) = read_cost_data()
(dict_demand) = read_demand_data()
(dict_max_demand, dict_max_demand_default) = read_max_demand()
(dict_irradiation, dict_temperature) = read_weather_data()
(dict_COP) = calculate_COP()
(dict_capacity_factor_PV, dict_temperature_factor_PV) = calculate_performance_PV()

# Sets
model.set_time = Set(initialize=set_time.keys(), doc="time in timesteps of 1h")
model.set_day = Set(initialize=set_day.keys(), doc="Day - 24h")
model.set_finance_options = Set(
    initialize=set_finance_options.keys(),
    doc="Elements of the model financed by self-investment OR by a contractor",
)
model.set_new_technologies = Set(
    initialize=set_technologies.keys(),
    doc="Technologies/Elements that can be financed e.g, PV, HP etc.",
)
model.set_default_technologies = Set(
    initialize=set_default_technologies.keys(),
    doc="Default elements that already exist e.g. electricity, gas, DH",
)
model.set_costs_new = Set(
    initialize=set_costs.keys(),
    doc="Types of costs for newly installed technologies e.g. investment,service,connection, fuel",
)
model.set_costs_default = Set(
    initialize=set_costs_default.keys(),
    doc="Types of costs for default technologies e.g. service,connection, fuel, feedin",
)
model.set_demand = Set(
    initialize=set_demand.keys(),
    doc="Demands that need to be fulfilled e.g. charging,electricity, hot water, heating",
)
model.set_PV2 = Set(
    initialize=set_PV2.keys(), doc="Elements that can be supplied by PV"
)
model.set_ST2 = Set(
    initialize=set_ST2.keys(), doc="Elements that can be supplied by ST"
)
model.set_elec_grid2 = Set(
    initialize=set_elec_grid2.keys(),
    doc="Elements that can be supplied by the electric grid",
)
model.set_car2 = Set(
    initialize=set_Car2.keys(),
    doc="Elements that can be supplied by the battery of electric vehicles",
)
model.set_2car = Set(
    initialize=set_2Car.keys(),
    doc="Elements that supply to the battery of electric vehicles",
)
model.set_Battery2 = Set(
    initialize=set_Battery2.keys(),
    doc="Elements that can be supplied by the stationary battery",
)
model.set_2Battery = Set(
    initialize=set_2Battery.keys(), doc="Elements that supply the stationary battery"
)
model.set_HP2 = Set(
    initialize=set_HP2.keys(), doc="Elements that can be supplied by HP"
)
model.set_2HP = Set(initialize=set_2HP.keys(), doc="Elements that supply to HP")

## Parameters
# General Parameters
model.annuity = Param(
    initialize=annuity_factor,
    mutable=False,
    doc="Annuity factor to convert investment costs in annual costs",
)
model.area_roof = Param(
    initialize=dict_general_parameters["Area Roof"],
    mutable=False,
    within=Any,
    doc="Area of the roof [m2], determines limit of PV and ST capacity",
)
model.capacity_density_PV = Param(
    initialize=dict_general_parameters["Area PV"],
    mutable=False,
    within=Any,
    doc="Capacity density of PV [kWp/m2]",
)
model.area_ST_per_person = Param(
    initialize=dict_general_parameters["Area ST per Person"],
    mutable=False,
    within=Any,
    doc="Demand of hot water per Person",
)
model.cop = Param(model.set_time, initialize=dict_COP, doc="Reduced COP per timestep")
model.powerflow_max_battery = Param(
    initialize=dict_general_parameters["Maximum Powerflow Battery"],
    mutable=False,
    within=Any,
    doc="Maximum powerflow into and out of stationary battery",
)
model.powerflow_max_battery_car = Param(
    initialize=dict_general_parameters["Maximum Powerflow Battery Car"],
    mutable=False,
    within=Any,
    doc="Maximum powerflow into and out of car battery",
)
model.capacity_car = Param(
    initialize=dict_general_parameters["Capacity Battery Car"],
    mutable=False,
    within=Any,
    doc="Capacity battery of chosen car model",
)
model.efficiency_battery = Param(
    initialize=dict_general_parameters["Efficiency Battery"],
    mutable=False,
    within=Any,
    doc="Efficiency of stationary battery",
)
model.efficiency_battery_car = Param(
    initialize=dict_general_parameters["Efficiency Battery Car"],
    mutable=False,
    within=Any,
    doc="Efficiency of car battery",
)
model.efficiency_gas = Param(
    initialize=dict_general_parameters["Efficiency Gas Boiler"],
    mutable=False,
    within=Any,
    doc="Efficiency of decentralized gas boilers",
)
model.number_cars = Param(
    initialize=dict_general_parameters["Number of Cars"],
    mutable=False,
    within=Any,
    doc="Number of charging stations (or cars) chosen",
)
model.number_households = Param(
    initialize=dict_general_parameters["Number of households"],
    mutable=False,
    within=Any,
    doc="Number of households",
)
model.simultaneity = Param(
    initialize=dict_general_parameters["Simultaneity factor"],
    mutable=False,
    within=Any,
    doc="Simultaneity factor for hot water usage",
)
model.cost_infrastructure_ST2DH = Param(
    initialize=dict_general_parameters["Investment ST to DH"],
    mutable=False,
    within=Any,
    doc="Additional investment if ST feed into DH",
)
model.bonus_shifting = Param(
    initialize=dict_general_parameters["Bonus shifting"],
    mutable=False,
    within=Any,
    doc="Price paid for shifting by contractor per kW",
)
model.efficiency_ST = Param(
    initialize=dict_general_parameters["Efficiency ST"],
    mutable=False,
    within=Any,
    doc="Efficiency ST module",
)
model.max_powerflow_charging_station = Param(
    initialize=dict_general_parameters["Max Powerflow Charging Station"],
    mutable=False,
    within=Any,
    doc="Maximum Powerflow over one charging station in kW",
)


# Cost Parameters
model.cost_new = Param(
    model.set_finance_options,
    model.set_new_technologies,
    model.set_costs_new,
    initialize=dict_cost_new,
    doc="Prices for initial investment",
)
model.cost_default = Param(
    model.set_default_technologies,
    model.set_costs_default,
    initialize=dict_cost_default,
    doc="Prices for initial investment",
)
model.weight = Param(
    initialize=float(8760) / (len(model.set_time)),
    doc="Pre-factor for variable costs for an annual result",
)

# Demand Parameters
model.demand = Param(
    model.set_time,
    model.set_demand,
    initialize=dict_demand,
    doc="Demand per timestep per demand type e.g. charging,electricity, hot water, heating",
)
model.connection_capacity_default = Param(
    model.set_default_technologies,
    initialize=dict_max_demand_default,
    doc="Max demand = Connection capacity per default technology",
)


# Weather Parameter
model.irradiation = Param(
    model.set_time,
    initialize=dict_irradiation,
    doc="Irradiation on flat surface per timestep",
)
model.temperature = Param(
    model.set_time, initialize=dict_temperature, doc="Outside temperature per timestep"
)

# PV Performance
model.capacity_factor_PV = Param(
    model.set_time,
    initialize=dict_capacity_factor_PV,
    doc="kW electricity produced from PV per kWp installes per timestep",
)
model.temperature_factor_PV = Param(
    model.set_time,
    initialize=dict_capacity_factor_PV,
    doc="kW electricity produced from PV per kWp installes per timestep",
)
model.max_capacity_PV = Param(
    initialize=(model.area_roof / model.capacity_density_PV),
    doc="Maximum PV capacity given by area of the roof",
)
model.min_capacity_PV_contractor = Param(
    initialize=dict_general_parameters["Min Capacity PV Contractor"],
    mutable=False,
    within=Any,
    doc="Minium capacity of PV that contractor wants to finance",
)
model.min_capacity_ST_contractor = Param(
    initialize=dict_general_parameters["Min Capacity ST Contractor"],
    mutable=False,
    within=Any,
    doc="Minium capacity of PV that contractor wants to finance",
)


# Vaiables
model.capacity = Var(
    model.set_finance_options,
    model.set_new_technologies,
    initialize=0,
    within=NonNegativeReals,
    doc="Newly installed capacity per financing option per technology",
)

# model.capacity['Contractor','HP'].fixed=True
# model.capacity['Contractor','HP'].value=50
model.supply_default = Var(
    model.set_time,
    model.set_default_technologies,
    within=NonNegativeReals,
    doc="Supply per timestep per default technology",
)
model.supply_new = Var(
    model.set_time,
    model.set_finance_options,
    model.set_new_technologies,
    within=NonNegativeReals,
    doc="Supply per timestepnew per financing option per technology",
)
model.supply_from_PV = Var(
    model.set_time,
    model.set_finance_options,
    model.set_PV2,
    within=NonNegativeReals,
    doc="Supply from PV per timestep per financing option",
)
model.supply_from_ST = Var(
    model.set_time,
    model.set_finance_options,
    model.set_ST2,
    initialize=0,
    within=NonNegativeReals,
    doc="Supply from ST per timestep per financing option",
)

model.supply_from_elec_grid = Var(
    model.set_time,
    model.set_elec_grid2,
    within=NonNegativeReals,
    doc="Supply from electric grid per timestep per financing option",
)
model.supply_from_car = Var(
    model.set_time,
    model.set_car2,
    within=NonNegativeReals,
    doc="Supply from Car Battery per timestep per financing option",
)
model.supply_to_car = Var(
    model.set_time,
    model.set_2car,
    within=NonNegativeReals,
    doc="Supply from Car Battery per timestep per financing option",
)
model.supply_from_battery = Var(
    model.set_time,
    model.set_finance_options,
    model.set_Battery2,
    within=NonNegativeReals,
    doc="Supply from stationary Battery per timestep per financing option",
)
model.supply_to_battery = Var(
    model.set_time,
    model.set_finance_options,
    model.set_2Battery,
    within=NonNegativeReals,
    doc="Supply to stationary Battery per timestep per financing option",
)
model.supply_from_HP = Var(
    model.set_time,
    model.set_finance_options,
    model.set_HP2,
    within=NonNegativeReals,
    doc="Supply from HP per timestep per financing option",
)
model.supply_to_HP = Var(
    model.set_time,
    model.set_finance_options,
    model.set_2HP,
    within=NonNegativeReals,
    doc="Supply to HP per timestep per financing option",
)
model.area_PV = Var(
    model.set_finance_options,
    within=NonNegativeReals,
    doc="Area of PV built per financing option",
)
model.demand_shift_total = Var(
    within=NonNegativeReals, doc="Total shift of demand in 1 year"
)
model.demand_shift_up = Var(
    model.set_time,
    bounds=(0, 5 * model.number_cars),
    within=NonNegativeReals,
    doc="Shift of charging demand up per timestep [kW]",
)
# model.demand_shift_up[12].fixed=True
# model.demand_shift_up[12].value=5

model.demand_shift_down = Var(
    model.set_time,
    bounds=(0, 5 * model.number_cars),
    within=NonNegativeReals,
    doc="Shift of charging demand up per timestep [kW]",
)
# model.demand_shift_down[12].fixed=True
# model.demand_shift_down[12].value=0
model.max_capacity_ST = Var(
    #model.set_finance_options,
    within=NonNegativeReals,
    doc="Max capacity of ST, differs if St can feed into DH or not",
)
model.reduction_heating_demand = Var(
    model.set_time,
    within=NonNegativeReals,
    doc="Reduction of heat demand after insulation",
)
model.reduced_heating_demand = Var(
    model.set_time, within=NonNegativeReals, doc="Reduced heat demand after insulation"
)
model.total_thermal_demand = Var(
    model.set_time,
    within=NonNegativeReals,
    doc="Total thermal demand from DHW and heating",
)
model.state_of_charge_battery = Var(
    model.set_time,
    model.set_finance_options,
    within=NonNegativeReals,
    doc="State of charge of stationary battery at every timestep",
)
model.state_of_charge_car = Var(
    model.set_time,
    bounds=(0, 1000),
    within=NonNegativeReals,
    doc="State of charge of car at every timestep",
)
model.number_charging_stations = Var(
    model.set_finance_options,
    within=NonNegativeReals,
    doc="Number of charging stations by financing option",
)
model.up_shifts_in_one_day = Var(
    model.set_day, within=NonNegativeReals, doc="Total shift of demand in 1 year"
)
model.down_shifts_in_one_day = Var(
    model.set_day, within=NonNegativeReals, doc="Total shift of demand in 1 year"
)
model.shifted_demand = Var(
    model.set_time, within=NonNegativeReals, doc="Shifted Demand"
)

# Binary Variables
model.binary_default_technologies = Var(
    model.set_default_technologies,
    initialize={"Electricity": 1, "DH": 1, "Gas": 0},
    within=Binary,
    doc="Binary Variable becomes TRUE if technology is installed",
)
model.binary_new_technologies = Var(
    model.set_finance_options,
    model.set_new_technologies,
    initialize=0,
    within=Binary,
    doc="Binary Variable becomes TRUE if technology is installed",
)

model.binary_ST = Var(
    initialize=0,
    within=Binary,
    doc="Binary Variable becomes TRUE if ST is installed",
)

# model.binary_default_technologies["Gas"].fix(1)
# model.binary_new_technologies['Self financed','ST'].fixed=True
# model.binary_new_technologies['Self financed','ST'].value=0
# model.binary_new_technologies['Contractor','ST'].fixed=True
# model.binary_new_technologies['Contractor','ST'].value=1


model.binary_ST_and_DH = Var(
    initialize=0,
    within=Binary,
    doc="Binary Variable becomes TRUE if ST AND DH are installed, ST can feed into DH",
)

model.binary_ST_to_DH  = Var(
    initialize=0,
    within=Binary,
    doc="Binary Variable becomes TRUE if ST feeds to DH",
)


model.binary_up_shift = Var(
    model.set_time,
    initialize=0,
    within=Binary,
    doc="Binary Variable becomes TRUE if up shift is done in this timestep",
)
model.binary_down_shift = Var(
    model.set_time,
    initialize=0,
    within=Binary,
    doc="Binary Variable becomes TRUE if down shift is done in this timestep",
)

# cost variables
model.investment_costs_total = Var()
model.service_costs_total = Var()
model.connection_costs_total = Var()
model.variable_cost_total = Var()
model.revenue = Var()
model.total_costs = Var()

# Objective
def total_cost_rule(model):
    return (
        model.investment_costs_total
        + model.service_costs_total
        + model.connection_costs_total
        + model.variable_cost_total
        - model.revenue
    )


model.obj = Objective(rule=total_cost_rule, sense=minimize, doc="minimize total costs")


def investment_costs_rule(model):
    return (
        model.investment_costs_total
        == sum(
            model.annuity
            * model.capacity[finance_options, technologies]
            * model.cost_new[finance_options, technologies, "Investment Price"]
            for finance_options in model.set_finance_options
            for technologies in model.set_new_technologies
        )
        + model.binary_ST_and_DH * model.cost_infrastructure_ST2DH
    )


model.ccost1 = Constraint(
    rule=investment_costs_rule, doc="Initital investment cost per installed capacity"
)


def service_costs_rule(model):
    return model.service_costs_total == sum(
        model.binary_default_technologies[default_technologies]
        * model.cost_default[default_technologies, "Service Cost"]
        for default_technologies in model.set_default_technologies
    ) + sum(
        model.binary_new_technologies[finance_options, new_technologies]
        * model.cost_new[finance_options, new_technologies, "Service Cost"]
        for finance_options in model.set_finance_options
        for new_technologies in model.set_new_technologies
    )


model.ccost2 = Constraint(
    rule=service_costs_rule,
    doc="Service and Maintenance Costs are annual lump-sum costs ",
)


def connection_costs_rule(model):
    return model.connection_costs_total == sum(
        model.binary_default_technologies[default_technologies]
        * model.connection_capacity_default[default_technologies]
        * model.cost_default[default_technologies, "Connection Price"]
        for default_technologies in model.set_default_technologies
    ) + sum(
        model.capacity[finance_options, technologies]
        * model.cost_new[finance_options, technologies, "Connection Price"]
        for finance_options in model.set_finance_options
        for technologies in model.set_new_technologies
    )


model.ccost3 = Constraint(
    rule=connection_costs_rule, doc="Annual connection costs per installed capacity"
)


def variable_cost_rule(model):
    return model.variable_cost_total == model.weight * (
        sum(
            model.supply_default[time, default_technologies]
            * model.cost_default[default_technologies, "Fuel Price"]
            for default_technologies in model.set_default_technologies
            for time in model.set_time
        )
        + sum(
            model.supply_from_PV[time, "Contractor", "Household"]
            * model.cost_new["Contractor", "PV", "Fuel Price"]
            for time in model.set_time
        )
        + sum(
            model.supply_from_PV[time, "Contractor", "Car"]
            * model.cost_new["Contractor", "Charging Station", "Fuel Price"]
            for time in model.set_time
        )
        + sum(
            model.supply_from_battery[time, "Contractor", "Car"]
            * model.cost_new["Contractor", "Charging Station", "Fuel Price"]
            for time in model.set_time
        )
        + sum(
            model.supply_from_HP[time, "Contractor", "Household"]
            * model.cost_new["Contractor", "HP", "Fuel Price"]
            for time in model.set_time
        )
        + sum(
            model.supply_from_ST[time, "Contractor", "Household"]
            * model.cost_new["Contractor", "ST", "Fuel Price"]
            for time in model.set_time
        )
    )


model.ccost4 = Constraint(
    rule=variable_cost_rule,
    doc="Variable Cost per kWh used - depends on contracting pricing model",
)


def revenue_rule(model):
    return model.revenue == model.weight * (
        model.demand_shift_total * model.bonus_shifting
        + sum(
            model.supply_from_PV[time, finance_options, "Electric Grid"]
            * model.cost_default["Electricity", "Feedin Price"]
            for time in model.set_time
            for finance_options in model.set_finance_options
        )
        + sum(
            model.supply_from_ST[time, finance_options, "DH"]
            * model.cost_default["DH", "Feedin Price"]
            for time in model.set_time
            for finance_options in model.set_finance_options
        )
    )


model.ccost5 = Constraint(rule=revenue_rule, doc="Revenues by feed-in to grid")


#### PV Constraints
def PV_production_rule(model, time, finance_options):
    return model.supply_new[time, finance_options, "PV"] == (
        model.capacity[finance_options, "PV"] * model.capacity_factor_PV[time]
    )  # -(model.capacity[finance_options,'PV']*model.capacity_factor_PV[time])*model.temperature_factor_PV[time]


model.cPV1 = Constraint(
    model.set_time,
    model.set_finance_options,
    rule=PV_production_rule,
    doc="Produced electricity from PV equals installed capacity lowered by capacity and temperature factors",
)


def from_PV_supply_rule(model, time, finance_options):
    return model.supply_new[time, finance_options, "PV"] == sum(
        model.supply_from_PV[time, finance_options, PV2technologies]
        for PV2technologies in model.set_PV2
    )


model.cPV2 = Constraint(
    model.set_time,
    model.set_finance_options,
    rule=from_PV_supply_rule,
    doc="Produced electricity from PV equals the electricity from PV to other elements/technologies",
)


# def no_PV_curtailment_rule(model, time, finance_options):
#     return model.supply_from_PV[time, finance_options, "Curtailment"] == 0


# model.cPV2a = Constraint(
#     model.set_time,
#     model.set_finance_options,
#     rule=no_PV_curtailment_rule,
#     doc="Unables PV curtailment",
# )


def PV_capacity_rule_contractor(model):
    return inequality(
        model.min_capacity_PV_contractor,
        model.capacity["Contractor", "PV"],
        model.max_capacity_PV,
    )


model.cPV3 = Constraint(
    rule=PV_capacity_rule_contractor,
    doc="PV capacity is limited by maximum capacity given by Area of the roof and minimum set by contractor",
)


def PV_capacity_rule(model):
    return inequality(0, model.capacity["Self financed", "PV"], model.max_capacity_PV)


model.cPV4 = Constraint(
    rule=PV_capacity_rule,
    doc="PV capacity is limited by maximum capacity given by Area of the roof",
)


def PV_area_required_rule(model):
    return (
        sum(
            model.area_PV[finance_options]
            for finance_options in model.set_finance_options
        )
        == sum(
            model.capacity[finance_options, "PV"]
            for finance_options in model.set_finance_options
        )
        * model.capacity_density_PV
    )


model.cPV5 = Constraint(
    rule=PV_area_required_rule,
    doc="PV area needed is set by installed PV by financing option",
)


def PV_binary_if_capacity_rule(model, finance_options):
    return (
        model.binary_new_technologies[finance_options, "PV"] * model.max_capacity_PV
        >= model.capacity[finance_options, "PV"]
    )


model.cPV6 = Constraint(
    model.set_finance_options,
    rule=PV_binary_if_capacity_rule,
    doc="PV can only supply if capacity is installed",
)


def shared_roof_rule(model):
    return model.area_roof >= sum(
        model.area_PV[finance_options] for finance_options in model.set_finance_options
    ) + sum(
        model.capacity[finance_options, "ST"]
        for finance_options in model.set_finance_options
    )


model.cPV7 = Constraint(
    rule=shared_roof_rule,
    doc="Area of roof is shared by total PV and total ST area (equals ST capacity)",
)

#### ST Constraints

def ST_production_rule(model, time, finance_options):
    return model.supply_new[time, finance_options, "ST"] == (
        model.capacity[finance_options, "ST"]
        * model.irradiation[time]
        * model.efficiency_ST
    )


model.cST1 = Constraint(
    model.set_time,
    model.set_finance_options,
    rule=ST_production_rule,
    doc="Produced energy from ST equals installed area*irradiation times efficiency",
)


def from_ST_supply_rule(model, time, finance_options):
    return  model.supply_new[time, finance_options, "ST"] == (
        sum(model.supply_from_ST[time, finance_options, ST2technologies]
        for ST2technologies in model.set_ST2)
    )
        
model.cST2 = Constraint(
    model.set_time,
    model.set_finance_options,
    rule=from_ST_supply_rule,
    doc="Produced energy from ST equals energy from ST to other elements/technologies",
)


def ST_max_capacity_rule(model):
    return (
        model.max_capacity_ST
        == (1 - model.binary_default_technologies["DH"])
        * model.number_households
        * model.area_ST_per_person
        * model.simultaneity
        + model.binary_default_technologies["DH"] * model.area_roof
    )


model.cST3 = Constraint(
    rule=ST_max_capacity_rule,
    doc="Max capacity ST = max area ST is limited by roof area if DH is installed, if not than limited by DHW demand per person",
)


def ST_capacity_rule_contractor(model):
    return model.capacity["Contractor", "ST"] <= model.max_capacity_ST


model.cST4 = Constraint(
    rule=ST_capacity_rule_contractor,
    doc="ST capacity is limited by maximum capacity given by Area of the roof",
)

def ST_capacity_rule_contractor_2(model):
    return model.min_capacity_ST_contractor <= model.capacity["Contractor", "ST"]

model.cST5 = Constraint(
    rule=ST_capacity_rule_contractor_2,
    doc="ST capacity is limited given by the minimum set by contractor",
)


def ST_capacity_rule(model):
    return model.capacity["Self financed", "ST"] <= model.max_capacity_ST


model.cST6 = Constraint(
    rule=ST_capacity_rule,
    doc="ST capacity is limited by maximum capacity given by Area of the roof",
)





def ST_binary_if_capacity_rule(model, finance_options):
    return (
        model.binary_new_technologies[finance_options, "ST"] * 10e10
        >= model.capacity[finance_options, "ST"]
    )


model.cST7 = Constraint(
    model.set_finance_options,
    rule=ST_binary_if_capacity_rule,
    doc="ST can only supply if capacity is installed",
)

def ST_binary_general (model):
    return (
        model.binary_ST *100 >=
        sum(model.binary_new_technologies[finance_options, "ST"] 
        for finance_options in model.set_finance_options) 
    )


model.cSTtestnew = Constraint(
    rule=ST_binary_general,
    doc="ST can only supply if capacity is installed",
)

def ST_plus_DH_rule(model):
    return (
        model.binary_ST_and_DH*10e10
        >= (model.binary_ST +
        model.binary_default_technologies["DH"]) 
        -1
    )


model.cST8 = Constraint(
    rule=ST_plus_DH_rule,
    doc="Binary variable turns TRUE is ST AND DH are installed",
)



def ST_to_DH_supply_if_both_installed_rule(model,time,finance_options):
    return (model.binary_ST_and_DH *10e10 
        >= 
         model.supply_from_ST[time, finance_options, 'DH'] 
    )


model.cST9 = Constraint(
    model.set_time,
    model.set_finance_options,
    rule=ST_to_DH_supply_if_both_installed_rule,
    doc="supply from ST to DH if ST AND DH are installed",
)


def binary_ST_to_DH_supply_rule(model,time, finance_options):
    return (
        model.binary_ST_to_DH * 10e10 >= model.supply_from_ST[time, finance_options, 'DH'] 
    )


model.cST10 = Constraint(
    model.set_time,
    model.set_finance_options,
    rule=binary_ST_to_DH_supply_rule,
    doc="binary true if supply from ST to DH",
)

def ST_binary_if_supply_to_DH_rule(model, time,finance_options):
    return (
        model.supply_from_ST[time, finance_options, 'DH'] 
        <= model.binary_default_technologies['DH']* 10e10
    )


model.cSTtest = Constraint(
    model.set_time,
    model.set_finance_options,
    rule=ST_binary_if_supply_to_DH_rule,
    doc="ST can only supply if capacity is installed",
)



#### Insulation Constraints
def reduction_heating_demand_rule(model, time):
    return model.reduction_heating_demand[time] == model.demand[time, "Heating"] * sum(
        model.capacity[finance_options, "Insulation"]
        for finance_options in model.set_finance_options
    )


model.cins1 = Constraint(
    model.set_time,
    rule=reduction_heating_demand_rule,
    doc="Heat demand is reduced by insulation",
)


def reduction_heating_demand_if_insulation_rule(model, time, finance_options):
    return model.reduction_heating_demand[time] <= (
        model.binary_new_technologies[finance_options, "Insulation"]
        * model.connection_capacity_default["DH"]
    )


model.cins2 = Constraint(
    model.set_time,
    model.set_finance_options,
    rule=reduction_heating_demand_if_insulation_rule,
    doc="Heating demand can only be reduced if insulation is done",
)


def insulation_no_split_rule(model):
    return (
        model.binary_new_technologies["Contractor", "Insulation"]
        + model.binary_new_technologies["Self financed", "Insulation"]
        <= 1
    )


model.cins3 = Constraint(
    rule=insulation_no_split_rule,
    doc="Insulation is only financed by one party no split possible",
)

#### Stationary Battery Constraints
def from_battery_supply_rule(model, time, finance_options):
    return model.supply_new[time, finance_options, "Battery Powerflow"] == sum(
        model.supply_from_battery[time, finance_options, Battery2technologies]
        for Battery2technologies in model.set_Battery2
    )


model.cbat1 = Constraint(
    model.set_time,
    model.set_finance_options,
    rule=from_battery_supply_rule,
    doc="Total energy from battery equals energy from battery to other elements/technologies - here only to car",
)


def to_battery_supply_rule(model, time):
    return (
        sum(
            model.supply_to_battery[time, finance_options, toBatterytechnologies]
            for finance_options in model.set_finance_options
            for toBatterytechnologies in model.set_2Battery
        )
        == sum(
            model.supply_from_PV[time, finance_options, "Battery"]
            for finance_options in model.set_finance_options
        )
        + model.supply_from_elec_grid[time, "Battery"]
    )  # \
    # +(model.supply_from_car[time,'Battery'])


model.cbat2 = Constraint(
    model.set_time,
    rule=to_battery_supply_rule,
    doc="Total energy to battery equals energy to battery from other elements/technologies",
)


def efficiency_battery_rule(model, time, finance_options):
    return (
        sum(
            model.supply_to_battery[time, finance_options, toBatterytechnologies]
            for toBatterytechnologies in model.set_2Battery
        )
        * model.efficiency_battery
        == model.supply_new[time, finance_options, "Battery Powerflow"]
    )


model.cbat3 = Constraint(
    model.set_time,
    model.set_finance_options,
    rule=efficiency_battery_rule,
    doc="Input times efficiency equals battery output",
)


def powerflow_battery_out_limited_rule(model, time, finance_options):
    return inequality(
        0,
        model.supply_new[time, finance_options, "Battery Powerflow"],
        model.powerflow_max_battery,
    )


model.cbat4 = Constraint(
    model.set_time,
    model.set_finance_options,
    rule=powerflow_battery_out_limited_rule,
    doc="Power out of battery cannot extend max powerflow",
)


def powerflow_battery_in_limited_rule(model, time, finance_options):
    return inequality(
        0,
        sum(
            model.supply_to_battery[time, finance_options, toBatterytechnologies]
            for toBatterytechnologies in model.set_2Battery
        ),
        model.powerflow_max_battery,
    )


model.cbat5 = Constraint(
    model.set_time,
    model.set_finance_options,
    rule=powerflow_battery_in_limited_rule,
    doc="Power into battery cannot extend max powerflow",
)


def soc_limited_by_capapcity_rule(model, time, finance_options):
    return model.state_of_charge_battery[time, finance_options] <= (
        model.capacity[finance_options, "Battery Capacity"]
    )


model.cbat6 = Constraint(
    model.set_time,
    model.set_finance_options,
    rule=soc_limited_by_capapcity_rule,
    doc="SOC at every timestep is limited by capacity of battery",
)


def soc_rule(model, time, finance_options):
    if time == model.set_time[1]:
        return model.state_of_charge_battery[time, finance_options] == 0.0

    else:
        return model.state_of_charge_battery[
            time, finance_options
        ] == model.state_of_charge_battery[time - 1, finance_options] + (
            sum(
                model.supply_to_battery[time, finance_options, toBatterytechnologies]
                for toBatterytechnologies in model.set_2Battery
            )
            * model.efficiency_battery
        ) - (
            (
                sum(
                    model.supply_from_battery[
                        time, finance_options, Battery2technologies
                    ]
                    for Battery2technologies in model.set_Battery2
                )
                / model.efficiency_battery
            )
        )


model.cbat7 = Constraint(
    model.set_time,
    model.set_finance_options,
    rule=soc_rule,
    doc="SOC defined by in- and output",
)


def battery_binary_if_capacity_rule(model, finance_options):
    return (
        model.binary_new_technologies[finance_options, "Battery Capacity"]
        * model.powerflow_max_battery
    ) >= model.capacity[finance_options, "Battery Capacity"]


model.cbat8 = Constraint(
    model.set_finance_options,
    rule=battery_binary_if_capacity_rule,
    doc="Battery can only supply if capacity is installed",
)


def battery_no_split_rule(model):
    return (
        model.binary_new_technologies["Contractor", "Battery Capacity"]
        + model.binary_new_technologies["Self financed", "Battery Capacity"]
        <= 1
    )


model.cbat9 = Constraint(
    rule=insulation_no_split_rule,
    doc="Battery is only financed by one party no split possible",
)

#### Heating System Constraints
def only_one_heating_system_rule(model):
    return (
        sum(
            model.binary_new_technologies[finance_options, "HP"]
            for finance_options in model.set_finance_options
        )
        + model.binary_default_technologies["DH"]
        + model.binary_default_technologies["Gas"]
        <= 1
    )


model.c_heating1 = Constraint(
    rule=only_one_heating_system_rule,
    doc="Only one heating system can be installed - HP, DH or Gas",
)



def gas_output_if_installed_rule(model, time):
    return model.supply_default[time, "Gas"] <= (
        model.binary_default_technologies["Gas"]
        * 10000
    )


model.c_heating2 = Constraint(
    model.set_time,
    rule=gas_output_if_installed_rule,
    doc="Gas can only supply if installed",
)


def DH_output_if_installed_rule(model, time):
    return model.supply_default[time, "DH"] <= (
        model.binary_default_technologies["DH"]
        * 10000
    )


model.c_heating3 = Constraint(
    model.set_time,
    rule=DH_output_if_installed_rule,
    doc="DH can only supply if installed",
)

#### Heat Pump Constraints
def from_HP_supply_rule(model, time, finance_options):
    return model.supply_new[time, finance_options, "HP"] == sum(
        model.supply_from_HP[time, finance_options, HP2technologies]
        for HP2technologies in model.set_HP2
    )


model.c_HP1 = Constraint(
    model.set_time,
    model.set_finance_options,
    rule=from_HP_supply_rule,
    doc="Total energy from HP equals energy from HP to other elements/technologies - here only to household",
)


def to_HP_supply_rule(model, time):
    return (
        sum(
            model.supply_to_HP[time, finance_options, toHPtechnologies]
            for finance_options in model.set_finance_options
            for toHPtechnologies in model.set_2HP
        )
        == sum(
            model.supply_from_PV[time, finance_options, "HP"]
            for finance_options in model.set_finance_options
        )
        + model.supply_from_elec_grid[time, "HP"]
    )


model.c_HP2 = Constraint(
    model.set_time,
    rule=to_HP_supply_rule,
    doc="Total energy to HP equals energy to HP from other elements/technologies",
)


def HP_capacity_rule(model, finance_options):
    return model.capacity[finance_options, "HP"] <= 1000


model.c_HP3 = Constraint(
    model.set_finance_options, rule=HP_capacity_rule, doc="Capacity of HP is bounded"
)


def HP_capacity_greater_than_supply_rule(model, time, finance_options):
    return (
        model.capacity[finance_options, "HP"]
        >= model.supply_new[time, finance_options, "HP"]
    )


model.c_HP4 = Constraint(
    model.set_time,
    model.set_finance_options,
    rule=HP_capacity_greater_than_supply_rule,
    doc="Capacity of HP has to be greater than maximum supply in any timestep",
)


def HP_efficiency_rule(model, time):
    return sum(
        model.supply_to_HP[time, finance_options, toHPtechnologies]
        for finance_options in model.set_finance_options
        for toHPtechnologies in model.set_2HP
    ) * model.cop[time] == sum(
        model.supply_new[time, finance_options, "HP"]
        for finance_options in model.set_finance_options
    )


model.c_HP5 = Constraint(
    model.set_time,
    rule=HP_efficiency_rule,
    doc="Input times COP at every timestep equals HP output",
)

# def HP_efficiency_rule(model,time):
#     return (sum(model.supply_from_PV[time,finance_options,'HP'] \
#     for finance_options in model.set_finance_options)+model.supply_from_elec_grid[time,'HP']) *model.cop[time] == \
#     model.supply_new[time,'Contractor','HP']
# model.c_HP5b = Constraint(model.set_time,rule= HP_efficiency_rule, \
#     doc='Input times COP at every timestep equals HP output')

# def HP_efficiency_rule(model,time,finance_options):
#     return (sum(model.supply_from_PV[time,finance_options,'HP'] \
#     for finance_options in model.set_finance_options)+model.supply_from_elec_grid[time,'HP']) *model.cop[time] == \
#     model.supply_new[time,finance_options,'HP']
# model.c_HP5c = Constraint(model.set_time,model.set_finance_options,rule= HP_efficiency_rule, \
#     doc='Input times COP at every timestep equals HP output')

# def HP_efficiency_rule(model,time):
#     return (model.supply_from_PV[time,'Contractor','HP'] +model.supply_from_elec_grid[time,'HP']) *model.cop[time] == \
#     model.supply_new[time,'Self financed','HP']
# model.c_HP5b = Constraint(model.set_time,rule= HP_efficiency_rule, \
#     doc='Input times COP at every timestep equals HP output')

# def HP_efficiency_rule(model,time):
#     return (model.supply_from_PV[time,'Contractor','HP'] +model.supply_from_elec_grid[time,'HP']) *model.cop[time] == \
#     model.supply_new[time,'Contractor','HP']
# model.c_HP5c = Constraint(model.set_time,rule= HP_efficiency_rule, \
#     doc='Input times COP at every timestep equals HP output')


def HP_binary_if_capacity_rule(model, finance_options):
    return (
        model.binary_new_technologies[finance_options, "HP"]
        * model.connection_capacity_default["Gas"]
    ) >= model.capacity[finance_options, "HP"]


model.c_HP6 = Constraint(
    model.set_finance_options,
    rule=HP_binary_if_capacity_rule,
    doc="HP can only supply if installed. Connection capacity gas equals max thermal demand",
)


def HP_no_split_rule(model):
    return (
        model.binary_new_technologies["Contractor", "HP"]
        + model.binary_new_technologies["Self financed", "HP"]
        <= 1
    )


model.c_HP7 = Constraint(
    rule=HP_no_split_rule, doc="HP is only financed by one party no split possible"
)

###### try start

# def from_car_supply_rule(model,time,):
#     return sum(model.supply_new[time,finance_options,'Charging Station'] for finance_options in model.set_finance_options) \
#     == sum(model.supply_from_car[time,Car2technologies] for Car2technologies in model.set_car2)
# model.c_car1 = Constraint(model.set_time,rule= from_car_supply_rule, \
#     doc='Total energy from Cars equals energy from Cars to other elements/technologies - here only to Battery')

# def from_car_supply_only_if_battery_capacity_rule(model,time,):
#     return sum(model.supply_new[time,finance_options,'Charging Station']for finance_options in model.set_finance_options)\
#     <= 1000*sum(model.binary_new_technologies[finance_options,'Battery Capacity']for finance_options in model.set_finance_options)
# model.c_car1a = Constraint(model.set_time,rule= from_car_supply_only_if_battery_capacity_rule, \
#     doc='Supply from car to battery only if battery exists')


def to_car_supply_rule(model, time):
    return (
        sum(
            model.supply_to_car[time, toCartechnologies]
            for toCartechnologies in model.set_2car
        )
        == sum(
            model.supply_from_PV[time, finance_options, "Car"]
            for finance_options in model.set_finance_options
        )
        + sum(
            model.supply_from_battery[time, finance_options, "Car"]
            for finance_options in model.set_finance_options
        )
        + model.supply_from_elec_grid[time, "Car"]
    )


model.c_car2 = Constraint(
    model.set_time,
    rule=to_car_supply_rule,
    doc="Total energy to car equals energy to car from other elements/technologies",
)


def to_car_supply_rule_2(model, time):
    return model.supply_to_car[time, "PV"] == sum(
        model.supply_from_PV[time, finance_options, "Car"]
        for finance_options in model.set_finance_options
    )


model.c_car2a = Constraint(
    model.set_time,
    rule=to_car_supply_rule_2,
    doc="Total energy to car equals energy to car from other elements/technologies",
)


def to_car_supply_rule_3(model, time):
    return model.supply_to_car[time, "Battery"] == sum(
        model.supply_from_battery[time, finance_options, "Car"]
        for finance_options in model.set_finance_options
    )


model.c_car2b = Constraint(
    model.set_time,
    rule=to_car_supply_rule_3,
    doc="Total energy to car equals energy to car from other elements/technologies",
)


def to_car_supply_rule_4(model, time):
    return (
        model.supply_to_car[time, "Electric Grid"]
        == model.supply_from_elec_grid[time, "Car"]
    )


model.c_car2c = Constraint(
    model.set_time,
    rule=to_car_supply_rule_4,
    doc="Total energy to car equals energy to car from other elements/technologies",
)


def car_charging_capacity_rule(model, time):
    return sum(
        model.number_charging_stations[finance_options]
        for finance_options in model.set_finance_options
    ) * model.max_powerflow_charging_station >= sum(
        model.supply_to_car[time, toCartechnologies]
        for toCartechnologies in model.set_2car
    )


model.c_car3 = Constraint(
    model.set_time,
    rule=car_charging_capacity_rule,
    doc="Charging Station Capacity need to be greater than the maximum charging demand per timestep",
)


def amount_charging_stations_rule(model):
    return (
        sum(
            model.number_charging_stations[finance_options]
            for finance_options in model.set_finance_options
        )
        == model.number_cars
    )


model.c_car4 = Constraint(
    rule=amount_charging_stations_rule,
    doc="Number of charging stations by financing options need to cover demand for charging station (now equals number of cars)",
)


def amount_charging_stations_equals_capacity_rule(model, finance_options):
    return (
        model.capacity[finance_options, "Charging Station"]
        == model.number_charging_stations[finance_options]
    )


model.c_car5 = Constraint(
    model.set_finance_options,
    rule=amount_charging_stations_equals_capacity_rule,
    doc="Number of charging stations by financing options need to cover demand for charging station (now equals number of cars)",
)  #### Battery of Cars Constraints


#### Battery of Cars Constraints


def car_powerflow_battery_out_limited_rule(model, time):
    return inequality(
        0,
        sum(
            model.supply_new[time, finance_options, "Charging Station"]
            for finance_options in model.set_finance_options
        ),
        (model.powerflow_max_battery_car * model.number_cars),
    )


model.c_car_bat1 = Constraint(
    model.set_time,
    rule=car_powerflow_battery_out_limited_rule,
    doc="Powerflow out of car battery cannot extend max powerflow",
)


def car_powerflow_battery_in_limited_rule(model, time):
    return inequality(
        0,
        sum(
            model.supply_to_car[time, toCartechnologies]
            for toCartechnologies in model.set_2car
        ),
        model.powerflow_max_battery_car * model.number_cars,
    )


model.c_car_bat2 = Constraint(
    model.set_time,
    rule=car_powerflow_battery_in_limited_rule,
    doc="Powerflow into car battery cannot extend max powerflow",
)


def car_soc_limited_by_capapcity_rule(model, time):
    return model.state_of_charge_car[time] <= model.capacity_car


model.c_car_bat3 = Constraint(
    model.set_time,
    rule=car_soc_limited_by_capapcity_rule,
    doc="SOC of car at every timestep is limited by capacity of battery",
)


def car_soc_rule(model, time):
    if time == model.set_time[1]:
        return model.state_of_charge_car[time] == 0
    else:
        return (
            model.state_of_charge_car[time]
            == model.state_of_charge_car[time - 1]
            + (
                sum(
                    model.supply_to_car[time, toCartechnologies]
                    for toCartechnologies in model.set_2car
                )
                * model.efficiency_battery_car
            )
            - (
                (
                    sum(
                        model.supply_from_car[time, Car2technologies]
                        for Car2technologies in model.set_car2
                    )
                    / model.efficiency_battery_car
                )
            )
            + model.demand_shift_up[time]
            - model.demand_shift_down[time]
        )


model.c_car_bat4 = Constraint(
    model.set_time,
    rule=car_soc_rule,
    doc="SOC car defined by in- and output puls minus demand shift",
)


def car_battery_efficiency_rule(model, time):
    return sum(
        model.supply_new[time, finance_options, "Charging Station"]
        for finance_options in model.set_finance_options
    ) <= (
        sum(
            model.supply_to_car[time, toCartechnologies]
            for toCartechnologies in model.set_2car
        )
        * model.efficiency_battery_car
    )


model.c_car_bat5 = Constraint(
    model.set_time,
    rule=car_battery_efficiency_rule,
    doc="Input times efficiency equals maximum Car output",
)


##### apply this rule if you know in which timestep the car need which SOC
# def charged_by_soc_rule(model,time):
#     if time in range(1,6) and range(24,30):
#         return  (model.state_of_charge_car[time]) >= (model.demand[time,'Car']) #+ model.demand_shift_up[time] -model.demand_shift_down[time])
#     else:
#         return model.state_of_charge_car[time] == model.state_of_charge_car[time-1] #+ model.demand_shift_up[time] -model.demand_shift_down[time]
# model.c_car_bat5 = Constraint(model.set_time,rule= charged_by_soc_rule, \
#     doc='Demand curve of charging needs to be met')

# def charged_by_soc_rule(model,time):
#     return  model.state_of_charge_car[time] == model.demand[time,'Car']
# model.c_car_bat5 = Constraint(model.set_time,rule= charged_by_soc_rule, \
#     doc='Demand curve of charging needs to be met'


### apply this rule if you know in which timestep the car needs the be charged
def demand_charging_rule(model, time):
    return (
        sum(
            model.supply_to_car[time, toCartechnologies]
            for toCartechnologies in model.set_2car
        )
        == model.demand[time, "Car"]
        + model.demand_shift_up[time]
        - model.demand_shift_down[time]
    )


model.c_car_bat6 = Constraint(
    model.set_time,
    rule=demand_charging_rule,
    doc="Demand curve of charging needs to be met",
)


#### Multi Party House Constraints
def household_electricity_demand_rule(model, time):
    return (
        model.supply_from_elec_grid[time, "Household"]
        + sum(
            model.supply_from_PV[time, finance_options, "Household"]
            for finance_options in model.set_finance_options
        )
        == model.demand[time, "Electricity household"]
    )


model.c_house1 = Constraint(
    model.set_time,
    rule=household_electricity_demand_rule,
    doc="Electricity demand curve of households plus charging need to be met",
)


def household_thermal_demand_rule(model, time):
    return model.total_thermal_demand[time] == model.supply_default[
        time, "Gas"
    ] * model.efficiency_gas + model.supply_default[time, "DH"] + sum(
        model.supply_new[time, finance_options, "HP"]
        for finance_options in model.set_finance_options
    ) + sum(
        model.supply_from_ST[time, finance_options, "Household"]
        for finance_options in model.set_finance_options
    )


model.c_house2 = Constraint(
    model.set_time,
    rule=household_thermal_demand_rule,
    doc="Thermal demand curve of households need to be met",
)


def household_total_thermal_demand_rule(model, time):
    return (
        model.total_thermal_demand[time]
        == model.demand[time, "DHW"] + model.reduced_heating_demand[time]
    )


model.c_house3 = Constraint(
    model.set_time,
    rule=household_total_thermal_demand_rule,
    doc="Thermal demand consists of DHw and heatig demand",
)


def reduced_heating_demand_rule(model, time):
    return (
        model.reduced_heating_demand[time]
        == model.demand[time, "Heating"] - model.reduction_heating_demand[time]
    )


model.c_house4 = Constraint(
    model.set_time,
    rule=reduced_heating_demand_rule,
    doc="Reduced heating demand after insulation",
)

#### Electric Grid Constraints
def from_grid_supply_rule(model, time):
    return model.supply_default[time, "Electricity"] == sum(
        model.supply_from_elec_grid[time, Grid2technologies]
        for Grid2technologies in model.set_elec_grid2
    )


model.c_grid1 = Constraint(
    model.set_time,
    rule=from_grid_supply_rule,
    doc="Total energy from electric grid equals energy from electric grid to other elements/technologies",
)

## Demand Side Management Constraints
def no_shift_rule (model):
    return sum(model.demand_shift_up[time] for time in model.set_time) == 0
model.c_dsm0a= Constraint(rule= no_shift_rule, \
    doc='Up shift in timestep 1 is zero as SOC of car is also zero')

def no_shift_rule_2 (model):
    return sum(model.demand_shift_down[time] for time in model.set_time) == 0
model.c_dsm0b= Constraint(rule= no_shift_rule_2, \
    doc='Up shift in timestep 1 is zero as SOC of car is also zero')


def first_up_shift_rule(model):
    return model.demand_shift_up[1] == 0


model.c_dsm1 = Constraint(
    rule=first_up_shift_rule,
    doc="Up shift in timestep 1 is zero as SOC of car is also zero",
)


def first_down_shift_rule(model):
    return model.demand_shift_down[1] == 0


model.c_dsm2 = Constraint(
    rule=first_down_shift_rule,
    doc="Up shift in timestep 1 is zero as SOC of car is also zero",
)


def dsm_up_rule_per_day_rule(model, day):
    return (model.up_shifts_in_one_day[day]) == sum(
        model.demand_shift_up[day * 24 + i] for i in range(1, 24)
    )


model.c_dsm3 = Constraint(
    model.set_day,
    rule=dsm_up_rule_per_day_rule,
    doc="Sum of upshifts equals downshifts within 24h",
)


def dsm_down_rule_per_day_rule(model, day):
    return (model.down_shifts_in_one_day[day]) == sum(
        model.demand_shift_down[day * 24 + i] for i in range(1, 24)
    )


model.c_dsm4 = Constraint(
    model.set_day,
    rule=dsm_down_rule_per_day_rule,
    doc="Sum of upshifts equals downshifts within 24h",
)


def up_and_down_equal_rule(model, day):
    return (model.up_shifts_in_one_day[day]) == (model.down_shifts_in_one_day[day])


model.c_dsm5 = Constraint(
    model.set_day,
    rule=up_and_down_equal_rule,
    doc="Sum of upshifts equals downshifts within 24h",
)


def total_dsm_rule(model):
    return model.demand_shift_total == sum(
        model.down_shifts_in_one_day[day] for day in model.set_day
    )


model.c_dsm6 = Constraint(
    rule=total_dsm_rule,
    doc="Sum of upshifts and downshifts within one year equals total shift",
)


def binary_if_shift_up_rule(model, time):
    return model.demand_shift_up[time] <= (
        model.binary_up_shift[time] *100* model.number_cars
    )


model.c_dsm7 = Constraint(
    model.set_time,
    rule=binary_if_shift_up_rule,
    doc="Binary variables becomes TRUE if up shift is done",
)


def binary_if_shift_down_rule(model, time):
    return model.demand_shift_down[time] <= (
        model.binary_down_shift[time]*100*model.number_cars
    )


model.c_dsm8 = Constraint(
    model.set_time,
    rule=binary_if_shift_down_rule,
    doc="Binary variables becomes TRUE if down shift is done",
)


def up_or_down_in_one_timestep_rule(model, time):
    return model.binary_up_shift[time] + model.binary_down_shift[time] <= 1


model.c_dsm9 = Constraint(
    model.set_time,
    rule=up_or_down_in_one_timestep_rule,
    doc="up OR down shift in one timestep",
)

# def total_dsm_rule(model):
#     return model.demand_shift_total \
#     == sum(model.demand_shift_up[time] for time in model.set_time)+sum(model.demand_shift_down[time] for time in model.set_time)
# model.c_dsm6 = Constraint(rule=total_dsm_rule, \
# doc='Sum of upshifts and downshifts within one year equals total shift')


def shifted_demand_rule(model, time):
    return (
        model.shifted_demand[time]
        == model.demand[time, "Car"]
        + model.demand_shift_up[time]
        - model.demand_shift_down[time]
    )


model.c_dsm10 = Constraint(
    model.set_time,
    rule=shifted_demand_rule,
    doc="Shifted demand defined by upshifts and downshifts",
)

########


# def to_battery_supply_rule(model,time,finance_options):
#     return model.supply_new[time,finance_options,'Battery Capacity']== model.supply_from_PV[time,finance_options,'Battery'] + \
#         model.supply_from_elec_grid[time,finance_options,'Battery'] + model.supply_from_car[time,finance_options,'Battery']
# model.c19 = Constraint(model.set_time,model.set_finance_options, rule= to_battery_supply_rule, \
#     doc='Total energy to battery equals energy to battery from other elements/technologies')


# model.cST3.pprint()
# model.ccost2.pprint()



opt = SolverFactory("glpk")
results = opt.solve(model)

# instance = model.create_instance()
# model.c_dsm6.pprint()
# model.cST1.pprint()

# print(model.max_capacity_PV.value)

status = results.solver.status
termination_condition = results.solver.termination_condition
print("termination_condition: ", termination_condition)
print("status: ", status)

# model.cST8.pprint()

print("Total Shift", model.demand_shift_total.value)




# for day in model.set_day:
#     if model.up_shifts_in_one_day[day].value and model.down_shifts_in_one_day[day].value != 0:
#         print('Up shift one day',day,model.up_shifts_in_one_day[day].value)
#         print('Down shift one day',day,model.down_shifts_in_one_day[day].value)

# for time in model.set_time:
#     if model.demand_shift_up[time].value or model.demand_shift_down[time].value != 0:
#         print("Up shift", time, model.demand_shift_up[time].value)
#         print("Down shift", time, model.demand_shift_down[time].value)

# for time in model.set_time:
#     print('Supply to car',time,sum(model.supply_to_car[time,toCartechnologies].value for toCartechnologies in model.set_2car))

# for time in model.set_time:
#     print('soc car',time,model.state_of_charge_car[time].value)

# for time in model.set_time:
#     print('Charging demand',time, model.demand[time,'Car'])

# print('Capacity charging station Self financed ',model.capacity['Self financed','Charging Station'].value)
# print('Capacity charging station Contractor',model.capacity['Contractor','Charging Station'].value)

# for finance_option in model.set_finance_options:
#     for technologies in model.set_new_technologies:
#         print('Capacity',finance_option, technologies, round(model.capacity[finance_option,technologies].value))

# for time in model.set_time:
#     print('Outcome HP',time,model.supply_new[time,'Self financed','HP'].value)
#     print('PV to HP',time,model.supply_from_PV[time,'Contractor','HP'].value)
#     print('Production PV',time,model.supply_new[time,'Contractor','PV'].value)


# # for time in model.set_time:
# #     print('Supply',time,'Contractor',model.supply_from_HP[time,'Contractor','Household'].value)

# # # for v in instance.component_objects(Var, active=True):
# # #     print ("Variable component object",v)
# # #     for index in v:
# # #         print ("   ", index, v[index].value)


# print('Total annual Cost:',round(model.obj()), '€')
# print('Total inbvestment Cost:', round(model.investment_costs_total.value),'€')
# print('Capacity Insulation Self financed',round(model.capacity['Self financed','Insulation'].value))
# print('Capacity Insulation Contractor',round(model.capacity['Contractor','Insulation'].value))

print("Capacity PV Self financed", round(model.capacity["Self financed", "PV"].value))
print("Capacity PV Contractor", round(model.capacity["Contractor", "PV"].value))
# print('Sum supply PV Self financed:', round(sum(model.supply_new[time,'Self financed','PV'].value for time in model.set_time)),'kWh')
# print('Sum supply PV Contractor:', round(sum(model.supply_new[time,'Contractor','PV'].value for time in model.set_time)),'kWh')
# print('Sum supply PV to Grid:', round(sum(model.supply_from_PV[time,finance_options,'Electric Grid'].value for time in model.set_time \
#     for finance_options in model.set_finance_options)),'kWh')
# print('Sum supply PV to Household:', round(sum(model.supply_from_PV[time,finance_options,'Household'].value for time in model.set_time \
#     for finance_options in model.set_finance_options)),'kWh')
# print('Sum supply PV to Car:', round(sum(model.supply_from_PV[time,finance_options,'Car'].value for time in model.set_time \
#     for finance_options in model.set_finance_options)),'kWh')
# print('Sum supply PV to Battery:', round(sum(model.supply_from_PV[time,finance_options,'Battery'].value for time in model.set_time \
#     for finance_options in model.set_finance_options)),'kWh')
# print('Sum supply PV to HP:', round(sum(model.supply_from_PV[time,finance_options,'HP'].value for time in model.set_time \
#     for finance_options in model.set_finance_options)),'kWh')

# print(
#     "Sum supply PV Contractor:",
#     round(
#         sum(model.supply_new[time, "Contractor", "PV"].value for time in model.set_time)
#     ),
#     "kWh",
# )
# print(
#     "Sum supply PV Contractor to Grid:",
#     round(
#         sum(
#             model.supply_from_PV[time, "Contractor", "Electric Grid"].value
#             for time in model.set_time
#         )
#     ),
#     "kWh",
# )
# print(
#     "Sum supply PV Contractor to Household:",
#     round(
#         sum(
#             model.supply_from_PV[time, "Contractor", "Household"].value
#             for time in model.set_time
#         )
#     ),
#     "kWh",
# )
# print(
#     "Sum supply PV Contractor to Car:",
#     round(
#         sum(
#             model.supply_from_PV[time, "Contractor", "Car"].value
#             for time in model.set_time
#         )
#     ),
#     "kWh",
# )
# print(
#     "Sum supply PV Contractor to Battery:",
#     round(
#         sum(
#             model.supply_from_PV[time, "Contractor", "Battery"].value
#             for time in model.set_time
#         )
#     ),
#     "kWh",
# )
# print(
#     "Sum supply PV Contractor to HP:",
#     round(
#         sum(
#             model.supply_from_PV[time, "Contractor", "HP"].value
#             for time in model.set_time
#         )
#     ),
#     "kWh",
# )
# print(
#     "Sum supply PV Contractor Curtailment:",
#     round(
#         sum(
#             model.supply_from_PV[time, "Contractor", "Curtailment"].value
#             for time in model.set_time
#         )
#     ),
#     "kWh",
# )
# print(
#     "Sum supply PV Self financed to Grid:",
#     round(
#         sum(
#             model.supply_from_PV[time, "Self financed", "Electric Grid"].value
#             for time in model.set_time
#         )
#     ),
#     "kWh",
# )
# print(
#     "Sum supply PV Self financed to Household:",
#     round(
#         sum(
#             model.supply_from_PV[time, "Self financed", "Household"].value
#             for time in model.set_time
#         )
#     ),
#     "kWh",
# )
# print(
#     "Sum supply PV Self financed to Car:",
#     round(
#         sum(
#             model.supply_from_PV[time, "Self financed", "Car"].value
#             for time in model.set_time
#         )
#     ),
#     "kWh",
# )
# print(
#     "Sum supply PV Self financed to Battery:",
#     round(
#         sum(
#             model.supply_from_PV[time, "Self financed", "Battery"].value
#             for time in model.set_time
#         )
#     ),
#     "kWh",
# )
# print(
#     "Sum supply PV Self financed to HP:",
#     round(
#         sum(
#             model.supply_from_PV[time, "Self financed", "HP"].value
#             for time in model.set_time
#         )
#     ),
#     "kWh",
# )
# print(
#     "Sum supply PV Self financed Curtailment:",
#     round(
#         sum(
#             model.supply_from_PV[time, "Self financed", "Curtailment"].value
#             for time in model.set_time
#         )
#     ),
#     "kWh",
# )

print('Capacity ST Self financed',(model.capacity['Self financed','ST'].value))
print('Capacity ST Contractor',(model.capacity['Contractor', "ST"].value))
# print('Sum supply ST Self financed:', round(sum(model.supply_new[time,'Self financed','ST'].value for time in model.set_time)),'kWh')
# print('Sum supply ST Contractor:', round(sum(model.supply_new[time,'Contractor','ST'].value for time in model.set_time)),'kWh')
# print('Sum supply ST to DH:', round(sum(model.supply_from_ST[time,finance_options,'DH'].value for time in model.set_time \
#     for finance_options in model.set_finance_options)),'kWh')

# print('Capacity HP Self financed',round(model.capacity['Self financed','HP'].value))
# print('Capacity HP Contractor',round(model.capacity['Contractor','HP'].value))
# print('Capacity HP total',round(sum(model.capacity[finance_options,'HP'].value for finance_options in model.set_finance_options)))
# print('Sum supply HP Self financed:', round(sum(model.supply_new[time,'Self financed','HP'].value for time in model.set_time)),'kWh')
# print('Sum supply HP Contractor:', round(sum(model.supply_new[time,'Contractor','HP'].value for time in model.set_time)),'kWh')
# print('Sum supply HP Self financed to household:', round(sum(model.supply_from_HP[time,'Self financed','Household'].value for time in model.set_time)),'kWh')
# print('Sum supply HP Contractor to household:', round(sum(model.supply_from_HP[time,'Contractor','Household'].value for time in model.set_time)),'kWh')

# print('Sum supply to HP Self financed from grid:', round(sum(model.supply_to_HP[time,'Self financed','Electric Grid'].value for time in model.set_time)),'kWh')

# print('Capacity Battery Self financed',round(model.capacity['Self financed','Battery Capacity'].value))
# print('Capacity Battery Contractor',round(model.capacity['Contractor','Battery Capacity'].value))


print('Sum supply electric Grid to household:', round(sum(model.supply_from_elec_grid[time,'Household'].value for time in model.set_time)),'kWh')

print('Sum supply electric Grid to Car:', round(sum(model.supply_from_elec_grid[time,'Car'].value for time in model.set_time)),'kWh')
print('Sum supply electric Grid to all elements:', round(sum(model.supply_from_elec_grid[time,grid2technologies].value for time in model.set_time \
    for grid2technologies in model.set_elec_grid2)),'kWh')
# # print('Sum supply electric Grid to all elements - check :', round(sum(model.supply_default[time,'Electricity'].value for time in model.set_time)),'kWh')

# # print('Sum supply DH:', round(sum(model.supply_default[time,'DH'].value for time in model.set_time)),'kWh')
# # print('Sum supply Gas:', round(sum(model.supply_default[time,'Gas'].value for time in model.set_time)),'kWh')

# print(
#     "PV Self financed installed?",
#     model.binary_new_technologies["Self financed", "PV"].value,
# )
# print(
#     "PV Contractor installed?", model.binary_new_technologies["Contractor", "PV"].value
# )
print(
    "ST Self financed installed?",
    model.binary_new_technologies['Self financed','ST'].value,
)
print(
    "ST Contractor installed?", model.binary_new_technologies['Contractor','ST'].value
)
print(
    "HP Self financed installed?",
    model.binary_new_technologies["Self financed", "HP"].value,
)
print(
    "HP Contractor installed?", model.binary_new_technologies["Contractor", "HP"].value
)
print("DH installed?", model.binary_default_technologies["DH"].value)

print("DH AND ST installed?", model.binary_ST_and_DH.value)
print("ST feeds into DH? ", model.binary_ST_to_DH.value)
print("ST generally installed? ", model.binary_ST.value)


print("Gas installed?", model.binary_default_technologies["Gas"].value)
# print(
#     "Battery Self financed installed?",
#     model.binary_new_technologies["Self financed", "Battery Capacity"].value,
# )
# print(
#     "Battery Contractor installed?",
#     model.binary_new_technologies["Contractor", "Battery Capacity"].value,
# )

# print('Total supply to Car:',round(sum(model.supply_to_car[time,toCartechnologies].value for time in model.set_time for toCartechnologies in model.set_2car)),'kWh')
# print('Is covered by:')
# print('PV to Car',round(sum(model.supply_from_PV[time,finance_options,'Car'].value for time in model.set_time for finance_options in model.set_finance_options)),'kWh')
# print('PV to Car check',round(sum(model.supply_to_car[time,'PV'].value for time in model.set_time)),'kWh')
# print('Battery to Car',round(sum(model.supply_from_battery[time,finance_options,'Car'].value for time in model.set_time for finance_options in model.set_finance_options)),'kWh')
# print('Battery to Car check',round(sum(model.supply_to_car[time,'Battery'].value for time in model.set_time)),'kWh')
# print('grid to Car',round(sum(model.supply_from_elec_grid[time,'Car'].value for time in model.set_time)),'kWh')
# print('grid to Car check',round(sum(model.supply_to_car[time,'Electric Grid'].value for time in model.set_time)),'kWh')
# print(
#     "Supply to car in hour 12",
#     round(
#         sum(
#             model.supply_to_car[12, toCartechnologies].value
#             for toCartechnologies in model.set_2car
#         )
#     ),
# )

# print('Total Supply from grid',round(sum(model.supply_default[time,'Electricity'].value for time in model.set_time)),'kWh')
# print('grid to household',round(sum(model.supply_from_elec_grid[time,'Household'].value for time in model.set_time)),'kWh')
# print('grid to HP',round(sum(model.supply_from_elec_grid[time,'HP'].value for time in model.set_time)),'kWh')

# print('grid to Car 16h',round(model.supply_from_elec_grid[16,'Car'].value))
# print('PV to Car 16h',round(model.supply_to_car[16,'PV'].value))
# print('sum to Car 16h',(sum(model.supply_to_car[16,toCartechnologies].value for toCartechnologies in model.set_2car)),'kWh')

# print('Car to battery:')
# print('Total supply from Car:',round(sum(model.supply_from_car[time,Car2technologies].value for time in model.set_time for Car2technologies in model.set_car2)),'kWh')
# print('Total supply from Car check:',round(sum(model.supply_new[time,finance_options,'Charging Station'].value for time in model.set_time for finance_options in model.set_finance_options)),'kWh')
# #print('Total supply from Car self financed:',round(sum(model.supply_from_car[time,'Self financed',Car2technologies].value for time in model.set_time for Car2technologies in model.set_car2)),'kWh')


print('Thermal demand:', round(sum(model.total_thermal_demand[time].value for time in model.set_time)),'kWh')
print('Thermal demand need to be covered by:')
print('Supply gas:',(sum(model.supply_default[time,'Gas'].value for time in model.set_time)),'kWh')
print('Supply DH:',(sum(model.supply_default[time,'DH'].value for time in model.set_time)),'kWh')
print('Supply from HP to household Contractor:',(sum(model.supply_from_HP[time,'Contractor','Household'].value for time in model.set_time)),'kWh')
print('Supply HP to household Contractor - check:',(sum(model.supply_new[time,'Contractor','HP'].value for time in model.set_time)),'kWh')
print('Supply from HP to household Self financed:',(sum(model.supply_from_HP[time,'Self financed','Household'].value for time in model.set_time)),'kWh')
print('Supply HP to household Self financed - check:',(sum(model.supply_new[time,'Self financed','HP'].value for time in model.set_time)),'kWh')
# for time in model.set_time:
#     print(time, model.supply_from_ST[time,'Contractor','DH'].value)

# for time in model.set_time:
#     print(time, model.supply_new[time,'Contractor','ST'].value)


print('Supply ST to DH Contractor:',round(sum(model.supply_from_ST[time,'Contractor','DH'].value for time in model.set_time)),'kWh')
print('Supply ST to DH Self financed:',round(sum(model.supply_from_ST[time,'Self financed','DH'].value for time in model.set_time)),'kWh')

print('Supply ST to household Contractor:',round(sum(model.supply_from_ST[time,'Contractor','Household'].value for time in model.set_time)),'kWh')
print('Supply ST to household Self financed:',round(sum(model.supply_from_ST[time,'Self financed','Household'].value for time in model.set_time)),'kWh')

print('Supply ST  Contractor - check:',round(sum(model.supply_new[time,'Contractor','ST'].value for time in model.set_time)),'kWh')
print('Supply ST  Self financed - check:',round(sum(model.supply_new[time,'Self financed','ST'].value for time in model.set_time)),'kWh')

print('Max capacity ST:',round(model.max_capacity_ST.value))
print('Max capacity PV:',round(model.max_capacity_PV.value))
print('min capacity ST:',round(model.min_capacity_ST_contractor.value))

