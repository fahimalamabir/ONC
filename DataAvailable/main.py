# -*- coding: utf-8 -*-
"""
Created on Fri Feb  4 20:32:11 2022

@author: aBr
"""

import streamlit as st
import pandas as pd
import numpy as np
from onc.onc import ONC
from dateutil.parser import parse
from datetime import datetime
import time

import sys
import plotly.express as px

st.cache(suppress_st_warning=True)

#Create a new environment with the latest version of python:

#   `conda create -n streamlit python=3.10`
    

# Activate the environment:
    
#   `conda activate streamlit`
    
# Run the code by calling it on the terminal:
    
 #   `streamlit main.py`
 
# containers
header  = st.markdown('''
                      # **Hydrophone Data Availablity Checker**
    ''')
pwd=st.text_input("Please paste your token:",type="password")


onc = ONC(token=pwd)

    
filters0 = {
    'deviceCategoryCode': 'HYDROPHONE',
}
resultX0 = onc.getLocations(filters0)
za0 = pd.DataFrame(resultX0)

fig0 = px.scatter_geo(za0,lat='lat',lon='lon',
                      hover_name="locationName",hover_data=["locationCode"])
fig0.update_geos(
    scope = "north america"
)
fig0.update_traces(marker=dict(size=12,
                              line=dict(width=2,
                                        color='DarkSlateGrey')),
                  selector=dict(mode='markers'))

fig0.update_layout(title = 'Location of the devices', title_x=0.5)
st.plotly_chart(fig0)

df_hy = []
for location in onc.getLocations({'deviceCategoryCode': 'HYDROPHONE'}):
    df_hy.append(location['locationCode'])
    
df_hy = pd.DataFrame({'Location code':df_hy})

hyl = df_hy['Location code'].unique()

deviceL = st.sidebar.selectbox("Select location:",hyl)

progress =  st.progress(0)
for i in range(1,100):
    time.sleep(0.1)
    progress.progress(i+1)
    
filters1 = {
    'locationCode': deviceL,
    'deviceCategoryCode': 'HYDROPHONE',
}
resultX = onc.getLocations(filters1)
za = pd.DataFrame(resultX)
st.markdown(za.description.values[0])


df_dep = []
for deployment in onc.getDeployments(filters={'locationCode': deviceL, 'deviceCategoryCode': 'HYDROPHONE'}):
    df_dep.append([deployment['locationCode'], deployment['begin'], deployment['end']])

npl = np.array(df_dep)
locationC = pd.DataFrame(npl[:,0])
deplF = pd.DataFrame(npl[:,1])
deplT = pd.DataFrame(npl[:,2])

df_dep = pd.concat([locationC,deplF,deplT],axis=1)
df_dep.columns=["Location Code", "Deployed from", "to"]


st.write("There are {} deployments.".format(df_dep.shape[0]))
st.write("Deployed dates are:",pd.to_datetime(df_dep["Deployed from"]).apply(lambda x: x.date())
)
st.write("Stayed till:",pd.to_datetime(df_dep["to"]).apply(lambda y: y.date()))
with st.form(key ='Form1'):
    with st.sidebar:
        start_date = st.sidebar.date_input("Select Start Date")
        end_date = st.sidebar.date_input("Select End Date")
        submitted1 = st.form_submit_button(label = 'Available Device ')


e = datetime.strptime(str(start_date),"%Y-%m-%d")
el =datetime.timestamp(e)
elT = datetime.utcfromtimestamp(el).strftime("%Y-%m-%dT%H:%M:%S")+'.000Z'
f = datetime.strptime(str(end_date),"%Y-%m-%d")
fl =datetime.timestamp(f)
flT = datetime.utcfromtimestamp(fl).strftime("%Y-%m-%dT%H:%M:%S")+'.000Z'


df_dev = []
for dev in onc.getDevices({
    'locationCode': deviceL,
    'dateFrom': elT,
    'dateTo': flT,
    'deviceCategoryCode':'HYDROPHONE'
}):
    df_dev.append(dev['deviceCode'])
    
df_dev = pd.DataFrame({'Device code':df_dev})


dyl = df_dev['Device code'].unique()

deviceD = st.sidebar.selectbox("Select Device:",dyl)

df_ext = []
for ext in onc.getDataProducts({
    'locationCode': deviceL
}):
    df_ext.append(ext['extension'])
    
df_ext = pd.DataFrame({'Extension':df_ext})


eyl = df_ext['Extension'].unique()


deviceZ = st.sidebar.selectbox("Available extension:",sorted(eyl))

filt ={
'deviceCode': deviceD,
'dateFrom': elT,
'dateTo'  : flT,
'extension': deviceZ
}

if deviceZ:
    with st.form(key ='Form2'):
        with st.sidebar:
            result1 = onc.getListByDevice(filt, allPages=True)
            submitted2 = st.form_submit_button(label = 'Search Available Data')

df = pd.DataFrame(result1)
if len(df) > 0:
    st.markdown("There are {} files".format(len(df)) + ' from ' + filt['deviceCode'] 
            + ' between '   + parse(filt['dateFrom']).strftime('%Y %b %d')
            + ' and ' + parse(filt['dateTo']).strftime('%Y %b %d'))
    st.text("Data:")
    st.write(df)
    if deviceL == 'BACAX' or deviceL == 'BACVP':
        if deviceZ == 'mp3':
            df_dt =  df.files.apply(lambda x: x.strip('.mp3').strip('-audio').split('_')[3])    
            UTC_dt = [pd.Timestamp (x) for x in df_dt]
            df['UTC time'] = UTC_dt
        elif deviceZ == 'wav':
            df_dt =  df.files.apply(lambda x: x.strip('.wav').strip('-HPF.wav').split('_')[3])    
            UTC_dt = [pd.Timestamp (x) for x in df_dt]
            df['UTC time'] = UTC_dt
        elif deviceZ == 'mat':
            df_dt =  df.files.apply(lambda x: x.strip('.mat').strip('-spect').split('_')[3])    
            UTC_dt = [pd.Timestamp (x) for x in df_dt]
            df['UTC time'] = UTC_dt
        elif deviceZ == 'png':
            df_dt =  df.files.apply(lambda x: x.strip('.png').strip('-spect-thumb').strip('-spect').strip('-spect-small').split('_')[3])    
            UTC_dt = [pd.Timestamp (x) for x in df_dt]
            df['UTC time'] = UTC_dt      
        else: 
            df_dt =  df.files.apply(lambda x: x.strip(deviceZ).split('_')[3])    
            UTC_dt = [pd.Timestamp (x) for x in df_dt]
            df['UTC time'] = UTC_dt
            
            
    else:
        if deviceZ == 'mp3':
            df_dt =  df.files.apply(lambda x: x.strip('.mp3').strip('-audio').split('_')[1])    
            UTC_dt = [pd.Timestamp (x) for x in df_dt]
            df['UTC time'] = UTC_dt
        elif deviceZ == 'flac':
            df_dt =  df.files.apply(lambda x: x.strip('.flac').strip('-LPF').split('_')[1])    
            UTC_dt = [pd.Timestamp (x) for x in df_dt]
            df['UTC time'] = UTC_dt
        elif deviceZ == 'wav':
            df_dt =  df.files.apply(lambda x: x.strip('.wav').split('_')[1])    
            UTC_dt = [pd.Timestamp (x) for x in df_dt]
            df['UTC time'] = UTC_dt
        elif deviceZ == 'mat':
            df_dt =  df.files.apply(lambda x: x.strip('.mat').strip('-spect-small')
                                    .strip('-FFT-spect').strip('-FFT-spect-thumb').strip('FFT-spect-small').strip('-spect-thumb')
                                    .strip('-spect').strip('-spect-small').strip('-LPF-spect').strip('-LPF-spect-thumb').split('_')[1])   
            UTC_dt = [pd.Timestamp (x) for x in df_dt]
            df['UTC time'] = UTC_dt
        elif deviceZ == 'png':
            df_dt =  df.files.apply(lambda x: x.strip('.png').strip('-spect-small')
                                    .strip('-FFT-spect').strip('-FFT-spect-thumb').strip('FFT-spect-small').strip('-spect-thumb')
                                    .strip('-spect').strip('-spect-small').strip('-LPF-spect').strip('-LPF-spect-thumb').split('_')[1])
                    
            UTC_dt = [pd.Timestamp (x) for x in df_dt]
            df['UTC time'] = UTC_dt      
        else: 
            df_dt =  df.files.apply(lambda x: x.strip(deviceZ).split('_')[1])    
            UTC_dt = [pd.Timestamp (x) for x in df_dt]
            df['UTC time'] = UTC_dt
        
    fig = px.scatter(df, x="files", y="UTC time",
                 hover_data=["files"],
                 title='Data Availabiltiy Plot',
                 template='plotly_white'
                )
    fig.update_layout(yaxis=dict(title=''), xaxis=dict(title='', showgrid=False, gridcolor='grey',
                      tickvals=[],
                                )
                     )
    st.plotly_chart(fig)
else:
    st.markdown("No data found, try other extension, please.")





