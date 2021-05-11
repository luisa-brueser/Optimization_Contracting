# -*- coding: utf-8 -*-
import pandas as pd
from pathlib import Path
from datetime import datetime

input_file_path = Path(__file__).parent / 'data_input_new_model.xlsx'

# param_interest_rate= general_df.at[0,2]
# print('param_interest_rate: ', param_interest_rate)

def read_set_data():
    '''
    Reads input data from excel file (e.g. data_input.xlsx) via pandas dataframe, which can then be used as model inputs.
    '''

    set_df = pd.read_excel(io=input_file_path, sheet_name='Sets')
    set_time = dict.fromkeys(set_df['Time'].dropna(),0)
    set_finance_options= dict.fromkeys(set_df['Finance Options'].dropna(),0)
    set_technologies = dict.fromkeys(set_df['Elements'].dropna(),0)
    set_default_technologies = dict.fromkeys(set_df['Default Elements'].dropna(),0)
    set_costs = dict.fromkeys(set_df['Cost type'].dropna(),0)
    set_costs_default= dict.fromkeys(set_df['Cost type default'].dropna(),0)
    set_demand= dict.fromkeys(set_df['Demand'].dropna(),0)
    set_PV2= dict.fromkeys(set_df['PV to'].dropna(),0)
    set_ST2= dict.fromkeys(set_df['ST to'].dropna(),0)
    set_elec_grid2= dict.fromkeys(set_df['Electric Grid to'].dropna(),0)
    set_Car2= dict.fromkeys(set_df['Car to'].dropna(),0)
    set_Battery2= dict.fromkeys(set_df['Battery to'].dropna(),0)
    set_2Battery= dict.fromkeys(set_df['to Battery'].dropna(),0)
    set_HP2= dict.fromkeys(set_df['HP to'].dropna(),0)
    set_2HP= dict.fromkeys(set_df['to HP'].dropna(),0)
    return (set_time,set_finance_options,set_technologies,set_default_technologies,set_costs,set_costs_default,set_demand, \
        set_PV2,set_ST2,set_elec_grid2,set_Car2,set_Battery2,set_2Battery,set_HP2,set_2HP)


# (set_time,set_finance_options,set_technologies,set_default_technologies,set_costs,set_costs_default,set_demand, \
#         set_PV2,set_ST2,set_elec_grid2,set_Car2,set_Battery2,set_2Battery,set_HP2)=read_set_data()
# print('set_2Battery: ', set_2Battery)



def read_general_data():
    '''
    Reads input data from excel file (e.g. data_input.xlsx) via pandas dataframe, which can then be used as model inputs.
    '''

    general_df = pd.read_excel(io=input_file_path, sheet_name='General Data').drop('Abbreviation', axis=1).set_index('Parameter')
    dict_general_parameters=general_df['Value'].to_dict()

    annuity_factor=(((1+dict_general_parameters['Interest rate'])**dict_general_parameters['Depreciation time'])*dict_general_parameters['Interest rate'])/ \
    (((1+dict_general_parameters['Interest rate'])**dict_general_parameters['Depreciation time'])-1)

    return (dict_general_parameters)
# (dict_general_parameters)=read_general_data()
# print('dict_general_parameters: ', dict_general_parameters)

def calculate_annuity_factor():
    '''
    Reads input data from excel file (e.g. data_input.xlsx) via pandas dataframe, which can then be used as model inputs.
    '''
    (dict_general_parameters)=read_general_data()
    
    annuity_factor=(((1+dict_general_parameters['Interest rate'])**dict_general_parameters['Depreciation time'])*dict_general_parameters['Interest rate'])/ \
    (((1+dict_general_parameters['Interest rate'])**dict_general_parameters['Depreciation time'])-1)

    return(annuity_factor)


def read_cost_data():
    '''
    Reads input data from excel file (e.g. data_input.xlsx) via pandas dataframe, which can then be used as model inputs.
    '''
    (set_time,set_finance_options,set_technologies,set_default_technologies,set_costs,set_costs_default,set_demand, \
        set_PV2,set_ST2,set_elec_grid2,set_Car2,set_Battery2,set_2Battery,set_HP2,set_2HP)=read_set_data()

    cost_new_df = pd.read_excel(io=input_file_path, sheet_name='Costs new investments').dropna().set_index(['Finance Options','Elements'])._drop_axis('Unit',0,level=1)

    dict_cost_new = dict()
    for idx1 in set_finance_options :
        for idx2 in set_technologies :
            for idx3 in set_costs: 
                dict_cost_new [idx1, idx2, idx3] = cost_new_df.loc[(idx1,idx2),idx3]

    cost_default_df = pd.read_excel(io=input_file_path, sheet_name='Costs default system').dropna().set_index('Elements')._drop_axis('Unit',0)

    dict_cost_default = dict()
    for idx1 in set_default_technologies :
        for idx2 in set_costs_default :
            dict_cost_default[idx1, idx2] = cost_default_df.loc[idx1][idx2]

    return (dict_cost_new,dict_cost_default)

# (dict_cost_new,dict_cost_default)=read_cost_data()
# print('dict_cost_default: ', dict_cost_default)
# print('dict_cost_new: ', dict_cost_new)

# print('dict_cost_new: ', dict_cost_new['Investment Price'])
# dict_you_want = { 'Investment Price': dict_cost_new['Investment Price'] for your_key in your_keys }

# for [a,b,c],d in dict_cost_new.items():
#     print(c)

# new=dict(([a,b,c],d) for [a,b,c],d  in dict_cost_new.items() if c == 'Investment Price')
# print('new: ', new)

# new=dict_cost_new['Contractor', Elements, 'Connection Price'] for Elements in dict_cost_new.key()
# print('new: ', new)

# investment=dict()
# for key in dict_cost_new.keys():
#     if key == 'Investment Price'

#     print(key)


def read_demand_data():
    '''
    Reads input data from excel file (e.g. data_input.xlsx) via pandas dataframe, which can then be used as model inputs.
    '''
    (set_time,set_finance_options,set_technologies,set_default_technologies,set_costs,set_costs_default,set_demand, \
        set_PV2,set_ST2,set_elec_grid2,set_Car2,set_Battery2,set_2Battery,set_HP2,set_2HP)=read_set_data()

    demand_df = pd.read_excel(io=input_file_path, sheet_name='Demand').reset_index().dropna().set_index('Time')

    dict_demand = dict()
    for idx1 in set_time:
        for idx2 in set_demand:
            dict_demand[idx1, idx2] = demand_df.loc[idx1][idx2]

    return(dict_demand)

# dict_demand=read_demand_data()
# print('dict_demand: ', dict_demand)

def read_max_demand():
    '''
    Reads input data from excel file (e.g. data_input.xlsx) via pandas dataframe, which can then be used as model inputs.
    '''
    (set_time,set_finance_options,set_technologies,set_default_technologies,set_costs,set_costs_default,set_demand, \
        set_PV2,set_ST2,set_elec_grid2,set_Car2,set_Battery2,set_2Battery,set_HP2,set_2HP)=read_set_data()

    demand_df = pd.read_excel(io=input_file_path, sheet_name='Demand').reset_index().dropna().set_index('Time')
    
    dict_max_demand=dict()
    for idx1 in set_demand:
        max_value=demand_df[idx1].max()
        dict_max_demand[idx1]=max_value

    max_electric_demand=dict_max_demand['Car']+dict_max_demand['Electricity household']
    max_thermal_demand=dict_max_demand['DHW']+dict_max_demand['Heating']   

    dict_max_demand_default={'Electricity':max_electric_demand,'DH': max_thermal_demand, 'Gas': max_thermal_demand}
    
    return(dict_max_demand,dict_max_demand_default)    


(dict_max_demand,dict_max_demand_default) =read_max_demand()
print('dict_max_demand_default: ', dict_max_demand_default)




def read_weather_data():
    '''
    Reads input data from excel file (e.g. data_input.xlsx) via pandas dataframe, which can then be used as model inputs.
    '''

    weather_df = pd.read_excel(io=input_file_path, sheet_name='Irradiation and temperatur').reset_index().dropna().set_index('Time')
    dict_irradiation = weather_df['Irradiation'].to_dict()
    dict_temperature = weather_df['Temperature'].to_dict()
    return(dict_irradiation,dict_temperature)

# (dict_irradiation,dict_temperature)=read_weather_data()
# print('dict_irradiation: ', dict_irradiation)

def calculate_COP():
    '''
    Reads input data from excel file (e.g. data_input.xlsx) via pandas dataframe, which can then be used as model inputs.
    '''
    general_df = pd.read_excel(io=input_file_path, sheet_name='General Data').drop('Abbreviation', axis=1).set_index('Parameter')   
    weather_df = pd.read_excel(io=input_file_path, sheet_name='Irradiation and temperatur').reset_index().dropna().set_index('Time')
    param_reduction_cop=general_df.at['Reduction COP','Value']
    param_temp_heating=general_df.at['Temperature heating','Value']
    dict_COP = weather_df['Temperature'].to_dict()
    for key in dict_COP:
            dict_COP[key] = ((dict_COP[key])/(param_temp_heating-dict_COP[key]))*param_reduction_cop

    return(dict_COP) 
# dict_COP=calculate_COP()
# print(dict_COP)

def calculate_performance_PV():
    '''
    Reads input data from excel file (e.g. data_input.xlsx) via pandas dataframe, which can then be used as model inputs.
    '''

    (dict_irradiation,dict_temperature)=read_weather_data()
    (dict_general_parameters)=read_general_data()
    dict_capacity_factor_PV= dict_irradiation.copy() 
    for key in dict_capacity_factor_PV:
        dict_capacity_factor_PV[key] = ((dict_capacity_factor_PV[key] *dict_general_parameters['Surface Factor PV'])/dict_general_parameters['Irradiation STC']) \
            *dict_general_parameters['Performance ratio PV']

    dict_temperature_factor_PV= dict_temperature.copy()
    for key in dict_temperature_factor_PV:
        dict_temperature_factor_PV[key]=(dict_temperature_factor_PV[key]-dict_general_parameters['Temperature STC'])*(dict_general_parameters['Temperatur factor PV']/100)
    return(dict_capacity_factor_PV,dict_temperature_factor_PV) 


# (dict_capacity_factor_PV,dict_temperature_factor_PV)=calculate_performance_PV()
# print('dict_temperature_factor_PV: ', dict_temperature_factor_PV)
# print('dict_capacity_factor: ', dict_capacity_factor_PV)



# (dict_price_invest,dict_cost_service,dict_price_connection,dict_price_fuel,dict_price_invest_contractor,dict_cost_service_contractor, \
#     dict_price_connection_contractor,dict_price_fuel_contractor,dict_price_invest_default,dict_cost_service_default, \
#     dict_price_connection_default,dict_price_fuel_default,dict_price_feedin_default)=read_cost_data()
# print('dict_price_feedin_default: ', dict_price_feedin_default)


#     demand_df = pd.read_excel(io=input_file_path, sheet_name='Demand').reset_index().dropna().set_index('time')
#     dict_dem = demand_df['demand'].to_dict()

#     irradiation_df = pd.read_excel(io=input_file_path, sheet_name='irradiation', index_col=0) 

#     #irradtion on the full roof area
#     dict_irradiation_full_PV_area = dict(irradiation_df['PV'])
#     for key in dict_irradiation_full_PV_area:
#         dict_irradiation_full_PV_area[key] = dict_irradiation_full_PV_area[key] *param_area_roof          

#     dict_irradiation = dict()
#     for idx1 in set_time :
#         for idx2 in set_options_var_supply:
#             dict_irradiation[idx1, idx2] = irradiation_df.loc[idx1][idx2]

#     # capacity factor of PV options is calculated from irradiation [kW/m²] multiplied by specific area of PV [m2/kWp]
#     dict_capacity_factor_var_supply = dict_irradiation.copy() 
#     for key in dict_capacity_factor_var_supply:
#         dict_capacity_factor_var_supply[key] = dict_capacity_factor_var_supply[key] *param_specific_area_PV

#     # # capacity factor is limited to 1
#     # for key,value in dict_capacity_factor_var_supply.items():
#     #     if value>1:
#     #         dict_capacity_factor_var_supply[key] = 1    

#     # capacity factor of grid is given as constant value
#     dict_capacity_factor_fix_supply= dict()
#     for idx1 in set_time :
#         for idx2 in set_options_fix_supply:
#             dict_capacity_factor_fix_supply[idx1,idx2] = param_capacity_factor_grid

#     # combine capacity factor of all options
#     dict_capacity_factor = {**dict_capacity_factor_fix_supply, **dict_capacity_factor_var_supply}

#     # maximum capacity of PV option is limited by the area of the roof
#     dict_max_capacity_PV= dict()
#     for idx in set_options_var_supply:
#         dict_max_capacity_PV[idx]=(param_area_roof/param_specific_area_PV)

#     # maximum capacity of grid is given as constant value
#     dict_max_capacity_grid= dict()
#     for idx in set_options_fix_supply:
#         dict_max_capacity_grid[idx] = param_max_capacity_grid

#     # combine maximum capacity of all options
#     dict_max_capacity = {**dict_max_capacity_PV, **dict_max_capacity_grid}

#     cost_df = pd.read_excel(io=input_file_path, sheet_name='Cost').set_index(['Options']).drop(['Unit'])
#     dict_price_elec = cost_df['Cost of Electricity'].to_dict()
#     dict_price_invest = cost_df['Investment Cost'].to_dict()
#     return (set_time,set_options,dict_dem,dict_irradiation_full_PV_area,dict_capacity_factor,dict_max_capacity,dict_price_elec,dict_price_invest,param_annuity,param_area_roof,param_specific_area_PV)

# set_time,set_options,dict_dem,dict_irradiation_full_PV_area,dict_capacity_factor,dict_max_capacity,dict_price_elec,dict_price_invest,param_annuity,param_area_roof,param_specific_area_PV=read_data()

# set_time,set_contractor

#print('dict_price_elec: ', dict_price_elec)
#print('dict_price_invest: ', dict_price_invest)
#print('dict_capacity_factor: ', dict_capacity_factor)
#print('dict_capacity_factor: ', dict_capacity_factor)
# print('dict_irradiation_full_PV_area: ', dict_irradiation_full_PV_area)
#print('dict_irradiation_full_PV_area: ', dict_irradiation_full_PV_area)
#print('set_options: ', set_options)
# print('dict_dem: ', dict_dem)
# print('set_time: ', set_time)
# print('dict_capacity_factor: ', dict_capacity_factor)
# print('dict_max_capacity: ', dict_max_capacity)


# def define_charging_time():
#     set_df = pd.read_excel(io=input_file_path, sheet_name='Sets')
#     set_df.set_index('time',inplace=True)
#     charging_time_idx = [idx for idx in set_df.index if (idx>=16)&(idx<=24)]
#     charging_time_df = set_df.loc[charging_time_idx]
#     set_charging_time = dict.fromkeys(charging_time_df.index,0)
#     return set_charging_time


# # ////// 'with timestamps'
# def define_charging_time():
#     set_df = pd.read_excel(io=input_file_path, sheet_name='Sets')
#     set_df.set_index('time',inplace=True)
#     charging_time_idx = [idx for idx in set_df.index if (idx.hour>=16)&(idx.hour<=24)]
#     charging_time_df = set_df.loc[charging_time_idx]
#     set_charging_time = dict.fromkeys(charging_time_df.index,0)
#     return set_charging_time


# set_charging_time=define_charging_time()
# print('set_charging_time: ', set_charging_time)

# test_time_df = pd.read_excel(io=input_file_path, sheet_name='test_date')
# # test_time_df['time']=pd.to_datetime(test_time_df['time'])
# # time_mask = (test_time_df['time'].dt.hour >= 13) & \
# #             (test_time_df['time'].dt.hour <= 15)

# # new_df=test_time_df[time_mask]

# # print('test_time_df[time_mask]: ', test_time_df[time_mask])

# test_time_df.set_index('time',inplace=True)
# choseInd = [ind for ind in test_time_df.index if (ind.hour>=13)&(ind.hour<=15)]
# df_select = test_time_df.loc[choseInd]
# print('df_select: ', df_select)
# set_time = dict.fromkeys(df_select.index,0)
# print('set_time: ', set_time)


# print('set_technologies: ', set_technologies)








# cost_without_contractor_df = pd.read_excel(io=input_file_path, sheet_name='Costs without contractor ').set_index(['Elements']).drop(['Unit'])
#     dict_price_invest = cost_without_contractor_df['Investment Price'].to_dict()
#     dict_cost_service = cost_without_contractor_df['Service Cost'].to_dict()
#     dict_price_connection = cost_without_contractor_df['Connection Price'].to_dict()
#     dict_price_fuel = cost_without_contractor_df['Fuel Price'].to_dict()

#     cost_with_contractor_df = pd.read_excel(io=input_file_path, sheet_name='Costs with contractor').set_index(['Elements']).drop(['Unit'])
#     dict_price_invest_contractor = cost_with_contractor_df['Investment Price'].to_dict()
#     dict_cost_service_contractor = cost_with_contractor_df['Service Cost'].to_dict()
#     dict_price_connection_contractor = cost_with_contractor_df['Connection Price'].to_dict()
#     dict_price_fuel_contractor = cost_with_contractor_df['Fuel Price'].to_dict()

#     cost_default_df = pd.read_excel(io=input_file_path, sheet_name='Costs of default system').set_index(['Elements']).drop(['Unit'])
#     dict_price_invest_default = cost_default_df['Investment Price'].to_dict()
#     dict_cost_service_default = cost_default_df['Service Cost'].to_dict()
#     dict_price_connection_default = cost_default_df['Connection Price'].to_dict()
#     dict_price_fuel_default = cost_default_df['Fuel Price'].to_dict()
#     dict_price_feedin_default = cost_default_df['Feedin Price'].to_dict()

#     return(dict_price_invest,dict_cost_service,dict_price_connection,dict_price_fuel,dict_price_invest_contractor,dict_cost_service_contractor, \
#     dict_price_connection_contractor,dict_price_fuel_contractor,dict_price_invest_default,dict_cost_service_default, \
#     dict_price_connection_default,dict_price_fuel_default,dict_price_feedin_default)


# general_df = pd.read_excel(io=input_file_path, sheet_name='General Data').drop('Abbreviation', axis=1).set_index('Parameter')   
    # param_interest_rate= general_df.at['Interest rate','Value']
    # param_depreciation= general_df.at['Depreciation time','Value']
    # param_annuity=(((1+param_interest_rate)**param_depreciation)*param_interest_rate)/(((1+param_interest_rate)**param_depreciation)-1)
    # param_area_roof=general_df.at['Area Roof','Value']
    # param_capacity_density_PV=general_df.at['Area PV','Value']
    # param_specific_DHW_demand=general_df.at['DOW p.P.','Value']
    # param_powerflow_max_battery=general_df.at['Maximum Powerflow Battery','Value']
    # param_powerflow_max_battery_car=general_df.at['Maximum Powerflow Battery Car','Value']
    # param_capacity_car=general_df.at['Capacity Battery Car','Value']
    # param_efficiency_battery=general_df.at['Efficiency Battery Car','Value']
    # param_efficiency_battery_car=general_df.at['Efficiency Battery Car','Value']
    # param_efficiency_gas=general_df.at['Efficiency Gas Boiler','Value']
    # param_number_chargingstations=general_df.at['Number of charging stations','Value']
    # param_number_households=general_df.at['Number of household','Value']
    # param_simultaneity=general_df.at['Simultaneity factor','Value']

