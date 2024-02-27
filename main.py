###############################
# PROJECT MADE FOR BUILDING GENERATION FOR RCS2_DOCTORATE DATABASE - MADE FOR RESPONSE RUNNING
# PRESENT CODE IS FOR „INPUTDATA.TXT” FILE GENERATION
# Main of all scripts
from datetime import datetime
# CLASSES NEEDED: 1) - MEMBER PROPERTIES (BEAM,COLOUMN, WALL, ISOLATOR, ....)
#                 2)  Class for 2 lines options (ex:Nonlinear Flexural Spring (0:Not considered, 1:Considered) = (newline) 1)


from pathlib import Path
import os
import pandas as pd
import shutil
import time
from concurrent.futures import ProcessPoolExecutor
from joblib import Parallel, delayed
import subprocess
from functools import partial
from multiprocessing import Process
import concurrent.futures
from concurrent.futures import as_completed, wait

import floor_properties
import output_stera_files
import general_model_info
import member_type
import options_for
import member_properties
import col_properties
import beam_properties
import general_model_info_2
import inputwave_writing
import public_func


def inputdata_generator(output_inputdata_file,unique_folder_name,parent_folder,input_folder,output_folder,input_list):
    # Call everything from here

    # 1
    # General Settings              -       could be moved in other place
    [index_of_accelerogram_set, timestep, scale_factor, story_height, building_height, span, bay,
                      no_story, no_span, no_bay, csi, col_width1, col_width2, beam_width, beam_height, young_modul,
                      mom_cap_x, mom_cap_y, mom_cap_beam, unique_index] = input_list


    # Create file "inputdata.txt" populate output_settings (and first line with options (0 1 or 2) )
    output_stera_files.output_folder_for_stera_files(output_inputdata_file,unique_folder_name,parent_folder, input_folder, output_folder)

    # 2
    # Populate general info of building
    # General Settings
    analysis_case = 3
    no_of_floors = int(no_story)
    no_x_spans = int(no_span)
    no_y_spans = int(no_bay)
        # join file path
    file_path = os.path.join(parent_folder, unique_folder_name, input_folder, output_inputdata_file)
    general_model_info.model_info(analysis_case, no_of_floors, no_x_spans, no_y_spans, file_path)

    # 3
    # Populate with member type
    member_type.model_member_type(no_of_floors, no_x_spans, no_y_spans,file_path)

    # 4
    # Populate with options for analysis
    options_for.write_options(file_path)

    # 5
    # Popualte main properties of structural elements - member first
    member_properties.member_type(file_path)

    # 5 A
    # Popualte main properties of structural elements - COLUMN
    #       col_properties_values_list = [col_w,col_h,ec,xMc,xMy,xMu,xK1_K0,xK2_K0,yMc,yMy,yMu,yK1_K0,yK2_K0,r1,r2,r3,Ramda,ID_Ramda,htype,110,0,0,0,0,0,0]
    col_w = int(float(col_width1)*1000)# mm
    col_h = int(float(col_width2)*1000)
    ec = 36
    xMc = int(float(mom_cap_x))*0.8
    xMy = int(float(mom_cap_x))*0.9
    xMu = int(float(mom_cap_x))
    xK1_K0 = 0.4
    xK2_K0 = 0.001
    yMc = int(float(mom_cap_y))*0.8
    yMy = int(float(mom_cap_y))*0.9
    yMu = int(float(mom_cap_y))
    yK1_K0 = 0.4
    yK2_K0 = 0.001
    col_properties.write_member_properties(file_path,col_w,col_h,ec,xMc,xMy,xMu,xK1_K0,xK2_K0,yMc,yMy,yMu,yK1_K0,yK2_K0)

    # 5 B
    # Popualte main properties of structural elements - BEAM
    beam_w = int(float(beam_width)*1000) # mm
    beam_h = int(float(beam_height)*1000)
    ec = 36
    xMc = int(float(mom_cap_beam))*0.8
    xMy = int(float(mom_cap_beam))*0.9
    xMu = int(float(mom_cap_beam))
    xK1_K0 = 0.4
    xK2_K0 = 0.001
    yMc = int(float(mom_cap_beam))*0.8
    yMy = int(float(mom_cap_beam))*0.9
    yMu = int(float(mom_cap_beam))
    yK1_K0 = 0.4
    yK2_K0 = 0.001
    beam_properties.write_member_properties(file_path, beam_w, beam_h, ec, xMc, xMy, xMu, xK1_K0, xK2_K0, yMc, yMy, yMu,yK1_K0, yK2_K0)
    # 5 C
    # Popualte main properties of structural elements - rest of the properties up to FLOOR: WALL and EXT_SPRING
    member_properties.wall_properties(file_path)
    member_properties.ext_spring_properties(file_path)
    # 5 D
    # Popualte main properties of structural elements - FLOOR
    thick = 150
    fc = 2400 # std value
    ec = 36000 # std value
    floor_properties.write_member_properties(file_path,thick,fc,ec)
    # 5 E
    # Popualte main properties of structural elements - REST of unused elements
    member_properties.isolator_properties(file_path)
    member_properties.damper_properties(file_path)
    member_properties.masonry_properties(file_path)

    # 6
    # FInal part
    # Populate with model info general 2
    input_file_location = ""
    def story_mass_calc(x_span,y_span,height,col_w,col_h,beam_w,beam_h,plate_t,no_x_span,no_y_span):
        # all calc is done in mm and kg
        no_col = (no_x_span+1)*(no_y_span+1)
        one_col_vol = col_w * col_h*height * 10**(-9)
        no_beams_x = (no_y_span+1) * no_x_span
        no_beams_y = (no_x_span+1) * no_y_span
        one_beam_vol_x = beam_h * beam_w * x_span * 10**(-9)
        one_beam_vol_y = beam_h * beam_w * y_span * 10**(-9)
        plate_volume = (no_x_span * x_span + no_y_span * y_span) * plate_t * 10**(-9)
        rho = 25 # kg/m3

        normal_weight = (no_col * one_col_vol + no_beams_x * one_beam_vol_x +no_beams_y * one_beam_vol_y + plate_volume)  * rho
        last_story_weight = (no_col * one_col_vol /2 + no_beams_x * one_beam_vol_x +no_beams_y * one_beam_vol_y + plate_volume)  * rho
        return normal_weight, last_story_weight
    x_span = int(float(span)*1000)
    y_span = int(float(bay)*1000)

    height = int(float(story_height)*1000)
    story_weight, last_story_weight = story_mass_calc(x_span,y_span,height,col_w,col_h,beam_w,beam_h,thick,no_x_spans,no_y_spans)  # [kN]



    amp_x = float(scale_factor)
    amp_y = float(scale_factor)
    amp_z = 1

    # out goes weight and load distribution - to be used in writing specific files for them
    weight_distribution,load_distribution = general_model_info_2.write_model_info_2(file_path, x_span, no_x_spans, y_span, no_y_spans, no_of_floors, height, story_weight,last_story_weight, amp_x, amp_y,
                       amp_z)
    return weight_distribution,load_distribution
def inputwave_x_generator(wave_file_location,output_folder,unique_folder,input_folder,timestep):

    output_wave_file = "inputwave_x.txt"
    output_wave_file_location = os.path.join(output_folder,unique_folder,input_folder,output_wave_file)
    df = pd.read_csv(wave_file_location)
    # THE CSV files are in m/s^2 and needs to be in cm/s^2
    wave_x_df = df[df.columns[0]]*100



    inputwave_writing.wave_write(wave_x_df,output_wave_file_location,timestep)
    return
def inputwave_y_generator(wave_file_location,output_folder,unique_folder,input_folder,timestep):
    output_wave_file = "inputwave_y.txt"
    output_wave_file_location = os.path.join(output_folder,unique_folder,input_folder,output_wave_file)
    df = pd.read_csv(wave_file_location)
    # THE CSV files are in m/s^2 and needs to be in cm/s^2
    wave_y_df = df[df.columns[1]]*100

    inputwave_writing.wave_write(wave_y_df, output_wave_file_location, timestep)
    return
def inputwave_z_generator(output_folder,unique_folder,input_folder):
    output_wave_file = "inputwave_z.txt"
    output_wave_file_location = os.path.join(output_folder, unique_folder, input_folder, output_wave_file)
    empty_list = [0 for element in range(3000)]

    with open(output_wave_file_location,"w+") as file:
        for element in empty_list:
            file.write(str(element))
            file.write("\n")

    # inputwave_writing.wave_write(wave_y_df, output_wave_file_location, timestep)
    return
def load_distribution_generator(work_folder,load_distribution):
    load_file = "load_distribution.txt"
    last_values_list = list(load_distribution.values())[-1]
    story_load_list = [sublist[:-2] for sublist in last_values_list]
    story_load_dict = {"Load distribution at each floor": '',
                       public_func.five_spaces + 'F        load': story_load_list
                       }
    with open(os.path.join(work_folder,load_file),"w+") as file:
        public_func.dict_write(story_load_dict,file)
def weight_distribution_generator(weight_distribution,work_folder):
    weight_file = "weight_distribution.txt"
    with open(os.path.join(work_folder,weight_file),"w+") as file:
        public_func.dict_write(weight_distribution,file)
    return
def copy_prereq_from_seed_folder(source_folder,stera_call,response_exe,destination_folder):
    def generate_bat_file():
        contetns_dict = {"@echo off" : "",
                        f"pushd {destination_folder}" : "",
                        "CALL Response.exe" : "",
                        "popd" : ""
                         }
        with open(os.path.join(destination_folder,stera_call), "w+") as file:
            public_func.dict_write(contetns_dict,file)
    generate_bat_file()
    # copy .bat file and stera_response.exe from seed folder to the UNique number id folder
    # Create the destination folder if it doesn't exist
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Get the list of files and subdirectories in the source folder
    contents = os.listdir(source_folder)

    # Copy each file and subdirectory to the destination folder
    for item in contents:
        source_path = os.path.join(source_folder, item)
        destination_path = os.path.join(destination_folder, item)
        for _ in range(5):
            try:
                if os.path.isdir(source_path):
                    shutil.copytree(source_path, destination_path, symlinks=False, ignore=None)
                else:
                    shutil.copy2(source_path, destination_path)
                return  # Success, exit the loop
            except PermissionError:
                print(f"PermissionError: {source_path} is in use, retrying...")
                time.sleep(10)

    return

def run_response(unique_folder,stera_call,processes):
    # RUN EVERYTHING IN A DIFFERENT PROCESS THAT DOES NOT WAIT FOR THE PREVIOUS ONE TO START

    # Specify the directory containing the batch file
    directory_path = unique_folder
    bat_file = stera_call
    # Change the current working directory
    os.chdir(directory_path)
    unique_file_location = os.path.join(directory_path,bat_file)

    stdout_file = open('stdout.txt', 'w')
    stderr_file = open('stderr.txt', 'w')
    process = subprocess.Popen(['Response.exe'],stdout=stdout_file, stderr=stderr_file, shell=True)

    processes.append(process)
    # this works up to here

    os.chdir('..')
    return processes


def read_database_Ruben_Vasile ():
    # RUBEN_VASILE database has some mistakes in terms of data format : some fields have comma separated values instead of dot
    def replace_comma_with_dot(database_file_location):
        with open(database_file_location, 'r') as file:
            lines = file.readlines()

        # Replace commas with dots (or dots with commas) in each line
        lines = [line.replace(',', '.') for line in lines]

        # Create a new string by joining the modified lines
        modified_data = ''.join(lines)
        return modified_data
    database_folder = "D:\\0 DOCTORAT\\00_RC2\Ruben_Vasile"
    database_file = "DataSet_P3_orig.csv"
    database_file_location = os.path.join(database_folder,database_file)
    def testing_of_alg(database_file_location):
        number_of_rows_to_read = 11
        rows_to_be_read_list = [x for x in range(number_of_rows_to_read + 1)]
        # Use pd.read_csv on the modified string
        df = pd.read_csv((database_file_location),
                         skiprows=lambda x: x not in rows_to_be_read_list)  # second option, skip some rows
        return df
    def full_alg_database(database_file_location):
        df = pd.read_csv((database_file_location))
        return df

    df = testing_of_alg(database_file_location)
    # Specify the condition for rows to keep
    condition_to_remove_L_shape_buildings = (df['Lshape'] != 1)
    # Filter the DataFrame based on the condition
    df_filtered = df[condition_to_remove_L_shape_buildings]

    return df
def database_parameter_selection(df):
    # df                - is of TYPE row entry of DATAFRAME (every call to df, return float value)

    # Set display options to show more rows and columns
    # pd.set_option('display.max_rows', None)  # Show all rows
    pd.set_option('display.max_columns', None)  # Show all columns
    index_of_accelerogram_set = df["Recording_index"]
    timestep =                  df["Timestep"]
    scale_factor =              df["Scale_factor"]
    story_height =              df["Hieght"]
    building_height =           df["b_Hieght"]
    # X direction
    span =                      df["span"]
    # Y Direction
    bay =                       df["bay"]
    no_story =                  df["no_story"]
    no_span =                   df["no_span"]
    no_bay =                    df["no_bay"]
    csi =                       df["csi"]
    col_width1 =                df["b_st"]
    col_width2 =                df["h_st"]
    beam_width =                df["b_gr"]
    beam_height =               df["h_gr"]
    young_modul =               df["E"]
    mom_cap_x =                 df["MstX"]
    mom_cap_y =                 df["MstY"]
    mom_cap_beam =              df["Mgr"]

    unique_index =              df["index"]

    input_set_list = [index_of_accelerogram_set,timestep,scale_factor,story_height,building_height,span,bay,
                      no_story,no_span,no_bay,csi,col_width1,col_width2,beam_width,beam_height,young_modul,
                      mom_cap_x,mom_cap_y,mom_cap_beam,unique_index]
    # modified_list=[] #to  single_value TYPE (not list)
    # for item in range(len(input_set_list)):
    #     modified_list.append(public_func.df_singular_to_string(input_set_list[item]))

    return input_set_list



def main_call_per_process(df):#,processes):
    df_and_index = df
    input_list = database_parameter_selection(df_and_index)

    output_inputdata_file = "inputdata.txt"

    parent_folder = "D:\\0 DOCTORAT\\00_RC2\\Testare_generare_cladiri_Stera\\dummy_foler_test"
    input_folder = "input"
    output_folder = "output"


    unique_folder_name = str(int(input_list[-1]))
    unique_folder_name = f"ID-{unique_folder_name}"


    weight_distribution,load_ditribution = inputdata_generator(output_inputdata_file,unique_folder_name,parent_folder,input_folder,output_folder,input_list)

    # THE CSV files are in m/s^2 and needs to be in cm/s^2 - they are scaled to meet correct UNITS inside the functions
    wave_folder = "D:\\0 DOCTORAT\\00_RC2\Ruben_Vasile\AccSet_V3"
    string_of_index_acc = str(int(input_list[0]))

    wave_file = string_of_index_acc + ".csv"
    wave_file_location = os.path.join(wave_folder, wave_file)
    timestep = (input_list[1])


    inputwave_x_generator(wave_file_location,parent_folder,unique_folder_name,input_folder,timestep)

    inputwave_y_generator(wave_file_location,parent_folder,unique_folder_name,input_folder,timestep)
    inputwave_z_generator(parent_folder,unique_folder_name,input_folder)

    work_folder = os.path.join(parent_folder, unique_folder_name, input_folder)

    load_distribution_generator(work_folder,load_ditribution)

    weight_distribution_generator(weight_distribution,work_folder)

    seed_folder = "D:\\0 DOCTORAT\\00_RC2\Testare_generare_cladiri_Stera\SEED_FOLDER"
    stera_call = "CALL_RESPONSE.bat"
    response_exe = "Response.exe"
    unique_folder = os.path.join(parent_folder,unique_folder_name)
    copy_prereq_from_seed_folder(seed_folder,stera_call,response_exe,unique_folder)
    # THis is necessary - is seems it does not create the folder by itself
    # create output folder and data_structure.txt file
    create_output_folder = Path(parent_folder, unique_folder_name, output_folder).mkdir(parents=True)
    processes = []
    # processes = run_response(unique_folder,stera_call,processes)
    run_response(unique_folder, stera_call, processes)
    print(f"Processing row {df_and_index['index']}")
    # return processes
    return


# this is working
# if __name__ == "__main__":
#     # Code to create and start processes
#     df = read_database_Ruben_Vasile()
#     # add index to the DATAFRAME
#     df = df.reset_index()
#     start_time_acc = datetime.now()
#     # Run each row in a separete process (this is done inside the response_function)
#     processes = []
#     for _, row in df.iterrows():
#         processes = main_call_per_process(row,processes)
#     # Wait for all processes to finish
#     for process in processes:
#         process.wait()
#
#     end_time_acc = datetime.now()
#     print('   TIME ELAPSED: ' + str(end_time_acc - start_time_acc) + '\n')


if __name__ == "__main__":
    # Code to create and start processes
    df = read_database_Ruben_Vasile()
    # Add index to the DATAFRAME
    df = df.reset_index()

    start_time_acc = datetime.now()

    # Use ProcessPoolExecutor for parallel processing with max_workers=3
    max_workers = 3
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        # Submit initial tasks up to max_workers
        futures = {executor.submit(main_call_per_process, df=row[1]) for _, row in zip(range(max_workers), df.iterrows())}

        while futures:
            # Wait for any completed task
            completed = as_completed(futures)

            # Retrieve the result (if needed)
            for future in completed:
                future.result()

            # Remove completed tasks from the set
            futures.difference_update(completed)

            # Submit a new task if there is a row available
            try:
                _, row = next(df.iterrows())
                future = executor.submit(main_call_per_process, df=row)
                futures.add(future)
            except StopIteration:
                pass  # All rows processed

    end_time_acc = datetime.now()
    print('TIME ELAPSED: ' + str(end_time_acc - start_time_acc) + '\n')


    #this is tested for git
    # tetst
