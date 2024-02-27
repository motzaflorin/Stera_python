###############################
# PROJECT MADE FOR BUILDING GENERATION FOR RCS2_DOCTORATE DATABASE - MADE FOR RESPONSE RUNNING
# PRESENT CODE IS FOR „INPUTwave_X_y_Z.TXT” FILE GENERATION
# 4) Options For Structure / Members / Dynamic Analysis



from pathlib import Path
import os
import public_func
import pandas as pd

def wave_write(wave_to_be_written,output_wave_file_location,timestep):  # folder output will be overwritten
    #####################################################
    #                    DESCRIPTION                    #
    #####################################################

    # @brief                        -       populate "inputdata.txt" with different options for: structure, member,
    #                                       analysis
    ###############
    #   param_in  TYPE: int for ALL except initial settings #
    ###############

    # wave_to_be_written            -       wave of type DATAFRAME containing only 1 col of data with name and length
    # output_wave_file_location     -       output path for inputwave                                   TYPE: string
    # timestep                      -       is of type string

    ###############
    #   params    #
    ###############
    # new_row                       -       row of type pandas

    #
    #
    # @return                       -

    #####################################################
    new_row = pd.Series([timestep])
    wave_to_be_written = pd.concat([new_row.to_frame().T, wave_to_be_written], ignore_index=True)
    # [wave_to_be_written.shape[0] - 1] - else Response stops at inputwave file
    new_row = pd.Series([wave_to_be_written.shape[0]-1])
    wave_to_be_written = pd.concat([new_row.to_frame().T, wave_to_be_written], ignore_index=True)

    wave_to_be_written.to_csv(output_wave_file_location, index=False, header=False, sep='\t')






