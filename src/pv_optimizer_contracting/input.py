import pandas as pd
from pathlib import Path
from datetime import datetime

input_file_path = Path(__file__).parent / 'data_input.xlsx'


def read_data():
    '''
    Reads input data from excel file (e.g. data_input.xlsx) via pandas dataframe, which can then be used as model inputs.
    '''
       
    set_df = pd.read_excel(io=input_file_path, sheet_name='Sets')
    set_time = dict.fromkeys(set_df['time'].dropna(),0)
    set_options = dict.fromkeys(set_df['options'].dropna(),0)
    set_options_var_supply = dict.fromkeys(set_df['options_var_supply'].dropna(),0)
    set_options_fix_supply = dict.fromkeys(set_df['options_fix_supply'].dropna(),0)

    general_df = pd.read_excel(io=input_file_path, sheet_name='General Data').drop([0])   
    param_annuity=general_df['Annuity Factor'].loc[1]
    param_area_roof=general_df['Area Roof'].loc[1]
    param_specific_area_pv=general_df['Area PV'].loc[1]
    param_capacity_factor_grid=general_df['Capacity factor grid'].loc[1]
    param_max_capacity_grid=general_df['Capacity limit grid'].loc[1]

    demand_df = pd.read_excel(io=input_file_path, sheet_name='Demand').reset_index().dropna().set_index('time')
    dict_dem = demand_df['demand'].to_dict()

    irradiation_df = pd.read_excel(io=input_file_path, sheet_name='irradiation', index_col=0) 

    #irradtion on the full roof area
    dict_irradiation_full_pv_area = dict(irradiation_df['PV'])
    for key in dict_irradiation_full_pv_area:
        dict_irradiation_full_pv_area[key] = dict_irradiation_full_pv_area[key] *param_area_roof          

    dict_irradiation = dict()
    for idx1 in set_time :
        for idx2 in set_options_var_supply:
            dict_irradiation[idx1, idx2] = irradiation_df.loc[idx1][idx2]

    # capacity factor of PV options is calculated from irradiation [kW/m²] multiplied by specific area of PV [m2/kWp]
    dict_capacity_factor_var_supply = dict_irradiation.copy() 
    for key in dict_capacity_factor_var_supply:
        dict_capacity_factor_var_supply[key] = dict_capacity_factor_var_supply[key] *param_specific_area_pv

    # # capacity factor is limited to 1
    # for key,value in dict_capacity_factor_var_supply.items():
    #     if value>1:
    #         dict_capacity_factor_var_supply[key] = 1    

    # capacity factor of grid is given as constant value
    dict_capacity_factor_fix_supply= dict()
    for idx1 in set_time :
        for idx2 in set_options_fix_supply:
            dict_capacity_factor_fix_supply[idx1,idx2] = param_capacity_factor_grid

    # combine capacity factor of all options
    dict_capacity_factor = {**dict_capacity_factor_fix_supply, **dict_capacity_factor_var_supply}

    # maximum capacity of PV option is limited by the area of the roof
    dict_max_capacity_pv= dict()
    for idx in set_options_var_supply:
        dict_max_capacity_pv[idx]=(param_area_roof/param_specific_area_pv)

    # maximum capacity of grid is given as constant value
    dict_max_capacity_grid= dict()
    for idx in set_options_fix_supply:
        dict_max_capacity_grid[idx] = param_max_capacity_grid

    # combine maximum capacity of all options
    dict_max_capacity = {**dict_max_capacity_pv, **dict_max_capacity_grid}

    cost_df = pd.read_excel(io=input_file_path, sheet_name='Cost').set_index(['Options']).drop(['Unit'])
    dict_price_elec = cost_df['Cost of Electricity'].to_dict()
    dict_price_invest = cost_df['Investment Cost'].to_dict()
    return (set_time,set_options,dict_dem,dict_irradiation_full_pv_area,dict_capacity_factor,dict_max_capacity,dict_price_elec,dict_price_invest,param_annuity,param_area_roof,param_specific_area_pv)

set_time,set_options,dict_dem,dict_irradiation_full_pv_area,dict_capacity_factor,dict_max_capacity,dict_price_elec,dict_price_invest,param_annuity,param_area_roof,param_specific_area_pv=read_data()
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
print(param_annuity)

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


