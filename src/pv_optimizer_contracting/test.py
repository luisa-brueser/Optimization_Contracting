import pandas as pd
from pathlib import Path
input_file_path = Path(__file__).parent / 'data_input_new_model.xlsx'

general_df = pd.read_excel(io=input_file_path, sheet_name='General Data').drop('Abbreviation', axis=1)   
print(general_df)
