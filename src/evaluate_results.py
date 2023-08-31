# -*- coding: utf-8 -*-
"""
use results from csv to analyze them

@author: 20181270
"""

import time                 # to measure the computation time
import os 
import multiprocessing as mp
# from PostprocessFunctions import PostprocessFunctions as pf
from Plots import Plots as pt
import numpy as np
import pandas as pd
import matplotlib
from matplotlib import pyplot as plt
from datetime import datetime
pd.options.mode.chained_assignment = None  
matplotlib.rcParams['lines.linewidth'] = 1
matplotlib.rcParams["figure.autolayout"] = True

res_folder = 'res\\'
trn_folder = 'res\\trn\\'
#%% Reading resuls and calculating fianl kpis for comparison, assigning results 
#   based on samples 
results = pd.read_csv(res_folder+'sim_results.csv', index_col='label')
results['total_costs'] = results['el_bill_1']+results['gas_bill']
results['total_emission'] = (results['el_em']+results['gas_em'])/1000
existing = pd.read_csv(trn_folder+'list_of_inputs.csv',header=0, index_col='label').sort_values(by='label')

dfresults = pd.concat([existing, results],axis=1)

#%% add a column to calculate battery size
dfresults.insert(4,'batt',None)
dfresults['batt'] = dfresults['design_case'].str.extract(r'(\d+)')
dfresults['batt'] = dfresults['batt'].fillna(0).astype(int)
df = dfresults.copy()
#%% Focussing on one volume
df = dfresults[(dfresults['r_level']=='r0') & (dfresults['volume']==0.2)]
fil = df[df['volume']==0.25]

#%% Scatter plots

fig,((ax1,ax2),(ax3,ax4)) = plt.subplots(2,2, figsize = (19,9))   
# scatter1, cbar1 = pt.scatter_plot(df[(df['design_case']=='ST') & (df['r_level']=='r1')], 
#                                   df[(df['design_case']=='PVT') & (df['r_level']=='r1')], 
#                                   ax=ax1, marker=['^', 'P'], 
#                                   xkey='volume', ykey='total_costs',ckey='coll_area',
#                                   xlabel='Volume [m3]', ylabel='Total cost [EUR]', 
#                                   clabel='Coll area [m2]')

scatter2, cbar2 = pt.scatter_plot(df[df['design_case']=='ST'], 
                                  df[df['design_case']=='PVT'], 
                                  ax=ax2, marker=['^', 'P'], 
                                  xkey='volume', ykey='total_costs',ckey='flow_rate',
                                  xlabel='Volume [m3]', ylabel='Total cost [EUR]', 
                                  clabel='Flow rate [kg/hr]')

scatter3, cbar3 = pt.scatter_plot(df[df['design_case']=='ST'],
                                  df[df['design_case']=='PVT'],
                                  df[df['design_case']=='PVT_Batt_6'],
                                  df[df['design_case']=='PVT_Batt_9'],
                                  df[df['design_case']=='cp_PV'], ax=ax3,
                                  marker=['^', 'o', 's','D'], 
                                  xkey='total_costs', ykey='total_emission',ckey='coll_area',
                                  xlabel='Total cost [EUR]', ylabel='Total emission [kgCO2]', 
                                  clabel='Coll area [m2]')

#%%
fig, ax = plt.subplots(figsize=(5,6))
st = df[df['design_case']=='ST']
pvt = df[df['design_case']=='PVT']
batt6 = df[df['design_case']=='PVT_Batt_6']
batt9 = df[df['design_case']=='PVT_Batt_9']
cp = df[df['design_case']=='cp_PV']
marker_size= 50

df_plot = {'df':[st,pvt,batt6, batt9,cp],
        'marker':['^','o','o','o','s'],
        'color':['red','purple','orange','green','black'],
        'alpha':[1,1,1,1,0.5],
        'size':[marker_size,marker_size,marker_size,marker_size,50]}
x_values = [1, 2, 3, 4]
for i in x_values:
    match i:
        case 1:
            kpi = 'el_bill_1'
        case 2:
            kpi = 'el_bill_0.5'
        case 3:
            kpi = 'el_bill_0.1'
        case 4:
            kpi = 'el_bill_0'
    for data in range(len(df_plot)):
        total_cost = df_plot['df'][data][kpi] + df_plot['df'][data]['gas_bill']
        ax.scatter([i]*len(df_plot['df'][data]),
                   total_cost,
                   marker = df_plot['marker'][data],
                   c='white',
                   edgecolors =df_plot['color'][data],
                   s =df_plot['size'][data],
                   alpha =df_plot['alpha'][data])
                   # label = df_plot['df'][data]['design_case'].iloc[0])

ax.legend(['ST', 'PVT','PVT_Batt_6','PVT_Batt_9','cp_PV'])
ax.set_xlabel('% net metering')
ax.set_ylabel('Energy bill')
ax.set_title('Volume = 200 L')
ax.set_ylim(1200,4300)
plt.xticks(x_values, ['1','0.5','0.1','0'])
# ax.legend()
#%%
fig, axx = plt.subplots()
df = dfresults.copy()
scatter3, cbar3 = pt.scatter_plot(df[df['design_case']=='ST'],
                                  df[df['design_case']=='PVT'],
                                  df[df['design_case']=='PVT_Batt_6'],
                                  df[df['design_case']=='PVT_Batt_9'],
                                  ax=axx,
                                  marker=['^', 'o', 's','D'], 
                                  xkey='flow_rate', ykey='el_bill_0',ckey='coll_area',
                                  xlabel='flow_rate', ylabel='Total cost [EUR]', 
                                  clabel='Coll area [m2]')
axx.set_ylim([1000,2600])
#%%
# def plotly_plots():
import plotly, plotly.graph_objects as go, plotly.offline as offline, plotly.io as pio
from plotly.subplots import make_subplots
import plotly.express as px
pio.renderers.default = 'browser'
fil_pvt = dfresults[(dfresults['design_case']=='cp_PV') & (dfresults['r_level']=='r0') &
                    (dfresults['volume']==0.2)]
#%%
fil_pvt['label2'] = fil_pvt.index
# fil_pvt['r_number'] = fil_pvt['r_level']
# fil_pvt['r_number']=fil_pvt['r_number'].replace('r0',0+1)
# fil_pvt['r_number']=fil_pvt['r_number'].replace('r1',1+3)

# fil_st['label'] = fil_st.index
fig = px.scatter(fil_pvt, x="volume", y="total_costs", color='coll_area', size='coll_area',  
                 hover_data=['label2'], size_max=20)
fig.update_traces(marker=dict(symbol='square'))

# st =  px.scatter(fil_st, x="flow_rate", y="total_costs", color='coll_area',  
#                  hover_data=['label'], size_max=20)
# st.update_traces(marker=dict(symbol='triangle-up', size=20))
# fig.add_trace(st.data[0])
fig.show()

#%%
# pd.options.plotting.backend = "plotly"
# fig = make_subplots(rows=2, shared_xaxes=True, vertical_spacing=0.05, 
#                     row_heights=[0.5,0.05],
#                     specs=[[{"secondary_y":True}],[{"secondary_y":True}],
#                             [{"secondary_y":True}],[{"secondary_y":True}],[{"secondary_y":False}]],
#                     subplot_titles=("flow rate [kg/hr]", "coll area [m2]"))

# temperatures = ['Thp_load_out','Tsh_in','Tdhw_in', 'Thp_load_in']
# mass_flow = ['mhp_load_out','msh_in', 'mdhw_in', 'mhp_load_in']

# fig.add_trace(go.Scatter(x=temp_flow.index, y=temp_flow['Tamb'], name='Tamb'), secondary_y=False,row=1, col=1)
# fig.add_trace(go.Scatter(x=energy.index, y=energy['Qirr'], name='Qirr'), secondary_y=True,row=1, col=1)
# fig.update_layout(yaxis=dict(title="temperature [deg C]"), yaxis2=dict(title="irradiance [kW]"))

# for i in temperatures:
#     fig.add_trace(go.Scatter(x=temp_flow.index, y=temp_flow[i], name=i), secondary_y=False, row=2, col=1)
# for i in mass_flow:
#     fig.add_trace(go.Scatter(x=temp_flow.index, y=temp_flow[i], name=i), secondary_y=True, row=2, col=1)
# fig.update_layout(yaxis3=dict(title="temperature [deg C]"), yaxis4=dict(title="flow rate [kg/hr]"))

# temperatures = ['T1_sh','Tavg_sh','T6_sh', 'Tsh_cold_out', 'Trad1_in','Tsh_return','Tfloor1','Tfloor2']
# mass_flow = ['msh_cold_out','mrad1_in','mrad2_in', 'msh_return']
# for i in temperatures:
#     fig.add_trace(go.Scatter(x=temp_flow.index, y=temp_flow[i], name=i), secondary_y=False, row=3, col=1)
# for i in mass_flow:
#     fig.add_trace(go.Scatter(x=temp_flow.index, y=temp_flow[i], name=i), secondary_y=True, row=3, col=1)
# fig.update_layout(yaxis5=dict(title="temperature [deg C]"), yaxis6=dict(title="flow rate [kg/hr]"))

# temperatures = ['T1_dhw','Tavg_dhw','T6_dhw', 'Tdhw_cold_out', 'Tdhw2tap','Tat_tap']
# mass_flow = ['mdhw_cold_out','mdhw2tap','mcold2tap', 'mat_tap']
# for i in temperatures:
#     fig.add_trace(go.Scatter(x=temp_flow.index, y=temp_flow[i], name=i), secondary_y=False, row=4, col=1)
# for i in mass_flow:
#     fig.add_trace(go.Scatter(x=temp_flow.index, y=temp_flow[i], name=i), secondary_y=True, row=4, col=1)
# fig.update_layout(yaxis7=dict(title="temperature [deg C]"), yaxis8=dict(title="flow rate [kg/hr]"))

# cntr = ['hp_pump','hp_div','ctr_sh','ctr_dhw','heatingctr1','heatingctr2']
# for i in cntr:
#     fig.append_trace(go.Scatter(x=temp_flow.index, y=controls[i], name=i),row=5, col=1)
# fig.update_layout(title_text='Output files: ' + output_prefix)
# fig.update_layout(xaxis_range=[t1,t2])
# fig.show()
#temp_flow.plot(y=['Thp_load_out','Tsh_in','Tdhw_in', 'Thp_load_in'])
#offline.plot(fig,filename='temp.html')
#%%S
# dfsobol = pd.read_csv('morris_pvt_sample.csv')
# dfresults = results.copy()

# sobol_out = pd.merge(dfsobol, dfresults, on = ['volume','coll_area','design_case'], how = 'left')

# list_volume = [0.1, 0.2, 0.3, 0.4]
# list_coll_area = [8, 16, 20]
# list_design_case_st = ['cp','cp_PV', 'ST']
# list_design_case_pvt = ['cp','cp_PV', 'PVT']
# list_design_case_pvt_batt = ['PVT_Batt_6', 'PVT_Batt_9']
# list_flow = [50, 100, 200]

# problem_pvt = {
#     'num_vars': 4,
#     'names':['tank_volume', 'coll_area', 'design_case', 'flow'],
#     'bounds':[[0, len(list_volume)-1],
#               [0, len(list_coll_area)-1],
#               [0, len(list_design_case_pvt)-1],
#               [0, len(list_flow)-1],]}

# list_volume = [0.1, 0.15, 0.2, 0.25, 0.3]
# list_coll_area = [10, 12, 14, 16, 18, 20]
# list_design_case = ['base','base_PV', 'ST', 'PVT', 'PVT_Batt_6', 'PVT_Batt_9']
# problem = {
#     'num_vars': 3,
#     'names':['tank_volume', 'coll_area', 'design_case'],#, 'r_values'],
#     'bounds':[[0, len(list_volume)-1],
#               [0, len(list_coll_area)-1],
#               [0, len(list_design_case)-1],]}

# Si_cost = morris.analyze(problem, np.ravel(sobol_out['total_costs']), calc_second_order=True)
# Si_em = sobol.analyze(problem, np.ravel(sobol_out['total_emission']), calc_second_order=True)

# Si_cost.plot()
# plt.suptitle('KPI: Energy Cost')
# Si_em.plot()
# plt.suptitle('KPI: Emissions')

#%% check which is missing or repeated
list_label = np.arange(264)
check = pd.DataFrame(index=list_label)
check['count'] = 0
for i in existing.index:
    if i in list_label:
        check.loc[i] = check.loc[i]+1