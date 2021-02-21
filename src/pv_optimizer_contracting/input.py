import pandas as pd
from pathlib import Path


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
    dict_irradiation = dict()
    for idx1 in set_time :
        for idx2 in set_options_var_supply:
            dict_irradiation[idx1, idx2] = irradiation_df.loc[idx1][idx2]

    # capacity factor of PV options is calculated from irradiation [kW/m²] multiplied by specific area of PV [m2/kWp]
    dict_capacity_factor_var_supply = dict_irradiation.copy() 
    for key in dict_capacity_factor_var_supply:
        dict_capacity_factor_var_supply[key] = dict_capacity_factor_var_supply[key] *param_specific_area_pv

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
    return (set_time,set_options,dict_dem,dict_capacity_factor,dict_max_capacity,dict_price_elec,dict_price_invest,param_annuity,param_area_roof,param_specific_area_pv)

# set_time,set_options,dict_dem,dict_capacity_factor,dict_max_capacity,dict_price_elec,dict_price_invest,param_annuity,param_area_roof,param_specific_area_pv=read_data()
# print('dict_capacity_factor: ', dict_capacity_factor)
# print('dict_max_capacity: ', dict_max_capacity)



#dict_dem = demand_df['demand'].to_dict()


set_time = dict.fromkeys(set_df['time'].dropna(),0)
print('set_time: ', set_time)
