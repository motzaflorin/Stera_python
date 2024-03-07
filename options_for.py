###############################
# PROJECT MADE FOR BUILDING GENERATION FOR RCS2_DOCTORATE DATABASE - MADE FOR RESPONSE RUNNING
# PRESENT CODE IS FOR „INPUTDATA.TXT” FILE GENERATION
# 4) Options For Structure / Members / Dynamic Analysis

# CLASSES NEEDED: 1) - MEMBER PROPERTIES (BEAM,COLOUMN, WALL, ISOLATOR, ....)
#                 2)  Class for 2 lines options (ex:Nonlinear Flexural Spring (0:Not considered, 1:Considered) = (newline) 1)


from pathlib import Path
import os
import public_func


def write_options(input_file_location):  # folder output will be overwritten
    #####################################################
    #                    DESCRIPTION                    #
    #####################################################

    # @brief                        -       populate "inputdata.txt" with different options for: structure, member,
    #                                       analysis
    ###############
    #   param_in  TYPE: int for ALL except initial settings #
    ###############
    # input_file_location           -       Full path to "inputdata.txt"                               TYPE: string
    #
    ###############
    #   params    #
    ###############
    # options_strcture_list     -       static list with output parameters
    # options_members_list     -       check and create if it does not exist, the unique_folder_name
    # options_analysis_list                   -       file name to be written in the inputdata.txt
    #
    #
    # @return                       -

    #####################################################

    # List is predetermined by STERA 3D
    options_strcture_dict = {"Options for structure"                                            :"",
                            "P-Delta effect (0: no P-Delta, 1: P-Delta)"                        :"0",
                            "Mass distribution (0: Same for all nodes, 1: Proportion to area)"  :"1",
                            "No. of restrained freedom"                                         :"0"}

    options_members_dict = {"Options for members"                                               :"",
                            "Column(0: RC, 1: S, 2: SRC, 3: Direct, 3: Mixed)"                  : "3",
                            "Beam(0: RC, 1: S, 2: SRC, 3: Direct, 3: Mixed)"                    : "3",
                            "Wall(0: RC, 1: S, 2: SRC, 3: Direct, 3: Mixed)"                    : "0",
                            "Floor Slab (0:2D Rigid, 1:3D Rigid, 2:Flexible, 3:Mixed)"          : "2",  # was rigid -> 0
                            "Ground Spring (0:None, 1:Cone model, 2:Direct)"                    : "0",
                            "Isolator(0:Not considered, 1: Considered)"                         : "0",
                            "Passive Damper (0:Not considered, 1:Considered)"                   : "0",
                            "Masonry Wall (0:Not considered, 1:Considered)"                     : "0",
                            "External Spring (0:Not considered, 1:Considered)"                  : "0",
                            "Nonlinear Shear Spring (0:Not considered, 1:Considered)"           : "1", # 1
                            "Nonlinear Flexural Spring (0:Not considered, 1:Considered)"        : "1", # 1 -was
                            "Pulley Damper (0:Not considered, 1:Considered)"                    : "0",
                            "Young_s Modulus (GPa)"                                             : "210",
                            "Rebar Size Table (0. Japan/ U.S., 2. Euro)"                        : "1"}

    options_analysis_dict = {"Options for dynamic analysis"                                      :"",
                             "Number of division of time interval"                              : "5",
                             "Damping type  (0. [C]=a[K0], 1. [C]=a[Kp], 2. [C]=a[K0]+b[M])"    : "2",
                             "Damping factors"                                                  : "",
                             str(public_func.five_spaces)+"h1"+str(public_func.five_spaces)+"h2"                        : [0.05,0.05],
                             "Numerical integration (0: Average acceleration method, 1: Operator splitting method)"     : "0",
                             "Type of dynamic input (0: Ground acceleration, 1: Vibrator on a floor, 2: Wind pressure)" : "0",
                             "Number of floor installing a vibrator"                            : "0"}


    with open(input_file_location, "a") as file:
        public_func.dict_write(options_strcture_dict, file)
        public_func.dict_write(options_members_dict, file)
        public_func.dict_write(options_analysis_dict,file)

    # return path_of_folder_output
