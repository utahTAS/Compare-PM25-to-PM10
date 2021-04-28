# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 14:40:32 2019

@author: bcubrich
"""

#%%

import numpy as np   #fast numerical computation
import pandas as pd

import seaborn as sns
from tkinter import Tk  #GUI
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
import matplotlib.pyplot as plt

def get_dat():  #this function won't do anything until you call it
    root = Tk()
    root.withdraw()
    root.focus_force()
    root.attributes("-topmost", True)      #makes the dialog appear on top
    filename = askopenfilename()      # Open single file
    
    return filename

station_sym_dict={'490110004':'BV', '490450004':'ED','490170006':'ES','490351007':'MA',
          '490030003':'BR','490571003':'HV','490570002':'O2', '490050007':'SM',
          '490494001':'LN', '490354002':'NR','490130002':'RS', '490495010':'SF', '490471004':'V4',
          '490353013':'H3','490353006':'HW','490071003':'P2','490116001':'AI','490456001':'490456001','490353005':'SA',
          '490352005':'CV','490210005':'EN','490530007':'HC','490353010':'RP','490353015':'UT'}

# data_file='U:/PLAN/BCUBRICH/Python/PM10_PM5 Comparison/Data/AMP501_1766130-0.txt'

data_file=get_dat()

df=pd.read_csv(data_file,sep='|',dtype=str) #need to delete the 
#df['Sample Value']=df['Sample Value'].apply(float)

df=df.dropna(subset=['Sample Value']).copy()
df=df[df['# RD']!='# RC']
df['Date']=df['Date'].apply(int)
df['Sample Value']=df['Sample Value'].apply(float)
df['Station ID']=df['State Code']+df['County Code']+df['Site ID']
df['Station Name']=df['Station ID'].map(station_sym_dict)
df['MethParam']=df['Parameter']+'_'+df['Method']
#%%
df['Continous']=np.where((df['Method']!='184')&(df['Method']!='182')&(df['Method']!='181'), True, False)

#print(df['Method'].unique())


df_filter=df[df['Continous']].copy()
df_filter['date_str']=df_filter['Date'].apply(str)+' '+df_filter['Start Time']
df_filter['dt']=df_filter['date_str'].apply(pd.to_datetime)



print(df_filter['MethParam'].unique())


df_filter_ts=df_filter[df_filter['Parameter']=='88101'].merge(
        df_filter[df_filter['Parameter']=='81102'],
                         on=['dt','Station ID'],how='left', suffixes=['_PM25','_PM10'])

df_filter_ts=df_filter_ts[['dt','Sample Value_PM25','Sample Value_PM10','Station Name_PM10', 'Station ID','POC_PM25','POC_PM10']].dropna(subset=('Sample Value_PM10','Sample Value_PM25'))

df_filter_ts['diff']=df_filter_ts['Sample Value_PM10']-df_filter_ts['Sample Value_PM25']

df_2019_ts=df_filter_ts[df_filter_ts['dt']>=pd.to_datetime('2019-01-01')].copy()


mismatch_df=df_filter_ts[df_filter_ts['diff']<0]

mismatch_df_2019=df_2019_ts[df_2019_ts['diff']<0]

#%%

data_dict=dict()

for name in df_2019_ts['Station ID'].unique():
    data_dict[name]=df_2019_ts[df_2019_ts['Station ID']==name]
#test=data_dict.get('490353006').sort_values('dt')

fig=plt.figure()
ax=fig.add_subplot(111)


def plot_plot(df):


    
    x=df['Sample Value_PM25']
    y= df['Sample Value_PM10']
    plt.scatter(x,y, alpha=0.4)
    
    x_one_to_one=np.linspace(0,max(x),10)
    y_one_to_one=x_one_to_one
    plt.plot(x_one_to_one, y_one_to_one, c='r')
    
    plt.xlabel('PM25')
    plt.ylabel('PM10')
    
    
#    plt.ylim(0,400)
    
#    plt.xlim(0,200)
    
#    ax.set_aspect('equal')

#%%
    
# plot_plot(df_2019_ts)

# plot_plot(mismatch_df_2019)   
    
    
#%%
    
plot_plot(df_filter_ts)

if len(mismatch_df)>0:
    plot_plot(mismatch_df)

#%%

#print(df_filter_ts['Station ID'].unique())
