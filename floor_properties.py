###############################
# PROJECT MADE FOR BUILDING GENERATION FOR RCS2_DOCTORATE DATABASE - MADE FOR RESPONSE RUNNING
# PRESENT CODE IS FOR „INPUTDATA.TXT” FILE GENERATION
# 4) Options For Structure / Members / Dynamic Analysis

# CLASSES NEEDED: 1) - MEMBER PROPERTIES (BEAM,COLOUMN, WALL, ISOLATOR, ....)
#                 2)  Class for 2 lines options (ex:Nonlinear Flexural Spring (0:Not considered, 1:Considered) = (newline) 1)


from pathlib import Path
import os
import public_func
def write_member_properties(input_file_location,thick,fc,ec):  # folder output will be overwritten
    #####################################################
    #                    DESCRIPTION                    #
    #####################################################

    # @brief                        -       populate "inputdata.txt" with different options for: structure, member,
    #                                       analysis
    ###############
    #   param_in  TYPE: int for ALL except initial settings #
    ###############
    # it seems all the params are default values
    # input_file_location           -       Full path to "inputdata.txt"                               TYPE: string
    # thick                         -       thickness
    # fc                            -       Force ?
    # ec                            -       Young's Modulus
    ###############
    #   params    #
    ###############

    #
    #
    # @return                       -

    #####################################################

    # List is predetermined by STERA 3D (maybe would be better to write it with DF, for now we use dict)

    floor_properties_dict = {"Member Properties (Floor)": "",
                                       public_func.five_spaces+"n        Type       thick          Fc          Ec": ""
                                       }

    # Lists with values for members
    type = 1
    floor_properties_values_list = [type, thick, fc, ec]
    with open(input_file_location, "a") as file:
        public_func.dict_write(floor_properties_dict, file)
        public_func.general_member_write(floor_properties_values_list, file)