import os

root_path = os.path.dirname(os.path.dirname(__file__))
database_path = root_path + "\\Database"
input_path = root_path + '\\input'
output_path = root_path + '\\output'

# #-------------------------------------------------
# # Here I want to make a process to automatically create a folder exactly empty for the initialization of a new project
# #-------------------------------------------------
# input folder
if not os.path.exists(input_path):
    os.mkdir(input_path)
#-------------------------------------------------
# output folder
if not os.path.exists(output_path):
    os.mkdir(output_path)