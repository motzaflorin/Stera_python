###############################
# PROJECT MADE FOR BUILDING GENERATION FOR RCS2_DOCTORATE DATABASE - MADE FOR RESPONSE RUNNING
# PRESENT CODE IS FOR „INPUTDATA.TXT” FILE GENERATION
# 4) Options For Structure / Members / Dynamic Analysis

# CLASSES NEEDED: 1) - MEMBER PROPERTIES (BEAM,COLOUMN, WALL, ISOLATOR, ....)
#                 2)  Class for 2 lines options (ex:Nonlinear Flexural Spring (0:Not considered, 1:Considered) = (newline) 1)


from pathlib import Path
import os
import public_func


def floor_data_generation(no_floors, height,weight, last_story_weight):
    floor_data_list = [[0,0,0] for floor in range(no_floors)]
    for floor in range(no_floors):
        if floor == 0:
            floor_data_list[floor] = [0, 0, 0]
        elif floor == no_floors - 1 :
            floor_data_list[floor] = [floor, height, last_story_weight]
        else:
            floor_data_list[floor] = [floor, height, weight]
    return floor_data_list

def determine_position_type(matrix, i, j):
    rows, cols = len(matrix), len(matrix[0])

    if i == 0 or i == rows - 1:
        if j == 0 or j == cols - 1:
            return "Corner"
        else:
            return "Marginal"
    elif j == 0 or j == cols - 1:
        return "Marginal"
    else:
        return "Center"
def weight_node_distribution(floor,no_x_spans,no_y_spans,x_span,y_span,current_story_weight,last_story_weight,no_floors):
    # wigth on node is in [N]
    def node_calculation (matrix_of_weights,x_span,y_span,weight,area):
        for row in range(len(matrix_of_weights)):
            for element in range(len(matrix_of_weights[row])):
                if (determine_position_type(matrix_of_weights,row,element) == "Corner"):
                    matrix_of_weights[row][element] = (x_span/2 * y_span/2) * weight/area *1000
                elif (determine_position_type(matrix_of_weights,row,element) == "Marginal"):
                    matrix_of_weights[row][element] = (x_span * y_span/2) * weight/area *1000
                elif (determine_position_type(matrix_of_weights,row,element) == "Center"):
                    matrix_of_weights[row][element] = (x_span * y_span) * weight/area *1000
        return matrix_of_weights
    matrix_of_weights = [[2*span for span in range(no_x_spans+1)] for span in range(no_y_spans+1)]
    area = (no_x_spans * x_span) * (no_y_spans * y_span)

    if floor == 0:
        return [[0 for span in range(no_x_spans+1)] for span in range(no_y_spans+1)]
    elif floor == no_floors -1:
        return node_calculation(matrix_of_weights,x_span,y_span,last_story_weight,area)
    else:
       return node_calculation(matrix_of_weights,x_span,y_span,current_story_weight,area)


def write_model_info_2(input_file_location,x_span,no_x_spans,y_span,no_y_spans,no_floors,height,weight,last_story_weight,amp_x,amp_y,amp_z):  # folder output will be overwritten
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
    # span data on x needs to reach 30 entries, and on y 20 entries
    span_data_dict =        {"Span data"                          :"",
                            "      X (mm)"                        :[ x_span for times in range(no_x_spans) ] + [0] * (30 - no_x_spans),
                            "      Y (mm)"                        :[ y_span for times in range(no_y_spans) ] + [0] * (20 - no_y_spans)
                            }

    floor_data_fict =       {"Floor data"                                                        :"",
                            public_func.five_spaces+"F  height(mm)  weight(kN)"                  : floor_data_generation(no_floors, height,weight,last_story_weight)
                            }

    weight_node_dict = {"Weight on each node (N)": ""}
    weight_node_dict.update({public_func.five_spaces+f'{floor}': weight_node_distribution(floor,no_x_spans,no_y_spans,x_span,y_span,weight,last_story_weight,no_floors) for floor in range(no_floors)})

    connection_panel_dict = {"Connection Panel": "",
                      public_func.five_spaces+"type effec.ratio": [1,1]
                      }
    ground_spring_dict = {"Ground Spring": "",
                          "(Cone)            F_RKhx      F_IKhx      F_RKry      F_IKry      F_RKrx      F_IKrx       F_Chx       F_Cry       F_Crx      P_RKhx      P_IKhx       P_Chx      P_RKhy      P_IKhy       P_Chy      P_RKry      P_RKrx      P_IKry      P_IKrx        Wh1X         IhX          e+         IhY          e+": "",
                          "(Direct)           D_Khx          e+       D_Chx          e+       D_Khy          e+       D_Chy          e+       D_Kry          e+       D_Cry          e+       D_Krx          e+       D_Crx          e+                                            Wh1X         IhX          e+         IhY          e+": [0 for no in range(25)]
                         }
    pully_damper_node_dict = {"Pully Damper Node": [[-1 for times in range(6)] for times in range(10)]
                              }

    # Add elements as new list to get the effect of column liek list
    rebar_size_table_list = [2827,5027,7854,11310,15394,20106,31416,49087,61575,80425,125664,196350,0,0,0,0,0,0,0,0,0,0,0,0]
    transpose_rebar_size_table_list = []
    for item in range(len(rebar_size_table_list)):
        transpose_rebar_size_table_list.append([rebar_size_table_list[item]])

    rebar_size_table_dict  = {"Rebar Size Table":transpose_rebar_size_table_list}

    load_distribution_dict = {"Load distribution at each floor": "",
                              public_func.five_spaces+"F     load(X)     load(Y)     load(Z)": [[floor]+[0 for item in range(3)] for floor in range(no_floors)],
                              }
    static_load_cond_dict = {"Static Load Condition": "",
                             "   Direction (1: x, -1: -x, 2: y, -2: -y, 3: z)"                                              :"1",
                             "   Distribution (1: Ai, 2: Tri-angular, 3: Uniform, 4:UBC, 5:ASCE, 6:Mode, 7:User defined)"   :"1",
                             "   Target drift (1: 1/50, 2: 1/100, 3: 1/200, 4: cyclic)"                                     :"1",
                             "   Total number of segments"                                                                  :"1",
                             "     segment        step        from          to"                                  :[0,500,0,0.02],
                             }
    dynamic_load_cond_dict = {"Dynamic Load Condition" : "",
                              " Amplification factors" : "",
                              public_func.five_spaces+"x           y           z"                               :[amp_x,amp_y,amp_z]
                              }

    with open(input_file_location, "a") as file:
        public_func.dict_write(span_data_dict,file)
        public_func.dict_write(floor_data_fict,file)
        public_func.dict_write(weight_node_dict, file)
        public_func.dict_write(connection_panel_dict, file)
        public_func.dict_write(ground_spring_dict, file)
        public_func.dict_write(pully_damper_node_dict, file)
        public_func.dict_write(rebar_size_table_dict, file)
        public_func.dict_write(load_distribution_dict, file)
        public_func.dict_write(static_load_cond_dict, file)
        public_func.dict_write(dynamic_load_cond_dict, file)

    return weight_node_dict,load_distribution_dict