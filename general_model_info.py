###############################
# PROJECT MADE FOR BUILDING GENERATION FOR RCS2_DOCTORATE DATABASE - MADE FOR RESPONSE RUNNING
# PRESENT CODE IS FOR „INPUTDATA.TXT” FILE GENERATION
# 1) OUTPUT LOCATION FILLING SCRIPT

# CLASSES NEEDED: 1) - MEMBER PROPERTIES (BEAM,COLOUMN, WALL, ISOLATOR, ....)
#                 2)  Class for 2 lines options (ex:Nonlinear Flexural Spring (0:Not considered, 1:Considered) = (newline) 1)


from pathlib import Path
import os
import public_func

def model_info(analysis_case, no_of_floors, no_x_spans, no_y_spans,input_file_location):  # folder output will be overwritten
    #####################################################
    #                    DESCRIPTION                    #
    #####################################################

    # @brief                        -       populate "inputdata.txt" member property
    ###############
    #   param_in  TYPE: int for ALL except initial settings #
    ###############
    # input_file_location           -       Full path to "inputdata.txt"                               TYPE: string
    # analysis_case                 -       Case to be run: modal, static, dynamic
    # no_of_floors                  -       floors in the model (+1 for base level)
    # no_x_spans                    -       Number of spans in X direction
    # no_y_spans                    -       Number of spans in Y direction
    #
    ###############
    #   params    #
    ###############
    # list_of_output_properties     -       static list with output parameters
    # create_unique_name_folder     -       check and create if it does not exist, the unique_folder_name
    # active_file                   -       file name to be written in the inputdata.txt
    #
    #
    # @return                       -

    #####################################################
    # Check input data
    public_func.check_data(analysis_case, int)
    public_func.check_data(no_of_floors, int)
    public_func.check_data(no_x_spans, int)
    public_func.check_data(no_y_spans, int)

    # List is predetermined by STERA 3D
    list_of_output_properties = ["Number of output members",
                            "Number of pulley damper",
                            "Number of complete rigid floor",
                            "Analysis case(1:mode, 2: static, 3: dynamic)",
                            " Max.number of floor",
                            "Max.number of x - span",
                            " Max.number of y - span"]

    # Input_values_lsit
    input_values_list = [analysis_case, no_of_floors, no_x_spans, no_y_spans]
    # Create value_list of options
    value_list_of_options = []
    for option in range(len(list_of_output_properties)):
        if option < 3:
            # Usually this options are 0
            value_list_of_options.append("0")
        else:
            value_list_of_options.append(str(input_values_list[option-3]))

    with open(input_file_location, "a") as file:
        for property in range(len(list_of_output_properties)):
            file.write("\n")
            file.write(list_of_output_properties[property])
            file.write("\n")
            file.write(public_func.five_spaces)
            file.write((value_list_of_options[property]))

    # return path_of_folder_output
