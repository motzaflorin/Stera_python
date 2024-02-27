###############################
# PROJECT MADE FOR BUILDING GENERATION FOR RCS2_DOCTORATE DATABASE - MADE FOR RESPONSE RUNNING
# PRESENT CODE IS FOR „INPUTDATA.TXT” FILE GENERATION
# 4) Options For Structure / Members / Dynamic Analysis

# CLASSES NEEDED: 1) - MEMBER PROPERTIES (BEAM,COLOUMN, WALL, ISOLATOR, ....)
#                 2)  Class for 2 lines options (ex:Nonlinear Flexural Spring (0:Not considered, 1:Considered) = (newline) 1)


from pathlib import Path
import os
import public_func

def write_member_properties(input_file_location,col_w,col_h,ec,xMc,xMy,xMu,xK1_K0,xK2_K0,yMc,yMy,yMu,yK1_K0,yK2_K0):  # folder output will be overwritten
    #####################################################
    #                    DESCRIPTION                    #
    #####################################################

    # @brief                        -       populate "inputdata.txt" with different options for: structure, member,
    #                                       analysis
    ###############
    #   param_in  TYPE: int for ALL except initial settings #
    ###############
    # input_file_location           -       Full path to "inputdata.txt"                               TYPE: string
    # col_w                         -       col width
    # col_h                         -       col height
    # ec                            -       times 1000  =  Young's modulus
    # xMc                           -       x-Axis M - linear end point (C)
    # xMy                           -       x-Axis M - yield point (Y)
    # xMu                           -       x-axis M - ultimate value (U)
    # xK1_K0                        -       x-axis 1st slope  (resulting in Rotation for point 2nd point here the My-Ry - point)
    # xK2_K0                        -       x-axis 2nd slope    (resulting in Rotation for point 3rd point here the Mu-Ru - point)
    # yMc                           -       y-Axis M - linear end point (C)
    # yMy                           -       y-Axis M - yield point (Y)
    # yMu                           -       y-Axis M - ultimate value (U)
    # yK1_K0                        -       y-Axis 1st slope
    # yK2_K0                        -       y-Axis 2nd slope
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

    # List is predetermined by STERA 3D (maybe would be better to write it with DF, for now we use dict)

    column_properties_dict = {"Member Properties (Column)"                                            :"",
                            "(RC,SRC)   n   Width(mm)  Height(mm)      d1(mm)      d2(mm)     vsize_C       vno_X     vsize_X       vno_Y     vsize_Y    vSD(MPa)       sno_X     ssize_X    sspace_X       sno_Y     ssize_Y    sspace_Y    sSD(MPa)     Fc(MPa)     Ec(MPa)     str.amp      S_type     S_width    S_height       S_web     S_flang     Fy(MPa)"                        :"",
                            "(S)        n   Width(mm)  Height(mm)         web      flange     Fy(MPa)      C_type     str.amp       k2/k0       Ramda    ID_Ramda"  :"",
                            "(Direct)   n   Width(mm)  Height(mm)   Ec(N/mm2)    xMc(kNm)    xMy(kNm)    xMu(kNm)     xK1/xK0     xK2/xK0    yMc(kNm)    yMy(kNm)    yMu(kNm)     yK1/yK0     yK2/yK0          r1          r2          r3       Ramda    ID_Ramda       htype"                                         :""
                              }


    # Lists with values for members                                                                         # last 6 values are for RC,SRC model - should be ignored in Direct definition
    r1 = 0.5        #   Stiffness degrading ratio
    r2 = 0          #   Slip Stiffness  ratio
    r3 = 0          #   Strength Degrading ratio
    # Steel properties
    Ramda = 60      #   Buckling
    ID_Ramda = 0    # NA
    htype = 0       # NA
    col_properties_values_list = [col_w,col_h,ec,xMc,xMy,xMu,xK1_K0,xK2_K0,yMc,yMy,yMu,yK1_K0,yK2_K0,r1,r2,r3,Ramda,ID_Ramda,htype,110,0,0,0,0,0,0]
    with open(input_file_location, "a") as file:
        public_func.dict_write(column_properties_dict, file)
        public_func.general_member_write(col_properties_values_list,file)