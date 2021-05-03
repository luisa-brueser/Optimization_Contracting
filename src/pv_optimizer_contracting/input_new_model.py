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
    set_finance_options= dict.fromkeys(set_df['Options'].dropna(),0)
    set_technologies = dict.fromkeys(set_df['Elements'].dropna(),0)
    set_default = dict.fromkeys(set_df['Default'].dropna(),0)
    return (set_time,set_finance_options,set_technologies,set_default)


def read_gerneral_data():
    '''
    Reads input data from excel file (e.g. data_input.xlsx) via pandas dataframe, which can then be used as model inputs.
    '''
       
    general_df = pd.read_excel(io=input_file_path, sheet_name='General Data').drop('Abbreviation', axis=1).set_index('Parameter')   
    param_interest_rate= general_df.at['Interest rate','Value']
    param_depreciation= general_df.at['Depreciation time','Value']
    param_area_roof=general_df.at['Area Roof','Value']
    param_specific_area_pv=general_df.at['Area PV','Value']
    param_DOW_demand=general_df.at['DOW p.P.','Value']
    param_reduction_cop=general_df.at['Reduction COP','Value']
    param_temp_heating=general_df.at['Temperature heating','Value']
    param_powerflow_max_battery=general_df.at['Maximum Powerflow Battery','Value']
    param_powerflow_max_battery_car=general_df.at['Maximum Powerflow Battery Car','Value']
    param_capacity_car=general_df.at['Capacity Battery Car','Value']
    param_efficiency_battery=general_df.at['Efficiency Battery Car','Value']
    param_efficiency_battery_car=general_df.at['Efficiency Battery Car','Value']
    param_efficiency_gas=general_df.at['Efficiency Gas Boiler','Value']
    param_number_chargingstations=general_df.at['Number of charging stations','Value']
    param_number_households=general_df.at['Number of household','Value']
    param_simultaneity=general_df.at['Simultaneity factor','Value']
    return (param_interest_rate,param_depreciation,param_area_roof,param_specific_area_pv,param_DOW_demand,param_reduction_cop,param_temp_heating,param_powerflow_max_battery,param_powerflow_max_battery_car,param_efficiency_gas,param_number_chargingstations,param_number_households,param_simultaneity)

def read_cost_data():
    '''
    Reads input data from excel file (e.g. data_input.xlsx) via pandas dataframe, which can then be used as model inputs.
    '''
    cost_without_contractor_df = pd.read_excel(io=input_file_path, sheet_name='Costs without contractor ').set_index(['Elements']).drop(['Unit'])
    dict_price_invest = cost_without_contractor_df['Investment Price'].to_dict()
    dict_price_service = cost_without_contractor_df['Service Cost'].to_dict()
    dict_price_connection = cost_without_contractor_df['Connection Price'].to_dict()
    dict_price_fuel = cost_without_contractor_df['Fuel Price'].to_dict()

    cost_with_contractor_df = pd.read_excel(io=input_file_path, sheet_name='Costs with contractor').set_index(['Elements']).drop(['Unit'])
    dict_price_invest_contractor = cost_with_contractor_df['Investment Price'].to_dict()
    dict_price_service_contractor = cost_with_contractor_df['Service Cost'].to_dict()
    dict_price_connection_contractor = cost_with_contractor_df['Connection Price'].to_dict()
    dict_price_fuel_contractor = cost_with_contractor_df['Fuel Price'].to_dict()

    cost_default_df = pd.read_excel(io=input_file_path, sheet_name='Costs of default system').set_index(['Elements']).drop(['Unit'])
    dict_price_invest_default = cost_default_df['Investment Price'].to_dict()
    dict_price_service_default = cost_default_df['Service Cost'].to_dict()
    dict_price_connection_default = cost_default_df['Connection Price'].to_dict()
    dict_price_fuel_default = cost_default_df['Fuel Price'].to_dict()
    dict_price_feedin_default = cost_default_df['Feedin Price'].to_dict()

    return(dict_price_invest,dict_price_service,dict_price_connection,dict_price_fuel,dict_price_invest_contractor,dict_price_service_contractor, \
    dict_price_connection_contractor,dict_price_fuel_contractor,dict_price_invest_default,dict_price_service_default, \
    dict_price_connection_default,dict_price_fuel_default,dict_price_feedin_default)

def read_demand_data():
    '''
    Reads input data from excel file (e.g. data_input.xlsx) via pandas dataframe, which can then be used as model inputs.
    '''
    demand_df = pd.read_excel(io=input_file_path, sheet_name='Demand').reset_index().dropna().set_index('Time')
    dict_demand_charging = demand_df['Car'].to_dict()
    dict_demand_hot_water = demand_df['DHW'].to_dict()
    dict_demand_electricity = demand_df['Electricity household'].to_dict()
    dict_demand_heating = demand_df['Heating'].to_dict()
    return(dict_demand_charging,dict_demand_hot_water,dict_demand_electricity,dict_demand_heating)

(dict_demand_charging,dict_demand_hot_water,dict_demand_electricity,dict_demand_heating)=read_demand_data()
print('dict_demand_hot_water: ', dict_demand_hot_water)

# (dict_price_invest,dict_price_service,dict_price_connection,dict_price_fuel,dict_price_invest_contractor,dict_price_service_contractor, \
#     dict_price_connection_contractor,dict_price_fuel_contractor,dict_price_invest_default,dict_price_service_default, \
#     dict_price_connection_default,dict_price_fuel_default,dict_price_feedin_default)=read_cost_data()
# print('dict_price_feedin_default: ', dict_price_feedin_default)


#     demand_df = pd.read_excel(io=input_file_path, sheet_name='Demand').reset_index().dropna().set_index('time')
#     dict_dem = demand_df['demand'].to_dict()

#     irradiation_df = pd.read_excel(io=input_file_path, sheet_name='irradiation', index_col=0) 

#     #irradtion on the full roof area
#     dict_irradiation_full_pv_area = dict(irradiation_df['PV'])
#     for key in dict_irradiation_full_pv_area:
#         dict_irradiation_full_pv_area[key] = dict_irradiation_full_pv_area[key] *param_area_roof          

#     dict_irradiation = dict()
#     for idx1 in set_time :
#         for idx2 in set_options_var_supply:
#             dict_irradiation[idx1, idx2] = irradiation_df.loc[idx1][idx2]

#     # capacity factor of PV options is calculated from irradiation [kW/m²] multiplied by specific area of PV [m2/kWp]
#     dict_capacity_factor_var_supply = dict_irradiation.copy() 
#     for key in dict_capacity_factor_var_supply:
#         dict_capacity_factor_var_supply[key] = dict_capacity_factor_var_supply[key] *param_specific_area_pv

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
#     dict_max_capacity_pv= dict()
#     for idx in set_options_var_supply:
#         dict_max_capacity_pv[idx]=(param_area_roof/param_specific_area_pv)

#     # maximum capacity of grid is given as constant value
#     dict_max_capacity_grid= dict()
#     for idx in set_options_fix_supply:
#         dict_max_capacity_grid[idx] = param_max_capacity_grid

#     # combine maximum capacity of all options
#     dict_max_capacity = {**dict_max_capacity_pv, **dict_max_capacity_grid}

#     cost_df = pd.read_excel(io=input_file_path, sheet_name='Cost').set_index(['Options']).drop(['Unit'])
#     dict_price_elec = cost_df['Cost of Electricity'].to_dict()
#     dict_price_invest = cost_df['Investment Cost'].to_dict()
#     return (set_time,set_options,dict_dem,dict_irradiation_full_pv_area,dict_capacity_factor,dict_max_capacity,dict_price_elec,dict_price_invest,param_annuity,param_area_roof,param_specific_area_pv)

# set_time,set_options,dict_dem,dict_irradiation_full_pv_area,dict_capacity_factor,dict_max_capacity,dict_price_elec,dict_price_invest,param_annuity,param_area_roof,param_specific_area_pv=read_data()

# set_time,set_contractor

#print('dict_price_elec: ', dict_price_elec)
#print('dict_price_invest: ', dict_price_invest)
#print('dict_capacity_factor: ', dict_capacity_factor)
#print('dict_capacity_factor: ', dict_capacity_factor)
# print('dict_irradiation_full_pv_area: ', dict_irradiation_full_pv_area)
#print('dict_irradiation_full_pv_area: ', dict_irradiation_full_pv_area)
#print('set_options: ', set_options)
# print('dict_dem: ', dict_dem)
# print('set_time: ', set_time)
# print('dict_capacity_factor: ', dict_capacity_factor)
# print('dict_max_capacity: ', dict_max_capacity)


def define_charging_time():
    set_df = pd.read_excel(io=input_file_path, sheet_name='Sets')
    set_df.set_index('time',inplace=True)
    charging_time_idx = [idx for idx in set_df.index if (idx>=16)&(idx<=24)]
    charging_time_df = set_df.loc[charging_time_idx]
    set_charging_time = dict.fromkeys(charging_time_df.index,0)
    return set_charging_time


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


