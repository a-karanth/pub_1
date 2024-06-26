# -*- coding: utf-8 -*-
"""
Delete the lst, log, PTI and ssr files from the /src folder. 
And then move the dck files in the backup folder
@author: 20181270
"""

import os
import shutil
import pandas as pd
# folder_path = ""

# Get a list of all files in the folder
files = os.listdir()
#%% Iterate through the files and delete .lst and .log files
# os.chdir('house_and_backup\\backup\\')
for file in files:
    if file.endswith((".lst", ".log",".PTI",'.ssr')):
        # file_path = os.path.join(folder_path, file)
        os.remove(file)

print("Deleted .lst and .log files in the specified folder.")

#%% Get labels for the files that need to be moved
listofinputs = pd.read_csv('res\\trn\\list_of_inputs.csv', index_col=0)
# listofinputs = pd.read_csv('res\\current_list.csv')
labels = listofinputs.index.astype(str)
labels = ['_'+i+'.dck' for i in labels]

#%% Identify and move files to the destination folder
files = os.listdir()
current_folder = os.getcwd()
destination_folder = "house_and_backup\\backup"
# Iterate through the files and move them to the destination folder
for file in files:
    if any(l in file for l in labels):
        source_file_path = os.path.join(current_folder, file)
        destination_file_path = os.path.join(destination_folder, file)
        shutil.move(source_file_path, destination_file_path)

print("Files moved from source folder to destination folder.")

