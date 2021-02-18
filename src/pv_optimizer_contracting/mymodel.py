from pyomo.environ import *
from pyomo.gdp import Disjunct, Disjunction
import pandas as pd
from input import read_data
from disjuncts import create_list_disjuncts

model = ConcreteModel()

# Loading all variables from input
set_time,set_options,dict_dem,dict_capacity_factor,dict_price_elec,dict_price_invest,param_annuity,param_area,param_specific_area_pv=read_data()


# Sets
model.time = Set(initialize = set_time.keys(),doc="time in timesteps of 1h")
model.options = Set(initialize = set_options.keys(),doc="grid only OR contractor OR pv")

# Parameters
model.annuity=Param(initialize = param_annuity,mutable=False)
model.area=Param(initialize = param_area,mutable=False,within=Any)
model.specific_area_pv=Param(initialize = param_specific_area_pv,mutable=False,within=Any)
model.demand = Param(model.time, initialize = dict_dem)
model.price_elec = Param(model.options, initialize = dict_price_elec, doc="Prices for electricity, per option per timestep")
model.price_invest = Param(model.options, initialize = dict_price_invest,doc="Prices for initial investment, per option")
model.capacity_factor = Param(model.time,model.options,initialize =dict_capacity_factor,doc="Maximum available electricity supply per unit of installed capacity, per option at each timeperiod [kW/kWp]")



# #Vaiable
model.supply = Var(model.time, model.options, within=NonNegativeReals,doc='Amount of electricity supplied, per option and timeperiod')
model.capacity=Var(model.options, within=NonNegativeReals,doc='Total installed capacity of per option')
#model.area_pv=Var()


##Disjunction
list_disjuncts=create_list_disjuncts(model=model)
model.supply_disjunction=Disjunction(expr=list_disjuncts)

def cost_rule(model):
    return sum(model.supply[time, option] * model.price_elec[option] + model.capacity[option] * model.price_invest[option]*model.annuity
    for time in model.time 
    for option in model.options)


model.obj = Objective(rule = cost_rule, sense=minimize, doc='minimize costs')

## Constraints
def demand_rule(model,time,option):
    return sum(model.supply[time,option] for option in model.options for time in model.time) == sum(model.demand[time] for time in model.time)

model.c1 = Constraint(model.time,model.options,rule=demand_rule, doc='Supply equals demand within the sum of all time steps')

def production_rule(model,time,option):
    return model.capacity_factor[time,option]* model.capacity[option] >= model.supply[time,option]
model.c2 = Constraint(model.time,model.options,rule=production_rule, doc='Supply is smaller or equal to max. production')

# def pv_rule(model,time):
#     return (model.supply[time,'PV'])*model.specific_area_pv <= model.area
# model.c7 = Constraint(model.time,rule=pv_rule, doc='PV area limited to area on roof')

# def cap_rule(model,time,option):
#     return model.supply[time,option] <= model.capacity_factor[time,option]
# model.c8 = Constraint(model.time,model.options, rule=cap_rule, doc='Supply within capacities')




## only for PV

# def production_rule(model,time,option):
#     return sum(model.supply[time,option]<= model.capacity_factor[time,option]*model.area_pv)

# model.c7 = Constraint(model.time,model.options,rule=demand_rule, doc='Supply is smaller or equal to max. production (irradition x area)')

# def pv_rule(model):
#     return model.area_pv<= model.area

# model.c8 = Constraint(model.time,rule=pv_rule, doc='Area of PV is smaller than roof area')

# def cap_rule(model,time,option):
#     return (model.area_pv/model.specific_area_pv) == model.capacity['PV']
# model.c9 = Constraint(model.time,model.options, rule=cap_rule, doc='PV installed equals installed capacity')


## Generalized



# def cap_PV_rule(model,option):
#     return (model.area/model.specific_area_pv) >= model.capacity['PV']
# model.c9 = Constraint(model.options, rule=cap_PV_rule, doc='PV capacity is linited by roof area')

# def cap_PV_contracting_rule(model,option):
#     return (model.area/model.specific_area_pv) >= model.capacity['Pv_Contractor']
# model.c10 = Constraint(model.options, rule=cap_PV_contracting_rule, doc='PV capacity is limited by roof area')


#Solve Optimization
opt = SolverFactory('glpk')
results=opt.solve(model)

# print('Grid_Only:', (model.supply[t, 'Grid_Only'] for t in model.time))
# print('Pv_Contractor:', (model.supply[t,'Pv_Contractor'].value for t in model.time))
# print('PV:', (model.supply[t,'PV'].value for t in model.time))
print('Total Cost:',model.obj())
print('Grid_Only in hour 1:',model.supply[1,'Grid_Only'].value)
print('Grid_Only in hour 2:',model.supply[2,'Grid_Only'].value)
print('PV in hour 1:', model.supply[1,'PV'].value)
print('PV in hour 2:', model.supply[2,'PV'].value)
print('Pv_Contractor in hour 1:',model.supply[1,'Pv_Contractor'].value)
print('Pv_Contractor in hour 2:',model.supply[2,'Pv_Contractor'].value)
print('Capacity PV',model.capacity['PV'].value)
print('Capacity Pv_Contractor',model.capacity['Pv_Contractor'].value)
print('Capacity Grid',model.capacity['Grid_Only'].value)

# instance = model.create_instance()

# model.pprint()
status = results.solver.status
termination_condition = results.solver.termination_condition
print('termination_condition: ', termination_condition)
print('status: ', status)
