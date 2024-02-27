#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
# PROJECT MADE FOR BUILDING GENERATION FOR RCS2_DOCTORATE DATABASE - MADE FOR RESPONSE RUNNING
# PRESENT CODE IS a PUBLIC FUNCTIONS HEADER
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
import os

five_spaces = "           " # now there are 11 spaces
def check_data(data,should_be_of_type):
    if type(data) != should_be_of_type:
        print("Error:Wrong type")
        return 0
    else:
        return
def generate_joined_string(*argv):
    return os.path.join("",*argv)


def member_property_write_with_spaces(file_open_already,matrix_np_array):
    for row in range(matrix_np_array.shape[0]):
        file_open_already.write("\n")
        for col in range(matrix_np_array.shape[1]):
            file_open_already.write("     ")
            file_open_already.write(str(matrix_np_array[row, col]))

# write empty dicts, dicts with strings in values, values = list, and values = list of lists
def dict_write(dictionary, file_open_already):
    def key_write(key):
        file_open_already.write(key)
        file_open_already.write("\n")
    def value_write(value):
        file_open_already.write(value)
        file_open_already.write("\n")
    def write_line_with_spaces(values_list):
        line = ""
        for item in values_list:
            line += five_spaces + str(item)
        return line
    for key, value in dictionary.items():
        if value == "":
            key_write(key)
            continue
        if type(value) == list:
            key_write(key)
            if type(value[0]) == list:
                for item_list in value:
                    line = write_line_with_spaces(item_list)
                    value_write(line)
            else:
                line = write_line_with_spaces(value)
                value_write(line)
            continue
        key_write(key)
        file_open_already.write(five_spaces)
        value_write(value)
# Write after dict header, the repeating list for all element types
def general_member_write(list_to_write, file_open_already):
    for row in range(1, 102):
        # file_open_already.write("\n")
        file_open_already.write(five_spaces)
        file_open_already.write(str(row))
        file_open_already.write(five_spaces)
        for item in range(len(list_to_write)):
            file_open_already.write(str(list_to_write[item]))
            file_open_already.write(five_spaces)
        file_open_already.write("\n")

def df_singular_to_string(singular_df_entry):
    return str((singular_df_entry[0]))