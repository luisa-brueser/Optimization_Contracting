from pyomo.environ import *
from pyomo.gdp import Disjunct, Disjunction
import pandas as pd
from input import *
from disjunction import *
import matplotlib
import matplotlib.pyplot as plt
from datetime import datetime


model = ConcreteModel()



# Loading all variables from input data
(set_time,set_options,dict_dem,dict_irradiation_full_pv_area,dict_capacity_factor,dict_max_capacity,
dict_price_elec,dict_price_invest,param_annuity,param_area_roof,param_specific_area_pv)=read_data()
set_charging_time=define_charging_time()

# Sets
model.time = Set(initialize = set_time.keys(),doc='time in timesteps of 1h')
model.charging_time = Set(initialize = set_charging_time.keys(),doc='Charging time (after 4pm) in timesteps of 1h')
model.options = Set(initialize = set_options.keys(),doc='Supply by grid only or contractor financed PV or PV')

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

#Vaiables
model.supply = Var(model.time, model.options, within=NonNegativeReals,doc='Amount of electricity supplied, per option per timeperiod')
model.capacity=Var(model.options, bounds=(0,2000),within=NonNegativeReals,doc='Total installed capacity per option')

#Objective
def cost_rule(model):
    return sum(model.supply[time, option] * model.price_elec[option] + model.capacity[option] * model.price_invest[option]*model.annuity
    for time in model.time 
    for option in model.options)
model.obj = Objective(rule = cost_rule, sense=minimize, doc='minimize total costs')

## Constraints
# def demand_rule(model,time,option):
#     return sum(model.supply[time,option] for option in model.options for time in model.time) == sum(model.demand[time] for time in model.time)
# model.c1 = Constraint(model.time,model.options,rule=demand_rule, doc='Supply equals demand within sum of all time steps')

# def demand_rule(model,time,option):
#     return sum(model.supply[time,option] for option in model.options) == model.demand[time] 
# model.c1 = Constraint(model.time,model.options,rule=demand_rule, doc='Supply equals demand at every timestep')

def demand_rule(model,time,option):
    return sum(model.supply[time,option] for option in model.options) == model.demand[time] 
model.c1 = Constraint(model.charging_time,model.options,rule=demand_rule, doc='Supply equals demand at charging times')

def production_rule(model,time,option):
    return model.capacity_factor[time,option]* model.capacity[option] >= model.supply[time,option]
model.c2 = Constraint(model.time,model.options,rule=production_rule, doc='Supply is smaller or equal to max. production')

def max_capacity_rule(model,option):
    return model.capacity[option] <= model.max_capacity[option]
model.c3 = Constraint(model.options,rule=max_capacity_rule, doc='Installed capacity is smaller or equal maximum capacity')

# Disjunction (to encure that only ONE option is chosen)
create_disjuction(model=model)
model.option_binary_var=create_boolean_var(model=model) 
TransformationFactory('core.logical_to_linear').apply_to(model)
TransformationFactory('gdp.bigm').apply_to(model)#

##Solve Optimization
opt = SolverFactory('glpk')
results=opt.solve(model)
# model.pprint()
update_boolean_vars_from_binary(model=model) #update binary variable after solving 
model.option_binary_var.display() #see which option is chosen
#
print('Total Cost:',model.obj(), '€')
#print('Supply Grid_Only in hour 1:',model.supply['1899-12-31 00:00:00','Grid_Only'].value,'kW')
# print('Supply Grid_Only in hour 1:',model.supply[Timestamp('2021-01-01 21:00:00'), 'Grid_Only'],'kW')
print('Supply Grid_Only in hour 1:',model.supply[1,'Grid_Only'].value,'kW')
# print('Supply Grid_Only in hour 2:',model.supply[2,'Grid_Only'].value,'kW')
# print('Supply PV in hour 1:', model.supply[1,'PV'].value,'kW')
# print('Supply PV in hour 2:', model.supply[2,'PV'].value,'kW')
# print('Supply Pv_Contractor in hour 1:',model.supply[1,'Pv_Contractor'].value,'kW')
# print('Supply Pv_Contractor in hour 2:',model.supply[2,'Pv_Contractor'].value,'kW')
print('Capacity Grid',model.capacity['Grid_Only'].value,'kW')
print('Capacity PV',model.capacity['PV'].value,'kW')
print('Capacity Pv_Contractor',model.capacity['Pv_Contractor'].value,'kW')
print('Sum supply Grid_Only',sum(model.supply[t,'Grid_Only'].value for t in model.time))
print('Sum supply PV',sum(model.supply[t,'PV'].value for t in model.time))
print('Sum supply Pv_Contractor',sum(model.supply[t,'Pv_Contractor'].value for t in model.time))

print('Supply Grid_Only in hour 1:',model.supply[1,'Grid_Only'].value,'kW')
print('Supply Grid_Only in hour 1:',model.supply[2,'Grid_Only'].value,'kW')
print('Supply Grid_Only in hour 1:',model.supply[3,'Grid_Only'].value,'kW')
print('Supply Grid_Only in hour 1:',model.supply[4,'Grid_Only'].value,'kW')
print('Supply Grid_Only in hour 1:',model.supply[5,'Grid_Only'].value,'kW')
print('Supply Grid_Only in hour 1:',model.supply[6,'Grid_Only'].value,'kW')
print('Supply Grid_Only in hour 1:',model.supply[7,'Grid_Only'].value,'kW')
print('Supply Grid_Only in hour 1:',model.supply[8,'Grid_Only'].value,'kW')
print('Supply Grid_Only in hour 1:',model.supply[9,'Grid_Only'].value,'kW')
print('Supply Grid_Only in hour 1:',model.supply[10,'Grid_Only'].value,'kW')
print('Supply Grid_Only in hour 1:',model.supply[11,'Grid_Only'].value,'kW')
print('Supply Grid_Only in hour 1:',model.supply[12,'Grid_Only'].value,'kW')
print('Supply Grid_Only in hour 1:',model.supply[13,'Grid_Only'].value,'kW')
print('Supply Grid_Only in hour 1:',model.supply[14,'Grid_Only'].value,'kW')
print('Supply Grid_Only in hour 1:',model.supply[15,'Grid_Only'].value,'kW')
print('Supply Grid_Only in hour 1:',model.supply[16,'Grid_Only'].value,'kW')
print('Supply Grid_Only in hour 1:',model.supply[17,'Grid_Only'].value,'kW')
print('Supply Grid_Only in hour 1:',model.supply[18,'Grid_Only'].value,'kW')
print('Supply Grid_Only in hour 1:',model.supply[19,'Grid_Only'].value,'kW')
print('Supply Grid_Only in hour 1:',model.supply[20,'Grid_Only'].value,'kW')
print('Supply Grid_Only in hour 1:',model.supply[21,'Grid_Only'].value,'kW')
print('Supply Grid_Only in hour 1:',model.supply[22,'Grid_Only'].value,'kW')
print('Supply Grid_Only in hour 1:',model.supply[23,'Grid_Only'].value,'kW')
print('Supply Grid_Only in hour 1:',model.supply[24,'Grid_Only'].value,'kW')



# instance = model.create_instance()
#model.pprint()

status = results.solver.status
termination_condition = results.solver.termination_condition
print('termination_condition: ', termination_condition)
print('status: ', status)


# fig, ax = plt.subplots()
# ax.plot(model.time,value(model.supply[t,'Grid_Only'] for t in model.time))
# plt.show()