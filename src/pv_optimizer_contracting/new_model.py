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
(set_time,set_finance_options,set_technologies,set_default_technologies,set_costs,set_costs_default,set_demand,\
    set_PV2,set_ST2,set_elec_grid2,set_Car2,set_Battery2,set_HP2)=read_set_data()
(dict_general_parameters)=read_general_data()
(annuity_factor)=calculate_annuity_factor()
(dict_cost_new,dict_cost_default)=read_cost_data()
(dict_demand)=read_demand_data()
(dict_max_demand,dict_max_demand_default) =read_max_demand()
(dict_irradiation,dict_temperature)=read_weather_data()
(dict_COP)=calculate_COP()
(dict_capacity_factor_PV,dict_temperature_factor_PV)=calculate_performance_PV()

# Sets
model.set_time = Set(initialize = set_time.keys(),doc='time in timesteps of 1h')
model.set_finance_options = Set(initialize = set_finance_options.keys(),doc='Elements of the model financed by self-investment OR by a contractor')
model.set_new_technologies = Set(initialize = set_technologies.keys(),doc='Technologies/Elements that can be financed e.g, PV, HP etc.')
model.set_default_technologies = Set(initialize = set_default_technologies.keys(),doc='Default elements that already exist e.g. electricity, gas, DH')
model.set_costs_new = Set(initialize = set_costs.keys(),doc='Types of costs for newly installed technologies e.g. investment,service,connection, fuel')
model.set_costs_default = Set(initialize = set_costs_default.keys(),doc='Types of costs for default technologies e.g. service,connection, fuel, feedin')
model.set_demand = Set(initialize = set_demand.keys(),doc='Demands that need to be fulfilled e.g. charging,electricity, hot water, heating')
model.set_PV2 = Set(initialize = set_PV2.keys(),doc='Elements that can be supplied by PV')
model.set_ST2 = Set(initialize = set_ST2.keys(),doc='Elements that can be supplied by ST')
model.set_elec_grid2 = Set(initialize = set_elec_grid2.keys(),doc='Elements that can be supplied by the electric grid')
model.set_Car2 = Set(initialize = set_Car2.keys(),doc='Elements that can be supplied by the battery of electric vehicles')
model.set_Battery2 = Set(initialize = set_Battery2.keys(),doc='Elements that can be supplied by the stationary battery')
model.set_HP2 = Set(initialize = set_HP2.keys(),doc='Elements that can be supplied by HP')


## Parameters
#General Parameters
model.annuity=Param(initialize = annuity_factor, mutable=False,doc='Annuity factor to convert investment costs in annual costs')
model.area_roof=Param(initialize = dict_general_parameters['Area Roof'],mutable=False,within=Any,doc='Area of the roof [m2], determines limit of PV and ST capacity')
model.capacity_density_PV=Param(initialize = dict_general_parameters['Area PV'],mutable=False,within=Any,doc='Capacity density of PV [kWp/m2]')
model.specific_DHW_demand = Param(initialize = dict_general_parameters['Specific DHW'],mutable=False,within=Any,doc='Demand of hot water per Person')
model.cop = Param(model.set_time, initialize = dict_COP,doc='Reduced COP per timestep')
model.powerflow_max_battery= Param(initialize = dict_general_parameters['Maximum Powerflow Battery'], mutable=False,within=Any,doc='Maximum powerflow into and out of stationary battery')
model.powerflow_max_battery_car= Param(initialize = dict_general_parameters['Maximum Powerflow Battery Car'], mutable=False,within=Any,doc='Maximum powerflow into and out of car battery')
model.capacity_car= Param(initialize = dict_general_parameters['Capacity Battery Car'], mutable=False,within=Any,doc='Capacity battery of chosen car model')
model.efficiency_battery= Param(initialize = dict_general_parameters['Efficiency Battery'], mutable=False,within=Any,doc='Efficiency of stationary battery')
model.efficiency_battery_car= Param(initialize = dict_general_parameters['Efficiency Battery Car'], mutable=False,within=Any,doc='Efficiency of car battery')
model.efficiency_gas= Param(initialize =dict_general_parameters['Efficiency Gas Boiler'], mutable=False,within=Any,doc='Efficiency of decentralized gas boilers')
model.number_cars= Param(initialize = dict_general_parameters['Number of cars'], mutable=False,within=Any,doc='Number of charging stations (or cars) chosen')
model.number_households= Param(initialize = dict_general_parameters['Number of cars'], mutable=False,within=Any,doc='Number of households')
model.simultaneity= Param(initialize = dict_general_parameters['Simultaneity factor'], mutable=False,within=Any,doc='Simultaneity factor for hot water usage')
model.cost_infrastructure_ST2DH= Param(initialize = dict_general_parameters['Investment ST to DH'], mutable=False,within=Any,doc='Additional investment if ST feed into DH')
model.bonus_shifting= Param(initialize = dict_general_parameters['Bonus shifting'], mutable=False,within=Any,doc='Price paid for shifting by contractor per kW')

#Cost Parameters
model.cost_new = Param(model.set_finance_options,model.set_new_technologies,model.set_costs_new, initialize = dict_cost_new,doc='Prices for initial investment')
model.cost_default = Param(model.set_default_technologies,model.set_costs_default, initialize = dict_cost_default,doc='Prices for initial investment')

#Demand Parameters
model.demand = Param(model.set_time,model.set_demand, initialize =dict_demand,doc='Demand per timestep per demand type e.g. charging,electricity, hot water, heating')
model.connection_capacity_default= Param(model.set_default_technologies, initialize =dict_max_demand_default,doc='Max demand = Connection capacity per default technology')


#Weather Parameter
model.irradiation = Param(model.set_time, initialize = dict_irradiation,doc='Irradiation on flat surface per timestep')
model.temperature = Param(model.set_time, initialize = dict_temperature,doc='Outside temperature per timestep')

#PV Performance
model.capacity_factor_PV = Param(model.set_time, initialize = dict_capacity_factor_PV,doc='kW electricity produced from PV per kWp installes per timestep')
model.temperature_factor_PV = Param(model.set_time, initialize = dict_capacity_factor_PV,doc='kW electricity produced from PV per kWp installes per timestep')




# model.capacity_factor = Param(model.time,model.options,initialize =dict_capacity_factor,
#                         doc='Maximum available electricity supply per unit of installed capacity, per option per timestep [kW/kWp]')
# model.max_capacity = Param(model.options,initialize =dict_max_capacity,
#                         doc='Maximum capacity that can be installed per option, for options with PV it is limited by the area of the roof [kW]')
# model.irradiation_full_PV_area=Param(model.time,initialize=dict_irradiation_full_PV_area,
#                         doc='Solar irradiation on the total possible PV area [kW]')
# model.weight = Param(initialize=float(8760) / (len(model.time)), doc='Pre-factor for variable costsfor an annual result')                        


#Vaiables
# model.capacity_PV=Var(set_finance_options, bounds=(0,2000),within=NonNegativeReals,doc='Installed PV capacity per financing option')
# model.area_ST=Var(set_finance_options, bounds=(0,2000),within=NonNegativeReals,doc='Installed ST area per financing option')
# model.capacity_HP=Var(set_finance_options, bounds=(0,2000),within=NonNegativeReals,doc='Installed HP capacity per financing option')
# model.reduction_demand_th=Var(set_finance_options, bounds=(0,2000),within=NonNegativeReals,doc='Percentual reduction of heat load per financing option')
# model.capacity_battery=Var(set_finance_options, bounds=(0,2000),within=NonNegativeReals,doc='Capacity of stationary battery per financing option')
# model.powerflow_battery=Var(set_finance_options, bounds=(0,2000),within=NonNegativeReals,doc='Powerflow of stationary battery per financing option')
# model.charging_stations=Var(set_finance_options, bounds=(0,2000),within=NonNegativeReals,doc='Number of charging stations per financing option')
model.capacity=Var(model.set_finance_options,model.set_new_technologies, bounds=(0,2000),within=NonNegativeReals,doc='Newly installed capacity per financing option per technology')
model.supply_default=Var(model.set_time,model.set_default_technologies, bounds=(0,2000),within=NonNegativeReals,doc='Supply per timestep per default technology')
model.supply_new=Var(model.set_time,model.set_finance_options,model.set_new_technologies, bounds=(0,2000),within=NonNegativeReals,doc='Supply per timestepnew per financing option per technology')
model.supply_from_PV=Var(model.set_time,model.set_finance_options,model.set_PV2, bounds=(0,2000),within=NonNegativeReals,doc='Supply from PV per timestep per financing option')    
model.supply_from_ST=Var(model.set_time,model.set_finance_options,model.set_ST2, bounds=(0,2000),within=NonNegativeReals,doc='Supply from ST per timestep per financing option')    
model.supply_from_elec_grid=Var(model.set_time,model.set_finance_options,model.set_elec_grid2 , bounds=(0,2000),within=NonNegativeReals,doc='Supply from electric grid per timestep per financing option')    
model.supply_from_Car=Var(model.set_time,model.set_finance_options,model.set_Car2, bounds=(0,2000),within=NonNegativeReals,doc='Supply from Car Battery per timestep per financing option')    
model.supply_from_battery=Var(model.set_time,model.set_finance_options,model.set_Battery2, bounds=(0,2000),within=NonNegativeReals,doc='Supply from stationary Battery per timestep per financing option')    
model.supply_from_HP=Var(model.set_time,model.set_finance_options,model.set_HP2, bounds=(0,2000),within=NonNegativeReals,doc='Supply from HP per timestep per financing option')    

model.demand_shift_total=Var(bounds=(0,2000),within=NonNegativeReals,doc='Total shift of demand in 1 year')


#Binary Variables
model.binary_default_technologies=Var(model.set_default_technologies, within=Binary,doc='Binary Variable becomes TRUE if technology is installed')
model.binary_new_technologies=Var(model.set_finance_options,model.set_new_technologies, within=Binary,doc='Binary Variable becomes TRUE if technology is installed')
model.binary_ST_DH=Var(within=Binary,doc='Binary Variable becomes TRUE if ST AND DH are installed, ST can feed into DH')



# model.supply = Var(model.time, model.options, within=NonNegativeReals,doc='Amount of electricity supplied, per option per timeperiod')

# model.delta_up=Var(model.time,bounds=(0,22),within =NonNegativeReals,doc='Demand shifted up [kW]')
# model.delta_down=Var(model.time, bounds=(0,22),within=NonNegativeReals,doc='Demand shifted down [kW]')
# model.shifted_demand=Var(model.time, within=NonNegativeReals,doc='Shifted Demand')
#var_cost=Var(model.time, model.options, within=NonNegativeReals)

#Objective
# def cost_rule(model):
#     return sum(model.supply[time, option] * model.price_elec[option] * model.weight for time in model.time for option in model.options) + \
#     sum(model.capacity[option] * model.price_invest[option] * model.annuity.value for option in model.options) 
# model.obj = Objective(rule = cost_rule, sense=minimize, doc='minimize total costs')

#Objective

# 
def cost_rule(model):
    investment_costs_total=sum(model.annuity*model.capacity[finance_options, technologies] * model.cost_new [finance_options, technologies,'Investment Price'] for finance_options in model.set_finance_options for technologies in model.set_new_technologies) +\
        model.binary_ST_DH*model.cost_infrastructure_ST2DH

    service_costs_total=sum(model.binary_default_technologies[default_technologies]*model.cost_default[default_technologies,'Service Cost'] \
        for default_technologies in model.set_default_technologies) + \
        sum(model.binary_new_technologies[finance_options,new_technologies]*model.cost_new[finance_options,new_technologies,'Service Cost'] \
        for finance_options in model.set_finance_options for new_technologies in model.set_new_technologies)

    connection_costs_total=sum(model.binary_default_technologies[default_technologies]*model.connection_capacity_default[default_technologies] *\
        model.cost_default[default_technologies,'Connection Price'] for default_technologies in model.set_default_technologies) +\
        sum(model.capacity[finance_options, technologies] * model.cost_new [finance_options, technologies,'Connection Price'] \
        for finance_options in model.set_finance_options for technologies in model.set_new_technologies)

    variable_cost_total= sum(model.supply_default[time,default_technologies]*model.cost_default[default_technologies,'Fuel Price'] \
        for default_technologies in model.set_default_technologies for time in model.set_time) +\
        sum(model.supply_from_PV[time,'Contractor','Household']*model.cost_new ['Contractor','PV','Fuel Price'] for time in model.set_time) +\
        sum(model.supply_from_PV[time,'Contractor','Car']*model.cost_new ['Contractor','Charging Station','Fuel Price'] for time in model.set_time) +\
        sum(model.supply_from_battery[time,'Contractor','Car']*model.cost_new ['Contractor','Charging Station','Fuel Price'] for time in model.set_time) +\
        sum(model.supply_from_HP[time,'Contractor','Household']*model.cost_new ['Contractor','HP','Fuel Price'] for time in model.set_time) +\
        sum(model.supply_from_ST[time,'Contractor','Household']*model.cost_new ['Contractor','ST','Fuel Price'] for time in model.set_time) 
      

    revenue= model.demand_shift_total*model.bonus_shifting+ \
        sum(model.supply_from_PV[time,finance_options,'Grid']*model.cost_default['Electricity','Feedin Price'] for time in model.set_time for finance_options in model.set_finance_options) +\
        sum(model.supply_from_ST[time,finance_options,'DH']*model.cost_default['DH','Feedin Price'] for time in model.set_time for finance_options in model.set_finance_options) 
          

    total_costs=investment_costs_total+service_costs_total+connection_costs_total+variable_cost_total-revenue
    return total_costs

model.obj = Objective(rule = cost_rule, sense=minimize, doc='minimize total costs')


def PV_supply_rule(model,time,finance_options):
    return model.supply_new[time,finance_options,'PV']==(model.capacity[finance_options,'PV']*model.capacity_factor_PV[time]) \
        -(model.capacity[finance_options,'PV']*model.capacity_factor_PV[time])*model.temperature_factor_PV[time]
   
model.c1 = Constraint(model.set_time,model.set_finance_options, rule= PV_supply_rule, \
    doc='Produces electricity from PV equals installed capacity lowered by capacity and temperature factors')
    
def from_PV_supply_rule(model,time,finance_options):
    return model.supply_new[time,finance_options,'PV']==sum(model.supply_from_PV[time,finance_options,PV2technologies] for PV2technologies in model.set_PV2)
model.c2 = Constraint(model.set_time,model.set_finance_options, rule= from_PV_supply_rule, \
    doc='Produces electricity from PV equals the electricity from PV to other elements/technologies')


opt = SolverFactory('glpk')
results=opt.solve(model)

instance = model.create_instance()
model.pprint()

status = results.solver.status
termination_condition = results.solver.termination_condition
print('termination_condition: ', termination_condition)
print('status: ', status)

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
