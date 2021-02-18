import pandas as pd
from pathlib import Path


input_file_path = Path(__file__).parent / "data_input.xlsx"


def read_data():
    """
    Reads input data from excel file (e.g. data_input.xlsx) via pandas dataframe, which can then be used as model inputs.
    """
       
    set_df = pd.read_excel(io=input_file_path, sheet_name="Sets")
    set_time = dict.fromkeys(set_df['time'].dropna(),0)
    set_options = dict.fromkeys(set_df['options'].dropna(),0)
    set_options_var_supply = dict.fromkeys(set_df['options_var_supply'].dropna(),0)
    set_options_fix_supply = dict.fromkeys(set_df['options_fix_supply'].dropna(),0)

    general_df = pd.read_excel(io=input_file_path, sheet_name="General Data").drop([0])   
    param_annuity=general_df['Annuity Factor'].loc[1]
    param_area=general_df['Area Roof'].loc[1]
    param_specific_area_pv=general_df['Area PV'].loc[1]
    param_capacity_factor_grid=general_df['Capacity factor grid'].loc[1]

    demand_df = pd.read_excel(io=input_file_path, sheet_name="Demand").reset_index().dropna().set_index('time')
    dict_dem = demand_df['demand'].to_dict()

    

    irradiation_df = pd.read_excel(io=input_file_path, sheet_name="irradiation", index_col=0) 
    dict_irradiation = dict()
    for k1 in set_time :
        for k2 in set_options_var_supply:
            dict_irradiation[k1, k2] = irradiation_df.loc[k1][k2]

    dict_capacity_factor_var_supply = dict_irradiation.copy() 
    for key in dict_capacity_factor_var_supply:
        dict_capacity_factor_var_supply[key] = dict_capacity_factor_var_supply[key] *param_specific_area_pv

    dict_capacity_factor_fix_supply= dict()
    for k1 in set_time :
        for k2 in set_options_fix_supply:
            dict_capacity_factor_fix_supply[k1,k2] = param_capacity_factor_grid

    dict_capacity_factor = {**dict_capacity_factor_fix_supply, **dict_capacity_factor_var_supply}

    cost_df = pd.read_excel(io=input_file_path, sheet_name="Cost").set_index(['Options']).drop(['Unit'])
    dict_price_elec = cost_df['Cost of Electricity'].to_dict()
    dict_price_invest = cost_df['Investment Cost'].to_dict()

    

    return (set_time,set_options,dict_dem,dict_capacity_factor,dict_price_elec,dict_price_invest,param_annuity,param_area,param_specific_area_pv)

# (set_time,set_options,dict_dem,dict_capacity_factor,dict_price_elec,dict_price_invest,param_annuity,param_area,param_specific_area_pv)=read_data()
# print('param_specific_area_pv: ', param_specific_area_pv)
# print('param_area: ', param_area)

# set_time,set_options,dict_dem,dict_capacity_factor,dict_price_elec,dict_price_invest,param_annuity,param_area,param_specific_area_pv = read_data()
# print('dict_capacity_factor: ', dict_capacity_factor)






# supply_df = pd.read_excel(io=input_file_path, sheet_name="Supply", index_col=0) 
#     dict_capacity_factor = dict()
#     for k1 in set_time :
#         for k2 in set_options:
#             dict_capacity_factor[k1, k2] = supply_df.loc[k1][k2]