# %%
# -*- coding: utf-8 -*-
"""
post processing results using parallel processing
collate results into a csv for later use

@author: 20181270
"""

import time                 # to measure the computation time
import os 
import multiprocessing as mp
from joblib import Parallel, delayed
# from PostprocessFunctions import PostprocessFunctions as pf
import numpy as np
import pandas as pd
import matplotlib
from matplotlib import pyplot as plt
from datetime import datetime
pd.options.mode.chained_assignment = None  
matplotlib.rcParams['lines.linewidth'] = 1
matplotlib.rcParams["figure.autolayout"] = True

global directory, result_folder
directory = 'C:\\Users\\20181270\\OneDrive - TU Eindhoven\\PhD\\TRNSYS\\Publication1\\pub_1\\src\\'
res_folder = 'res\\'
trn_folder = 'res\\trn\\'

# %%
# result_folder = '\\with_summer_loop\\2parameterSA_volume_area'

temp = os.listdir(directory+trn_folder)
labels = []
for i in temp:
    if '_temp_flow' in i:
        prefix = i[:-14]
    elif '_control_signal' in i:
        prefix = i[:-19]
    elif '_energy' in i:
        prefix = i[:-11]
    else:
        continue
    labels.append(prefix)

labels = np.array(labels)
labels = np.unique(labels)
check_labels = np.array([''.join(filter(str.isdigit, s)) for s in labels])

#%% check if sim_results.csv exists. create if it doesnt, add new values to it, if it does
sim_yn =  os.listdir(directory+res_folder)
if 'sim_results.csv' in sim_yn:
    existing_res = pd.read_csv(directory+res_folder + 'sim_results.csv',index_col='label')
    existing_labels = np.array(existing_res.index.astype(str).tolist())

else:
    existing_res = pd.DataFrame()
#%%
DT = '6min'
t_start = datetime(2001,1,1, 0,0,0)
t_end = datetime(2002,1,1, 0,0,0)
inputs = pd.read_csv(trn_folder+'list_of_inputs.csv',header=0, index_col='label').sort_values(by='label')
#%%
os.chdir(directory)
from PostprocessFunctions import PostprocessFunctions as pf
def new_column(label):
    # t1 = datetime(2001,3,5, 0,0,0)
    # t2 = datetime(2001,3,9, 0,0,0)
    # if 'cp' in label:
    #     controls, energy, temp_flow = pf.cal_base_case(directory+trn_folder + label)
        
    # else:
    #     temp_flow = pd.read_csv(directory+trn_folder + label+'_temp_flow.txt', delimiter=",",index_col=0)
    #     energy = pd.read_csv(directory+trn_folder + label+'_energy.txt', delimiter=",", index_col=0)
    #     controls = pd.read_csv(directory+trn_folder + label+'_control_signal.txt', delimiter=",",index_col=0)
 
    #     controls = pf.modify_df(controls, t_start, t_end)
    #     temp_flow = pf.modify_df(temp_flow, t_start, t_end)     
    #     energy = pf.modify_df(energy, t_start, t_end)/3600     # kJ/hr to kW 
    
    # occ = pd.read_csv(directory+trn_folder+'occ.txt', delimiter=",",index_col=0)
    # occ = pf.modify_df(occ, t_start, t_end)
    # controls = pd.concat([controls,occ],axis=1)
    
    # unmet = pf.unmet_hours(controls, temp_flow)
    
    index = int(''.join([i for i in label if i.isdigit()]))
    design_case = inputs.loc[index]['design_case']
    vol = inputs.loc[index]['volume']
    coll_area = inputs.loc[index]['coll_area']
    cost = pf.investment_cost(design_case, vol, coll_area)
    return cost, label
    # return el_bill, gas_bill, el_em, gas_em, label

#%% Parallel processing
t1 = time.time()
# if __name__ == "__main__":
#     pool = mp.Pool(8)
#     results = pool.map(new_column, labels)
    
#     pool.close()
#     pool.join()

results = Parallel(n_jobs=8)(delayed(new_column)(label) for label in labels)

t2 = time.time()
print(t2-t1)

#%% exporting the results in a csv
# #    isolating the results that come as dictionaries: annual energy, electricity 
# #    bill for different net metering levels
# week = 'march'
# # el_bill = results[0][0]
# # el_bill = ['el_bill_'+week+'_'+i for i in el_bill]   #adding the label el_bill before each bill value
# # list_columns = [el_bill,'gas_bill_'+week,'el_em_'+week,'gas_em_'+week,'spf','penalty','label']
# list_columns = ['cost','label']
# columns = []
# #    converting the conbunation of dict an dlist, into a list
# for item in list_columns:
#     if isinstance(item, list):
#         columns.extend(item)
#     else:
#         columns.append(item)
        
# output = pd.DataFrame(columns=columns)        
# for i in range(len(results)):
#     row = []
#     row_data = results[i]#[2:] #use the last part when you've calculated OPP
#     for r in row_data:
#         if isinstance(r,dict):
#             row.extend(r.values())
#         else:
#             row.append(r)
#     output.loc[i] = row

# output['label'] = output['label'].str.extract('(\d+)').astype(int)
# output=output.sort_values(by='label', ignore_index=True)
# output = output.set_index('label')
# output = pd.concat([existing_res,output], axis=1)
# output.to_csv(res_folder+'sim_results'+'.csv', index='label', index_label='label')

#%% Use this for saving load duration curves
# ldc = pd.DataFrame(columns=np.arange(len(results)), data=np.array([[0]*(len(results))]*8762))
# rldc = pd.DataFrame(columns=np.arange(len(results)), data=np.array([[0]*(len(results))]*8762))
# for i in results:
#     r = i[1]
#     l = i[2]
#     label = int(''.join(char for char in i[-1] if char.isdigit()))
#     rldc[label] = r[r.columns[0]]
#     ldc[label] = l[l.columns[0]]
    
# rldc = rldc.drop(0)
# ldc = ldc.drop(0)

# # the next steps are only if values have to be replaced by simulating redo.csv
# rldc_og = pd.read_csv(res_folder+'rldc.csv',index_col=0)
# ldc_og = pd.read_csv(res_folder+'ldc.csv',index_col=0)

# rldc_og.columns = rldc_og.columns.astype(int)
# ldc_og.columns = ldc_og.columns.astype(int)

# rldc_og[rldc.columns] = rldc
# ldc_og[ldc.columns] = ldc

# ldc.to_csv(res_folder+'ldc'+'.csv', index=True, index_label='Duration')
# rldc.to_csv(res_folder+'rldc'+'.csv', index=True, index_label='Duration')