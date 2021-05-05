from datetime import datetime
from pprint import pprint

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from pyomo.environ import *
from pyomo.gdp import Disjunct, Disjunction

from disjunction import *
from input_new_model import *

model = ConcreteModel()

# Loading all variables from input data
(set_time,set_finance_options,set_technologies,set_default_technologies,set_costs,set_costs_default,set_demand)=read_set_data()
(dict_general_parameters)=read_general_data()
(annuity_factor)=calculate_annuity_factor()
(dict_cost_new,dict_cost_default)=read_cost_data()
(dict_demand)=read_demand_data()
(dict_irradiation,dict_temperature)=read_weather_data()
(dict_COP)=calculate_COP()

# Sets
model.time = Set(initialize = set_time.keys(),doc='time in timesteps of 1h')
model.finance_options = Set(initialize = set_finance_options.keys(),doc='Elements of the model financed by self-investment OR by a contractor')
model.technologies = Set(initialize = set_technologies.keys(),doc='Technologies/Elements that can be financed e.g, PV, HP etc.')
model.default_technologies = Set(initialize = set_default_technologies.keys(),doc='Default elements that already exist e.g. electricity, gas, DH')
model.costs_new = Set(initialize = set_costs.keys(),doc='Types of costs for newly installed technologies e.g. investment,service,connection, fuel')
model.costs_default = Set(initialize = set_costs_default.keys(),doc='Types of costs for default technologies e.g. service,connection, fuel, feedin')
model.demand = Set(initialize = set_demand.keys(),doc='Demands that need to be fulfilled e.g. charging,electricity, hot water, heating')

## Parameters
#General Parameters
model.annuity=Param(initialize = annuity_factor, mutable=False,doc='Annuity factor to convert investment costs in annual costs')
model.area_roof=Param(initialize = dict_general_parameters['Area Roof'],mutable=False,within=Any,doc='Area of the roof [m2], determines limit of PV and ST capacity')
model.capacity_density_pv=Param(initialize = dict_general_parameters['Area PV'],mutable=False,within=Any,doc='Capacity density of PV [kWp/m2]')
model.specific_DHW_demand = Param(initialize = dict_general_parameters['Specific DHW'],mutable=False,within=Any,doc='Demand of hot water per Person')
model.cop = Param(model.time, initialize = dict_COP,doc='Reduced COP per timestep')
model.powerflow_max_battery= Param(initialize = dict_general_parameters['Maximum Powerflow Battery'], mutable=False,within=Any,doc='Maximum powerflow into and out of stationary battery')
model.powerflow_max_battery_car= Param(initialize = dict_general_parameters['Maximum Powerflow Battery Car'], mutable=False,within=Any,doc='Maximum powerflow into and out of car battery')
model.capacity_car= Param(initialize = dict_general_parameters['Capacity Battery Car'], mutable=False,within=Any,doc='Capacity battery of chosen car model')
model.efficiency_battery= Param(initialize = dict_general_parameters['Efficiency Battery'], mutable=False,within=Any,doc='Efficiency of stationary battery')
model.efficiency_battery_car= Param(initialize = dict_general_parameters['Efficiency Battery Car'], mutable=False,within=Any,doc='Efficiency of car battery')
model.efficiency_gas= Param(initialize =dict_general_parameters['Efficiency Gas Boiler'], mutable=False,within=Any,doc='Efficiency of decentralized gas boilers')
model.number_cars= Param(initialize = dict_general_parameters['Number of cars'], mutable=False,within=Any,doc='Number of charging stations (or cars) chosen')
model.number_households= Param(initialize = dict_general_parameters['Number of cars'], mutable=False,within=Any,doc='Number of households')
model.simultaneity= Param(initialize = dict_general_parameters['Simultaneity factor'], mutable=False,within=Any,doc='Simultaneity factor for hot water usage')

#Cost Parameters
model.cost_new = Param(model.finance_options,model.technologies,model.costs_new, initialize = dict_cost_new,doc='Prices for initial investment')
model.cost_default = Param(model.finance_options,model.technologies,model.costs_default, initialize = dict_cost_default,doc='Prices for initial investment')

# model.cost_service = Param(model.technologies, initialize = dict_cost_service,doc='Annual service and maintenance Costs (lump-sum costs)')
# model.price_connection = Param(model.technologies, initialize = dict_price_connection,doc='Annual connection price per kW')
# model.price_fuel = Param(model.technologies, initialize = dict_price_fuel,doc='Fuel price per kWh')
# model.price_invest_contractor = Param(model.technologies, initialize = dict_price_invest_contractor,doc='Prices for initial investment by contractor')
# model.cost_service_contractor = Param(model.technologies, initialize = dict_cost_service_contractor,doc='Annual service and maintenance Costs (lump-sum costs) by contractor'')
# model.price_connection_contractor = Param(model.technologies, initialize = dict_price_connection_contractor,doc='Annual connection price per kW by contractor'')
# model.price_fuel_contractor = Param(model.technologies, initialize = dict_price_fuel_contractor,doc='Fuel price per kWh by contractor'')
# model.price_invest_default = Param(model.technologies, initialize = dict_price_invest_default,doc='Prices for initial investment for default elements')
# model.cost_service_default = Param(model.technologies, initialize = dict_cost_service_default,doc='Annual service and maintenance Costs (lump-sum costs) for default elements')
# model.price_connection_default = Param(model.technologies, initialize = dict_price_connection_default,doc='Annual connection price per kW for default elements')
# model.price_fuel_default = Param(model.technologies, initialize = dict_price_fuel_default,doc='Fuel price per kWh for default elements')
# model.price_feedin_default = Param(model.technologies, initialize = dict_price_feedin_default,doc='Feedin priced for default elements')

#Demand Parameters




# model.demand = Param(model.time, initialize = dict_dem,doc='Demand per timestep')
# model.price_elec = Param(model.options, initialize = dict_price_elec, doc='Prices for electricity, per option per timestep')
# )
# model.capacity_factor = Param(model.time,model.options,initialize =dict_capacity_factor,
#                         doc='Maximum available electricity supply per unit of installed capacity, per option per timestep [kW/kWp]')
# model.max_capacity = Param(model.options,initialize =dict_max_capacity,
#                         doc='Maximum capacity that can be installed per option, for options with PV it is limited by the area of the roof [kW]')
# model.irradiation_full_pv_area=Param(model.time,initialize=dict_irradiation_full_pv_area,
#                         doc='Solar irradiation on the total possible PV area [kW]')
# model.weight = Param(initialize=float(8760) / (len(model.time)), doc='Pre-factor for variable costsfor an annual result')                        


#Vaiables
# model.supply = Var(model.time, model.options, within=NonNegativeReals,doc='Amount of electricity supplied, per option per timeperiod')
# model.capacity=Var(model.options, bounds=(0,2000),within=NonNegativeReals,doc='Total installed capacity per option')
# model.delta_up=Var(model.time,bounds=(0,22),within =NonNegativeReals,doc='Demand shifted up [kW]')
# model.delta_down=Var(model.time, bounds=(0,22),within=NonNegativeReals,doc='Demand shifted down [kW]')
# model.shifted_demand=Var(model.time, within=NonNegativeReals,doc='Shifted Demand')
#var_cost=Var(model.time, model.options, within=NonNegativeReals)

#Objective
# def cost_rule(model):
#     return sum(model.supply[time, option] * model.price_elec[option] * model.weight for time in model.time for option in model.options) + \
#     sum(model.capacity[option] * model.price_invest[option] * model.annuity.value for option in model.options) 
# model.obj = Objective(rule = cost_rule, sense=minimize, doc='minimize total costs')




# def cost_rule(model):
#     return sum(var_cost*365+ model.capacity[option] * model.price_invest[option]*model.annuity
#     for time in model.time 
#     for option in model.options)
# model.obj = Objective(rule = cost_rule, sense=minimize, doc='minimize total costs')

# def var_cost_rule(model):
#     return sum(model.supply[time, option] * model.price_elec[option]
#     for time in model.time 
#     for option in model.options)==var_cost
# model.c0 = Constraint(model.time,model.options,rule = var_cost_rule,  doc='minimize total costs')


## Constraints
# def demand_rule(model,time,option):
#     return sum(model.supply[time,option] for option in model.options for time in model.time) == sum(model.demand[time] for time in model.time)
# model.c1 = Constraint(model.time,model.options,rule=demand_rule, doc='Supply equals demand within sum of all time steps')

# def demand_rule(model,time,option):
#     return sum(model.supply[time,option] for option in model.options) == model.shifted_demand[time]
# model.c1 = Constraint(model.time,model.options,rule=demand_rule, doc='Supply equals demand at every timestep with DSM')

# ################
# def demand_rule_1(model,time,option):
#     return sum(model.supply[time,option] for option in model.options) == model.demand[time]+model.delta_up[time]-model.delta_down[time]
# model.c1 = Constraint(model.time,model.options,rule=demand_rule_1, doc='Supply equals demand at every timestep with DSM')

# def demand_rule_2(model,time,option):
#     return sum(model.supply[time,option] for option in model.options) == model.demand[time]-model.delta_down[time]
# model.c11 = Constraint(model.time,model.options,rule=demand_rule_2, doc='Supply equals demand at every timestep with DSM')

# ################

# def demand_rule(model,time,option):
#     return sum(model.supply[time,option] for option in model.options) == model.demand[time]
# model.c1 = Constraint(model.time,model.options,rule=demand_rule, doc='Supply equals demand at every timestep')

# def demand_rule(model,time,option):
#     return sum(model.supply[time,option] for option in model.options) == model.demand[time] 
# model.c1 = Constraint(model.charging_time,model.options,rule=demand_rule, doc='Supply equals demand at charging times')

# def production_rule(model,time,option):
#     return model.capacity_factor[time,option]* model.capacity[option] >= model.supply[time,option]
# model.c2 = Constraint(model.time,model.options,rule=production_rule, doc='Supply is smaller or equal to max. production')

# def max_capacity_rule(model,option):
#     return model.capacity[option] <= model.max_capacity[option]
# model.c3 = Constraint(model.options,rule=max_capacity_rule, doc='Installed capacity is smaller or equal maximum capacity')

# def dsm_rule(model,time):
#     return sum(model.delta_up[time] for time in model.time)==sum(model.delta_down[time] for time in model.time)
# model.c4 = Constraint(model.time,rule=dsm_rule, doc='Sum of upshifts equals downshifts')   

# def shifted_demand_rule(model,time):
#     return model.shifted_demand[time]==model.demand[time]+model.delta_up[time]-model.delta_down[time]
# model.c5 = Constraint(model.time,rule=shifted_demand_rule, doc='Shifted demand defined by upshifts and downshifts') 

# def shifted_demand_equal_original_demand_rule(model,time):
#     return sum(model.shifted_demand[time]for time in model.time)==sum(model.demand[time]for time in model.time)
# model.c6 = Constraint(model.time,rule=shifted_demand_equal_original_demand_rule, doc='Shifted demand defined by upshifts and downshifts') 

 
# Disjunction (to encure that only ONE option is chosen)
# create_disjunction(model=model)
# model.option_binary_var=create_boolean_var(model=model) 
# TransformationFactory('core.logical_to_linear').apply_to(model)
# TransformationFactory('gdp.bigm').apply_to(model)#

##Solve Optimization

#instance = model.create_instance()
opt = SolverFactory('glpk')
results=opt.solve(model)
model.pprint()
# update_boolean_vars_from_binary(model=model) #update binary variable after solving 
# model.option_binary_var.display() #see which option is chosen
#
# print('Total Cost:',round(model.obj()), 'Total annual costs')
#print('Supply Grid_Only in hour 1:',model.supply['1899-12-31 00:00:00','Grid_Only'].value,'kW')
# print('Supply Grid_Only in hour 1:',model.supply[Timestamp('2021-01-01 21:00:00'), 'Grid_Only'],'kW')
#print('Supply Grid_Only in hour 1:',model.supply[1,'Grid_Only'].value,'kW')
# print('Supply Grid_Only in hour 2:',model.supply[2,'Grid_Only'].value,'kW')
# print('Supply PV in hour 1:', model.supply[1,'PV'].value,'kW')
# print('Supply PV in hour 2:', model.supply[2,'PV'].value,'kW')
# print('Supply Pv_Contractor in hour 1:',model.supply[1,'Pv_Contractor'].value,'kW')
# print('Supply Pv_Contractor in hour 2:',model.supply[2,'Pv_Contractor'].value,'kW')
# print('Capacity Grid',round(model.capacity['Grid_Only'].value),'kW')
# print('Capacity PV',round(model.capacity['PV'].value),'kW')
# print('Capacity Pv_Contractor',round(model.capacity['Pv_Contractor'].value),'kW')

# print('Sum supply Grid_Only',sum(model.supply[t,'Grid_Only'].value for t in model.time),'kWh')
# print('Sum supply PV',round(sum(model.supply[t,'PV'].value for t in model.time)),'kWh')
# print('Sum supply Pv_Contractor',round(sum(model.supply[t,'Pv_Contractor'].value for t in model.time)),'kWh')
#print('Sum supply Pv_Contractor',sum(model.supply[t].value for t in model.time)
# print('Supply Grid_Only in hour 1:',model.supply[1,'Grid_Only'].value,'kW')
# print('Supply Grid_Only in hour 1:',model.supply[2,'Grid_Only'].value,'kW')
# print('Supply Grid_Only in hour 1:',model.supply[3,'Grid_Only'].value,'kW')
# print('Supply Grid_Only in hour 1:',model.supply[4,'Grid_Only'].value,'kW')
# print('Supply Grid_Only in hour 1:',model.supply[5,'Grid_Only'].value,'kW')
# print('Supply Grid_Only in hour 1:',model.supply[6,'Grid_Only'].value,'kW')
# print('Supply Grid_Only in hour 1:',model.supply[7,'Grid_Only'].value,'kW')
# print('Supply Grid_Only in hour 1:',model.supply[8,'Grid_Only'].value,'kW')
# print('Supply Grid_Only in hour 1:',model.supply[9,'Grid_Only'].value,'kW')
# print('Supply Grid_Only in hour 1:',model.supply[10,'Grid_Only'].value,'kW')
# print('Supply Grid_Only in hour 1:',model.supply[11,'Grid_Only'].value,'kW')
# print('Supply Grid_Only in hour 1:',model.supply[12,'Grid_Only'].value,'kW')
# print('Supply Grid_Only in hour 1:',model.supply[13,'Grid_Only'].value,'kW')
# print('Supply Grid_Only in hour 1:',model.supply[14,'Grid_Only'].value,'kW')
# print('Supply Grid_Only in hour 1:',model.supply[15,'Grid_Only'].value,'kW')
# print('Supply Grid_Only in hour 1:',model.supply[16,'Grid_Only'].value,'kW')
# print('Supply Grid_Only in hour 1:',model.supply[17,'Grid_Only'].value,'kW')
# print('Supply Grid_Only in hour 1:',model.supply[18,'Grid_Only'].value,'kW')
# print('Supply Grid_Only in hour 1:',model.supply[19,'Grid_Only'].value,'kW')
# print('Supply Grid_Only in hour 1:',model.supply[20,'Grid_Only'].value,'kW')
# print('Supply Grid_Only in hour 1:',model.supply[21,'Grid_Only'].value,'kW')
# print('Supply Grid_Only in hour 1:',model.supply[22,'Grid_Only'].value,'kW')
# print('Supply Grid_Only in hour 1:',model.supply[23,'Grid_Only'].value,'kW')
# print('Supply Grid_Only in hour 1:',model.supply[24,'Grid_Only'].value,'kW')
# print('Supply Grid_Only in hour 1:', sum(model.shifted_demand[t].value for t in model.time),'kW')

# print('Sum shifted demand:', round(sum(model.shifted_demand[t].value for t in model.time)),'kWh')
# print('Sum original demand:', round(sum(model.demand[t] for t in model.time)),'kWh')
# print('Model weight:', model.weight.value)
# # instance = model.create_instance()
# # model.pprint()

# status = results.solver.status
# termination_condition = results.solver.termination_condition
# print('termination_condition: ', termination_condition)
# print('status: ', status)


