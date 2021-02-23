import pandas as pd
from pathlib import Path
import numpy as np
import pyam
import matplotlib.pyplot as plt

output_file_path = Path(__file__).parent / 'data_output.csv'
#cur_dir=Path.cwd()
#csv_path=str(cur_dir)+"\\..\\Dataset\\data_output_test.csv"

# df = pyam.IamDataFrame(output_file_path)
# df

# model, scenario = 'Luisa', 'Contracting1'

# # data = (
# #     df.filter(model=model, scenario=scenario, variable='Supply_PV')
# #     .filter(region='Vienna')
# # )

# df.plot(color='region', title='Test')

# plt.show()
# print(data.timeseries())

data={'Model':['Contracting_model'],'Scenario':['Contracting_1'],'Region':['Vienna'],'Variable':['Supply_PV'],'Unit':['kW'],'0':[0],'4':[0],'8':[4],'12':[6],'16':[8],'20':[2],'24':[0]}
df = pd.DataFrame(data=data)
print('df: ', df)
df.to_csv(str(output_file_path),index=False)
#df.to_csv(r"c:\Users\Thomas\Desktop\DA\Code\pv_optimizer_contracting\src\pv_optimizer_contracting",index=False)
#df.to_csv(r str(output_file_path),index=False)
# new = pyam.IamDataFrame(df)



df = pyam.IamDataFrame(output_file_path)
df

model, scenario = 'Luisa', 'Contracting1'

# data = (
#     df.filter(model=model, scenario=scenario, variable='Supply_PV')
#     .filter(region='Vienna')
# )

df.plot(color='region', title='Test')

plt.show()
print(data.timeseries())

