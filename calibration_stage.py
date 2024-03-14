import os.path
import pandas as pd
import main
import os
import cProfile



import time



def calibration ():
    parent_folder = "D:\\0 DOCTORAT\\00_RC2\Testare_generare_cladiri_Stera\dummy_foler_test"
    id_folder = [a for a in os.listdir(parent_folder) if os.path.isdir(os.path.join(parent_folder, a))]
    # print(id_folder)
    df_orig = main.read_database_Ruben_Vasile()
    df_orig = df_orig.reset_index()
    ux_max = df_orig["UXMAX"]
    uy_max = df_orig["UYMAX"]
    my_dict={}
    dict_col_names = ["Run_ID","Stories","dx_min","dx_max","dy_min","dy_max","dx_abs","uxmax","Diff X [%]","dy_abs","uymax","Diff Y [%]"]
    value = []
    current_header = None


    for no_file in range(len(id_folder)):
        output_folder="output"
        response = "response_structure.txt"
        id = id_folder[no_file]
        id_file = os.path.join(parent_folder, id, output_folder, response)
        # Define the main column names (excluding repeated headers)
        main_column_names = ['kstep', 't', 'a0x', 'a0y', 'a0z',
                             'd0x', 'd0y', 'd0z',"F","sdx(cm)","sdy(cm)","sfx(kN)","sfy(kN)","dx(cm)","dy(cm)","rz(rad)","vx(cm/s)","vy(cm/s)","ax(gal)","ay(gal)"]
        # Read the text file without header to get the number of floors
        with open(id_file, 'r') as file:
            header_line = file.readline().strip()
            f_indices = [i for i, header in enumerate(header_line.split()) if 'F' in header]
            num_floors = (header_line.split('F'))
        df = pd.read_csv(id_file, delimiter='\s+', skiprows=0)
        no_floors = 0
        for floor_number in f_indices:
            try:
                int(df.iloc[0,floor_number])
                no_floors = df.iloc[0, floor_number]

            except ValueError:
                continue
        # Generate column names including floor information
        column_names = main_column_names + [f'{header}_Floor{i +1}' for i in range(no_floors) for header in
                                                                                ['F', 'sdx(cm)', 'sdy(cm)', 'sfx(kN)', 'sfy(kN)', 'dx(cm)', 'dy(cm)', 'rz(rad)',
                                                                                 'vx(cm/s)', 'vy(cm/s)', 'ax(gal)', 'ay(gal)']]

        # Read the text file into a DataFrame, skipping the first row with column names
        df = pd.read_csv(id_file, delimiter='\s+', names=column_names, skiprows=1)

        last_floor_dx = [max(df[f"dx(cm)_Floor{no_floors}"]), min(df[f"dx(cm)_Floor{no_floors}"])]
        last_floor_dy= [max(df[f"dy(cm)_Floor{no_floors}"]), min(df[f"dy(cm)_Floor{no_floors}"])]
        x_disp = max(abs(df[f"dx(cm)_Floor{no_floors}"]))
        y_disp = max(abs(df[f"dy(cm)_Floor{no_floors}"]))
        x_max = float(ux_max[no_file])*100
        y_max = float(uy_max[no_file]) * 100
        # print(f"Building-ID {id}:\n Last floor {no_floors} dx(cm) {last_floor_dx}\n Last floor dy(cm) {last_floor_dy}\n")
        # print(f"\tOrig UXMAX:{x_max}\n\tOrig UYMAX:{y_max}")
        # print("\n Diffference in [%]\n")
        delta_x = str(int((max(x_max,x_disp) - min(x_max,x_disp))/max(x_max,x_disp)*100)) + " %"
        delta_y = str(int((max(y_max,y_disp) - min(y_max,y_disp))/max(y_max,y_disp)*100)) + " %"
        # print(f"X difference {delta_x}% \tY difference {delta_y}% \n")
        data_values = [id, no_floors, last_floor_dx[1],last_floor_dx[0],last_floor_dy[1],last_floor_dy[0],x_disp,x_max,delta_x,y_disp,y_max,delta_y]
        for header, value in zip(dict_col_names, data_values):
            if header not in my_dict:
                my_dict[header] = value
            else:
            #     # If the header already exists, create a list for the values
            #         print(my_dict[header])
                if not isinstance(my_dict[header], list):
                    my_dict[header] = [my_dict[header]]
                my_dict[header].append(value)

    # print(my_dict)
    # for key, value in my_dict.items():
    #     print(f"{key}: {value}")

    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', 20)
    # Convert the dictionary to a DataFrame
    df = pd.DataFrame.from_dict(my_dict, orient='index')

    # Transpose the DataFrame for a better display
    df = df.transpose()

    # Display the DataFrame
    print(df.to_string())

if __name__ == "__main__":
    # pr = cProfile.Profile()
    # pr.enable()
    calibration()
    # pr.disable()
    # # after your program ends
    # pr.print_stats(sort="calls")
