###############################
# PROJECT MADE FOR BUILDING GENERATION FOR RCS2_DOCTORATE DATABASE - MADE FOR RESPONSE RUNNING
# PRESENT CODE IS FOR „INPUTDATA.TXT” FILE GENERATION
# 3) Member Type

# CLASSES NEEDED: 1) - MEMBER PROPERTIES (BEAM,COLOUMN, WALL, ISOLATOR, ....)
#                 2)  Class for 2 lines options (ex:Nonlinear Flexural Spring (0:Not considered, 1:Considered) = (newline) 1)


from pathlib import Path
import os
import numpy as np
import public_func

def model_member_type(no_of_floors, no_x_spans, no_y_spans,input_file_location):  # folder output will be overwritten
    #####################################################
    #                    DESCRIPTION                    #
    #####################################################

    # @brief                        -       populate "inputdata.txt" with output files location and create
    #                                       unique folder for the output of STERA
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
    # list_of_output_properties     -       list of Stera properties
    # input_values_list             -       make a list from inputs
    # value_list_of_options         -       values of the above list with some initial params
    # @return                       -

    #####################################################
    # Check input data
    public_func.check_data(no_of_floors, int)
    public_func.check_data(no_x_spans, int)
    public_func.check_data(no_y_spans, int)

    # List is predetermined by STERA 3D
    list_of_headers = ["Member type number",
                            "(0: nothing, 1: Column, 2: Beam, 3: Wall, 4: Spring, 5: Floor, 6: Damper, 7: Masonry, 8: Isolator)",
                            "Member property number"]

    # Input_values_lsit
    input_values_list = [no_of_floors, no_x_spans, no_y_spans]
    def floor_matrix():
        matrix_property = np.zeros(((no_y_spans * 2) + 1, (no_x_spans * 2) + 1), dtype=int)
        for y in range(0, (no_y_spans * 2) + 1):
            for x in range(0, (no_x_spans * 2) + 1):
                if (x % 2 == 0) and (y % 2 == 0):
                    matrix_property[y, x] = 4       # option: 4 (for spring)
        return matrix_property
    # Creatix matrix (spans x2)+1
    matrix_property = np.zeros(((no_y_spans*2)+1, (no_x_spans*2)+1), dtype=int)
    for y in range(0,(no_y_spans*2)+1):
        for x in range(0,(no_x_spans*2)+1):
            if ((x % 2 == 0) and (y % 2 == 0)):     # the indices are reversed in terms od odd and even because it is 0-indexed, not 1-indexed
                matrix_property[y,x] = 1                 # column
            elif ((x % 2 == 0) and (y % 2 != 0)):
                matrix_property[y,x] = 2                 # beam
            elif ((x % 2 != 0) and (y % 2 == 0)):
                matrix_property[y,x] = 2                 # beam
            elif ((x % 2 != 0) and (y % 2 != 0)):
                matrix_property[y,x] = 5                 # floor

# Write Member type number
    with open(input_file_location, "a") as file:
        file.write("\n")
        file.write(str(list_of_headers[0]))
        file.write("\n")
        file.write(str(list_of_headers[1]))
        file.write("\n")
        for floor in range(no_of_floors):
            file.write("     "+str(floor))
            if floor == 0:
                matrix_of_zeros = np.zeros(((no_y_spans*2)+1, (no_x_spans*2)+1), dtype=int)
                matrix = floor_matrix()
                public_func.member_property_write_with_spaces(file,matrix)
                # public_func.member_property_write_with_spaces(file,matrix_of_zeros)
            else:   # Here we have the type of element (ex: C1, C2, and so on)
                public_func.member_property_write_with_spaces(file, matrix_property)
            file.write("\n")

# Write Member property type number
    with open(input_file_location, "a") as file:
        file.write(str(list_of_headers[2]))
        file.write("\n")
        for floor in range(no_of_floors):
            file.write("     " + str(floor))
            matrix_of_ones = np.ones(((no_y_spans * 2) + 1, (no_x_spans * 2) + 1), dtype=int)
            public_func.member_property_write_with_spaces(file, matrix_of_ones)
            file.write("\n")
