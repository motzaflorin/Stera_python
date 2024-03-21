# MAIN PURPOSE OF THIS SCRIPT IS TO READ THE WHOLE 60.000 BUILDING DATABASE
# AND TO REMOVE THE BUILDINGS IN L-SHAPE AND WRTIE A NEW CSV FILE



import main
import os
import pandas
from pathlib import Path

database_folder = os.path.join(Path(__file__).parents[1],"DATABASE") #"D:\\0 DOCTORAT\\00_RC2\Ruben_Vasile"
database_file = "30000_BUILDINGS.csv"
database_file_location = os.path.join(database_folder,database_file)



df = main.read_database_Ruben_Vasile()

# Specify the condition for rows to keep
condition_to_remove_L_shape_buildings = (df['Lshape'] != 1)
# print(condition_to_remove_L_shape_buildings)
# Filter the DataFrame based on the condition
df_filtered = df[condition_to_remove_L_shape_buildings]
print(df_filtered)
file_path = "D:\\0 DOCTORAT\\00_RC2\StructuraL_FEM_Nonlinear_Analysis_Suite\DATABASE\\30000_BUILDINGS_good.csv"
df_filtered.to_csv(file_path)