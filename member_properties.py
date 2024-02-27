###############################
# PROJECT MADE FOR BUILDING GENERATION FOR RCS2_DOCTORATE DATABASE - MADE FOR RESPONSE RUNNING
# PRESENT CODE IS FOR „INPUTDATA.TXT” FILE GENERATION
# 4) Options For Structure / Members / Dynamic Analysis

# CLASSES NEEDED: 1) - MEMBER PROPERTIES (BEAM,COLOUMN, WALL, ISOLATOR, ....)
#                 2)  Class for 2 lines options (ex:Nonlinear Flexural Spring (0:Not considered, 1:Considered) = (newline) 1)


from pathlib import Path
import os
import public_func



# List is predetermined by STERA 3D (maybe would be better to write it with DF, for now we use dict)
member_type_dict =      {"Member structural type": "",
                        "type     C     B     W     F     (C,B 1:RC, 2:S, 3:SRC, 4:Direct) (W 1:RC, 2:S, 3:Direct) (F 1:2D rigid, 2:3D rigid, 3:Flexible)": ""}


wall_properties_dict = {"Member Properties (Wall)":         "",
                        "(RC,SRC)   n   Thick(mm)         sno       ssize      sspace         sSD     Fc(MPa)     Ec(MPa)     str.amp   stf.reduc   str.reduc     As(mm2)     R(deg.)   Fy(N/mm2)"      :       "",
                        "(Brace)    n    Beam No.     Br.Type      A(mm2)   Fy(N/mm2)       Ramda    ID_Ramda"          :       "",
                        "(Direct)   n      S.Type      B.Type      Q1(kN)      Q2(kN)      Q3(kN)   K0(kN/mm)       K1/K0       K2/K0       K3/K0          d1          d2          d3     QM1(kN)    e+           QM2(kN)    e+           QM3(kN)    e+         K0(kN/mm)    e+             K1/K0       K2/K0       K3/K0          d1          d2          d3   Kv(kN/mm)    e+"        :       ""
                        }
external_spring_properties_dict = {"Member Properties (External Spring)" : "",
                                   "(support: 1-Pin, 2-Spring, stype: 0-Elastic, 1-Lift up)": "",
                                   public_func.five_spaces+"n     support       stype          k0          k1          k2          c0           B": ""
                                   }
isolator_properties_dict = {"Member Properties (Isolator)": "",
                                   public_func.five_spaces+"n    Iso.Type   Hyst.Type   No.Spring       Kv/K0   K0(kN/mm)       K1/K0      Fy(kN)          D1          D2          D3    Energy.R          p1          p2          p3          p4          p5          p6          p7          p8": ""
                                   }
damper_properties_dict = {"Member Properties (Damper)": "",
                         public_func.five_spaces+"n    Beam No.      D.Type      H.Type      V.Type      F1(kN)      F2(kN)      F3(kN)   K0(kN/mm)       K1/K0       K2/K0       K3/K0  C1(kNs/mm)       C1/C0    V0(mm/s)          d1          d2          d3           N       Alpha        Beta       Gamma           A         D_A       D_Myu       D_Eta": ""
                         }
masonry_properties_dict = {"Member Properties (Masonry)": "",
                         public_func.five_spaces+"n    Beam No.    Br.H(mm)   Br.Th(mm)   Mor.H(mm)  BFc(N/mm2)  MFc(N/mm2)   stf.reduc   str.reduc": ""
                         }
def member_write(list_to_write,file_open_already):
    for row in range(0,101):
        # file_open_already.write("\n")
        file_open_already.write(public_func.five_spaces)
        file_open_already.write(str(row))
        file_open_already.write(public_func.five_spaces)
        for item in range(len(list_to_write)):
            file_open_already.write(str(list_to_write[item]))
            file_open_already.write(public_func.five_spaces)
        file_open_already.write("\n")


def write_to_file_member(member_dict,member_values,file_input_location):
    with open(file_input_location, "a") as file:
        public_func.dict_write(member_dict, file)
        member_write(member_values, file)
def write_to_file_general_member(member_dict,member_values,file_input_location):
    with open(file_input_location, "a") as file:
        public_func.dict_write(member_dict, file)
        public_func.general_member_write(member_values, file)

# Write Member Type
def member_type(file_input_location):
    # Lists with values for members - except first no_count!!!!!
    member_type_values_list = [4, 4, 4, 1]
    write_to_file_member(member_type_dict,member_type_values_list,file_input_location)

# Write wall_properties_dict
def wall_properties(file_input_location):
    # Lists with values for wall - for now it is unused - standard values
    wall_properties_values_list = [0,0,0,0,0,1100,0,0,0,0.5,0,0,0,0,0,0,0,0,21000,17000,0,0,0,0.5,0,0,300,17000]
    write_to_file_general_member(wall_properties_dict,wall_properties_values_list,file_input_location)

# Write external_spring_properties_dict
def ext_spring_properties(file_input_location):
    # Lists with values for ext_spring - for now it is unused - standard values
    ext_spring_properties_values_list = [1,0,100000000,0,0,0]
    write_to_file_general_member(external_spring_properties_dict,ext_spring_properties_values_list,file_input_location)

# Write isolator_properties_dict
def isolator_properties(file_input_location):
    # Lists with values for isolator_properties - for now it is unused - standard values
    isolator_properties_values_list = [0,0,0,1000,0,0,0,0,0,0,0,2,0.01,0.5,0.5,1,0,0,0]
    write_to_file_general_member(isolator_properties_dict,isolator_properties_values_list,file_input_location)

# Write damper_properties_dict
def damper_properties(file_input_location):
    # Lists with values for damper_properties - for now it is unused - standard values
    damper_properties_values_list = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.5,0,0,2,0.01,0.50,0.50,1,0,0,0]
    write_to_file_general_member(damper_properties_dict,damper_properties_values_list,file_input_location)

# Write masonry_properties_dict
def masonry_properties(file_input_location):
    # Lists with values for masonry_properties_dict - for now it is unused - standard values
    masonry_properties_values_list = [1,60,100,750,10,5,0,1,1]
    write_to_file_general_member(masonry_properties_dict,masonry_properties_values_list,file_input_location)
