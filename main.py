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
import threading
from concurrent.futures import as_completed, wait
import pathlib

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
import itertools
from datetime import date


def inputdata_generator(output_inputdata_file,unique_folder_name,parent_folder,input_folder,output_folder,input_list):
    # Call everything from here

    # 1
    # General Settings              -       could be moved in other place
    [index_of_accelerogram_set, timestep, scale_factor, story_height, building_height, span, bay,
                      no_story, no_span, no_bay, csi, col_width1, col_width2, beam_width, beam_height, py, young_modul,
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
    options_for.write_options(file_path,csi)

    # 5
    # Popualte main properties of structural elements - member first
    member_properties.member_type(file_path)

    # 5 A
    # Popualte main properties of structural elements - COLUMN
    #       col_properties_values_list = [col_w,col_h,ec,xMc,xMy,xMu,xK1_K0,xK2_K0,yMc,yMy,yMu,yK1_K0,yK2_K0,r1,r2,r3,Ramda,ID_Ramda,htype,110,0,0,0,0,0,0]
    col_w = int(float(col_width1)*1000)# mm
    col_h = int(float(col_width2)*1000)
    ec = young_modul/(10**6) #(Mpa without 1000)
    xMc = int(float(mom_cap_x))*0.9
    xMy = int(float(mom_cap_x))*0.95
    xMu = int(float(mom_cap_x))
    xK1_K0 = 1
    xK2_K0 = 0.0001
    yMc = int(float(mom_cap_y))*0.9
    yMy = int(float(mom_cap_y))*0.95
    yMu = int(float(mom_cap_y))
    yK1_K0 = 1
    yK2_K0 = 0.0001
    col_properties.write_member_properties(file_path,col_w,col_h,ec,xMc,xMy,xMu,xK1_K0,xK2_K0,yMc,yMy,yMu,yK1_K0,yK2_K0)

    # 5 B
    # Popualte main properties of structural elements - BEAM
    beam_w = int(float(beam_width)*1000) # mm
    beam_h = int(float(beam_height)*1000)
    ec = young_modul/(10**6)
    xMc = int(float(mom_cap_beam))*0.9
    xMy = int(float(mom_cap_beam))*0.95
    xMu = int(float(mom_cap_beam))
    xK1_K0 = 1
    xK2_K0 = 0.0001
    yMc = int(float(mom_cap_beam))*0.9
    yMy = int(float(mom_cap_beam))*0.95
    yMu = int(float(mom_cap_beam))
    yK1_K0 = 1
    yK2_K0 = 0.0001
    beam_properties.write_member_properties(file_path, beam_w, beam_h, ec, xMc, xMy, xMu, xK1_K0, xK2_K0, yMc, yMy, yMu,yK1_K0, yK2_K0)
    # 5 C
    # Popualte main properties of structural elements - rest of the properties up to FLOOR: WALL and EXT_SPRING
    member_properties.wall_properties(file_path)
    member_properties.ext_spring_properties(file_path)
    # 5 D
    # Popualte main properties of structural elements - FLOOR
    thick = 150
    fc = 2400 # std value
    ec = young_modul/(10**6) # std value
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
    def story_mass_calc(x_span,y_span,height,col_w,col_h,beam_w,beam_h,plate_t,no_x_span,no_y_span,py):
        # all calc is done in m and kg although the inputs are in mm
        no_col = (no_x_span+1)*(no_y_span+1)
        one_col_vol = col_w * col_h * height * 10**(-9)
        no_beams_x = (no_y_span+1) * no_x_span
        no_beams_y = (no_x_span+1) * no_y_span
        one_beam_vol_x = beam_h * beam_w * x_span * 10**(-9)
        one_beam_vol_y = beam_h * beam_w * y_span * 10**(-9)
        plate_volume = (no_x_span * x_span + no_y_span * y_span) * plate_t * 10**(-9)
        rho = 25  # kN/m3
        py = py  # in kN/m
        current_story_beam_distributed_weight = (no_beams_x * x_span/1000 +no_beams_y * y_span/1000) * py
        # print(current_story_beam_distributed_weight)

        normal_weight = (no_col * one_col_vol + no_beams_x * one_beam_vol_x +no_beams_y * one_beam_vol_y + plate_volume)  * rho + current_story_beam_distributed_weight
        last_story_weight = (no_col * one_col_vol /2 + no_beams_x * one_beam_vol_x +no_beams_y * one_beam_vol_y + plate_volume)  * rho + current_story_beam_distributed_weight
        return normal_weight, last_story_weight
    x_span = int(float(span)*1000)
    y_span = int(float(bay)*1000)

    height = int(float(story_height)*1000)
    story_weight, last_story_weight = story_mass_calc(x_span,y_span,height,col_w,col_h,beam_w,beam_h,thick,no_x_spans,no_y_spans,py)  # [kN]



    amp_x = float(scale_factor)
    amp_y = float(scale_factor)
    amp_z = 1

    # out goes weight and load distribution - to be used in writing specific files for them
    weight_distribution,load_distribution = general_model_info_2.write_model_info_2(file_path, x_span, no_x_spans, y_span, no_y_spans, no_of_floors, height, story_weight,last_story_weight, amp_x, amp_y,
                       amp_z,py)
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

        try:
            if os.path.isdir(source_path):
                # continue
                shutil.copytree(source_path, destination_path, symlinks=False, ignore=None)

            else:
                shutil.copy2(source_path, destination_path)
                # breakpoint()
            return  # Success, exit the loop
        except PermissionError:
            print(f"PermissionError: {source_path} is in use, retrying...")


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

    database_folder = os.path.join(Path(__file__).parents[1],"DATABASE") #"D:\\0 DOCTORAT\\00_RC2\Ruben_Vasile"
    database_file = "30000_BUILDINGS.csv"
    database_file_location = os.path.join(database_folder,database_file)
    def testing_of_alg(database_file_location):
        # number_of_rows_to_read = 33
        number_of_rows_to_read = 5
        rows_to_be_read_list = [x for x in range(number_of_rows_to_read+1)] #if x % 2 == 0]
        # rows_to_be_read_list = [1,2,3]
        # print(rows_to_be_read_list)
        # print()
        # breakpoint()
        # Use pd.read_csv on the modified string
        df = pd.read_csv((database_file_location),
                         skiprows=lambda x: x not in rows_to_be_read_list)  # second option, skip some rows
        # print(df)
        return df
    def full_alg_database(database_file_location):
        df = pd.read_csv((database_file_location))
        return df

    df = testing_of_alg(database_file_location)
    # Specify the condition for rows to keep
    condition_to_remove_L_shape_buildings = (df['Lshape'] != 1)
    # print(condition_to_remove_L_shape_buildings)
    # Filter the DataFrame based on the condition
    df_filtered = df[condition_to_remove_L_shape_buildings]
    # print(df_filtered)
    return df_filtered
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
    py =                        df["py"]
    young_modul =               df["E"]
    mom_cap_x =                 df["MstX"]
    mom_cap_y =                 df["MstY"]
    mom_cap_beam =              df["Mgr"]

    unique_index =              df["index"]

    input_set_list = [index_of_accelerogram_set,timestep,scale_factor,story_height,building_height,span,bay,
                      no_story,no_span,no_bay,csi,col_width1,col_width2,beam_width,beam_height,py,young_modul,
                      mom_cap_x,mom_cap_y,mom_cap_beam,unique_index]
    # modified_list=[] #to  single_value TYPE (not list)
    # for item in range(len(input_set_list)):
    #     modified_list.append(public_func.df_singular_to_string(input_set_list[item]))

    return input_set_list



def main_call_per_process(df):#,processes):
    start_time_process = time.time()
    df_and_index = df
    input_list = database_parameter_selection(df_and_index)

    output_inputdata_file = "inputdata.txt"

    # today = date.today()
    date_now = datetime.now().strftime("%d-%m-%Y_%H-%M")
    print(date_now)
    # breakpoint()
    # date_now = "14.03"
    folder_of_output_all_simulations = "OUTPUT_" + date_now
    parent_folder = os.path.join(Path(__file__).parents[1],folder_of_output_all_simulations) #"D:\\0 DOCTORAT\\00_RC2\\Testare_generare_cladiri_Stera\\dummy_foler_test"
    big_log_file = "log.txt"
    input_folder = "input"
    output_folder = "output"

    def is_one_digit(number):
        return 0 <= abs(number) <= 9
    unique_folder_name = (int(input_list[-1]))
    if is_one_digit(unique_folder_name):
        unique_folder_name = "ID-0" + str(int(input_list[-1]))
    else:
        unique_folder_name = f"ID-{str(unique_folder_name)}"

    # breakpoint()

    weight_distribution,load_ditribution = inputdata_generator(output_inputdata_file,unique_folder_name,parent_folder,input_folder,output_folder,input_list)

    # THE CSV files are in m/s^2 and needs to be in cm/s^2 - they are scaled to meet correct UNITS inside the functions
    wave_folder = os.path.join(Path(__file__).parents[1],"ACCEL_SET")#"D:\\0 DOCTORAT\\00_RC2\Ruben_Vasile\ACCEL_SET"
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

    seed_folder = os.path.join(Path(__file__).parents[1],"SEED_FOLDER")#"D:\\0 DOCTORAT\\00_RC2\Testare_generare_cladiri_Stera\SEED_FOLDER"
    stera_call = "CALL_RESPONSE.bat"
    response_exe = "Response.exe"
    unique_folder = os.path.join(parent_folder,unique_folder_name)
    copy_prereq_from_seed_folder(seed_folder,stera_call,response_exe,unique_folder)
    # THis is necessary - is seems it does not create the folder by itself
    # create output folder and data_structure.txt file
    create_output_folder = Path(parent_folder, unique_folder_name, output_folder).mkdir(parents=True,exist_ok=True)
    processes = []
    # processes = run_response(unique_folder,stera_call,processes)
    run_response(unique_folder, stera_call, processes)
    print(f"Processing row {df_and_index['index']}")
    # Assuming "100 % finished" is the last line written to the file
    stdout_file = os.path.join(unique_folder, "stdout.txt")

    while True:
        try:
            with open(stdout_file, "r") as f:
                # Read all lines and check the last line
                lines = f.readlines()
                if lines and lines[-1].strip() == "100 % finished":
                    # Calculate the elapsed time for the current process
                    elapsed_time_process = time.time() - start_time_process
                    processing_string = f"Processing row {df['index']} - 100% finished. Elapsed time: {elapsed_time_process:.2f} seconds"
                    print(processing_string)
                    with open (os.path.join(parent_folder,big_log_file), "a+") as file:
                        file.write(processing_string)
                        file.write("\n")

                    break

        except FileNotFoundError:
            # Handle the case when stdout.txt is not found (process hasn't started yet)
            pass
        # Wait for a while before checking again
        # time.sleep(5)
    # return processes
    return


def generate_tasks(df):
    for _, row in df.iterrows():
        yield row

def process_rows(executor, tasks):
    futures = set()

    for task in tasks:
        future = executor.submit(main_call_per_process, df=task)
        futures.add(future)

    # Wait for all submitted futures to complete
    for future in as_completed(futures):
        try:
            # Retrieve the result (if needed)
            result = future.result()
            # Handle the result if needed
        except Exception as e:
            # Handle exceptions if needed
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Code to create and start processes
    df = read_database_Ruben_Vasile()
    # Add index to the DATAFRAME
    df = df.reset_index()

    start_time_acc = datetime.now()

    # Use ProcessPoolExecutor for parallel processing with max_workers=3
    max_workers = 15
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        # Create a generator to yield tasks one by one
        task_generator = generate_tasks(df)


        # Semaphore to limit the number of concurrently running tasks
        semaphore = threading.Semaphore(max_workers)

        # Submit tasks and wait for them to complete
        process_rows(executor, task_generator)

    end_time_acc = datetime.now()

    parent_folder = Path(__file__).parents[1]
    big_log_file = "log.txt"
    processing_string = 'TIME ELAPSED: ' + str(end_time_acc - start_time_acc) + '\n'
    with open(os.path.join(parent_folder, big_log_file), "a+") as file:
        file.write(processing_string)
        file.write("\n")

    print(processing_string)

p = Path(__file__).parents[1]

print(p)