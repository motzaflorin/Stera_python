#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
# PROJECT MADE FOR BUILDING GENERATION FOR RCS2_DOCTORATE DATABASE - MADE FOR RESPONSE RUNNING
# PRESENT CODE IS FOR „INPUTDATA.TXT” FILE GENERATION
# 2) GENERAL INFORMATION
# CLASSES NEEDED: 1) - MEMBER PROPERTIES (BEAM,COLOUMN, WALL, ISOLATOR, ....)
#                 2)  Class for 2 lines options (ex:Nonlinear Flexural (0:Not considered, 1:Considered) = (newline) 1)
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################

from pathlib import Path
import os
import public_func


def output_folder_for_stera_files(text_file, unique_folder_name, parent_folder, input_folder, output_folder):  # folder output will be overwritten
    #####################################################
    #                    DESCRIPTION                    #
    #####################################################

    # @brief                        -       populate "inputdata.txt" with general information about output members,
    #                                       type of analysis, stories,spans
    ###############
    #   param_in  #
    ###############
    # text_file                     -       text_file for data to be written to \ appended to                               TYPE: string
    # unique_folder_name            -       folder which needs to be created for each new instance of BUILDING-QUAKE pair   TYPE: string
    # parent_folder                 -       the whole address of the project location \\ Should exist                       TYPE: string
    #
    ###############
    #   params    #
    ###############
    # list_of_output_files          -       static list with names of output files
    # create_unique_name_folder     -       check and create if it does not exist, the unique_folder_name
    # active_file                   -       file name to be written in the inputdata.txt
    #
    #
    # @return                       -

    #####################################################
    # Check input data
    public_func.check_data(text_file, str)
    public_func.check_data(unique_folder_name, str)
    public_func.check_data(parent_folder, str)

    # List is predetermined by STERA 3D
    list_of_output_files = ["data_structure.txt", "data_column.txt", "data_beam.txt", "data_wall.txt", "data_floor.txt",
                            "data_damper.txt","data_spring.txt", "data_bi.txt", "data_panel.txt", "data_ground.txt", "data_pulley.txt",
                            "max_structure.txt","max_column.txt", "max_beam.txt", "max_wall.txt", "max_floor.txt", "max_damper.txt",
                            "max_spring.txt", "max_bi.txt", "max_panel.txt","max_ground.txt", "max_pulley.txt", "max_node.txt", 'response_eigen.txt',
                            'response_structure.txt', 'response_energy.txt']



    # Check OUTPUT_FOLDER for EACH ID and create one if it does not exist
    create_unique_name_folder = Path(parent_folder,unique_folder_name,input_folder).mkdir(parents=True,exist_ok=True)
    # full_path
    inputdata_file_full_path = os.path.join(parent_folder, unique_folder_name, input_folder, text_file)
    # Write type of setting for STERA - 0 INITIAL    1 CONTINUOUS ?? (I THINK? - SHOULD BE CHECKED)
    # then the contents of output_location
    with open(inputdata_file_full_path, "w") as file:
        file.write("0")  # INITIAL
        for stera_output_file in list_of_output_files:
            active_file = public_func.generate_joined_string(parent_folder,unique_folder_name,output_folder,stera_output_file)
            file.write("\n")
            file.write(active_file)

    # return path_of_folder_output
