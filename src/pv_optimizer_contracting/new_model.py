from pyomo.environ import *
from pyomo.gdp import Disjunct, Disjunction
import pandas as pd
from input import *
from disjunction import *
import matplotlib
import matplotlib.pyplot as plt
from datetime import datetime
from pprint import pprint

model = ConcreteModel()

# Loading all variables from input data
(set_time,set_options,dict_dem,dict_irradiation_full_pv_area,dict_capacity_factor,dict_max_capacity,
dict_price_elec,dict_price_invest,param_annuity,param_area_roof,param_specific_area_pv)=read_data()
set_charging_time=define_charging_time()

# Sets
model.time = Set(initialize = set_time.keys(),doc='time in timesteps of 1h')
model.charging_time = Set(initialize = set_charging_time.keys(),doc='Charging time (after 4pm) in timesteps of 1h')
model.options = Set(initialize = set_options.keys(),doc='Elements of the model financed by self-investment OR by a contractor')

# Parameters
model.annuity=Param(initialize = param_annuity,mutable=False,doc='Annuity factor to convert investment costs in annual costs')
model.area_roof=Param(initialize = param_area_roof,mutable=False,within=Any,doc='Area of the roof [m2], determines limit of PV capacity')
model.specific_area_pv=Param(initialize = param_specific_area_pv,mutable=False,within=Any,doc='Capacity intensity of PV [kWp/m2]')
model.demand = Param(model.time, initialize = dict_dem,doc='Demand per timestep')
model.price_elec = Param(model.options, initialize = dict_price_elec, doc='Prices for electricity, per option per timestep')
model.price_invest = Param(model.options, initialize = dict_price_invest,doc='Prices for initial investment, per option')
model.capacity_factor = Param(model.time,model.options,initialize =dict_capacity_factor,
                        doc='Maximum available electricity supply per unit of installed capacity, per option per timestep [kW/kWp]')
model.max_capacity = Param(model.options,initialize =dict_max_capacity,
                        doc='Maximum capacity that can be installed per option, for options with PV it is limited by the area of the roof [kW]')
model.irradiation_full_pv_area=Param(model.time,initialize=dict_irradiation_full_pv_area,
                        doc='Solar irradiation on the total possible PV area [kW]')
model.weight = Param(initialize=float(8760) / (len(model.time)), doc='Pre-factor for variable costsfor an annual result')                        


#Vaiables
model.supply = Var(model.time, model.options, within=NonNegativeReals,doc='Amount of electricity supplied, per option per timeperiod')
model.capacity=Var(model.options, bounds=(0,2000),within=NonNegativeReals,doc='Total installed capacity per option')
model.delta_up=Var(model.time,bounds=(0,22),within =NonNegativeReals,doc='Demand shifted up [kW]')
model.delta_down=Var(model.time, bounds=(0,22),within=NonNegativeReals,doc='Demand shifted down [kW]')
model.shifted_demand=Var(model.time, within=NonNegativeReals,doc='Shifted Demand')
#var_cost=Var(model.time, model.options, within=NonNegativeReals)

##Objective
def cost_rule(model):
    return sum(model.supply[time, option] * model.price_elec[option] * model.weight for time in model.time for option in model.options) + \
    sum(model.capacity[option] * model.price_invest[option] * model.annuity.value for option in model.options) 
model.obj = Objective(rule = cost_rule, sense=minimize, doc='minimize total costs')




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

def demand_rule(model,time,option):
    return sum(model.supply[time,option] for option in model.options) == model.shifted_demand[time]
model.c1 = Constraint(model.time,model.options,rule=demand_rule, doc='Supply equals demand at every timestep with DSM')

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

def production_rule(model,time,option):
    return model.capacity_factor[time,option]* model.capacity[option] >= model.supply[time,option]
model.c2 = Constraint(model.time,model.options,rule=production_rule, doc='Supply is smaller or equal to max. production')

def max_capacity_rule(model,option):
    return model.capacity[option] <= model.max_capacity[option]
model.c3 = Constraint(model.options,rule=max_capacity_rule, doc='Installed capacity is smaller or equal maximum capacity')

def dsm_rule(model,time):
    return sum(model.delta_up[time] for time in model.time)==sum(model.delta_down[time] for time in model.time)
model.c4 = Constraint(model.time,rule=dsm_rule, doc='Sum of upshifts equals downshifts')   

def shifted_demand_rule(model,time):
    return model.shifted_demand[time]==model.demand[time]+model.delta_up[time]-model.delta_down[time]
model.c5 = Constraint(model.time,rule=shifted_demand_rule, doc='Shifted demand defined by upshifts and downshifts') 

def shifted_demand_equal_original_demand_rule(model,time):
    return sum(model.shifted_demand[time]for time in model.time)==sum(model.demand[time]for time in model.time)
model.c6 = Constraint(model.time,rule=shifted_demand_equal_original_demand_rule, doc='Shifted demand defined by upshifts and downshifts') 

 
# Disjunction (to encure that only ONE option is chosen)
create_disjunction(model=model)
model.option_binary_var=create_boolean_var(model=model) 
TransformationFactory('core.logical_to_linear').apply_to(model)
TransformationFactory('gdp.bigm').apply_to(model)#

##Solve Optimization

#instance = model.create_instance()
opt = SolverFactory('glpk')
results=opt.solve(model)
# model.pprint()
update_boolean_vars_from_binary(model=model) #update binary variable after solving 
model.option_binary_var.display() #see which option is chosen
#
print('Total Cost:',round(model.obj()), 'Total annual costs')
#print('Supply Grid_Only in hour 1:',model.supply['1899-12-31 00:00:00','Grid_Only'].value,'kW')
# print('Supply Grid_Only in hour 1:',model.supply[Timestamp('2021-01-01 21:00:00'), 'Grid_Only'],'kW')
#print('Supply Grid_Only in hour 1:',model.supply[1,'Grid_Only'].value,'kW')
# print('Supply Grid_Only in hour 2:',model.supply[2,'Grid_Only'].value,'kW')
# print('Supply PV in hour 1:', model.supply[1,'PV'].value,'kW')
# print('Supply PV in hour 2:', model.supply[2,'PV'].value,'kW')
# print('Supply Pv_Contractor in hour 1:',model.supply[1,'Pv_Contractor'].value,'kW')
# print('Supply Pv_Contractor in hour 2:',model.supply[2,'Pv_Contractor'].value,'kW')
print('Capacity Grid',round(model.capacity['Grid_Only'].value),'kW')
print('Capacity PV',round(model.capacity['PV'].value),'kW')
print('Capacity Pv_Contractor',round(model.capacity['Pv_Contractor'].value),'kW')

print('Sum supply Grid_Only',sum(model.supply[t,'Grid_Only'].value for t in model.time),'kWh')
print('Sum supply PV',round(sum(model.supply[t,'PV'].value for t in model.time)),'kWh')
print('Sum supply Pv_Contractor',round(sum(model.supply[t,'Pv_Contractor'].value for t in model.time)),'kWh')
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

print('Sum shifted demand:', round(sum(model.shifted_demand[t].value for t in model.time)),'kWh')
print('Sum original demand:', round(sum(model.demand[t] for t in model.time)),'kWh')
print('Model weight:', model.weight.value)
# instance = model.create_instance()
# model.pprint()

status = results.solver.status
termination_condition = results.solver.termination_condition
print('termination_condition: ', termination_condition)
print('status: ', status)


