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
import seaborn as sns
import matplotlib.pyplot as plt
import sys
import plotly.express as px
import os

st.set_page_config(layout='wide')
st.markdown(
    """
<style>
.reportview-container .markdown-text-container {
    font-family: serif;
    color: #0000CD	
}
.sidebar .sidebar-content {
    color: #0000CD;
}
.Widget>label {
    color: #0000CD;
    font-family: serif;
}
[class^="st-b"]  {
    color: #0000CD	;
    font-family: serif;
}
.st-bb {
    background-color: transparent;
}
.st-at {
    background-color: #7cb9e8;
}
header {
    font-family: serif;
    color: #00bfff;
}
body {
    font-family: serif;
    color: #00bfff;
}
footer {
    font-family: serif;
    color: #00bfff;
}
.reportview-container .main footer, .reportview-container .main footer a {
    color: white;
}
header .decoration {
    background-image: none;
}

</style>
""",
    unsafe_allow_html=True,
)
st.cache(suppress_st_warning=True)

#Create a new environment with the latest version of python:

#   `conda create -n streamlit python=3.10`
#im = 'image/onc_dataTeam_logo.png'



#Create a new environment with the latest version of python:

im = 'DataAvailable/image/onc_dataTeam_logo.png'
st.sidebar.image(im,use_column_width=True)
st.get_option("theme.primaryColor")
st.get_option("theme.textColor")
# Activate the environment:
    
#   `conda activate streamlit`
    
# Run the code by calling it on the terminal:
    
 #   `streamlit main.py`
 
# containers


header  = st.markdown('''
                      # **Hydrophone Data Availablity Checker**
    ''')
pwd=st.text_input("Please paste your token:",type="password")
if pwd:
    onc = ONC(token=pwd)
    st.cache(ttl =3600)

    data = [['Barkley Node - Hydrophone Array A'], 
                    ['Barkley Node - Hydrophone Array B'], 
                    ['Barkley Node - Hydrophone Array C'], 
                    ['Barkley Node - Hydrophone Array D'],
                    ['Barkley Sound - Folger Deep'],
                    ['Burrard Inlet Underwater Network'],
                    ['Cambridge Bay'],
                    ['Cascadia Basin - Hydrophone Array A'],
                    ['Cascadia Basin - Hydrophone Array B'],
                    ['Cascadia Basin - Hydrophone Array C'],
                    ['Cascadia Basin - Hydrophone Array D'],
                    ['Chatham Sound - Digby Island'],
                    ['Clayoquot Slope - Hydrophone A'],
                    ['Clayoquot Slope - Hydrophone B'],
                    ['Clayoquot Slope - Hydrophone C'],
                    ['Clayoquot Slope - Hydrophone D'],
                    ['Conception Bay - Holyrood Bay'],
                    ['Conception Bay - Holyrood Bay Underwater Network'],
                    ['Discovery Passage - Campbell River'],
                    ['Douglas Channel - Hartley Bay'],
                    ['Douglas Channel - Kitamaat Village'],
                    ['Endeavour - Main Endeavour Field'],
                    ['Saanich Inlet -Patricia Bay-VENUS'],
                    ['SOG-Fraser River Delta Upper Slope'],
                    ['SOG Central -VENUS Instrument'],
                    ['SOG East - Hydrophone Array A'],
                    ['SOG East - Hydrophone Array B'],
                    ['SOG East - Hydrophone Array C'],
                    ['SOG East - Hydrophone Array D'],
                    ['Vancouver Island - China Creek']]
    dfL = pd.DataFrame(data, columns = ['Location'])

    opt = st.sidebar.selectbox(
                'Please select a location:',dfL['Location'])

    if opt=='Barkley Node - Hydrophone Array A':
        filters1 = {
            'locationCode': 'BACNH.H1',
            'deviceCategoryCode': 'HYDROPHONE',
            }
        resultX = onc.getLocations(filters1)
        za = pd.DataFrame(resultX)
        st.markdown(za.description.values[0])


        df_dep = []
        for deployment in onc.getDeployments(filters={'locationCode': 'BACNH.H1', 'deviceCategoryCode': 'HYDROPHONE'}):
            df_dep.append([deployment['locationCode'], deployment['begin'], deployment['end']])

        npl = np.array(df_dep)
        locationC = pd.DataFrame(npl[:,0])
        deplF = pd.DataFrame(npl[:,1])
        deplT = pd.DataFrame(npl[:,2])

        df_dep = pd.concat([locationC,deplF,deplT],axis=1)
        df_dep.columns=["Location Code", "Deployed from", "Deployed to"]


        st.write("There are {} deployments.".format(df_dep.shape[0]))
        df_dep["Deployed from"] = pd.to_datetime(df_dep["Deployed from"]).apply(lambda y: y.date())
        df_dep["Deployed to"] = pd.to_datetime(df_dep["Deployed to"]).apply(lambda y: y.date())
        fe = df_dep.style.hide_index()
        st.write(fe.to_html(), unsafe_allow_html=True)

        start_date = st.sidebar.date_input("Select Start Date")
        end_date = st.sidebar.date_input("Select End Date")

        e = datetime.strptime(str(start_date),"%Y-%m-%d")
        el =datetime.timestamp(e)
        elT = datetime.utcfromtimestamp(el).strftime("%Y-%m-%dT%H:%M:%S")+'.000Z'
        f = datetime.strptime(str(end_date),"%Y-%m-%d")
        fl =datetime.timestamp(f)
        flT = datetime.utcfromtimestamp(fl).strftime("%Y-%m-%dT%H:%M:%S")+'.000Z'


        df_dev = []
        for dev in onc.getDevices({
            'locationCode': 'BACNH.H1',
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
                'locationCode': 'BACNH.H1'
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
        result1 = onc.getListByDevice(filt, allPages=True)
        df = pd.DataFrame(result1)
        if len(df) > 0:
            st.markdown("There are {} files".format(len(df)) + ' from ' + filt['deviceCode'] 
                    + ' between '   + parse(filt['dateFrom']).strftime('%Y %b %d')
            + ' and ' + parse(filt['dateTo']).strftime('%Y %b %d'))
            with st.expander("Data:"):
                st.write(df)
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
                                    .strip('-spect').strip('-spect-small').strip('-LPF-spect').strip('-LPF-spect-thumb')
                                    .strip('-HPF-spect').strip('-HPF-spect-thumb').split('_')[1])   
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
            
                    
            option = st.selectbox(
                'How would you like to visualize the data availability:?',
                ('Line only', 'Bar only', 'Both'))
            
            if option == 'Line only':
                fig = px.scatter(df, x="files", y="UTC time",
                                 title='Data Availabiltiy Plot for {} of the entire deployment (Please enlarge the plot for better visualization)'.format(deviceZ),
                                 template='plotly_white'
                )
                fig.update_layout(yaxis=dict(title=''), xaxis=dict(title='', showgrid=False, gridcolor='grey',
                      tickvals=[],),hovermode="y unified")
                fig.update_traces(connectgaps=False,hovertemplate=None)


                st.plotly_chart(fig)

            elif option=='Bar only':
                df_dt = pd.to_datetime(df_dt)
                dm = df_dt.dt.strftime('%m-%d')
                dav = dm.value_counts().sort_index()


                fig1 = plt.figure(figsize = (4,2))

                ax = plt.axes()
                ax.barh(dav.index,dav,color=sns.color_palette("tab10"),align ='center')
                # Remove axes splines
                for s in ['top', 'bottom', 'left', 'right']:
                    ax.spines[s].set_visible(False)
                    # Remove x, y Ticks
                ax.xaxis.set_ticks_position('none')
                ax.yaxis.set_ticks_position('none')

                plt.yticks(fontsize=5)
                plt.ylabel("day",size = 4)

                ax.legend()        
 
                ax.get_xaxis().set_visible(False)

                ax.set_title('Data Available Per day',
                         loc ='left',fontsize=5 )
            # Add annotation to bars
                for p in ax.patches:
                    left, bottom, width, height = p.get_bbox().bounds
                    ax.annotate(str(int(width)), xy=(left+width/2, bottom+height/2), 
                                ha='center', va='center', size = 3)
            
                # save image, display it, and delete after usage.
                plt.savefig('x',dpi=200)
                st.image('x.png')
                os.remove('x.png')
                        
            else:
                fig = px.scatter(df, x="files", y="UTC time",
                                 title='Data Availabiltiy Plot for {} of the entire deployment (Please enlarge the plot for better visualization)'.format(deviceZ),
                                 template='plotly_white'
                )
                fig.update_layout(yaxis=dict(title=''), xaxis=dict(title='', showgrid=False, gridcolor='grey',
                      tickvals=[],),hovermode="y unified")
                fig.update_traces(connectgaps=False,hovertemplate=None)
                
                df_dt = pd.to_datetime(df_dt)
                dm = df_dt.dt.strftime('%m-%d')
                dav = dm.value_counts().sort_index()


                fig1 = plt.figure(figsize = (4,2))

                ax = plt.axes()
                ax.barh(dav.index,dav,color=sns.color_palette("tab10"),align ='center')
                # Remove axes splines
                for s in ['top', 'bottom', 'left', 'right']:
                    ax.spines[s].set_visible(False)
                    # Remove x, y Ticks
                ax.xaxis.set_ticks_position('none')
                ax.yaxis.set_ticks_position('none')

                plt.yticks(fontsize=5)
                plt.ylabel("day",size = 4)

                ax.legend()        
 
                ax.get_xaxis().set_visible(False)

                ax.set_title('Data Available Per day',
                         loc ='left',fontsize=5 )
            # Add annotation to bars
                for p in ax.patches:
                    left, bottom, width, height = p.get_bbox().bounds
                    ax.annotate(str(int(width)), xy=(left+width/2, bottom+height/2), 
                                ha='center', va='center', size = 3)
            
                # save image, display it, and delete after usage.
                plt.savefig('x',dpi=200)
                st.image('x.png')
                os.remove('x.png')
                st.plotly_chart(fig)

        else:
            st.markdown("No data found, try other extension, please.")
    elif opt=='Barkley Node - Hydrophone Array B':
        filters1 = {
            'locationCode': 'BACNH.H2',
            'deviceCategoryCode': 'HYDROPHONE',
            }
        resultX = onc.getLocations(filters1)
        za = pd.DataFrame(resultX)
        st.markdown(za.description.values[0])


        df_dep = []
        for deployment in onc.getDeployments(filters={'locationCode': 'BACNH.H2', 'deviceCategoryCode': 'HYDROPHONE'}):
            df_dep.append([deployment['locationCode'], deployment['begin'], deployment['end']])

        npl = np.array(df_dep)
        locationC = pd.DataFrame(npl[:,0])
        deplF = pd.DataFrame(npl[:,1])
        deplT = pd.DataFrame(npl[:,2])

        df_dep = pd.concat([locationC,deplF,deplT],axis=1)
        df_dep.columns=["Location Code", "Deployed from", "Deployed to"]


        st.write("There are {} deployments.".format(df_dep.shape[0]))
        df_dep["Deployed from"] = pd.to_datetime(df_dep["Deployed from"]).apply(lambda y: y.date())
        df_dep["Deployed to"] = pd.to_datetime(df_dep["Deployed to"]).apply(lambda y: y.date())
        fe = df_dep.style.hide_index()
        st.write(fe.to_html(), unsafe_allow_html=True)

        start_date = st.sidebar.date_input("Select Start Date")
        end_date = st.sidebar.date_input("Select End Date")

        e = datetime.strptime(str(start_date),"%Y-%m-%d")
        el =datetime.timestamp(e)
        elT = datetime.utcfromtimestamp(el).strftime("%Y-%m-%dT%H:%M:%S")+'.000Z'
        f = datetime.strptime(str(end_date),"%Y-%m-%d")
        fl =datetime.timestamp(f)
        flT = datetime.utcfromtimestamp(fl).strftime("%Y-%m-%dT%H:%M:%S")+'.000Z'


        df_dev = []
        for dev in onc.getDevices({
            'locationCode': 'BACNH.H2',
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
                'locationCode': 'BACNH.H2'
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
        result1 = onc.getListByDevice(filt, allPages=True)
        df = pd.DataFrame(result1)
        if len(df) > 0:
            st.markdown("There are {} files".format(len(df)) + ' from ' + filt['deviceCode'] 
                    + ' between '   + parse(filt['dateFrom']).strftime('%Y %b %d')
            + ' and ' + parse(filt['dateTo']).strftime('%Y %b %d'))
            with st.expander("Data:"):
                st.write(df)
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
                                    .strip('-spect').strip('-spect-small').strip('-LPF-spect').strip('-LPF-spect-thumb')
                                    .strip('-HPF-spect').strip('-HPF-spect-thumb').split('_')[1])   
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
            
                    
            option = st.selectbox(
                'How would you like to visualize the data availability:?',
                ('Line only', 'Bar only', 'Both'))
            
            if option == 'Line only':
                fig = px.scatter(df, x="files", y="UTC time",
                                 title='Data Availabiltiy Plot for {} of the entire deployment (Please enlarge the plot for better visualization)'.format(deviceZ),
                                 template='plotly_white'
                )
                fig.update_layout(yaxis=dict(title=''), xaxis=dict(title='', showgrid=False, gridcolor='grey',
                      tickvals=[],),hovermode="y unified")
                fig.update_traces(connectgaps=False,hovertemplate=None)


                st.plotly_chart(fig)

            elif option=='Bar only':
                df_dt = pd.to_datetime(df_dt)
                dm = df_dt.dt.strftime('%m-%d')
                dav = dm.value_counts().sort_index()


                fig1 = plt.figure(figsize = (4,2))

                ax = plt.axes()
                ax.barh(dav.index,dav,color=sns.color_palette("tab10"),align ='center')
                # Remove axes splines
                for s in ['top', 'bottom', 'left', 'right']:
                    ax.spines[s].set_visible(False)
                    # Remove x, y Ticks
                ax.xaxis.set_ticks_position('none')
                ax.yaxis.set_ticks_position('none')

                plt.yticks(fontsize=5)
                plt.ylabel("day",size = 4)

                ax.legend()        
 
                ax.get_xaxis().set_visible(False)

                ax.set_title('Data Available Per day',
                         loc ='left',fontsize=5 )
            # Add annotation to bars
                for p in ax.patches:
                    left, bottom, width, height = p.get_bbox().bounds
                    ax.annotate(str(int(width)), xy=(left+width/2, bottom+height/2), 
                                ha='center', va='center', size = 3)
            
                # save image, display it, and delete after usage.
                plt.savefig('x',dpi=200)
                st.image('x.png')
                os.remove('x.png')
                        
            else:
                fig = px.scatter(df, x="files", y="UTC time",
                                 title='Data Availabiltiy Plot for {} of the entire deployment (Please enlarge the plot for better visualization)'.format(deviceZ),
                                 template='plotly_white'
                )
                fig.update_layout(yaxis=dict(title=''), xaxis=dict(title='', showgrid=False, gridcolor='grey',
                      tickvals=[],),hovermode="y unified")
                fig.update_traces(connectgaps=False,hovertemplate=None)
                
                df_dt = pd.to_datetime(df_dt)
                dm = df_dt.dt.strftime('%m-%d')
                dav = dm.value_counts().sort_index()


                fig1 = plt.figure(figsize = (4,2))

                ax = plt.axes()
                ax.barh(dav.index,dav,color=sns.color_palette("tab10"),align ='center')
                # Remove axes splines
                for s in ['top', 'bottom', 'left', 'right']:
                    ax.spines[s].set_visible(False)
                    # Remove x, y Ticks
                ax.xaxis.set_ticks_position('none')
                ax.yaxis.set_ticks_position('none')

                plt.yticks(fontsize=5)
                plt.ylabel("day",size = 4)

                ax.legend()        
 
                ax.get_xaxis().set_visible(False)

                ax.set_title('Data Available Per day',
                         loc ='left',fontsize=5 )
            # Add annotation to bars
                for p in ax.patches:
                    left, bottom, width, height = p.get_bbox().bounds
                    ax.annotate(str(int(width)), xy=(left+width/2, bottom+height/2), 
                                ha='center', va='center', size = 3)
            
                # save image, display it, and delete after usage.
                plt.savefig('x',dpi=200)
                st.image('x.png')
                os.remove('x.png')
                st.plotly_chart(fig)

        else:
            st.markdown("No data found, try other extension, please.")


    elif opt=='Barkley Node - Hydrophone Array C':
        filters1 = {
            'locationCode': 'BACNH.H3',
            'deviceCategoryCode': 'HYDROPHONE',
            }
        resultX = onc.getLocations(filters1)
        za = pd.DataFrame(resultX)
        st.markdown(za.description.values[0])


        df_dep = []
        for deployment in onc.getDeployments(filters={'locationCode': 'BACNH.H3', 'deviceCategoryCode': 'HYDROPHONE'}):
            df_dep.append([deployment['locationCode'], deployment['begin'], deployment['end']])

        npl = np.array(df_dep)
        locationC = pd.DataFrame(npl[:,0])
        deplF = pd.DataFrame(npl[:,1])
        deplT = pd.DataFrame(npl[:,2])

        df_dep = pd.concat([locationC,deplF,deplT],axis=1)
        df_dep.columns=["Location Code", "Deployed from", "Deployed to"]


        st.write("There are {} deployments.".format(df_dep.shape[0]))
        df_dep["Deployed from"] = pd.to_datetime(df_dep["Deployed from"]).apply(lambda y: y.date())
        df_dep["Deployed to"] = pd.to_datetime(df_dep["Deployed to"]).apply(lambda y: y.date())
        fe = df_dep.style.hide_index()
        st.write(fe.to_html(), unsafe_allow_html=True)

        start_date = st.sidebar.date_input("Select Start Date")
        end_date = st.sidebar.date_input("Select End Date")

        e = datetime.strptime(str(start_date),"%Y-%m-%d")
        el =datetime.timestamp(e)
        elT = datetime.utcfromtimestamp(el).strftime("%Y-%m-%dT%H:%M:%S")+'.000Z'
        f = datetime.strptime(str(end_date),"%Y-%m-%d")
        fl =datetime.timestamp(f)
        flT = datetime.utcfromtimestamp(fl).strftime("%Y-%m-%dT%H:%M:%S")+'.000Z'


        df_dev = []
        for dev in onc.getDevices({
            'locationCode': 'BACNH.H3',
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
                'locationCode': 'BACNH.H3'
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
        result1 = onc.getListByDevice(filt, allPages=True)
        df = pd.DataFrame(result1)
        if len(df) > 0:
            st.markdown("There are {} files".format(len(df)) + ' from ' + filt['deviceCode'] 
                    + ' between '   + parse(filt['dateFrom']).strftime('%Y %b %d')
            + ' and ' + parse(filt['dateTo']).strftime('%Y %b %d'))
            with st.expander("Data:"):
                st.write(df)
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
                                    .strip('-spect').strip('-spect-small').strip('-LPF-spect').strip('-LPF-spect-thumb')
                                    .strip('-HPF-spect').strip('-HPF-spect-thumb').split('_')[1])   
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
            
                    
            option = st.selectbox(
                'How would you like to visualize the data availability:?',
                ('Line only', 'Bar only', 'Both'))
            
            if option == 'Line only':
                fig = px.scatter(df, x="files", y="UTC time",
                                 title='Data Availabiltiy Plot for {} of the entire deployment (Please enlarge the plot for better visualization)'.format(deviceZ),
                                 template='plotly_white'
                )
                fig.update_layout(yaxis=dict(title=''), xaxis=dict(title='', showgrid=False, gridcolor='grey',
                      tickvals=[],),hovermode="y unified")
                fig.update_traces(connectgaps=False,hovertemplate=None)


                st.plotly_chart(fig)

            elif option=='Bar only':
                df_dt = pd.to_datetime(df_dt)
                dm = df_dt.dt.strftime('%m-%d')
                dav = dm.value_counts().sort_index()


                fig1 = plt.figure(figsize = (4,2))

                ax = plt.axes()
                ax.barh(dav.index,dav,color=sns.color_palette("tab10"),align ='center')
                # Remove axes splines
                for s in ['top', 'bottom', 'left', 'right']:
                    ax.spines[s].set_visible(False)
                    # Remove x, y Ticks
                ax.xaxis.set_ticks_position('none')
                ax.yaxis.set_ticks_position('none')

                plt.yticks(fontsize=5)
                plt.ylabel("day",size = 4)

                ax.legend()        
 
                ax.get_xaxis().set_visible(False)

                ax.set_title('Data Available Per day',
                         loc ='left',fontsize=5 )
            # Add annotation to bars
                for p in ax.patches:
                    left, bottom, width, height = p.get_bbox().bounds
                    ax.annotate(str(int(width)), xy=(left+width/2, bottom+height/2), 
                                ha='center', va='center', size = 3)
            
                # save image, display it, and delete after usage.
                plt.savefig('x',dpi=200)
                st.image('x.png')
                os.remove('x.png')
                        
            else:
                fig = px.scatter(df, x="files", y="UTC time",
                                 title='Data Availabiltiy Plot for {} of the entire deployment (Please enlarge the plot for better visualization)'.format(deviceZ),
                                 template='plotly_white'
                )
                fig.update_layout(yaxis=dict(title=''), xaxis=dict(title='', showgrid=False, gridcolor='grey',
                      tickvals=[],),hovermode="y unified")
                fig.update_traces(connectgaps=False,hovertemplate=None)
                
                df_dt = pd.to_datetime(df_dt)
                dm = df_dt.dt.strftime('%m-%d')
                dav = dm.value_counts().sort_index()


                fig1 = plt.figure(figsize = (4,2))

                ax = plt.axes()
                ax.barh(dav.index,dav,color=sns.color_palette("tab10"),align ='center')
                # Remove axes splines
                for s in ['top', 'bottom', 'left', 'right']:
                    ax.spines[s].set_visible(False)
                    # Remove x, y Ticks
                ax.xaxis.set_ticks_position('none')
                ax.yaxis.set_ticks_position('none')

                plt.yticks(fontsize=5)
                plt.ylabel("day",size = 4)

                ax.legend()        
 
                ax.get_xaxis().set_visible(False)

                ax.set_title('Data Available Per day',
                         loc ='left',fontsize=5 )
            # Add annotation to bars
                for p in ax.patches:
                    left, bottom, width, height = p.get_bbox().bounds
                    ax.annotate(str(int(width)), xy=(left+width/2, bottom+height/2), 
                                ha='center', va='center', size = 3)
            
                # save image, display it, and delete after usage.
                plt.savefig('x',dpi=200)
                st.image('x.png')
                os.remove('x.png')
                st.plotly_chart(fig)

        else:
            st.markdown("No data found, try other extension, please.")
            
    elif opt=='Barkley Node - Hydrophone Array D':
        filters1 = {
            'locationCode': 'BACNH.H4',
            'deviceCategoryCode': 'HYDROPHONE',
            }
        resultX = onc.getLocations(filters1)
        za = pd.DataFrame(resultX)
        st.markdown(za.description.values[0])


        df_dep = []
        for deployment in onc.getDeployments(filters={'locationCode': 'BACNH.H4', 'deviceCategoryCode': 'HYDROPHONE'}):
            df_dep.append([deployment['locationCode'], deployment['begin'], deployment['end']])

        npl = np.array(df_dep)
        locationC = pd.DataFrame(npl[:,0])
        deplF = pd.DataFrame(npl[:,1])
        deplT = pd.DataFrame(npl[:,2])

        df_dep = pd.concat([locationC,deplF,deplT],axis=1)
        df_dep.columns=["Location Code", "Deployed from", "Deployed to"]


        st.write("There are {} deployments.".format(df_dep.shape[0]))
        df_dep["Deployed from"] = pd.to_datetime(df_dep["Deployed from"]).apply(lambda y: y.date())
        df_dep["Deployed to"] = pd.to_datetime(df_dep["Deployed to"]).apply(lambda y: y.date())
        fe = df_dep.style.hide_index()
        st.write(fe.to_html(), unsafe_allow_html=True)

        start_date = st.sidebar.date_input("Select Start Date")
        end_date = st.sidebar.date_input("Select End Date")

        e = datetime.strptime(str(start_date),"%Y-%m-%d")
        el =datetime.timestamp(e)
        elT = datetime.utcfromtimestamp(el).strftime("%Y-%m-%dT%H:%M:%S")+'.000Z'
        f = datetime.strptime(str(end_date),"%Y-%m-%d")
        fl =datetime.timestamp(f)
        flT = datetime.utcfromtimestamp(fl).strftime("%Y-%m-%dT%H:%M:%S")+'.000Z'


        df_dev = []
        for dev in onc.getDevices({
            'locationCode': 'BACNH.H4',
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
                'locationCode': 'BACNH.H4'
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
        result1 = onc.getListByDevice(filt, allPages=True)
        df = pd.DataFrame(result1)
        if len(df) > 0:
            st.markdown("There are {} files".format(len(df)) + ' from ' + filt['deviceCode'] 
                    + ' between '   + parse(filt['dateFrom']).strftime('%Y %b %d')
            + ' and ' + parse(filt['dateTo']).strftime('%Y %b %d'))
            with st.expander("Data:"):
                st.write(df)
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
                                    .strip('-spect').strip('-spect-small').strip('-LPF-spect').strip('-LPF-spect-thumb')
                                    .strip('-HPF-spect').strip('-HPF-spect-thumb').split('_')[1])   
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
            
                    
            option = st.selectbox(
                'How would you like to visualize the data availability:?',
                ('Line only', 'Bar only', 'Both'))
            
            if option == 'Line only':
                fig = px.scatter(df, x="files", y="UTC time",
                                 title='Data Availabiltiy Plot for {} of the entire deployment (Please enlarge the plot for better visualization)'.format(deviceZ),
                                 template='plotly_white'
                )
                fig.update_layout(yaxis=dict(title=''), xaxis=dict(title='', showgrid=False, gridcolor='grey',
                      tickvals=[],),hovermode="y unified")
                fig.update_traces(connectgaps=False,hovertemplate=None)


                st.plotly_chart(fig)

            elif option=='Bar only':
                df_dt = pd.to_datetime(df_dt)
                dm = df_dt.dt.strftime('%m-%d')
                dav = dm.value_counts().sort_index()


                fig1 = plt.figure(figsize = (4,2))

                ax = plt.axes()
                ax.barh(dav.index,dav,color=sns.color_palette("tab10"),align ='center')
                # Remove axes splines
                for s in ['top', 'bottom', 'left', 'right']:
                    ax.spines[s].set_visible(False)
                    # Remove x, y Ticks
                ax.xaxis.set_ticks_position('none')
                ax.yaxis.set_ticks_position('none')

                plt.yticks(fontsize=5)
                plt.ylabel("day",size = 4)

                ax.legend()        
 
                ax.get_xaxis().set_visible(False)

                ax.set_title('Data Available Per day',
                         loc ='left',fontsize=5 )
            # Add annotation to bars
                for p in ax.patches:
                    left, bottom, width, height = p.get_bbox().bounds
                    ax.annotate(str(int(width)), xy=(left+width/2, bottom+height/2), 
                                ha='center', va='center', size = 3)
            
                # save image, display it, and delete after usage.
                plt.savefig('x',dpi=200)
                st.image('x.png')
                os.remove('x.png')
                        
            else:
                fig = px.scatter(df, x="files", y="UTC time",
                                 title='Data Availabiltiy Plot for {} of the entire deployment (Please enlarge the plot for better visualization)'.format(deviceZ),
                                 template='plotly_white'
                )
                fig.update_layout(yaxis=dict(title=''), xaxis=dict(title='', showgrid=False, gridcolor='grey',
                      tickvals=[],),hovermode="y unified")
                fig.update_traces(connectgaps=False,hovertemplate=None)
                
                df_dt = pd.to_datetime(df_dt)
                dm = df_dt.dt.strftime('%m-%d')
                dav = dm.value_counts().sort_index()


                fig1 = plt.figure(figsize = (4,2))

                ax = plt.axes()
                ax.barh(dav.index,dav,color=sns.color_palette("tab10"),align ='center')
                # Remove axes splines
                for s in ['top', 'bottom', 'left', 'right']:
                    ax.spines[s].set_visible(False)
                    # Remove x, y Ticks
                ax.xaxis.set_ticks_position('none')
                ax.yaxis.set_ticks_position('none')

                plt.yticks(fontsize=5)
                plt.ylabel("day",size = 4)

                ax.legend()        
 
                ax.get_xaxis().set_visible(False)

                ax.set_title('Data Available Per day',
                         loc ='left',fontsize=5 )
            # Add annotation to bars
                for p in ax.patches:
                    left, bottom, width, height = p.get_bbox().bounds
                    ax.annotate(str(int(width)), xy=(left+width/2, bottom+height/2), 
                                ha='center', va='center', size = 3)
            
                # save image, display it, and delete after usage.
                plt.savefig('x',dpi=200)
                st.image('x.png')
                os.remove('x.png')
                st.plotly_chart(fig)

        else:
            st.markdown("No data found, try other extension, please.")


    elif opt=='Cascadia Basin - Hydrophone Array A':
        filters1 = {
            'locationCode': 'CBCH.H1',
            'deviceCategoryCode': 'HYDROPHONE',
            }
        resultX = onc.getLocations(filters1)
        za = pd.DataFrame(resultX)
        st.markdown(za.description.values[0])


        df_dep = []
        for deployment in onc.getDeployments(filters={'locationCode': 'CBCH.H1', 'deviceCategoryCode': 'HYDROPHONE'}):
            df_dep.append([deployment['locationCode'], deployment['begin'], deployment['end']])

        npl = np.array(df_dep)
        locationC = pd.DataFrame(npl[:,0])
        deplF = pd.DataFrame(npl[:,1])
        deplT = pd.DataFrame(npl[:,2])

        df_dep = pd.concat([locationC,deplF,deplT],axis=1)
        df_dep.columns=["Location Code", "Deployed from", "Deployed to"]


        st.write("There are {} deployments.".format(df_dep.shape[0]))
        df_dep["Deployed from"] = pd.to_datetime(df_dep["Deployed from"]).apply(lambda y: y.date())
        df_dep["Deployed to"] = pd.to_datetime(df_dep["Deployed to"]).apply(lambda y: y.date())
        fe = df_dep.style.hide_index()
        st.write(fe.to_html(), unsafe_allow_html=True)

        start_date = st.sidebar.date_input("Select Start Date")
        end_date = st.sidebar.date_input("Select End Date")

        e = datetime.strptime(str(start_date),"%Y-%m-%d")
        el =datetime.timestamp(e)
        elT = datetime.utcfromtimestamp(el).strftime("%Y-%m-%dT%H:%M:%S")+'.000Z'
        f = datetime.strptime(str(end_date),"%Y-%m-%d")
        fl =datetime.timestamp(f)
        flT = datetime.utcfromtimestamp(fl).strftime("%Y-%m-%dT%H:%M:%S")+'.000Z'


        df_dev = []
        for dev in onc.getDevices({
            'locationCode': 'CBCH.H1',
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
                'locationCode': 'CBCH.H1'
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
        result1 = onc.getListByDevice(filt, allPages=True)
        df = pd.DataFrame(result1)
        if len(df) > 0:
            st.markdown("There are {} files".format(len(df)) + ' from ' + filt['deviceCode'] 
                    + ' between '   + parse(filt['dateFrom']).strftime('%Y %b %d')
            + ' and ' + parse(filt['dateTo']).strftime('%Y %b %d'))
            with st.expander("Data:"):
                st.write(df)
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
                                    .strip('-spect').strip('-spect-small').strip('-LPF-spect').strip('-LPF-spect-thumb')
                                    .strip('-HPF-spect').strip('-HPF-spect-thumb').split('_')[1])   
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
            
                    
            option = st.selectbox(
                'How would you like to visualize the data availability:?',
                ('Line only', 'Bar only', 'Both'))
            
            if option == 'Line only':
                fig = px.scatter(df, x="files", y="UTC time",
                                 title='Data Availabiltiy Plot for {} of the entire deployment (Please enlarge the plot for better visualization)'.format(deviceZ),
                                 template='plotly_white'
                )
                fig.update_layout(yaxis=dict(title=''), xaxis=dict(title='', showgrid=False, gridcolor='grey',
                      tickvals=[],),hovermode="y unified")
                fig.update_traces(connectgaps=False,hovertemplate=None)


                st.plotly_chart(fig)

            elif option=='Bar only':
                df_dt = pd.to_datetime(df_dt)
                dm = df_dt.dt.strftime('%m-%d')
                dav = dm.value_counts().sort_index()


                fig1 = plt.figure(figsize = (4,2))

                ax = plt.axes()
                ax.barh(dav.index,dav,color=sns.color_palette("tab10"),align ='center')
                # Remove axes splines
                for s in ['top', 'bottom', 'left', 'right']:
                    ax.spines[s].set_visible(False)
                    # Remove x, y Ticks
                ax.xaxis.set_ticks_position('none')
                ax.yaxis.set_ticks_position('none')

                plt.yticks(fontsize=5)
                plt.ylabel("day",size = 4)

                ax.legend()        
 
                ax.get_xaxis().set_visible(False)

                ax.set_title('Data Available Per day',
                         loc ='left',fontsize=5 )
            # Add annotation to bars
                for p in ax.patches:
                    left, bottom, width, height = p.get_bbox().bounds
                    ax.annotate(str(int(width)), xy=(left+width/2, bottom+height/2), 
                                ha='center', va='center', size = 3)
            
                # save image, display it, and delete after usage.
                plt.savefig('x',dpi=200)
                st.image('x.png')
                os.remove('x.png')
                        
            else:
                fig = px.scatter(df, x="files", y="UTC time",
                                 title='Data Availabiltiy Plot for {} of the entire deployment (Please enlarge the plot for better visualization)'.format(deviceZ),
                                 template='plotly_white'
                )
                fig.update_layout(yaxis=dict(title=''), xaxis=dict(title='', showgrid=False, gridcolor='grey',
                      tickvals=[],),hovermode="y unified")
                fig.update_traces(connectgaps=False,hovertemplate=None)
                
                df_dt = pd.to_datetime(df_dt)
                dm = df_dt.dt.strftime('%m-%d')
                dav = dm.value_counts().sort_index()


                fig1 = plt.figure(figsize = (4,2))

                ax = plt.axes()
                ax.barh(dav.index,dav,color=sns.color_palette("tab10"),align ='center')
                # Remove axes splines
                for s in ['top', 'bottom', 'left', 'right']:
                    ax.spines[s].set_visible(False)
                    # Remove x, y Ticks
                ax.xaxis.set_ticks_position('none')
                ax.yaxis.set_ticks_position('none')

                plt.yticks(fontsize=5)
                plt.ylabel("day",size = 4)

                ax.legend()        
 
                ax.get_xaxis().set_visible(False)

                ax.set_title('Data Available Per day',
                         loc ='left',fontsize=5 )
            # Add annotation to bars
                for p in ax.patches:
                    left, bottom, width, height = p.get_bbox().bounds
                    ax.annotate(str(int(width)), xy=(left+width/2, bottom+height/2), 
                                ha='center', va='center', size = 3)
            
                # save image, display it, and delete after usage.
                plt.savefig('x',dpi=200)
                st.image('x.png')
                os.remove('x.png')
                st.plotly_chart(fig)
        else:
            st.markdown("No data found, try other extension, please.")
    elif opt=='Cascadia Basin - Hydrophone Array B':
        filters1 = {
            'locationCode': 'CBCH.H2',
            'deviceCategoryCode': 'HYDROPHONE',
            }
        resultX = onc.getLocations(filters1)
        za = pd.DataFrame(resultX)
        st.markdown(za.description.values[0])


        df_dep = []
        for deployment in onc.getDeployments(filters={'locationCode': 'CBCH.H2', 'deviceCategoryCode': 'HYDROPHONE'}):
            df_dep.append([deployment['locationCode'], deployment['begin'], deployment['end']])

        npl = np.array(df_dep)
        locationC = pd.DataFrame(npl[:,0])
        deplF = pd.DataFrame(npl[:,1])
        deplT = pd.DataFrame(npl[:,2])

        df_dep = pd.concat([locationC,deplF,deplT],axis=1)
        df_dep.columns=["Location Code", "Deployed from", "Deployed to"]


        st.write("There are {} deployments.".format(df_dep.shape[0]))
        df_dep["Deployed from"] = pd.to_datetime(df_dep["Deployed from"]).apply(lambda y: y.date())
        df_dep["Deployed to"] = pd.to_datetime(df_dep["Deployed to"]).apply(lambda y: y.date())
        fe = df_dep.style.hide_index()
        st.write(fe.to_html(), unsafe_allow_html=True)

        start_date = st.sidebar.date_input("Select Start Date")
        end_date = st.sidebar.date_input("Select End Date")

        e = datetime.strptime(str(start_date),"%Y-%m-%d")
        el =datetime.timestamp(e)
        elT = datetime.utcfromtimestamp(el).strftime("%Y-%m-%dT%H:%M:%S")+'.000Z'
        f = datetime.strptime(str(end_date),"%Y-%m-%d")
        fl =datetime.timestamp(f)
        flT = datetime.utcfromtimestamp(fl).strftime("%Y-%m-%dT%H:%M:%S")+'.000Z'


        df_dev = []
        for dev in onc.getDevices({
            'locationCode': 'CBCH.H2',
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
                'locationCode': 'CBCH.H2'
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
        result1 = onc.getListByDevice(filt, allPages=True)
        df = pd.DataFrame(result1)
        if len(df) > 0:
            st.markdown("There are {} files".format(len(df)) + ' from ' + filt['deviceCode'] 
                    + ' between '   + parse(filt['dateFrom']).strftime('%Y %b %d')
            + ' and ' + parse(filt['dateTo']).strftime('%Y %b %d'))
            with st.expander("Data:"):
                st.write(df)
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
                                    .strip('-spect').strip('-spect-small').strip('-LPF-spect').strip('-LPF-spect-thumb')
                                    .strip('-HPF-spect').strip('-HPF-spect-thumb').split('_')[1])   
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
            
                    
            option = st.selectbox(
                'How would you like to visualize the data availability:?',
                ('Line only', 'Bar only', 'Both'))
            
            if option == 'Line only':
                fig = px.scatter(df, x="files", y="UTC time",
                                 title='Data Availabiltiy Plot for {} of the entire deployment (Please enlarge the plot for better visualization)'.format(deviceZ),
                                 template='plotly_white'
                )
                fig.update_layout(yaxis=dict(title=''), xaxis=dict(title='', showgrid=False, gridcolor='grey',
                      tickvals=[],),hovermode="y unified")
                fig.update_traces(connectgaps=False,hovertemplate=None)


                st.plotly_chart(fig)

            elif option=='Bar only':
                df_dt = pd.to_datetime(df_dt)
                dm = df_dt.dt.strftime('%m-%d')
                dav = dm.value_counts().sort_index()


                fig1 = plt.figure(figsize = (4,2))

                ax = plt.axes()
                ax.barh(dav.index,dav,color=sns.color_palette("tab10"),align ='center')
                # Remove axes splines
                for s in ['top', 'bottom', 'left', 'right']:
                    ax.spines[s].set_visible(False)
                    # Remove x, y Ticks
                ax.xaxis.set_ticks_position('none')
                ax.yaxis.set_ticks_position('none')

                plt.yticks(fontsize=5)
                plt.ylabel("day",size = 4)

                ax.legend()        
 
                ax.get_xaxis().set_visible(False)

                ax.set_title('Data Available Per day',
                         loc ='left',fontsize=5 )
            # Add annotation to bars
                for p in ax.patches:
                    left, bottom, width, height = p.get_bbox().bounds
                    ax.annotate(str(int(width)), xy=(left+width/2, bottom+height/2), 
                                ha='center', va='center', size = 3)
            
                # save image, display it, and delete after usage.
                plt.savefig('x',dpi=200)
                st.image('x.png')
                os.remove('x.png')
                        
            else:
                fig = px.scatter(df, x="files", y="UTC time",
                                 title='Data Availabiltiy Plot for {} of the entire deployment (Please enlarge the plot for better visualization)'.format(deviceZ),
                                 template='plotly_white'
                )
                fig.update_layout(yaxis=dict(title=''), xaxis=dict(title='', showgrid=False, gridcolor='grey',
                      tickvals=[],),hovermode="y unified")
                fig.update_traces(connectgaps=False,hovertemplate=None)
                
                df_dt = pd.to_datetime(df_dt)
                dm = df_dt.dt.strftime('%m-%d')
                dav = dm.value_counts().sort_index()


                fig1 = plt.figure(figsize = (4,2))

                ax = plt.axes()
                ax.barh(dav.index,dav,color=sns.color_palette("tab10"),align ='center')
                # Remove axes splines
                for s in ['top', 'bottom', 'left', 'right']:
                    ax.spines[s].set_visible(False)
                    # Remove x, y Ticks
                ax.xaxis.set_ticks_position('none')
                ax.yaxis.set_ticks_position('none')

                plt.yticks(fontsize=5)
                plt.ylabel("day",size = 4)

                ax.legend()        
 
                ax.get_xaxis().set_visible(False)

                ax.set_title('Data Available Per day',
                         loc ='left',fontsize=5 )
            # Add annotation to bars
                for p in ax.patches:
                    left, bottom, width, height = p.get_bbox().bounds
                    ax.annotate(str(int(width)), xy=(left+width/2, bottom+height/2), 
                                ha='center', va='center', size = 3)
            
                # save image, display it, and delete after usage.
                plt.savefig('x',dpi=200)
                st.image('x.png')
                os.remove('x.png')
                st.plotly_chart(fig)
        else:
            st.markdown("No data found, try other extension, please.")
    elif opt=='Cascadia Basin - Hydrophone Array C':
        filters1 = {
            'locationCode': 'CBCH.H3',
            'deviceCategoryCode': 'HYDROPHONE',
            }
        resultX = onc.getLocations(filters1)
        za = pd.DataFrame(resultX)
        st.markdown(za.description.values[0])


        df_dep = []
        for deployment in onc.getDeployments(filters={'locationCode': 'CBCH.H3', 'deviceCategoryCode': 'HYDROPHONE'}):
            df_dep.append([deployment['locationCode'], deployment['begin'], deployment['end']])

        npl = np.array(df_dep)
        locationC = pd.DataFrame(npl[:,0])
        deplF = pd.DataFrame(npl[:,1])
        deplT = pd.DataFrame(npl[:,2])

        df_dep = pd.concat([locationC,deplF,deplT],axis=1)
        df_dep.columns=["Location Code", "Deployed from", "Deployed to"]


        st.write("There are {} deployments.".format(df_dep.shape[0]))
        df_dep["Deployed from"] = pd.to_datetime(df_dep["Deployed from"]).apply(lambda y: y.date())
        df_dep["Deployed to"] = pd.to_datetime(df_dep["Deployed to"]).apply(lambda y: y.date())
        fe = df_dep.style.hide_index()
        st.write(fe.to_html(), unsafe_allow_html=True)

        start_date = st.sidebar.date_input("Select Start Date")
        end_date = st.sidebar.date_input("Select End Date")

        e = datetime.strptime(str(start_date),"%Y-%m-%d")
        el =datetime.timestamp(e)
        elT = datetime.utcfromtimestamp(el).strftime("%Y-%m-%dT%H:%M:%S")+'.000Z'
        f = datetime.strptime(str(end_date),"%Y-%m-%d")
        fl =datetime.timestamp(f)
        flT = datetime.utcfromtimestamp(fl).strftime("%Y-%m-%dT%H:%M:%S")+'.000Z'


        df_dev = []
        for dev in onc.getDevices({
            'locationCode': 'CBCH.H3',
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
                'locationCode': 'CBCH.H3'
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
        result1 = onc.getListByDevice(filt, allPages=True)
        df = pd.DataFrame(result1)
        if len(df) > 0:
            st.markdown("There are {} files".format(len(df)) + ' from ' + filt['deviceCode'] 
                    + ' between '   + parse(filt['dateFrom']).strftime('%Y %b %d')
            + ' and ' + parse(filt['dateTo']).strftime('%Y %b %d'))
            with st.expander("Data:"):
                st.write(df)
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
                                    .strip('-spect').strip('-spect-small').strip('-LPF-spect').strip('-LPF-spect-thumb')
                                    .strip('-HPF-spect').strip('-HPF-spect-thumb').split('_')[1])   
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
            
                    
            option = st.selectbox(
                'How would you like to visualize the data availability:?',
                ('Line only', 'Bar only', 'Both'))
            
            if option == 'Line only':
                fig = px.scatter(df, x="files", y="UTC time",
                                 title='Data Availabiltiy Plot for {} of the entire deployment (Please enlarge the plot for better visualization)'.format(deviceZ),
                                 template='plotly_white'
                )
                fig.update_layout(yaxis=dict(title=''), xaxis=dict(title='', showgrid=False, gridcolor='grey',
                      tickvals=[],),hovermode="y unified")
                fig.update_traces(connectgaps=False,hovertemplate=None)


                st.plotly_chart(fig)

            elif option=='Bar only':
                df_dt = pd.to_datetime(df_dt)
                dm = df_dt.dt.strftime('%m-%d')
                dav = dm.value_counts().sort_index()


                fig1 = plt.figure(figsize = (4,2))

                ax = plt.axes()
                ax.barh(dav.index,dav,color=sns.color_palette("tab10"),align ='center')
                # Remove axes splines
                for s in ['top', 'bottom', 'left', 'right']:
                    ax.spines[s].set_visible(False)
                    # Remove x, y Ticks
                ax.xaxis.set_ticks_position('none')
                ax.yaxis.set_ticks_position('none')

                plt.yticks(fontsize=5)
                plt.ylabel("day",size = 4)

                ax.legend()        
 
                ax.get_xaxis().set_visible(False)

                ax.set_title('Data Available Per day',
                         loc ='left',fontsize=5 )
            # Add annotation to bars
                for p in ax.patches:
                    left, bottom, width, height = p.get_bbox().bounds
                    ax.annotate(str(int(width)), xy=(left+width/2, bottom+height/2), 
                                ha='center', va='center', size = 3)
            
                # save image, display it, and delete after usage.
                plt.savefig('x',dpi=200)
                st.image('x.png')
                os.remove('x.png')
                        
            else:
                fig = px.scatter(df, x="files", y="UTC time",
                                 title='Data Availabiltiy Plot for {} of the entire deployment (Please enlarge the plot for better visualization)'.format(deviceZ),
                                 template='plotly_white'
                )
                fig.update_layout(yaxis=dict(title=''), xaxis=dict(title='', showgrid=False, gridcolor='grey',
                      tickvals=[],),hovermode="y unified")
                fig.update_traces(connectgaps=False,hovertemplate=None)
                
                df_dt = pd.to_datetime(df_dt)
                dm = df_dt.dt.strftime('%m-%d')
                dav = dm.value_counts().sort_index()


                fig1 = plt.figure(figsize = (4,2))

                ax = plt.axes()
                ax.barh(dav.index,dav,color=sns.color_palette("tab10"),align ='center')
                # Remove axes splines
                for s in ['top', 'bottom', 'left', 'right']:
                    ax.spines[s].set_visible(False)
                    # Remove x, y Ticks
                ax.xaxis.set_ticks_position('none')
                ax.yaxis.set_ticks_position('none')

                plt.yticks(fontsize=5)
                plt.ylabel("day",size = 4)

                ax.legend()        
 
                ax.get_xaxis().set_visible(False)

                ax.set_title('Data Available Per day',
                         loc ='left',fontsize=5 )
            # Add annotation to bars
                for p in ax.patches:
                    left, bottom, width, height = p.get_bbox().bounds
                    ax.annotate(str(int(width)), xy=(left+width/2, bottom+height/2), 
                                ha='center', va='center', size = 3)
            
                # save image, display it, and delete after usage.
                plt.savefig('x',dpi=200)
                st.image('x.png')
                os.remove('x.png')
                st.plotly_chart(fig)
        else:
            st.markdown("No data found, try other extension, please.")
    elif opt=='Cascadia Basin - Hydrophone Array D':
        filters1 = {
            'locationCode': 'CBCH.H4',
            'deviceCategoryCode': 'HYDROPHONE',
            }
        resultX = onc.getLocations(filters1)
        za = pd.DataFrame(resultX)
        st.markdown(za.description.values[0])


        df_dep = []
        for deployment in onc.getDeployments(filters={'locationCode': 'CBCH.H4', 'deviceCategoryCode': 'HYDROPHONE'}):
            df_dep.append([deployment['locationCode'], deployment['begin'], deployment['end']])

        npl = np.array(df_dep)
        locationC = pd.DataFrame(npl[:,0])
        deplF = pd.DataFrame(npl[:,1])
        deplT = pd.DataFrame(npl[:,2])

        df_dep = pd.concat([locationC,deplF,deplT],axis=1)
        df_dep.columns=["Location Code", "Deployed from", "Deployed to"]


        st.write("There are {} deployments.".format(df_dep.shape[0]))
        df_dep["Deployed from"] = pd.to_datetime(df_dep["Deployed from"]).apply(lambda y: y.date())
        df_dep["Deployed to"] = pd.to_datetime(df_dep["Deployed to"]).apply(lambda y: y.date())
        fe = df_dep.style.hide_index()
        st.write(fe.to_html(), unsafe_allow_html=True)

        start_date = st.sidebar.date_input("Select Start Date")
        end_date = st.sidebar.date_input("Select End Date")

        e = datetime.strptime(str(start_date),"%Y-%m-%d")
        el =datetime.timestamp(e)
        elT = datetime.utcfromtimestamp(el).strftime("%Y-%m-%dT%H:%M:%S")+'.000Z'
        f = datetime.strptime(str(end_date),"%Y-%m-%d")
        fl =datetime.timestamp(f)
        flT = datetime.utcfromtimestamp(fl).strftime("%Y-%m-%dT%H:%M:%S")+'.000Z'


        df_dev = []
        for dev in onc.getDevices({
            'locationCode': 'CBCH.H4',
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
                'locationCode': 'CBCH.H4'
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
        result1 = onc.getListByDevice(filt, allPages=True)
        df = pd.DataFrame(result1)
        if len(df) > 0:
            st.markdown("There are {} files".format(len(df)) + ' from ' + filt['deviceCode'] 
                    + ' between '   + parse(filt['dateFrom']).strftime('%Y %b %d')
            + ' and ' + parse(filt['dateTo']).strftime('%Y %b %d'))
            with st.expander("Data:"):
                st.write(df)
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
                                    .strip('-spect').strip('-spect-small').strip('-LPF-spect').strip('-LPF-spect-thumb')
                                    .strip('-HPF-spect').strip('-HPF-spect-thumb').split('_')[1])   
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
            
                    
            option = st.selectbox(
                'How would you like to visualize the data availability:?',
                ('Line only', 'Bar only', 'Both'))
            
            if option == 'Line only':
                fig = px.scatter(df, x="files", y="UTC time",
                                 title='Data Availabiltiy Plot for {} of the entire deployment (Please enlarge the plot for better visualization)'.format(deviceZ),
                                 template='plotly_white'
                )
                fig.update_layout(yaxis=dict(title=''), xaxis=dict(title='', showgrid=False, gridcolor='grey',
                      tickvals=[],),hovermode="y unified")
                fig.update_traces(connectgaps=False,hovertemplate=None)


                st.plotly_chart(fig)

            elif option=='Bar only':
                df_dt = pd.to_datetime(df_dt)
                dm = df_dt.dt.strftime('%m-%d')
                dav = dm.value_counts().sort_index()


                fig1 = plt.figure(figsize = (4,2))

                ax = plt.axes()
                ax.barh(dav.index,dav,color=sns.color_palette("tab10"),align ='center')
                # Remove axes splines
                for s in ['top', 'bottom', 'left', 'right']:
                    ax.spines[s].set_visible(False)
                    # Remove x, y Ticks
                ax.xaxis.set_ticks_position('none')
                ax.yaxis.set_ticks_position('none')

                plt.yticks(fontsize=5)
                plt.ylabel("day",size = 4)

                ax.legend()        
 
                ax.get_xaxis().set_visible(False)

                ax.set_title('Data Available Per day',
                         loc ='left',fontsize=5 )
            # Add annotation to bars
                for p in ax.patches:
                    left, bottom, width, height = p.get_bbox().bounds
                    ax.annotate(str(int(width)), xy=(left+width/2, bottom+height/2), 
                                ha='center', va='center', size = 3)
            
                # save image, display it, and delete after usage.
                plt.savefig('x',dpi=200)
                st.image('x.png')
                os.remove('x.png')
                        
            else:
                fig = px.scatter(df, x="files", y="UTC time",
                                 title='Data Availabiltiy Plot for {} of the entire deployment (Please enlarge the plot for better visualization)'.format(deviceZ),
                                 template='plotly_white'
                )
                fig.update_layout(yaxis=dict(title=''), xaxis=dict(title='', showgrid=False, gridcolor='grey',
                      tickvals=[],),hovermode="y unified")
                fig.update_traces(connectgaps=False,hovertemplate=None)
                
                df_dt = pd.to_datetime(df_dt)
                dm = df_dt.dt.strftime('%m-%d')
                dav = dm.value_counts().sort_index()


                fig1 = plt.figure(figsize = (4,2))

                ax = plt.axes()
                ax.barh(dav.index,dav,color=sns.color_palette("tab10"),align ='center')
                # Remove axes splines
                for s in ['top', 'bottom', 'left', 'right']:
                    ax.spines[s].set_visible(False)
                    # Remove x, y Ticks
                ax.xaxis.set_ticks_position('none')
                ax.yaxis.set_ticks_position('none')

                plt.yticks(fontsize=5)
                plt.ylabel("day",size = 4)

                ax.legend()        
 
                ax.get_xaxis().set_visible(False)

                ax.set_title('Data Available Per day',
                         loc ='left',fontsize=5 )
            # Add annotation to bars
                for p in ax.patches:
                    left, bottom, width, height = p.get_bbox().bounds
                    ax.annotate(str(int(width)), xy=(left+width/2, bottom+height/2), 
                                ha='center', va='center', size = 3)
            
                # save image, display it, and delete after usage.
                plt.savefig('x',dpi=200)
                st.image('x.png')
                os.remove('x.png')
                st.plotly_chart(fig)
        else:
            st.markdown("No data found, try other extension, please.")
    elif opt=='SOG-Fraser River Delta Upper Slope':
        filters1 = {
            'locationCode': 'USDDL',
            'deviceCategoryCode': 'HYDROPHONE',
            }
        resultX = onc.getLocations(filters1)
        za = pd.DataFrame(resultX)
        st.markdown(za.description.values[0])


        df_dep = []
        for deployment in onc.getDeployments(filters={'locationCode': 'USDDL', 'deviceCategoryCode': 'HYDROPHONE'}):
            df_dep.append([deployment['locationCode'], deployment['begin'], deployment['end']])

        npl = np.array(df_dep)
        locationC = pd.DataFrame(npl[:,0])
        deplF = pd.DataFrame(npl[:,1])
        deplT = pd.DataFrame(npl[:,2])

        df_dep = pd.concat([locationC,deplF,deplT],axis=1)
        df_dep.columns=["Location Code", "Deployed from", "Deployed to"]


        st.write("There are {} deployments.".format(df_dep.shape[0]))
        df_dep["Deployed from"] = pd.to_datetime(df_dep["Deployed from"]).apply(lambda y: y.date())
        df_dep["Deployed to"] = pd.to_datetime(df_dep["Deployed to"]).apply(lambda y: y.date())
        fe = df_dep.style.hide_index()
        st.write(fe.to_html(), unsafe_allow_html=True)

        start_date = st.sidebar.date_input("Select Start Date")
        end_date = st.sidebar.date_input("Select End Date")

        e = datetime.strptime(str(start_date),"%Y-%m-%d")
        el =datetime.timestamp(e)
        elT = datetime.utcfromtimestamp(el).strftime("%Y-%m-%dT%H:%M:%S")+'.000Z'
        f = datetime.strptime(str(end_date),"%Y-%m-%d")
        fl =datetime.timestamp(f)
        flT = datetime.utcfromtimestamp(fl).strftime("%Y-%m-%dT%H:%M:%S")+'.000Z'


        df_dev = []
        for dev in onc.getDevices({
            'locationCode': 'USDDL',
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
                'locationCode': 'USDDL'
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
        result1 = onc.getListByDevice(filt, allPages=True)
        df = pd.DataFrame(result1)
        if len(df) > 0:
            st.markdown("There are {} files".format(len(df)) + ' from ' + filt['deviceCode'] 
                    + ' between '   + parse(filt['dateFrom']).strftime('%Y %b %d')
            + ' and ' + parse(filt['dateTo']).strftime('%Y %b %d'))
            with st.expander("Data:"):
                st.write(df)
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
                                    .strip('-spect').strip('-spect-small').strip('-LPF-spect').strip('-LPF-spect-thumb')
                                    .strip('-HPF-spect').strip('-HPF-spect-thumb').split('_')[1])   
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
            
                    
            option = st.selectbox(
                'How would you like to visualize the data availability:?',
                ('Line only', 'Bar only', 'Both'))
            
            if option == 'Line only':
                fig = px.scatter(df, x="files", y="UTC time",
                                 title='Data Availabiltiy Plot for {} of the entire deployment (Please enlarge the plot for better visualization)'.format(deviceZ),
                                 template='plotly_white'
                )
                fig.update_layout(yaxis=dict(title=''), xaxis=dict(title='', showgrid=False, gridcolor='grey',
                      tickvals=[],),hovermode="y unified")
                fig.update_traces(connectgaps=False,hovertemplate=None)


                st.plotly_chart(fig)

            elif option=='Bar only':
                df_dt = pd.to_datetime(df_dt)
                dm = df_dt.dt.strftime('%m-%d')
                dav = dm.value_counts().sort_index()


                fig1 = plt.figure(figsize = (4,2))

                ax = plt.axes()
                ax.barh(dav.index,dav,color=sns.color_palette("tab10"),align ='center')
                # Remove axes splines
                for s in ['top', 'bottom', 'left', 'right']:
                    ax.spines[s].set_visible(False)
                    # Remove x, y Ticks
                ax.xaxis.set_ticks_position('none')
                ax.yaxis.set_ticks_position('none')

                plt.yticks(fontsize=5)
                plt.ylabel("day",size = 4)

                ax.legend()        
 
                ax.get_xaxis().set_visible(False)

                ax.set_title('Data Available Per day',
                         loc ='left',fontsize=5 )
            # Add annotation to bars
                for p in ax.patches:
                    left, bottom, width, height = p.get_bbox().bounds
                    ax.annotate(str(int(width)), xy=(left+width/2, bottom+height/2), 
                                ha='center', va='center', size = 3)
            
                # save image, display it, and delete after usage.
                plt.savefig('x',dpi=200)
                st.image('x.png')
                os.remove('x.png')
                        
            else:
                fig = px.scatter(df, x="files", y="UTC time",
                                 title='Data Availabiltiy Plot for {} of the entire deployment (Please enlarge the plot for better visualization)'.format(deviceZ),
                                 template='plotly_white'
                )
                fig.update_layout(yaxis=dict(title=''), xaxis=dict(title='', showgrid=False, gridcolor='grey',
                      tickvals=[],),hovermode="y unified")
                fig.update_traces(connectgaps=False,hovertemplate=None)
                
                df_dt = pd.to_datetime(df_dt)
                dm = df_dt.dt.strftime('%m-%d')
                dav = dm.value_counts().sort_index()


                fig1 = plt.figure(figsize = (4,2))

                ax = plt.axes()
                ax.barh(dav.index,dav,color=sns.color_palette("tab10"),align ='center')
                # Remove axes splines
                for s in ['top', 'bottom', 'left', 'right']:
                    ax.spines[s].set_visible(False)
                    # Remove x, y Ticks
                ax.xaxis.set_ticks_position('none')
                ax.yaxis.set_ticks_position('none')

                plt.yticks(fontsize=5)
                plt.ylabel("day",size = 4)

                ax.legend()        
 
                ax.get_xaxis().set_visible(False)

                ax.set_title('Data Available Per day',
                         loc ='left',fontsize=5 )
            # Add annotation to bars
                for p in ax.patches:
                    left, bottom, width, height = p.get_bbox().bounds
                    ax.annotate(str(int(width)), xy=(left+width/2, bottom+height/2), 
                                ha='center', va='center', size = 3)
            
                # save image, display it, and delete after usage.
                plt.savefig('x',dpi=200)
                st.image('x.png')
                os.remove('x.png')
                st.plotly_chart(fig)

        else:
            st.markdown("No data found, try other extension, please.")
    elif opt=='SOG Central -VENUS Instrument':
        filters1 = {
            'locationCode': 'SCVIP',
            'deviceCategoryCode': 'HYDROPHONE',
            }
        resultX = onc.getLocations(filters1)
        za = pd.DataFrame(resultX)
        st.markdown(za.description.values[0])


        df_dep = []
        for deployment in onc.getDeployments(filters={'locationCode': 'SCVIP', 'deviceCategoryCode': 'HYDROPHONE'}):
            df_dep.append([deployment['locationCode'], deployment['begin'], deployment['end']])

        npl = np.array(df_dep)
        locationC = pd.DataFrame(npl[:,0])
        deplF = pd.DataFrame(npl[:,1])
        deplT = pd.DataFrame(npl[:,2])

        df_dep = pd.concat([locationC,deplF,deplT],axis=1)
        df_dep.columns=["Location Code", "Deployed from", "Deployed to"]


        st.write("There are {} deployments.".format(df_dep.shape[0]))
        df_dep["Deployed from"] = pd.to_datetime(df_dep["Deployed from"]).apply(lambda y: y.date())
        df_dep["Deployed to"] = pd.to_datetime(df_dep["Deployed to"]).apply(lambda y: y.date())
        fe = df_dep.style.hide_index()
        st.write(fe.to_html(), unsafe_allow_html=True)

        start_date = st.sidebar.date_input("Select Start Date")
        end_date = st.sidebar.date_input("Select End Date")

        e = datetime.strptime(str(start_date),"%Y-%m-%d")
        el =datetime.timestamp(e)
        elT = datetime.utcfromtimestamp(el).strftime("%Y-%m-%dT%H:%M:%S")+'.000Z'
        f = datetime.strptime(str(end_date),"%Y-%m-%d")
        fl =datetime.timestamp(f)
        flT = datetime.utcfromtimestamp(fl).strftime("%Y-%m-%dT%H:%M:%S")+'.000Z'


        df_dev = []
        for dev in onc.getDevices({
            'locationCode': 'SCVIP',
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
                'locationCode': 'SCVIP'
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
        result1 = onc.getListByDevice(filt, allPages=True)
        df = pd.DataFrame(result1)
        if len(df) > 0:
            st.markdown("There are {} files".format(len(df)) + ' from ' + filt['deviceCode'] 
                    + ' between '   + parse(filt['dateFrom']).strftime('%Y %b %d')
            + ' and ' + parse(filt['dateTo']).strftime('%Y %b %d'))
            with st.expander("Data:"):
                st.write(df)
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
                                    .strip('-spect').strip('-spect-small').strip('-LPF-spect').strip('-LPF-spect-thumb')
                                    .strip('-HPF-spect').strip('-HPF-spect-thumb').split('_')[1])   
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
            
                    
            option = st.selectbox(
                'How would you like to visualize the data availability:?',
                ('Line only', 'Bar only', 'Both'))
            
            if option == 'Line only':
                fig = px.scatter(df, x="files", y="UTC time",
                                 title='Data Availabiltiy Plot for {} of the entire deployment (Please enlarge the plot for better visualization)'.format(deviceZ),
                                 template='plotly_white'
                )
                fig.update_layout(yaxis=dict(title=''), xaxis=dict(title='', showgrid=False, gridcolor='grey',
                      tickvals=[],),hovermode="y unified")
                fig.update_traces(connectgaps=False,hovertemplate=None)


                st.plotly_chart(fig)

            elif option=='Bar only':
                df_dt = pd.to_datetime(df_dt)
                dm = df_dt.dt.strftime('%m-%d')
                dav = dm.value_counts().sort_index()


                fig1 = plt.figure(figsize = (4,2))

                ax = plt.axes()
                ax.barh(dav.index,dav,color=sns.color_palette("tab10"),align ='center')
                # Remove axes splines
                for s in ['top', 'bottom', 'left', 'right']:
                    ax.spines[s].set_visible(False)
                    # Remove x, y Ticks
                ax.xaxis.set_ticks_position('none')
                ax.yaxis.set_ticks_position('none')

                plt.yticks(fontsize=5)
                plt.ylabel("day",size = 4)

                ax.legend()        
 
                ax.get_xaxis().set_visible(False)

                ax.set_title('Data Available Per day',
                         loc ='left',fontsize=5 )
            # Add annotation to bars
                for p in ax.patches:
                    left, bottom, width, height = p.get_bbox().bounds
                    ax.annotate(str(int(width)), xy=(left+width/2, bottom+height/2), 
                                ha='center', va='center', size = 3)
            
                # save image, display it, and delete after usage.
                plt.savefig('x',dpi=200)
                st.image('x.png')
                os.remove('x.png')
                        
            else:
                fig = px.scatter(df, x="files", y="UTC time",
                                 title='Data Availabiltiy Plot for {} of the entire deployment (Please enlarge the plot for better visualization)'.format(deviceZ),
                                 template='plotly_white'
                )
                fig.update_layout(yaxis=dict(title=''), xaxis=dict(title='', showgrid=False, gridcolor='grey',
                      tickvals=[],),hovermode="y unified")
                fig.update_traces(connectgaps=False,hovertemplate=None)
                
                df_dt = pd.to_datetime(df_dt)
                dm = df_dt.dt.strftime('%m-%d')
                dav = dm.value_counts().sort_index()


                fig1 = plt.figure(figsize = (4,2))

                ax = plt.axes()
                ax.barh(dav.index,dav,color=sns.color_palette("tab10"),align ='center')
                # Remove axes splines
                for s in ['top', 'bottom', 'left', 'right']:
                    ax.spines[s].set_visible(False)
                    # Remove x, y Ticks
                ax.xaxis.set_ticks_position('none')
                ax.yaxis.set_ticks_position('none')

                plt.yticks(fontsize=5)
                plt.ylabel("day",size = 4)

                ax.legend()        
 
                ax.get_xaxis().set_visible(False)

                ax.set_title('Data Available Per day',
                         loc ='left',fontsize=5 )
            # Add annotation to bars
                for p in ax.patches:
                    left, bottom, width, height = p.get_bbox().bounds
                    ax.annotate(str(int(width)), xy=(left+width/2, bottom+height/2), 
                                ha='center', va='center', size = 3)
            
                # save image, display it, and delete after usage.
                plt.savefig('x',dpi=200)
                st.image('x.png')
                os.remove('x.png')
                st.plotly_chart(fig)

        else:
            st.markdown("No data found, try other extension, please.")
    elif opt=='Saanich Inlet -Patricia Bay-VENUS':
        filters1 = {
            'locationCode': 'PVIP',
            'deviceCategoryCode': 'HYDROPHONE',
            }
        resultX = onc.getLocations(filters1)
        za = pd.DataFrame(resultX)
        st.markdown(za.description.values[0])


        df_dep = []
        for deployment in onc.getDeployments(filters={'locationCode': 'PVIP', 'deviceCategoryCode': 'HYDROPHONE'}):
            df_dep.append([deployment['locationCode'], deployment['begin'], deployment['end']])

        npl = np.array(df_dep)
        locationC = pd.DataFrame(npl[:,0])
        deplF = pd.DataFrame(npl[:,1])
        deplT = pd.DataFrame(npl[:,2])

        df_dep = pd.concat([locationC,deplF,deplT],axis=1)
        df_dep.columns=["Location Code", "Deployed from", "Deployed to"]


        st.write("There are {} deployments.".format(df_dep.shape[0]))
        df_dep["Deployed from"] = pd.to_datetime(df_dep["Deployed from"]).apply(lambda y: y.date())
        df_dep["Deployed to"] = pd.to_datetime(df_dep["Deployed to"]).apply(lambda y: y.date())
        fe = df_dep.style.hide_index()
        st.write(fe.to_html(), unsafe_allow_html=True)

        start_date = st.sidebar.date_input("Select Start Date")
        end_date = st.sidebar.date_input("Select End Date")

        e = datetime.strptime(str(start_date),"%Y-%m-%d")
        el =datetime.timestamp(e)
        elT = datetime.utcfromtimestamp(el).strftime("%Y-%m-%dT%H:%M:%S")+'.000Z'
        f = datetime.strptime(str(end_date),"%Y-%m-%d")
        fl =datetime.timestamp(f)
        flT = datetime.utcfromtimestamp(fl).strftime("%Y-%m-%dT%H:%M:%S")+'.000Z'


        df_dev = []
        for dev in onc.getDevices({
            'locationCode': 'PVIP',
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
                'locationCode': 'PVIP'
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
        result1 = onc.getListByDevice(filt, allPages=True)
        df = pd.DataFrame(result1)
        if len(df) > 0:
            st.markdown("There are {} files".format(len(df)) + ' from ' + filt['deviceCode'] 
                    + ' between '   + parse(filt['dateFrom']).strftime('%Y %b %d')
            + ' and ' + parse(filt['dateTo']).strftime('%Y %b %d'))
            with st.expander("Data:"):
                st.write(df)
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
                                    .strip('-spect').strip('-spect-small').strip('-LPF-spect').strip('-LPF-spect-thumb')
                                    .strip('-HPF-spect').strip('-HPF-spect-thumb').split('_')[1])   
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
            
                    
            option = st.selectbox(
                'How would you like to visualize the data availability:?',
                ('Line only', 'Bar only', 'Both'))
            
            if option == 'Line only':
                fig = px.scatter(df, x="files", y="UTC time",
                                 title='Data Availabiltiy Plot for {} of the entire deployment (Please enlarge the plot for better visualization)'.format(deviceZ),
                                 template='plotly_white'
                )
                fig.update_layout(yaxis=dict(title=''), xaxis=dict(title='', showgrid=False, gridcolor='grey',
                      tickvals=[],),hovermode="y unified")
                fig.update_traces(connectgaps=False,hovertemplate=None)


                st.plotly_chart(fig)

            elif option=='Bar only':
                df_dt = pd.to_datetime(df_dt)
                dm = df_dt.dt.strftime('%m-%d')
                dav = dm.value_counts().sort_index()


                fig1 = plt.figure(figsize = (4,2))

                ax = plt.axes()
                ax.barh(dav.index,dav,color=sns.color_palette("tab10"),align ='center')
                # Remove axes splines
                for s in ['top', 'bottom', 'left', 'right']:
                    ax.spines[s].set_visible(False)
                    # Remove x, y Ticks
                ax.xaxis.set_ticks_position('none')
                ax.yaxis.set_ticks_position('none')

                plt.yticks(fontsize=5)
                plt.ylabel("day",size = 4)

                ax.legend()        
 
                ax.get_xaxis().set_visible(False)

                ax.set_title('Data Available Per day',
                         loc ='left',fontsize=5 )
            # Add annotation to bars
                for p in ax.patches:
                    left, bottom, width, height = p.get_bbox().bounds
                    ax.annotate(str(int(width)), xy=(left+width/2, bottom+height/2), 
                                ha='center', va='center', size = 3)
            
                # save image, display it, and delete after usage.
                plt.savefig('x',dpi=200)
                st.image('x.png')
                os.remove('x.png')
                        
            else:
                fig = px.scatter(df, x="files", y="UTC time",
                                 title='Data Availabiltiy Plot for {} of the entire deployment (Please enlarge the plot for better visualization)'.format(deviceZ),
                                 template='plotly_white'
                )
                fig.update_layout(yaxis=dict(title=''), xaxis=dict(title='', showgrid=False, gridcolor='grey',
                      tickvals=[],),hovermode="y unified")
                fig.update_traces(connectgaps=False,hovertemplate=None)
                
                df_dt = pd.to_datetime(df_dt)
                dm = df_dt.dt.strftime('%m-%d')
                dav = dm.value_counts().sort_index()


                fig1 = plt.figure(figsize = (4,2))

                ax = plt.axes()
                ax.barh(dav.index,dav,color=sns.color_palette("tab10"),align ='center')
                # Remove axes splines
                for s in ['top', 'bottom', 'left', 'right']:
                    ax.spines[s].set_visible(False)
                    # Remove x, y Ticks
                ax.xaxis.set_ticks_position('none')
                ax.yaxis.set_ticks_position('none')

                plt.yticks(fontsize=5)
                plt.ylabel("day",size = 4)

                ax.legend()        
 
                ax.get_xaxis().set_visible(False)

                ax.set_title('Data Available Per day',
                         loc ='left',fontsize=5 )
            # Add annotation to bars
                for p in ax.patches:
                    left, bottom, width, height = p.get_bbox().bounds
                    ax.annotate(str(int(width)), xy=(left+width/2, bottom+height/2), 
                                ha='center', va='center', size = 3)
            
                # save image, display it, and delete after usage.
                plt.savefig('x',dpi=200)
                st.image('x.png')
                os.remove('x.png')
                st.plotly_chart(fig)

        else:
            st.markdown("No data found, try other extension, please.")
    elif opt=='Vancouver Island - China Creek':
        filters1 = {
            'locationCode': 'JAKOC',
            'deviceCategoryCode': 'HYDROPHONE',
            }
        resultX = onc.getLocations(filters1)
        za = pd.DataFrame(resultX)
        st.markdown(za.description.values[0])


        df_dep = []
        for deployment in onc.getDeployments(filters={'locationCode': 'JAKOC', 'deviceCategoryCode': 'HYDROPHONE'}):
            df_dep.append([deployment['locationCode'], deployment['begin'], deployment['end']])

        npl = np.array(df_dep)
        locationC = pd.DataFrame(npl[:,0])
        deplF = pd.DataFrame(npl[:,1])
        deplT = pd.DataFrame(npl[:,2])

        df_dep = pd.concat([locationC,deplF,deplT],axis=1)
        df_dep.columns=["Location Code", "Deployed from", "Deployed to"]


        st.write("There are {} deployments.".format(df_dep.shape[0]))
        df_dep["Deployed from"] = pd.to_datetime(df_dep["Deployed from"]).apply(lambda y: y.date())
        df_dep["Deployed to"] = pd.to_datetime(df_dep["Deployed to"]).apply(lambda y: y.date())
        fe = df_dep.style.hide_index()
        st.write(fe.to_html(), unsafe_allow_html=True)

        start_date = st.sidebar.date_input("Select Start Date")
        end_date = st.sidebar.date_input("Select End Date")

        e = datetime.strptime(str(start_date),"%Y-%m-%d")
        el =datetime.timestamp(e)
        elT = datetime.utcfromtimestamp(el).strftime("%Y-%m-%dT%H:%M:%S")+'.000Z'
        f = datetime.strptime(str(end_date),"%Y-%m-%d")
        fl =datetime.timestamp(f)
        flT = datetime.utcfromtimestamp(fl).strftime("%Y-%m-%dT%H:%M:%S")+'.000Z'


        df_dev = []
        for dev in onc.getDevices({
            'locationCode': 'JAKOC',
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
                'locationCode': 'JAKOC'
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
        result1 = onc.getListByDevice(filt, allPages=True)
        df = pd.DataFrame(result1)
        if len(df) > 0:
            st.markdown("There are {} files".format(len(df)) + ' from ' + filt['deviceCode'] 
                    + ' between '   + parse(filt['dateFrom']).strftime('%Y %b %d')
            + ' and ' + parse(filt['dateTo']).strftime('%Y %b %d'))
            with st.expander("Data:"):
                st.write(df)
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
                                    .strip('-spect').strip('-spect-small').strip('-LPF-spect').strip('-LPF-spect-thumb')
                                    .strip('-HPF-spect').strip('-HPF-spect-thumb').split('_')[1])   
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
            
                    
            option = st.selectbox(
                'How would you like to visualize the data availability:?',
                ('Line only', 'Bar only', 'Both'))
            
            if option == 'Line only':
                fig = px.scatter(df, x="files", y="UTC time",
                                 title='Data Availabiltiy Plot for {} of the entire deployment (Please enlarge the plot for better visualization)'.format(deviceZ),
                                 template='plotly_white'
                )
                fig.update_layout(yaxis=dict(title=''), xaxis=dict(title='', showgrid=False, gridcolor='grey',
                      tickvals=[],),hovermode="y unified")
                fig.update_traces(connectgaps=False,hovertemplate=None)


                st.plotly_chart(fig)

            elif option=='Bar only':
                df_dt = pd.to_datetime(df_dt)
                dm = df_dt.dt.strftime('%m-%d')
                dav = dm.value_counts().sort_index()


                fig1 = plt.figure(figsize = (4,2))

                ax = plt.axes()
                ax.barh(dav.index,dav,color=sns.color_palette("tab10"),align ='center')
                # Remove axes splines
                for s in ['top', 'bottom', 'left', 'right']:
                    ax.spines[s].set_visible(False)
                    # Remove x, y Ticks
                ax.xaxis.set_ticks_position('none')
                ax.yaxis.set_ticks_position('none')

                plt.yticks(fontsize=5)
                plt.ylabel("day",size = 4)

                ax.legend()        
 
                ax.get_xaxis().set_visible(False)

                ax.set_title('Data Available Per day',
                         loc ='left',fontsize=5 )
            # Add annotation to bars
                for p in ax.patches:
                    left, bottom, width, height = p.get_bbox().bounds
                    ax.annotate(str(int(width)), xy=(left+width/2, bottom+height/2), 
                                ha='center', va='center', size = 3)
            
                # save image, display it, and delete after usage.
                plt.savefig('x',dpi=200)
                st.image('x.png')
                os.remove('x.png')
                        
            else:
                fig = px.scatter(df, x="files", y="UTC time",
                                 title='Data Availabiltiy Plot for {} of the entire deployment (Please enlarge the plot for better visualization)'.format(deviceZ),
                                 template='plotly_white'
                )
                fig.update_layout(yaxis=dict(title=''), xaxis=dict(title='', showgrid=False, gridcolor='grey',
                      tickvals=[],),hovermode="y unified")
                fig.update_traces(connectgaps=False,hovertemplate=None)
                
                df_dt = pd.to_datetime(df_dt)
                dm = df_dt.dt.strftime('%m-%d')
                dav = dm.value_counts().sort_index()


                fig1 = plt.figure(figsize = (4,2))

                ax = plt.axes()
                ax.barh(dav.index,dav,color=sns.color_palette("tab10"),align ='center')
                # Remove axes splines
                for s in ['top', 'bottom', 'left', 'right']:
                    ax.spines[s].set_visible(False)
                    # Remove x, y Ticks
                ax.xaxis.set_ticks_position('none')
                ax.yaxis.set_ticks_position('none')

                plt.yticks(fontsize=5)
                plt.ylabel("day",size = 4)

                ax.legend()        
 
                ax.get_xaxis().set_visible(False)

                ax.set_title('Data Available Per day',
                         loc ='left',fontsize=5 )
            # Add annotation to bars
                for p in ax.patches:
                    left, bottom, width, height = p.get_bbox().bounds
                    ax.annotate(str(int(width)), xy=(left+width/2, bottom+height/2), 
                                ha='center', va='center', size = 3)
            
                # save image, display it, and delete after usage.
                plt.savefig('x',dpi=200)
                st.image('x.png')
                os.remove('x.png')
                st.plotly_chart(fig)

        else:
            st.markdown("No data found, try other extension, please.")

    elif opt=='Conception Bay - Holyrood Bay':
        filters1 = {
            'locationCode': 'HRBIP',
            'deviceCategoryCode': 'HYDROPHONE',
            }
        resultX = onc.getLocations(filters1)
        za = pd.DataFrame(resultX)
        st.markdown(za.description.values[0])


        df_dep = []
        for deployment in onc.getDeployments(filters={'locationCode': 'HRBIP', 'deviceCategoryCode': 'HYDROPHONE'}):
            df_dep.append([deployment['locationCode'], deployment['begin'], deployment['end']])

        npl = np.array(df_dep)
        locationC = pd.DataFrame(npl[:,0])
        deplF = pd.DataFrame(npl[:,1])
        deplT = pd.DataFrame(npl[:,2])

        df_dep = pd.concat([locationC,deplF,deplT],axis=1)
        df_dep.columns=["Location Code", "Deployed from", "Deployed to"]


        st.write("There are {} deployments.".format(df_dep.shape[0]))
        df_dep["Deployed from"] = pd.to_datetime(df_dep["Deployed from"]).apply(lambda y: y.date())
        df_dep["Deployed to"] = pd.to_datetime(df_dep["Deployed to"]).apply(lambda y: y.date())
        fe = df_dep.style.hide_index()
        st.write(fe.to_html(), unsafe_allow_html=True)

        start_date = st.sidebar.date_input("Select Start Date")
        end_date = st.sidebar.date_input("Select End Date")

        e = datetime.strptime(str(start_date),"%Y-%m-%d")
        el =datetime.timestamp(e)
        elT = datetime.utcfromtimestamp(el).strftime("%Y-%m-%dT%H:%M:%S")+'.000Z'
        f = datetime.strptime(str(end_date),"%Y-%m-%d")
        fl =datetime.timestamp(f)
        flT = datetime.utcfromtimestamp(fl).strftime("%Y-%m-%dT%H:%M:%S")+'.000Z'


        df_dev = []
        for dev in onc.getDevices({
            'locationCode': 'HRBIP',
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
                'locationCode': 'HRBIP'
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
        result1 = onc.getListByDevice(filt, allPages=True)
        df = pd.DataFrame(result1)
        if len(df) > 0:
            st.markdown("There are {} files".format(len(df)) + ' from ' + filt['deviceCode'] 
                    + ' between '   + parse(filt['dateFrom']).strftime('%Y %b %d')
            + ' and ' + parse(filt['dateTo']).strftime('%Y %b %d'))
            with st.expander("Data:"):
                st.write(df)
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
                                    .strip('-spect').strip('-spect-small').strip('-LPF-spect').strip('-LPF-spect-thumb')
                                    .strip('-HPF-spect').strip('-HPF-spect-thumb').split('_')[1])   
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
            
                    
            option = st.selectbox(
                'How would you like to visualize the data availability:?',
                ('Line only', 'Bar only', 'Both'))
            
            if option == 'Line only':
                fig = px.scatter(df, x="files", y="UTC time",
                                 title='Data Availabiltiy Plot for {} of the entire deployment (Please enlarge the plot for better visualization)'.format(deviceZ),
                                 template='plotly_white'
                )
                fig.update_layout(yaxis=dict(title=''), xaxis=dict(title='', showgrid=False, gridcolor='grey',
                      tickvals=[],),hovermode="y unified")
                fig.update_traces(connectgaps=False,hovertemplate=None)


                st.plotly_chart(fig)

            elif option=='Bar only':
                df_dt = pd.to_datetime(df_dt)
                dm = df_dt.dt.strftime('%m-%d')
                dav = dm.value_counts().sort_index()


                fig1 = plt.figure(figsize = (4,2))

                ax = plt.axes()
                ax.barh(dav.index,dav,color=sns.color_palette("tab10"),align ='center')
                # Remove axes splines
                for s in ['top', 'bottom', 'left', 'right']:
                    ax.spines[s].set_visible(False)
                    # Remove x, y Ticks
                ax.xaxis.set_ticks_position('none')
                ax.yaxis.set_ticks_position('none')

                plt.yticks(fontsize=5)
                plt.ylabel("day",size = 4)

                ax.legend()        
 
                ax.get_xaxis().set_visible(False)

                ax.set_title('Data Available Per day',
                         loc ='left',fontsize=5 )
            # Add annotation to bars
                for p in ax.patches:
                    left, bottom, width, height = p.get_bbox().bounds
                    ax.annotate(str(int(width)), xy=(left+width/2, bottom+height/2), 
                                ha='center', va='center', size = 3)
            
                # save image, display it, and delete after usage.
                plt.savefig('x',dpi=200)
                st.image('x.png')
                os.remove('x.png')
                        
            else:
                fig = px.scatter(df, x="files", y="UTC time",
                                 title='Data Availabiltiy Plot for {} of the entire deployment (Please enlarge the plot for better visualization)'.format(deviceZ),
                                 template='plotly_white'
                )
                fig.update_layout(yaxis=dict(title=''), xaxis=dict(title='', showgrid=False, gridcolor='grey',
                      tickvals=[],),hovermode="y unified")
                fig.update_traces(connectgaps=False,hovertemplate=None)
                
                df_dt = pd.to_datetime(df_dt)
                dm = df_dt.dt.strftime('%m-%d')
                dav = dm.value_counts().sort_index()


                fig1 = plt.figure(figsize = (4,2))

                ax = plt.axes()
                ax.barh(dav.index,dav,color=sns.color_palette("tab10"),align ='center')
                # Remove axes splines
                for s in ['top', 'bottom', 'left', 'right']:
                    ax.spines[s].set_visible(False)
                    # Remove x, y Ticks
                ax.xaxis.set_ticks_position('none')
                ax.yaxis.set_ticks_position('none')

                plt.yticks(fontsize=5)
                plt.ylabel("day",size = 4)

                ax.legend()        
 
                ax.get_xaxis().set_visible(False)

                ax.set_title('Data Available Per day',
                         loc ='left',fontsize=5 )
            # Add annotation to bars
                for p in ax.patches:
                    left, bottom, width, height = p.get_bbox().bounds
                    ax.annotate(str(int(width)), xy=(left+width/2, bottom+height/2), 
                                ha='center', va='center', size = 3)
            
                # save image, display it, and delete after usage.
                plt.savefig('x',dpi=200)
                st.image('x.png')
                os.remove('x.png')
                st.plotly_chart(fig)

        else:
            st.markdown("No data found, try other extension, please.")
    elif opt=='Barkley Sound - Folger Deep':
        filters1 = {
            'locationCode': 'FGPD',
            'deviceCategoryCode': 'HYDROPHONE',
            }
        resultX = onc.getLocations(filters1)
        za = pd.DataFrame(resultX)
        st.markdown(za.description.values[0])


        df_dep = []
        for deployment in onc.getDeployments(filters={'locationCode': 'FGPD', 'deviceCategoryCode': 'HYDROPHONE'}):
            df_dep.append([deployment['locationCode'], deployment['begin'], deployment['end']])

        npl = np.array(df_dep)
        locationC = pd.DataFrame(npl[:,0])
        deplF = pd.DataFrame(npl[:,1])
        deplT = pd.DataFrame(npl[:,2])

        df_dep = pd.concat([locationC,deplF,deplT],axis=1)
        df_dep.columns=["Location Code", "Deployed from", "Deployed to"]


        st.write("There are {} deployments.".format(df_dep.shape[0]))
        df_dep["Deployed from"] = pd.to_datetime(df_dep["Deployed from"]).apply(lambda y: y.date())
        df_dep["Deployed to"] = pd.to_datetime(df_dep["Deployed to"]).apply(lambda y: y.date())
        fe = df_dep.style.hide_index()
        st.write(fe.to_html(), unsafe_allow_html=True)

        start_date = st.sidebar.date_input("Select Start Date")
        end_date = st.sidebar.date_input("Select End Date")

        e = datetime.strptime(str(start_date),"%Y-%m-%d")
        el =datetime.timestamp(e)
        elT = datetime.utcfromtimestamp(el).strftime("%Y-%m-%dT%H:%M:%S")+'.000Z'
        f = datetime.strptime(str(end_date),"%Y-%m-%d")
        fl =datetime.timestamp(f)
        flT = datetime.utcfromtimestamp(fl).strftime("%Y-%m-%dT%H:%M:%S")+'.000Z'


        df_dev = []
        for dev in onc.getDevices({
            'locationCode': 'FGPD',
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
                'locationCode': 'FGPD'
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
        result1 = onc.getListByDevice(filt, allPages=True)
        df = pd.DataFrame(result1)
        if len(df) > 0:
            st.markdown("There are {} files".format(len(df)) + ' from ' + filt['deviceCode'] 
                    + ' between '   + parse(filt['dateFrom']).strftime('%Y %b %d')
            + ' and ' + parse(filt['dateTo']).strftime('%Y %b %d'))
            with st.expander("Data:"):
                st.write(df)
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
                                    .strip('-spect').strip('-spect-small').strip('-LPF-spect').strip('-LPF-spect-thumb')
                                    .strip('-HPF-spect').strip('-HPF-spect-thumb').split('_')[1])   
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
            
                    
            option = st.selectbox(
                'How would you like to visualize the data availability:?',
                ('Line only', 'Bar only', 'Both'))
            
            if option == 'Line only':
                fig = px.scatter(df, x="files", y="UTC time",
                                 title='Data Availabiltiy Plot for {} of the entire deployment (Please enlarge the plot for better visualization)'.format(deviceZ),
                                 template='plotly_white'
                )
                fig.update_layout(yaxis=dict(title=''), xaxis=dict(title='', showgrid=False, gridcolor='grey',
                      tickvals=[],),hovermode="y unified")
                fig.update_traces(connectgaps=False,hovertemplate=None)


                st.plotly_chart(fig)

            elif option=='Bar only':
                df_dt = pd.to_datetime(df_dt)
                dm = df_dt.dt.strftime('%m-%d')
                dav = dm.value_counts().sort_index()


                fig1 = plt.figure(figsize = (4,2))

                ax = plt.axes()
                ax.barh(dav.index,dav,color=sns.color_palette("tab10"),align ='center')
                # Remove axes splines
                for s in ['top', 'bottom', 'left', 'right']:
                    ax.spines[s].set_visible(False)
                    # Remove x, y Ticks
                ax.xaxis.set_ticks_position('none')
                ax.yaxis.set_ticks_position('none')

                plt.yticks(fontsize=5)
                plt.ylabel("day",size = 4)

                ax.legend()        
 
                ax.get_xaxis().set_visible(False)

                ax.set_title('Data Available Per day',
                         loc ='left',fontsize=5 )
            # Add annotation to bars
                for p in ax.patches:
                    left, bottom, width, height = p.get_bbox().bounds
                    ax.annotate(str(int(width)), xy=(left+width/2, bottom+height/2), 
                                ha='center', va='center', size = 3)
            
                # save image, display it, and delete after usage.
                plt.savefig('x',dpi=200)
                st.image('x.png')
                os.remove('x.png')
                        
            else:
                fig = px.scatter(df, x="files", y="UTC time",
                                 title='Data Availabiltiy Plot for {} of the entire deployment (Please enlarge the plot for better visualization)'.format(deviceZ),
                                 template='plotly_white'
                )
                fig.update_layout(yaxis=dict(title=''), xaxis=dict(title='', showgrid=False, gridcolor='grey',
                      tickvals=[],),hovermode="y unified")
                fig.update_traces(connectgaps=False,hovertemplate=None)
                
                df_dt = pd.to_datetime(df_dt)
                dm = df_dt.dt.strftime('%m-%d')
                dav = dm.value_counts().sort_index()


                fig1 = plt.figure(figsize = (4,2))

                ax = plt.axes()
                ax.barh(dav.index,dav,color=sns.color_palette("tab10"),align ='center')
                # Remove axes splines
                for s in ['top', 'bottom', 'left', 'right']:
                    ax.spines[s].set_visible(False)
                    # Remove x, y Ticks
                ax.xaxis.set_ticks_position('none')
                ax.yaxis.set_ticks_position('none')

                plt.yticks(fontsize=5)
                plt.ylabel("day",size = 4)

                ax.legend()        
 
                ax.get_xaxis().set_visible(False)

                ax.set_title('Data Available Per day',
                         loc ='left',fontsize=5 )
            # Add annotation to bars
                for p in ax.patches:
                    left, bottom, width, height = p.get_bbox().bounds
                    ax.annotate(str(int(width)), xy=(left+width/2, bottom+height/2), 
                                ha='center', va='center', size = 3)
            
                # save image, display it, and delete after usage.
                plt.savefig('x',dpi=200)
                st.image('x.png')
                os.remove('x.png')
                st.plotly_chart(fig)

        else:
            st.markdown("No data found, try other extension, please.")
    elif opt=='Endeavour - Main Endeavour Field':
        filters1 = {
            'locationCode': 'KEMF',
            'deviceCategoryCode': 'HYDROPHONE',
            }
        resultX = onc.getLocations(filters1)
        za = pd.DataFrame(resultX)
        st.markdown(za.description.values[0])


        df_dep = []
        for deployment in onc.getDeployments(filters={'locationCode': 'KEMF', 'deviceCategoryCode': 'HYDROPHONE'}):
            df_dep.append([deployment['locationCode'], deployment['begin'], deployment['end']])

        npl = np.array(df_dep)
        locationC = pd.DataFrame(npl[:,0])
        deplF = pd.DataFrame(npl[:,1])
        deplT = pd.DataFrame(npl[:,2])

        df_dep = pd.concat([locationC,deplF,deplT],axis=1)
        df_dep.columns=["Location Code", "Deployed from", "Deployed to"]


        st.write("There are {} deployments.".format(df_dep.shape[0]))
        df_dep["Deployed from"] = pd.to_datetime(df_dep["Deployed from"]).apply(lambda y: y.date())
        df_dep["Deployed to"] = pd.to_datetime(df_dep["Deployed to"]).apply(lambda y: y.date())
        fe = df_dep.style.hide_index()
        st.write(fe.to_html(), unsafe_allow_html=True)

        start_date = st.sidebar.date_input("Select Start Date")
        end_date = st.sidebar.date_input("Select End Date")

        e = datetime.strptime(str(start_date),"%Y-%m-%d")
        el =datetime.timestamp(e)
        elT = datetime.utcfromtimestamp(el).strftime("%Y-%m-%dT%H:%M:%S")+'.000Z'
        f = datetime.strptime(str(end_date),"%Y-%m-%d")
        fl =datetime.timestamp(f)
        flT = datetime.utcfromtimestamp(fl).strftime("%Y-%m-%dT%H:%M:%S")+'.000Z'


        df_dev = []
        for dev in onc.getDevices({
            'locationCode': 'KEMF',
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
                'locationCode': 'KEMF'
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
        result1 = onc.getListByDevice(filt, allPages=True)
        df = pd.DataFrame(result1)
        if len(df) > 0:
            st.markdown("There are {} files".format(len(df)) + ' from ' + filt['deviceCode'] 
                    + ' between '   + parse(filt['dateFrom']).strftime('%Y %b %d')
            + ' and ' + parse(filt['dateTo']).strftime('%Y %b %d'))
            with st.expander("Data:"):
                st.write(df)
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
                                    .strip('-spect').strip('-spect-small').strip('-LPF-spect').strip('-LPF-spect-thumb')
                                    .strip('-HPF-spect').strip('-HPF-spect-thumb').split('_')[1])   
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
            
                    
            option = st.selectbox(
                'How would you like to visualize the data availability:?',
                ('Line only', 'Bar only', 'Both'))
            
            if option == 'Line only':
                fig = px.scatter(df, x="files", y="UTC time",
                                 title='Data Availabiltiy Plot for {} of the entire deployment (Please enlarge the plot for better visualization)'.format(deviceZ),
                                 template='plotly_white'
                )
                fig.update_layout(yaxis=dict(title=''), xaxis=dict(title='', showgrid=False, gridcolor='grey',
                      tickvals=[],),hovermode="y unified")
                fig.update_traces(connectgaps=False,hovertemplate=None)


                st.plotly_chart(fig)

            elif option=='Bar only':
                df_dt = pd.to_datetime(df_dt)
                dm = df_dt.dt.strftime('%m-%d')
                dav = dm.value_counts().sort_index()


                fig1 = plt.figure(figsize = (4,2))

                ax = plt.axes()
                ax.barh(dav.index,dav,color=sns.color_palette("tab10"),align ='center')
                # Remove axes splines
                for s in ['top', 'bottom', 'left', 'right']:
                    ax.spines[s].set_visible(False)
                    # Remove x, y Ticks
                ax.xaxis.set_ticks_position('none')
                ax.yaxis.set_ticks_position('none')

                plt.yticks(fontsize=5)
                plt.ylabel("day",size = 4)

                ax.legend()        
 
                ax.get_xaxis().set_visible(False)

                ax.set_title('Data Available Per day',
                         loc ='left',fontsize=5 )
            # Add annotation to bars
                for p in ax.patches:
                    left, bottom, width, height = p.get_bbox().bounds
                    ax.annotate(str(int(width)), xy=(left+width/2, bottom+height/2), 
                                ha='center', va='center', size = 3)
            
                # save image, display it, and delete after usage.
                plt.savefig('x',dpi=200)
                st.image('x.png')
                os.remove('x.png')
                        
            else:
                fig = px.scatter(df, x="files", y="UTC time",
                                 title='Data Availabiltiy Plot for {} of the entire deployment (Please enlarge the plot for better visualization)'.format(deviceZ),
                                 template='plotly_white'
                )
                fig.update_layout(yaxis=dict(title=''), xaxis=dict(title='', showgrid=False, gridcolor='grey',
                      tickvals=[],),hovermode="y unified")
                fig.update_traces(connectgaps=False,hovertemplate=None)
                
                df_dt = pd.to_datetime(df_dt)
                dm = df_dt.dt.strftime('%m-%d')
                dav = dm.value_counts().sort_index()


                fig1 = plt.figure(figsize = (4,2))

                ax = plt.axes()
                ax.barh(dav.index,dav,color=sns.color_palette("tab10"),align ='center')
                # Remove axes splines
                for s in ['top', 'bottom', 'left', 'right']:
                    ax.spines[s].set_visible(False)
                    # Remove x, y Ticks
                ax.xaxis.set_ticks_position('none')
                ax.yaxis.set_ticks_position('none')

                plt.yticks(fontsize=5)
                plt.ylabel("day",size = 4)

                ax.legend()        
 
                ax.get_xaxis().set_visible(False)

                ax.set_title('Data Available Per day',
                         loc ='left',fontsize=5 )
            # Add annotation to bars
                for p in ax.patches:
                    left, bottom, width, height = p.get_bbox().bounds
                    ax.annotate(str(int(width)), xy=(left+width/2, bottom+height/2), 
                                ha='center', va='center', size = 3)
            
                # save image, display it, and delete after usage.
                plt.savefig('x',dpi=200)
                st.image('x.png')
                os.remove('x.png')
                st.plotly_chart(fig)

        else:
            st.markdown("No data found, try other extension, please.")
    elif opt=='Clayoquot Slope - Hydrophone A':
        filters1 = {
            'locationCode': 'CQSH.H1',
            'deviceCategoryCode': 'HYDROPHONE',
            }
        resultX = onc.getLocations(filters1)
        za = pd.DataFrame(resultX)
        st.markdown(za.description.values[0])


        df_dep = []
        for deployment in onc.getDeployments(filters={'locationCode': 'CQSH.H1', 'deviceCategoryCode': 'HYDROPHONE'}):
            df_dep.append([deployment['locationCode'], deployment['begin'], deployment['end']])

        npl = np.array(df_dep)
        locationC = pd.DataFrame(npl[:,0])
        deplF = pd.DataFrame(npl[:,1])
        deplT = pd.DataFrame(npl[:,2])

        df_dep = pd.concat([locationC,deplF,deplT],axis=1)
        df_dep.columns=["Location Code", "Deployed from", "Deployed to"]


        st.write("There are {} deployments.".format(df_dep.shape[0]))
        df_dep["Deployed from"] = pd.to_datetime(df_dep["Deployed from"]).apply(lambda y: y.date())
        df_dep["Deployed to"] = pd.to_datetime(df_dep["Deployed to"]).apply(lambda y: y.date())
        fe = df_dep.style.hide_index()
        st.write(fe.to_html(), unsafe_allow_html=True)

        start_date = st.sidebar.date_input("Select Start Date")
        end_date = st.sidebar.date_input("Select End Date")

        e = datetime.strptime(str(start_date),"%Y-%m-%d")
        el =datetime.timestamp(e)
        elT = datetime.utcfromtimestamp(el).strftime("%Y-%m-%dT%H:%M:%S")+'.000Z'
        f = datetime.strptime(str(end_date),"%Y-%m-%d")
        fl =datetime.timestamp(f)
        flT = datetime.utcfromtimestamp(fl).strftime("%Y-%m-%dT%H:%M:%S")+'.000Z'


        df_dev = []
        for dev in onc.getDevices({
            'locationCode': 'CQSH.H1',
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
                'locationCode': 'CQSH.H1'
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
        result1 = onc.getListByDevice(filt, allPages=True)
        df = pd.DataFrame(result1)
        if len(df) > 0:
            st.markdown("There are {} files".format(len(df)) + ' from ' + filt['deviceCode'] 
                    + ' between '   + parse(filt['dateFrom']).strftime('%Y %b %d')
            + ' and ' + parse(filt['dateTo']).strftime('%Y %b %d'))
            with st.expander("Data:"):
                st.write(df)
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
                                    .strip('-spect').strip('-spect-small').strip('-LPF-spect').strip('-LPF-spect-thumb')
                                    .strip('-HPF-spect').strip('-HPF-spect-thumb').split('_')[1])   
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
            
                    
            option = st.selectbox(
                'How would you like to visualize the data availability:?',
                ('Line only', 'Bar only', 'Both'))
            
            if option == 'Line only':
                fig = px.scatter(df, x="files", y="UTC time",
                                 title='Data Availabiltiy Plot for {} of the entire deployment (Please enlarge the plot for better visualization)'.format(deviceZ),
                                 template='plotly_white'
                )
                fig.update_layout(yaxis=dict(title=''), xaxis=dict(title='', showgrid=False, gridcolor='grey',
                      tickvals=[],),hovermode="y unified")
                fig.update_traces(connectgaps=False,hovertemplate=None)


                st.plotly_chart(fig)

            elif option=='Bar only':
                df_dt = pd.to_datetime(df_dt)
                dm = df_dt.dt.strftime('%m-%d')
                dav = dm.value_counts().sort_index()


                fig1 = plt.figure(figsize = (4,2))

                ax = plt.axes()
                ax.barh(dav.index,dav,color=sns.color_palette("tab10"),align ='center')
                # Remove axes splines
                for s in ['top', 'bottom', 'left', 'right']:
                    ax.spines[s].set_visible(False)
                    # Remove x, y Ticks
                ax.xaxis.set_ticks_position('none')
                ax.yaxis.set_ticks_position('none')

                plt.yticks(fontsize=5)
                plt.ylabel("day",size = 4)

                ax.legend()        
 
                ax.get_xaxis().set_visible(False)

                ax.set_title('Data Available Per day',
                         loc ='left',fontsize=5 )
            # Add annotation to bars
                for p in ax.patches:
                    left, bottom, width, height = p.get_bbox().bounds
                    ax.annotate(str(int(width)), xy=(left+width/2, bottom+height/2), 
                                ha='center', va='center', size = 3)
            
                # save image, display it, and delete after usage.
                plt.savefig('x',dpi=200)
                st.image('x.png')
                os.remove('x.png')
                        
            else:
                fig = px.scatter(df, x="files", y="UTC time",
                                 title='Data Availabiltiy Plot for {} of the entire deployment (Please enlarge the plot for better visualization)'.format(deviceZ),
                                 template='plotly_white'
                )
                fig.update_layout(yaxis=dict(title=''), xaxis=dict(title='', showgrid=False, gridcolor='grey',
                      tickvals=[],),hovermode="y unified")
                fig.update_traces(connectgaps=False,hovertemplate=None)
                
                df_dt = pd.to_datetime(df_dt)
                dm = df_dt.dt.strftime('%m-%d')
                dav = dm.value_counts().sort_index()


                fig1 = plt.figure(figsize = (4,2))

                ax = plt.axes()
                ax.barh(dav.index,dav,color=sns.color_palette("tab10"),align ='center')
                # Remove axes splines
                for s in ['top', 'bottom', 'left', 'right']:
                    ax.spines[s].set_visible(False)
                    # Remove x, y Ticks
                ax.xaxis.set_ticks_position('none')
                ax.yaxis.set_ticks_position('none')

                plt.yticks(fontsize=5)
                plt.ylabel("day",size = 4)

                ax.legend()        
 
                ax.get_xaxis().set_visible(False)

                ax.set_title('Data Available Per day',
                         loc ='left',fontsize=5 )
            # Add annotation to bars
                for p in ax.patches:
                    left, bottom, width, height = p.get_bbox().bounds
                    ax.annotate(str(int(width)), xy=(left+width/2, bottom+height/2), 
                                ha='center', va='center', size = 3)
            
                # save image, display it, and delete after usage.
                plt.savefig('x',dpi=200)
                st.image('x.png')
                os.remove('x.png')
                st.plotly_chart(fig)

        else:
            st.markdown("No data found, try other extension, please.")
    elif opt=='Clayoquot Slope - Hydrophone B':
        filters1 = {
            'locationCode': 'CQSH.H2',
            'deviceCategoryCode': 'HYDROPHONE',
            }
        resultX = onc.getLocations(filters1)
        za = pd.DataFrame(resultX)
        st.markdown(za.description.values[0])


        df_dep = []
        for deployment in onc.getDeployments(filters={'locationCode': 'CQSH.H2', 'deviceCategoryCode': 'HYDROPHONE'}):
            df_dep.append([deployment['locationCode'], deployment['begin'], deployment['end']])

        npl = np.array(df_dep)
        locationC = pd.DataFrame(npl[:,0])
        deplF = pd.DataFrame(npl[:,1])
        deplT = pd.DataFrame(npl[:,2])

        df_dep = pd.concat([locationC,deplF,deplT],axis=1)
        df_dep.columns=["Location Code", "Deployed from", "Deployed to"]


        st.write("There are {} deployments.".format(df_dep.shape[0]))
        df_dep["Deployed from"] = pd.to_datetime(df_dep["Deployed from"]).apply(lambda y: y.date())
        df_dep["Deployed to"] = pd.to_datetime(df_dep["Deployed to"]).apply(lambda y: y.date())
        fe = df_dep.style.hide_index()
        st.write(fe.to_html(), unsafe_allow_html=True)

        start_date = st.sidebar.date_input("Select Start Date")
        end_date = st.sidebar.date_input("Select End Date")

        e = datetime.strptime(str(start_date),"%Y-%m-%d")
        el =datetime.timestamp(e)
        elT = datetime.utcfromtimestamp(el).strftime("%Y-%m-%dT%H:%M:%S")+'.000Z'
        f = datetime.strptime(str(end_date),"%Y-%m-%d")
        fl =datetime.timestamp(f)
        flT = datetime.utcfromtimestamp(fl).strftime("%Y-%m-%dT%H:%M:%S")+'.000Z'


        df_dev = []
        for dev in onc.getDevices({
            'locationCode': 'CQSH.H2',
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
                'locationCode': 'CQSH.H2'
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
        result1 = onc.getListByDevice(filt, allPages=True)
        df = pd.DataFrame(result1)
        if len(df) > 0:
            st.markdown("There are {} files".format(len(df)) + ' from ' + filt['deviceCode'] 
                    + ' between '   + parse(filt['dateFrom']).strftime('%Y %b %d')
            + ' and ' + parse(filt['dateTo']).strftime('%Y %b %d'))
            with st.expander("Data:"):
                st.write(df)
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
                                    .strip('-spect').strip('-spect-small').strip('-LPF-spect').strip('-LPF-spect-thumb')
                                    .strip('-HPF-spect').strip('-HPF-spect-thumb').split('_')[1])   
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
            
                    
            option = st.selectbox(
                'How would you like to visualize the data availability:?',
                ('Line only', 'Bar only', 'Both'))
            
            if option == 'Line only':
                fig = px.scatter(df, x="files", y="UTC time",
                                 title='Data Availabiltiy Plot for {} of the entire deployment (Please enlarge the plot for better visualization)'.format(deviceZ),
                                 template='plotly_white'
                )
                fig.update_layout(yaxis=dict(title=''), xaxis=dict(title='', showgrid=False, gridcolor='grey',
                      tickvals=[],),hovermode="y unified")
                fig.update_traces(connectgaps=False,hovertemplate=None)


                st.plotly_chart(fig)

            elif option=='Bar only':
                df_dt = pd.to_datetime(df_dt)
                dm = df_dt.dt.strftime('%m-%d')
                dav = dm.value_counts().sort_index()


                fig1 = plt.figure(figsize = (4,2))

                ax = plt.axes()
                ax.barh(dav.index,dav,color=sns.color_palette("tab10"),align ='center')
                # Remove axes splines
                for s in ['top', 'bottom', 'left', 'right']:
                    ax.spines[s].set_visible(False)
                    # Remove x, y Ticks
                ax.xaxis.set_ticks_position('none')
                ax.yaxis.set_ticks_position('none')

                plt.yticks(fontsize=5)
                plt.ylabel("day",size = 4)

                ax.legend()        
 
                ax.get_xaxis().set_visible(False)

                ax.set_title('Data Available Per day',
                         loc ='left',fontsize=5 )
            # Add annotation to bars
                for p in ax.patches:
                    left, bottom, width, height = p.get_bbox().bounds
                    ax.annotate(str(int(width)), xy=(left+width/2, bottom+height/2), 
                                ha='center', va='center', size = 3)
            
                # save image, display it, and delete after usage.
                plt.savefig('x',dpi=200)
                st.image('x.png')
                os.remove('x.png')
                        
            else:
                fig = px.scatter(df, x="files", y="UTC time",
                                 title='Data Availabiltiy Plot for {} of the entire deployment (Please enlarge the plot for better visualization)'.format(deviceZ),
                                 template='plotly_white'
                )
                fig.update_layout(yaxis=dict(title=''), xaxis=dict(title='', showgrid=False, gridcolor='grey',
                      tickvals=[],),hovermode="y unified")
                fig.update_traces(connectgaps=False,hovertemplate=None)
                
                df_dt = pd.to_datetime(df_dt)
                dm = df_dt.dt.strftime('%m-%d')
                dav = dm.value_counts().sort_index()


                fig1 = plt.figure(figsize = (4,2))

                ax = plt.axes()
                ax.barh(dav.index,dav,color=sns.color_palette("tab10"),align ='center')
                # Remove axes splines
                for s in ['top', 'bottom', 'left', 'right']:
                    ax.spines[s].set_visible(False)
                    # Remove x, y Ticks
                ax.xaxis.set_ticks_position('none')
                ax.yaxis.set_ticks_position('none')

                plt.yticks(fontsize=5)
                plt.ylabel("day",size = 4)

                ax.legend()        
 
                ax.get_xaxis().set_visible(False)

                ax.set_title('Data Available Per day',
                         loc ='left',fontsize=5 )
            # Add annotation to bars
                for p in ax.patches:
                    left, bottom, width, height = p.get_bbox().bounds
                    ax.annotate(str(int(width)), xy=(left+width/2, bottom+height/2), 
                                ha='center', va='center', size = 3)
            
                # save image, display it, and delete after usage.
                plt.savefig('x',dpi=200)
                st.image('x.png')
                os.remove('x.png')
                st.plotly_chart(fig)

        else:
            st.markdown("No data found, try other extension, please.")
    elif opt=='Clayoquot Slope - Hydrophone C':
        filters1 = {
            'locationCode': 'CQSH.H3',
            'deviceCategoryCode': 'HYDROPHONE',
            }
        resultX = onc.getLocations(filters1)
        za = pd.DataFrame(resultX)
        st.markdown(za.description.values[0])


        df_dep = []
        for deployment in onc.getDeployments(filters={'locationCode': 'CQSH.H3', 'deviceCategoryCode': 'HYDROPHONE'}):
            df_dep.append([deployment['locationCode'], deployment['begin'], deployment['end']])

        npl = np.array(df_dep)
        locationC = pd.DataFrame(npl[:,0])
        deplF = pd.DataFrame(npl[:,1])
        deplT = pd.DataFrame(npl[:,2])

        df_dep = pd.concat([locationC,deplF,deplT],axis=1)
        df_dep.columns=["Location Code", "Deployed from", "Deployed to"]


        st.write("There are {} deployments.".format(df_dep.shape[0]))
        df_dep["Deployed from"] = pd.to_datetime(df_dep["Deployed from"]).apply(lambda y: y.date())
        df_dep["Deployed to"] = pd.to_datetime(df_dep["Deployed to"]).apply(lambda y: y.date())
        fe = df_dep.style.hide_index()
        st.write(fe.to_html(), unsafe_allow_html=True)

        start_date = st.sidebar.date_input("Select Start Date")
        end_date = st.sidebar.date_input("Select End Date")

        e = datetime.strptime(str(start_date),"%Y-%m-%d")
        el =datetime.timestamp(e)
        elT = datetime.utcfromtimestamp(el).strftime("%Y-%m-%dT%H:%M:%S")+'.000Z'
        f = datetime.strptime(str(end_date),"%Y-%m-%d")
        fl =datetime.timestamp(f)
        flT = datetime.utcfromtimestamp(fl).strftime("%Y-%m-%dT%H:%M:%S")+'.000Z'


        df_dev = []
        for dev in onc.getDevices({
            'locationCode': 'CQSH.H3',
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
                'locationCode': 'CQSH.H3'
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
        result1 = onc.getListByDevice(filt, allPages=True)
        df = pd.DataFrame(result1)
        if len(df) > 0:
            st.markdown("There are {} files".format(len(df)) + ' from ' + filt['deviceCode'] 
                    + ' between '   + parse(filt['dateFrom']).strftime('%Y %b %d')
            + ' and ' + parse(filt['dateTo']).strftime('%Y %b %d'))
            with st.expander("Data:"):
                st.write(df)
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
                                    .strip('-spect').strip('-spect-small').strip('-LPF-spect').strip('-LPF-spect-thumb')
                                    .strip('-HPF-spect').strip('-HPF-spect-thumb').split('_')[1])   
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
            
                    
            option = st.selectbox(
                'How would you like to visualize the data availability:?',
                ('Line only', 'Bar only', 'Both'))
            
            if option == 'Line only':
                fig = px.scatter(df, x="files", y="UTC time",
                                 title='Data Availabiltiy Plot for {} of the entire deployment (Please enlarge the plot for better visualization)'.format(deviceZ),
                                 template='plotly_white'
                )
                fig.update_layout(yaxis=dict(title=''), xaxis=dict(title='', showgrid=False, gridcolor='grey',
                      tickvals=[],),hovermode="y unified")
                fig.update_traces(connectgaps=False,hovertemplate=None)


                st.plotly_chart(fig)

            elif option=='Bar only':
                df_dt = pd.to_datetime(df_dt)
                dm = df_dt.dt.strftime('%m-%d')
                dav = dm.value_counts().sort_index()


                fig1 = plt.figure(figsize = (4,2))

                ax = plt.axes()
                ax.barh(dav.index,dav,color=sns.color_palette("tab10"),align ='center')
                # Remove axes splines
                for s in ['top', 'bottom', 'left', 'right']:
                    ax.spines[s].set_visible(False)
                    # Remove x, y Ticks
                ax.xaxis.set_ticks_position('none')
                ax.yaxis.set_ticks_position('none')

                plt.yticks(fontsize=5)
                plt.ylabel("day",size = 4)

                ax.legend()        
 
                ax.get_xaxis().set_visible(False)

                ax.set_title('Data Available Per day',
                         loc ='left',fontsize=5 )
            # Add annotation to bars
                for p in ax.patches:
                    left, bottom, width, height = p.get_bbox().bounds
                    ax.annotate(str(int(width)), xy=(left+width/2, bottom+height/2), 
                                ha='center', va='center', size = 3)
            
                # save image, display it, and delete after usage.
                plt.savefig('x',dpi=200)
                st.image('x.png')
                os.remove('x.png')
                        
            else:
                fig = px.scatter(df, x="files", y="UTC time",
                                 title='Data Availabiltiy Plot for {} of the entire deployment (Please enlarge the plot for better visualization)'.format(deviceZ),
                                 template='plotly_white'
                )
                fig.update_layout(yaxis=dict(title=''), xaxis=dict(title='', showgrid=False, gridcolor='grey',
                      tickvals=[],),hovermode="y unified")
                fig.update_traces(connectgaps=False,hovertemplate=None)
                
                df_dt = pd.to_datetime(df_dt)
                dm = df_dt.dt.strftime('%m-%d')
                dav = dm.value_counts().sort_index()


                fig1 = plt.figure(figsize = (4,2))

                ax = plt.axes()
                ax.barh(dav.index,dav,color=sns.color_palette("tab10"),align ='center')
                # Remove axes splines
                for s in ['top', 'bottom', 'left', 'right']:
                    ax.spines[s].set_visible(False)
                    # Remove x, y Ticks
                ax.xaxis.set_ticks_position('none')
                ax.yaxis.set_ticks_position('none')

                plt.yticks(fontsize=5)
                plt.ylabel("day",size = 4)

                ax.legend()        
 
                ax.get_xaxis().set_visible(False)

                ax.set_title('Data Available Per day',
                         loc ='left',fontsize=5 )
            # Add annotation to bars
                for p in ax.patches:
                    left, bottom, width, height = p.get_bbox().bounds
                    ax.annotate(str(int(width)), xy=(left+width/2, bottom+height/2), 
                                ha='center', va='center', size = 3)
            
                # save image, display it, and delete after usage.
                plt.savefig('x',dpi=200)
                st.image('x.png')
                os.remove('x.png')
                st.plotly_chart(fig)

        else:
            st.markdown("No data found, try other extension, please.")
    elif opt=='Clayoquot Slope - Hydrophone D':
        filters1 = {
            'locationCode': 'CQSH.H4',
            'deviceCategoryCode': 'HYDROPHONE',
            }
        resultX = onc.getLocations(filters1)
        za = pd.DataFrame(resultX)
        st.markdown(za.description.values[0])


        df_dep = []
        for deployment in onc.getDeployments(filters={'locationCode': 'CQSH.H4', 'deviceCategoryCode': 'HYDROPHONE'}):
            df_dep.append([deployment['locationCode'], deployment['begin'], deployment['end']])

        npl = np.array(df_dep)
        locationC = pd.DataFrame(npl[:,0])
        deplF = pd.DataFrame(npl[:,1])
        deplT = pd.DataFrame(npl[:,2])

        df_dep = pd.concat([locationC,deplF,deplT],axis=1)
        df_dep.columns=["Location Code", "Deployed from", "Deployed to"]


        st.write("There are {} deployments.".format(df_dep.shape[0]))
        df_dep["Deployed from"] = pd.to_datetime(df_dep["Deployed from"]).apply(lambda y: y.date())
        df_dep["Deployed to"] = pd.to_datetime(df_dep["Deployed to"]).apply(lambda y: y.date())
        fe = df_dep.style.hide_index()
        st.write(fe.to_html(), unsafe_allow_html=True)

        start_date = st.sidebar.date_input("Select Start Date")
        end_date = st.sidebar.date_input("Select End Date")

        e = datetime.strptime(str(start_date),"%Y-%m-%d")
        el =datetime.timestamp(e)
        elT = datetime.utcfromtimestamp(el).strftime("%Y-%m-%dT%H:%M:%S")+'.000Z'
        f = datetime.strptime(str(end_date),"%Y-%m-%d")
        fl =datetime.timestamp(f)
        flT = datetime.utcfromtimestamp(fl).strftime("%Y-%m-%dT%H:%M:%S")+'.000Z'


        df_dev = []
        for dev in onc.getDevices({
            'locationCode': 'CQSH.H4',
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
                'locationCode': 'CQSH.H4'
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
        result1 = onc.getListByDevice(filt, allPages=True)
        df = pd.DataFrame(result1)
        if len(df) > 0:
            st.markdown("There are {} files".format(len(df)) + ' from ' + filt['deviceCode'] 
                    + ' between '   + parse(filt['dateFrom']).strftime('%Y %b %d')
            + ' and ' + parse(filt['dateTo']).strftime('%Y %b %d'))
            with st.expander("Data:"):
                st.write(df)
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
                                    .strip('-spect').strip('-spect-small').strip('-LPF-spect').strip('-LPF-spect-thumb')
                                    .strip('-HPF-spect').strip('-HPF-spect-thumb').split('_')[1])   
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
            
                    
            option = st.selectbox(
                'How would you like to visualize the data availability:?',
                ('Line only', 'Bar only', 'Both'))
            
            if option == 'Line only':
                fig = px.scatter(df, x="files", y="UTC time",
                                 title='Data Availabiltiy Plot for {} of the entire deployment (Please enlarge the plot for better visualization)'.format(deviceZ),
                                 template='plotly_white'
                )
                fig.update_layout(yaxis=dict(title=''), xaxis=dict(title='', showgrid=False, gridcolor='grey',
                      tickvals=[],),hovermode="y unified")
                fig.update_traces(connectgaps=False,hovertemplate=None)


                st.plotly_chart(fig)

            elif option=='Bar only':
                df_dt = pd.to_datetime(df_dt)
                dm = df_dt.dt.strftime('%m-%d')
                dav = dm.value_counts().sort_index()


                fig1 = plt.figure(figsize = (4,2))

                ax = plt.axes()
                ax.barh(dav.index,dav,color=sns.color_palette("tab10"),align ='center')
                # Remove axes splines
                for s in ['top', 'bottom', 'left', 'right']:
                    ax.spines[s].set_visible(False)
                    # Remove x, y Ticks
                ax.xaxis.set_ticks_position('none')
                ax.yaxis.set_ticks_position('none')

                plt.yticks(fontsize=5)
                plt.ylabel("day",size = 4)

                ax.legend()        
 
                ax.get_xaxis().set_visible(False)

                ax.set_title('Data Available Per day',
                         loc ='left',fontsize=5 )
            # Add annotation to bars
                for p in ax.patches:
                    left, bottom, width, height = p.get_bbox().bounds
                    ax.annotate(str(int(width)), xy=(left+width/2, bottom+height/2), 
                                ha='center', va='center', size = 3)
            
                # save image, display it, and delete after usage.
                plt.savefig('x',dpi=200)
                st.image('x.png')
                os.remove('x.png')
                        
            else:
                fig = px.scatter(df, x="files", y="UTC time",
                                 title='Data Availabiltiy Plot for {} of the entire deployment (Please enlarge the plot for better visualization)'.format(deviceZ),
                                 template='plotly_white'
                )
                fig.update_layout(yaxis=dict(title=''), xaxis=dict(title='', showgrid=False, gridcolor='grey',
                      tickvals=[],),hovermode="y unified")
                fig.update_traces(connectgaps=False,hovertemplate=None)
                
                df_dt = pd.to_datetime(df_dt)
                dm = df_dt.dt.strftime('%m-%d')
                dav = dm.value_counts().sort_index()


                fig1 = plt.figure(figsize = (4,2))

                ax = plt.axes()
                ax.barh(dav.index,dav,color=sns.color_palette("tab10"),align ='center')
                # Remove axes splines
                for s in ['top', 'bottom', 'left', 'right']:
                    ax.spines[s].set_visible(False)
                    # Remove x, y Ticks
                ax.xaxis.set_ticks_position('none')
                ax.yaxis.set_ticks_position('none')

                plt.yticks(fontsize=5)
                plt.ylabel("day",size = 4)

                ax.legend()        
 
                ax.get_xaxis().set_visible(False)

                ax.set_title('Data Available Per day',
                         loc ='left',fontsize=5 )
            # Add annotation to bars
                for p in ax.patches:
                    left, bottom, width, height = p.get_bbox().bounds
                    ax.annotate(str(int(width)), xy=(left+width/2, bottom+height/2), 
                                ha='center', va='center', size = 3)
            
                # save image, display it, and delete after usage.
                plt.savefig('x',dpi=200)
                st.image('x.png')
                os.remove('x.png')
                st.plotly_chart(fig)

        else:
            st.markdown("No data found, try other extension, please.")
    elif opt=='SOG East - Hydrophone Array A':
        filters1 = {
            'locationCode': 'ECHO3.H1',
            'deviceCategoryCode': 'HYDROPHONE',
            }
        resultX = onc.getLocations(filters1)
        za = pd.DataFrame(resultX)
        st.markdown(za.description.values[0])


        df_dep = []
        for deployment in onc.getDeployments(filters={'locationCode': 'ECHO3.H1', 'deviceCategoryCode': 'HYDROPHONE'}):
            df_dep.append([deployment['locationCode'], deployment['begin'], deployment['end']])

        npl = np.array(df_dep)
        locationC = pd.DataFrame(npl[:,0])
        deplF = pd.DataFrame(npl[:,1])
        deplT = pd.DataFrame(npl[:,2])

        df_dep = pd.concat([locationC,deplF,deplT],axis=1)
        df_dep.columns=["Location Code", "Deployed from", "Deployed to"]


        st.write("There are {} deployments.".format(df_dep.shape[0]))
        df_dep["Deployed from"] = pd.to_datetime(df_dep["Deployed from"]).apply(lambda y: y.date())
        df_dep["Deployed to"] = pd.to_datetime(df_dep["Deployed to"]).apply(lambda y: y.date())
        fe = df_dep.style.hide_index()
        st.write(fe.to_html(), unsafe_allow_html=True)

        start_date = st.sidebar.date_input("Select Start Date")
        end_date = st.sidebar.date_input("Select End Date")

        e = datetime.strptime(str(start_date),"%Y-%m-%d")
        el =datetime.timestamp(e)
        elT = datetime.utcfromtimestamp(el).strftime("%Y-%m-%dT%H:%M:%S")+'.000Z'
        f = datetime.strptime(str(end_date),"%Y-%m-%d")
        fl =datetime.timestamp(f)
        flT = datetime.utcfromtimestamp(fl).strftime("%Y-%m-%dT%H:%M:%S")+'.000Z'


        df_dev = []
        for dev in onc.getDevices({
            'locationCode': 'ECHO3.H1',
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
                'locationCode': 'ECHO3.H1'
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
        result1 = onc.getListByDevice(filt, allPages=True)
        df = pd.DataFrame(result1)
        if len(df) > 0:
            st.markdown("There are {} files".format(len(df)) + ' from ' + filt['deviceCode'] 
                    + ' between '   + parse(filt['dateFrom']).strftime('%Y %b %d')
            + ' and ' + parse(filt['dateTo']).strftime('%Y %b %d'))
            with st.expander("Data:"):
                st.write(df)
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
                                    .strip('-spect').strip('-spect-small').strip('-LPF-spect').strip('-LPF-spect-thumb')
                                    .strip('-HPF-spect').strip('-HPF-spect-thumb').split('_')[1])   
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
            
                    
            option = st.selectbox(
                'How would you like to visualize the data availability:?',
                ('Line only', 'Bar only', 'Both'))
            
            if option == 'Line only':
                fig = px.scatter(df, x="files", y="UTC time",
                                 title='Data Availabiltiy Plot for {} of the entire deployment (Please enlarge the plot for better visualization)'.format(deviceZ),
                                 template='plotly_white'
                )
                fig.update_layout(yaxis=dict(title=''), xaxis=dict(title='', showgrid=False, gridcolor='grey',
                      tickvals=[],),hovermode="y unified")
                fig.update_traces(connectgaps=False,hovertemplate=None)


                st.plotly_chart(fig)

            elif option=='Bar only':
                df_dt = pd.to_datetime(df_dt)
                dm = df_dt.dt.strftime('%m-%d')
                dav = dm.value_counts().sort_index()


                fig1 = plt.figure(figsize = (4,2))

                ax = plt.axes()
                ax.barh(dav.index,dav,color=sns.color_palette("tab10"),align ='center')
                # Remove axes splines
                for s in ['top', 'bottom', 'left', 'right']:
                    ax.spines[s].set_visible(False)
                    # Remove x, y Ticks
                ax.xaxis.set_ticks_position('none')
                ax.yaxis.set_ticks_position('none')

                plt.yticks(fontsize=5)
                plt.ylabel("day",size = 4)

                ax.legend()        
 
                ax.get_xaxis().set_visible(False)

                ax.set_title('Data Available Per day',
                         loc ='left',fontsize=5 )
            # Add annotation to bars
                for p in ax.patches:
                    left, bottom, width, height = p.get_bbox().bounds
                    ax.annotate(str(int(width)), xy=(left+width/2, bottom+height/2), 
                                ha='center', va='center', size = 3)
            
                # save image, display it, and delete after usage.
                plt.savefig('x',dpi=200)
                st.image('x.png')
                os.remove('x.png')
                        
            else:
                fig = px.scatter(df, x="files", y="UTC time",
                                 title='Data Availabiltiy Plot for {} of the entire deployment (Please enlarge the plot for better visualization)'.format(deviceZ),
                                 template='plotly_white'
                )
                fig.update_layout(yaxis=dict(title=''), xaxis=dict(title='', showgrid=False, gridcolor='grey',
                      tickvals=[],),hovermode="y unified")
                fig.update_traces(connectgaps=False,hovertemplate=None)
                
                df_dt = pd.to_datetime(df_dt)
                dm = df_dt.dt.strftime('%m-%d')
                dav = dm.value_counts().sort_index()


                fig1 = plt.figure(figsize = (4,2))

                ax = plt.axes()
                ax.barh(dav.index,dav,color=sns.color_palette("tab10"),align ='center')
                # Remove axes splines
                for s in ['top', 'bottom', 'left', 'right']:
                    ax.spines[s].set_visible(False)
                    # Remove x, y Ticks
                ax.xaxis.set_ticks_position('none')
                ax.yaxis.set_ticks_position('none')

                plt.yticks(fontsize=5)
                plt.ylabel("day",size = 4)

                ax.legend()        
 
                ax.get_xaxis().set_visible(False)

                ax.set_title('Data Available Per day',
                         loc ='left',fontsize=5 )
            # Add annotation to bars
                for p in ax.patches:
                    left, bottom, width, height = p.get_bbox().bounds
                    ax.annotate(str(int(width)), xy=(left+width/2, bottom+height/2), 
                                ha='center', va='center', size = 3)
            
                # save image, display it, and delete after usage.
                plt.savefig('x',dpi=200)
                st.image('x.png')
                os.remove('x.png')
                st.plotly_chart(fig)

        else:
            st.markdown("No data found, try other extension, please.")
    elif opt=='SOG East - Hydrophone Array B':
        filters1 = {
            'locationCode': 'ECHO3.H2',
            'deviceCategoryCode': 'HYDROPHONE',
            }
        resultX = onc.getLocations(filters1)
        za = pd.DataFrame(resultX)
        st.markdown(za.description.values[0])


        df_dep = []
        for deployment in onc.getDeployments(filters={'locationCode': 'ECHO3.H2', 'deviceCategoryCode': 'HYDROPHONE'}):
            df_dep.append([deployment['locationCode'], deployment['begin'], deployment['end']])

        npl = np.array(df_dep)
        locationC = pd.DataFrame(npl[:,0])
        deplF = pd.DataFrame(npl[:,1])
        deplT = pd.DataFrame(npl[:,2])

        df_dep = pd.concat([locationC,deplF,deplT],axis=1)
        df_dep.columns=["Location Code", "Deployed from", "Deployed to"]


        st.write("There are {} deployments.".format(df_dep.shape[0]))
        df_dep["Deployed from"] = pd.to_datetime(df_dep["Deployed from"]).apply(lambda y: y.date())
        df_dep["Deployed to"] = pd.to_datetime(df_dep["Deployed to"]).apply(lambda y: y.date())
        fe = df_dep.style.hide_index()
        st.write(fe.to_html(), unsafe_allow_html=True)

        start_date = st.sidebar.date_input("Select Start Date")
        end_date = st.sidebar.date_input("Select End Date")

        e = datetime.strptime(str(start_date),"%Y-%m-%d")
        el =datetime.timestamp(e)
        elT = datetime.utcfromtimestamp(el).strftime("%Y-%m-%dT%H:%M:%S")+'.000Z'
        f = datetime.strptime(str(end_date),"%Y-%m-%d")
        fl =datetime.timestamp(f)
        flT = datetime.utcfromtimestamp(fl).strftime("%Y-%m-%dT%H:%M:%S")+'.000Z'


        df_dev = []
        for dev in onc.getDevices({
            'locationCode': 'ECHO3.H2',
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
                'locationCode': 'ECHO3.H2'
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
        result1 = onc.getListByDevice(filt, allPages=True)
        df = pd.DataFrame(result1)
        if len(df) > 0:
            st.markdown("There are {} files".format(len(df)) + ' from ' + filt['deviceCode'] 
                    + ' between '   + parse(filt['dateFrom']).strftime('%Y %b %d')
            + ' and ' + parse(filt['dateTo']).strftime('%Y %b %d'))
            with st.expander("Data:"):
                st.write(df)
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
                                    .strip('-spect').strip('-spect-small').strip('-LPF-spect').strip('-LPF-spect-thumb')
                                    .strip('-HPF-spect').strip('-HPF-spect-thumb').split('_')[1])   
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
            
                    
            option = st.selectbox(
                'How would you like to visualize the data availability:?',
                ('Line only', 'Bar only', 'Both'))
            
            if option == 'Line only':
                fig = px.scatter(df, x="files", y="UTC time",
                                 title='Data Availabiltiy Plot for {} of the entire deployment (Please enlarge the plot for better visualization)'.format(deviceZ),
                                 template='plotly_white'
                )
                fig.update_layout(yaxis=dict(title=''), xaxis=dict(title='', showgrid=False, gridcolor='grey',
                      tickvals=[],),hovermode="y unified")
                fig.update_traces(connectgaps=False,hovertemplate=None)


                st.plotly_chart(fig)

            elif option=='Bar only':
                df_dt = pd.to_datetime(df_dt)
                dm = df_dt.dt.strftime('%m-%d')
                dav = dm.value_counts().sort_index()


                fig1 = plt.figure(figsize = (4,2))

                ax = plt.axes()
                ax.barh(dav.index,dav,color=sns.color_palette("tab10"),align ='center')
                # Remove axes splines
                for s in ['top', 'bottom', 'left', 'right']:
                    ax.spines[s].set_visible(False)
                    # Remove x, y Ticks
                ax.xaxis.set_ticks_position('none')
                ax.yaxis.set_ticks_position('none')

                plt.yticks(fontsize=5)
                plt.ylabel("day",size = 4)

                ax.legend()        
 
                ax.get_xaxis().set_visible(False)

                ax.set_title('Data Available Per day',
                         loc ='left',fontsize=5 )
            # Add annotation to bars
                for p in ax.patches:
                    left, bottom, width, height = p.get_bbox().bounds
                    ax.annotate(str(int(width)), xy=(left+width/2, bottom+height/2), 
                                ha='center', va='center', size = 3)
            
                # save image, display it, and delete after usage.
                plt.savefig('x',dpi=200)
                st.image('x.png')
                os.remove('x.png')
                        
            else:
                fig = px.scatter(df, x="files", y="UTC time",
                                 title='Data Availabiltiy Plot for {} of the entire deployment (Please enlarge the plot for better visualization)'.format(deviceZ),
                                 template='plotly_white'
                )
                fig.update_layout(yaxis=dict(title=''), xaxis=dict(title='', showgrid=False, gridcolor='grey',
                      tickvals=[],),hovermode="y unified")
                fig.update_traces(connectgaps=False,hovertemplate=None)
                
                df_dt = pd.to_datetime(df_dt)
                dm = df_dt.dt.strftime('%m-%d')
                dav = dm.value_counts().sort_index()


                fig1 = plt.figure(figsize = (4,2))

                ax = plt.axes()
                ax.barh(dav.index,dav,color=sns.color_palette("tab10"),align ='center')
                # Remove axes splines
                for s in ['top', 'bottom', 'left', 'right']:
                    ax.spines[s].set_visible(False)
                    # Remove x, y Ticks
                ax.xaxis.set_ticks_position('none')
                ax.yaxis.set_ticks_position('none')

                plt.yticks(fontsize=5)
                plt.ylabel("day",size = 4)

                ax.legend()        
 
                ax.get_xaxis().set_visible(False)

                ax.set_title('Data Available Per day',
                         loc ='left',fontsize=5 )
            # Add annotation to bars
                for p in ax.patches:
                    left, bottom, width, height = p.get_bbox().bounds
                    ax.annotate(str(int(width)), xy=(left+width/2, bottom+height/2), 
                                ha='center', va='center', size = 3)
            
                # save image, display it, and delete after usage.
                plt.savefig('x',dpi=200)
                st.image('x.png')
                os.remove('x.png')
                st.plotly_chart(fig)

        else:
            st.markdown("No data found, try other extension, please.")
    elif opt=='SOG East - Hydrophone Array C':
        filters1 = {
            'locationCode': 'ECHO3.H3',
            'deviceCategoryCode': 'HYDROPHONE',
            }
        resultX = onc.getLocations(filters1)
        za = pd.DataFrame(resultX)
        st.markdown(za.description.values[0])


        df_dep = []
        for deployment in onc.getDeployments(filters={'locationCode': 'ECHO3.H3', 'deviceCategoryCode': 'HYDROPHONE'}):
            df_dep.append([deployment['locationCode'], deployment['begin'], deployment['end']])

        npl = np.array(df_dep)
        locationC = pd.DataFrame(npl[:,0])
        deplF = pd.DataFrame(npl[:,1])
        deplT = pd.DataFrame(npl[:,2])

        df_dep = pd.concat([locationC,deplF,deplT],axis=1)
        df_dep.columns=["Location Code", "Deployed from", "Deployed to"]


        st.write("There are {} deployments.".format(df_dep.shape[0]))
        df_dep["Deployed from"] = pd.to_datetime(df_dep["Deployed from"]).apply(lambda y: y.date())
        df_dep["Deployed to"] = pd.to_datetime(df_dep["Deployed to"]).apply(lambda y: y.date())
        fe = df_dep.style.hide_index()
        st.write(fe.to_html(), unsafe_allow_html=True)

        start_date = st.sidebar.date_input("Select Start Date")
        end_date = st.sidebar.date_input("Select End Date")

        e = datetime.strptime(str(start_date),"%Y-%m-%d")
        el =datetime.timestamp(e)
        elT = datetime.utcfromtimestamp(el).strftime("%Y-%m-%dT%H:%M:%S")+'.000Z'
        f = datetime.strptime(str(end_date),"%Y-%m-%d")
        fl =datetime.timestamp(f)
        flT = datetime.utcfromtimestamp(fl).strftime("%Y-%m-%dT%H:%M:%S")+'.000Z'


        df_dev = []
        for dev in onc.getDevices({
            'locationCode': 'ECHO3.H3',
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
                'locationCode': 'ECHO3.H3'
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
        result1 = onc.getListByDevice(filt, allPages=True)
        df = pd.DataFrame(result1)
        if len(df) > 0:
            st.markdown("There are {} files".format(len(df)) + ' from ' + filt['deviceCode'] 
                    + ' between '   + parse(filt['dateFrom']).strftime('%Y %b %d')
            + ' and ' + parse(filt['dateTo']).strftime('%Y %b %d'))
            with st.expander("Data:"):
                st.write(df)
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
                                    .strip('-spect').strip('-spect-small').strip('-LPF-spect').strip('-LPF-spect-thumb')
                                    .strip('-HPF-spect').strip('-HPF-spect-thumb').split('_')[1])   
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
            
                    
            option = st.selectbox(
                'How would you like to visualize the data availability:?',
                ('Line only', 'Bar only', 'Both'))
            
            if option == 'Line only':
                fig = px.scatter(df, x="files", y="UTC time",
                                 title='Data Availabiltiy Plot for {} of the entire deployment (Please enlarge the plot for better visualization)'.format(deviceZ),
                                 template='plotly_white'
                )
                fig.update_layout(yaxis=dict(title=''), xaxis=dict(title='', showgrid=False, gridcolor='grey',
                      tickvals=[],),hovermode="y unified")
                fig.update_traces(connectgaps=False,hovertemplate=None)


                st.plotly_chart(fig)

            elif option=='Bar only':
                df_dt = pd.to_datetime(df_dt)
                dm = df_dt.dt.strftime('%m-%d')
                dav = dm.value_counts().sort_index()


                fig1 = plt.figure(figsize = (4,2))

                ax = plt.axes()
                ax.barh(dav.index,dav,color=sns.color_palette("tab10"),align ='center')
                # Remove axes splines
                for s in ['top', 'bottom', 'left', 'right']:
                    ax.spines[s].set_visible(False)
                    # Remove x, y Ticks
                ax.xaxis.set_ticks_position('none')
                ax.yaxis.set_ticks_position('none')

                plt.yticks(fontsize=5)
                plt.ylabel("day",size = 4)

                ax.legend()        
 
                ax.get_xaxis().set_visible(False)

                ax.set_title('Data Available Per day',
                         loc ='left',fontsize=5 )
            # Add annotation to bars
                for p in ax.patches:
                    left, bottom, width, height = p.get_bbox().bounds
                    ax.annotate(str(int(width)), xy=(left+width/2, bottom+height/2), 
                                ha='center', va='center', size = 3)
            
                # save image, display it, and delete after usage.
                plt.savefig('x',dpi=200)
                st.image('x.png')
                os.remove('x.png')
                        
            else:
                fig = px.scatter(df, x="files", y="UTC time",
                                 title='Data Availabiltiy Plot for {} of the entire deployment (Please enlarge the plot for better visualization)'.format(deviceZ),
                                 template='plotly_white'
                )
                fig.update_layout(yaxis=dict(title=''), xaxis=dict(title='', showgrid=False, gridcolor='grey',
                      tickvals=[],),hovermode="y unified")
                fig.update_traces(connectgaps=False,hovertemplate=None)
                
                df_dt = pd.to_datetime(df_dt)
                dm = df_dt.dt.strftime('%m-%d')
                dav = dm.value_counts().sort_index()


                fig1 = plt.figure(figsize = (4,2))

                ax = plt.axes()
                ax.barh(dav.index,dav,color=sns.color_palette("tab10"),align ='center')
                # Remove axes splines
                for s in ['top', 'bottom', 'left', 'right']:
                    ax.spines[s].set_visible(False)
                    # Remove x, y Ticks
                ax.xaxis.set_ticks_position('none')
                ax.yaxis.set_ticks_position('none')

                plt.yticks(fontsize=5)
                plt.ylabel("day",size = 4)

                ax.legend()        
 
                ax.get_xaxis().set_visible(False)

                ax.set_title('Data Available Per day',
                         loc ='left',fontsize=5 )
            # Add annotation to bars
                for p in ax.patches:
                    left, bottom, width, height = p.get_bbox().bounds
                    ax.annotate(str(int(width)), xy=(left+width/2, bottom+height/2), 
                                ha='center', va='center', size = 3)
            
                # save image, display it, and delete after usage.
                plt.savefig('x',dpi=200)
                st.image('x.png')
                os.remove('x.png')
                st.plotly_chart(fig)

        else:
            st.markdown("No data found, try other extension, please.")
    elif opt=='SOG East - Hydrophone Array D':
        filters1 = {
            'locationCode': 'ECHO3.H4',
            'deviceCategoryCode': 'HYDROPHONE',
            }
        resultX = onc.getLocations(filters1)
        za = pd.DataFrame(resultX)
        st.markdown(za.description.values[0])


        df_dep = []
        for deployment in onc.getDeployments(filters={'locationCode': 'ECHO3.H4', 'deviceCategoryCode': 'HYDROPHONE'}):
            df_dep.append([deployment['locationCode'], deployment['begin'], deployment['end']])

        npl = np.array(df_dep)
        locationC = pd.DataFrame(npl[:,0])
        deplF = pd.DataFrame(npl[:,1])
        deplT = pd.DataFrame(npl[:,2])

        df_dep = pd.concat([locationC,deplF,deplT],axis=1)
        df_dep.columns=["Location Code", "Deployed from", "Deployed to"]


        st.write("There are {} deployments.".format(df_dep.shape[0]))
        df_dep["Deployed from"] = pd.to_datetime(df_dep["Deployed from"]).apply(lambda y: y.date())
        df_dep["Deployed to"] = pd.to_datetime(df_dep["Deployed to"]).apply(lambda y: y.date())
        fe = df_dep.style.hide_index()
        st.write(fe.to_html(), unsafe_allow_html=True)

        start_date = st.sidebar.date_input("Select Start Date")
        end_date = st.sidebar.date_input("Select End Date")

        e = datetime.strptime(str(start_date),"%Y-%m-%d")
        el =datetime.timestamp(e)
        elT = datetime.utcfromtimestamp(el).strftime("%Y-%m-%dT%H:%M:%S")+'.000Z'
        f = datetime.strptime(str(end_date),"%Y-%m-%d")
        fl =datetime.timestamp(f)
        flT = datetime.utcfromtimestamp(fl).strftime("%Y-%m-%dT%H:%M:%S")+'.000Z'


        df_dev = []
        for dev in onc.getDevices({
            'locationCode': 'ECHO3.H4',
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
                'locationCode': 'ECHO3.H4'
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
        result1 = onc.getListByDevice(filt, allPages=True)
        df = pd.DataFrame(result1)
        if len(df) > 0:
            st.markdown("There are {} files".format(len(df)) + ' from ' + filt['deviceCode'] 
                    + ' between '   + parse(filt['dateFrom']).strftime('%Y %b %d')
            + ' and ' + parse(filt['dateTo']).strftime('%Y %b %d'))
            with st.expander("Data:"):
                st.write(df)
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
                                    .strip('-spect').strip('-spect-small').strip('-LPF-spect').strip('-LPF-spect-thumb')
                                    .strip('-HPF-spect').strip('-HPF-spect-thumb').split('_')[1])   
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
            
                    
            option = st.selectbox(
                'How would you like to visualize the data availability:?',
                ('Line only', 'Bar only', 'Both'))
            
            if option == 'Line only':
                fig = px.scatter(df, x="files", y="UTC time",
                                 title='Data Availabiltiy Plot for {} of the entire deployment (Please enlarge the plot for better visualization)'.format(deviceZ),
                                 template='plotly_white'
                )
                fig.update_layout(yaxis=dict(title=''), xaxis=dict(title='', showgrid=False, gridcolor='grey',
                      tickvals=[],),hovermode="y unified")
                fig.update_traces(connectgaps=False,hovertemplate=None)


                st.plotly_chart(fig)

            elif option=='Bar only':
                df_dt = pd.to_datetime(df_dt)
                dm = df_dt.dt.strftime('%m-%d')
                dav = dm.value_counts().sort_index()


                fig1 = plt.figure(figsize = (4,2))

                ax = plt.axes()
                ax.barh(dav.index,dav,color=sns.color_palette("tab10"),align ='center')
                # Remove axes splines
                for s in ['top', 'bottom', 'left', 'right']:
                    ax.spines[s].set_visible(False)
                    # Remove x, y Ticks
                ax.xaxis.set_ticks_position('none')
                ax.yaxis.set_ticks_position('none')

                plt.yticks(fontsize=5)
                plt.ylabel("day",size = 4)

                ax.legend()        
 
                ax.get_xaxis().set_visible(False)

                ax.set_title('Data Available Per day',
                         loc ='left',fontsize=5 )
            # Add annotation to bars
                for p in ax.patches:
                    left, bottom, width, height = p.get_bbox().bounds
                    ax.annotate(str(int(width)), xy=(left+width/2, bottom+height/2), 
                                ha='center', va='center', size = 3)
            
                # save image, display it, and delete after usage.
                plt.savefig('x',dpi=200)
                st.image('x.png')
                os.remove('x.png')
                        
            else:
                fig = px.scatter(df, x="files", y="UTC time",
                                 title='Data Availabiltiy Plot for {} of the entire deployment (Please enlarge the plot for better visualization)'.format(deviceZ),
                                 template='plotly_white'
                )
                fig.update_layout(yaxis=dict(title=''), xaxis=dict(title='', showgrid=False, gridcolor='grey',
                      tickvals=[],),hovermode="y unified")
                fig.update_traces(connectgaps=False,hovertemplate=None)
                
                df_dt = pd.to_datetime(df_dt)
                dm = df_dt.dt.strftime('%m-%d')
                dav = dm.value_counts().sort_index()


                fig1 = plt.figure(figsize = (4,2))

                ax = plt.axes()
                ax.barh(dav.index,dav,color=sns.color_palette("tab10"),align ='center')
                # Remove axes splines
                for s in ['top', 'bottom', 'left', 'right']:
                    ax.spines[s].set_visible(False)
                    # Remove x, y Ticks
                ax.xaxis.set_ticks_position('none')
                ax.yaxis.set_ticks_position('none')

                plt.yticks(fontsize=5)
                plt.ylabel("day",size = 4)

                ax.legend()        
 
                ax.get_xaxis().set_visible(False)

                ax.set_title('Data Available Per day',
                         loc ='left',fontsize=5 )
            # Add annotation to bars
                for p in ax.patches:
                    left, bottom, width, height = p.get_bbox().bounds
                    ax.annotate(str(int(width)), xy=(left+width/2, bottom+height/2), 
                                ha='center', va='center', size = 3)
            
                # save image, display it, and delete after usage.
                plt.savefig('x',dpi=200)
                st.image('x.png')
                os.remove('x.png')
                st.plotly_chart(fig)

        else:
            st.markdown("No data found, try other extension, please.")
    elif opt=='Discovery Passage - Campbell River':
        filters1 = {
            'locationCode': 'CRIP',
            'deviceCategoryCode': 'HYDROPHONE',
            }
        resultX = onc.getLocations(filters1)
        za = pd.DataFrame(resultX)
        st.markdown(za.description.values[0])


        df_dep = []
        for deployment in onc.getDeployments(filters={'locationCode': 'CRIP', 'deviceCategoryCode': 'HYDROPHONE'}):
            df_dep.append([deployment['locationCode'], deployment['begin'], deployment['end']])

        npl = np.array(df_dep)
        locationC = pd.DataFrame(npl[:,0])
        deplF = pd.DataFrame(npl[:,1])
        deplT = pd.DataFrame(npl[:,2])

        df_dep = pd.concat([locationC,deplF,deplT],axis=1)
        df_dep.columns=["Location Code", "Deployed from", "Deployed to"]


        st.write("There are {} deployments.".format(df_dep.shape[0]))
        df_dep["Deployed from"] = pd.to_datetime(df_dep["Deployed from"]).apply(lambda y: y.date())
        df_dep["Deployed to"] = pd.to_datetime(df_dep["Deployed to"]).apply(lambda y: y.date())
        fe = df_dep.style.hide_index()
        st.write(fe.to_html(), unsafe_allow_html=True)

        start_date = st.sidebar.date_input("Select Start Date")
        end_date = st.sidebar.date_input("Select End Date")

        e = datetime.strptime(str(start_date),"%Y-%m-%d")
        el =datetime.timestamp(e)
        elT = datetime.utcfromtimestamp(el).strftime("%Y-%m-%dT%H:%M:%S")+'.000Z'
        f = datetime.strptime(str(end_date),"%Y-%m-%d")
        fl =datetime.timestamp(f)
        flT = datetime.utcfromtimestamp(fl).strftime("%Y-%m-%dT%H:%M:%S")+'.000Z'


        df_dev = []
        for dev in onc.getDevices({
            'locationCode': 'CRIP',
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
                'locationCode': 'CRIP'
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
        result1 = onc.getListByDevice(filt, allPages=True)
        df = pd.DataFrame(result1)
        if len(df) > 0:
            st.markdown("There are {} files".format(len(df)) + ' from ' + filt['deviceCode'] 
                    + ' between '   + parse(filt['dateFrom']).strftime('%Y %b %d')
            + ' and ' + parse(filt['dateTo']).strftime('%Y %b %d'))
            with st.expander("Data:"):
                st.write(df)
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
                                    .strip('-spect').strip('-spect-small').strip('-LPF-spect').strip('-LPF-spect-thumb')
                                    .strip('-HPF-spect').strip('-HPF-spect-thumb').split('_')[1])   
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
            
                    
            option = st.selectbox(
                'How would you like to visualize the data availability:?',
                ('Line only', 'Bar only', 'Both'))
            
            if option == 'Line only':
                fig = px.scatter(df, x="files", y="UTC time",
                                 title='Data Availabiltiy Plot for {} of the entire deployment (Please enlarge the plot for better visualization)'.format(deviceZ),
                                 template='plotly_white'
                )
                fig.update_layout(yaxis=dict(title=''), xaxis=dict(title='', showgrid=False, gridcolor='grey',
                      tickvals=[],),hovermode="y unified")
                fig.update_traces(connectgaps=False,hovertemplate=None)


                st.plotly_chart(fig)

            elif option=='Bar only':
                df_dt = pd.to_datetime(df_dt)
                dm = df_dt.dt.strftime('%m-%d')
                dav = dm.value_counts().sort_index()


                fig1 = plt.figure(figsize = (4,2))

                ax = plt.axes()
                ax.barh(dav.index,dav,color=sns.color_palette("tab10"),align ='center')
                # Remove axes splines
                for s in ['top', 'bottom', 'left', 'right']:
                    ax.spines[s].set_visible(False)
                    # Remove x, y Ticks
                ax.xaxis.set_ticks_position('none')
                ax.yaxis.set_ticks_position('none')

                plt.yticks(fontsize=5)
                plt.ylabel("day",size = 4)

                ax.legend()        
 
                ax.get_xaxis().set_visible(False)

                ax.set_title('Data Available Per day',
                         loc ='left',fontsize=5 )
            # Add annotation to bars
                for p in ax.patches:
                    left, bottom, width, height = p.get_bbox().bounds
                    ax.annotate(str(int(width)), xy=(left+width/2, bottom+height/2), 
                                ha='center', va='center', size = 3)
            
                # save image, display it, and delete after usage.
                plt.savefig('x',dpi=200)
                st.image('x.png')
                os.remove('x.png')
                        
            else:
                fig = px.scatter(df, x="files", y="UTC time",
                                 title='Data Availabiltiy Plot for {} of the entire deployment (Please enlarge the plot for better visualization)'.format(deviceZ),
                                 template='plotly_white'
                )
                fig.update_layout(yaxis=dict(title=''), xaxis=dict(title='', showgrid=False, gridcolor='grey',
                      tickvals=[],),hovermode="y unified")
                fig.update_traces(connectgaps=False,hovertemplate=None)
                
                df_dt = pd.to_datetime(df_dt)
                dm = df_dt.dt.strftime('%m-%d')
                dav = dm.value_counts().sort_index()


                fig1 = plt.figure(figsize = (4,2))

                ax = plt.axes()
                ax.barh(dav.index,dav,color=sns.color_palette("tab10"),align ='center')
                # Remove axes splines
                for s in ['top', 'bottom', 'left', 'right']:
                    ax.spines[s].set_visible(False)
                    # Remove x, y Ticks
                ax.xaxis.set_ticks_position('none')
                ax.yaxis.set_ticks_position('none')

                plt.yticks(fontsize=5)
                plt.ylabel("day",size = 4)

                ax.legend()        
 
                ax.get_xaxis().set_visible(False)

                ax.set_title('Data Available Per day',
                         loc ='left',fontsize=5 )
            # Add annotation to bars
                for p in ax.patches:
                    left, bottom, width, height = p.get_bbox().bounds
                    ax.annotate(str(int(width)), xy=(left+width/2, bottom+height/2), 
                                ha='center', va='center', size = 3)
            
                # save image, display it, and delete after usage.
                plt.savefig('x',dpi=200)
                st.image('x.png')
                os.remove('x.png')
                st.plotly_chart(fig)

        else:
            st.markdown("No data found, try other extension, please.")
    elif opt=='Burrard Inlet Underwater Network':
        filters1 = {
            'locationCode': 'BIIP',
            'deviceCategoryCode': 'HYDROPHONE',
            }
        resultX = onc.getLocations(filters1)
        za = pd.DataFrame(resultX)
        st.markdown(za.description.values[0])


        df_dep = []
        for deployment in onc.getDeployments(filters={'locationCode': 'BIIP', 'deviceCategoryCode': 'HYDROPHONE'}):
            df_dep.append([deployment['locationCode'], deployment['begin'], deployment['end']])

        npl = np.array(df_dep)
        locationC = pd.DataFrame(npl[:,0])
        deplF = pd.DataFrame(npl[:,1])
        deplT = pd.DataFrame(npl[:,2])

        df_dep = pd.concat([locationC,deplF,deplT],axis=1)
        df_dep.columns=["Location Code", "Deployed from", "Deployed to"]


        st.write("There are {} deployments.".format(df_dep.shape[0]))
        df_dep["Deployed from"] = pd.to_datetime(df_dep["Deployed from"]).apply(lambda y: y.date())
        df_dep["Deployed to"] = pd.to_datetime(df_dep["Deployed to"]).apply(lambda y: y.date())
        fe = df_dep.style.hide_index()
        st.write(fe.to_html(), unsafe_allow_html=True)

        start_date = st.sidebar.date_input("Select Start Date")
        end_date = st.sidebar.date_input("Select End Date")

        e = datetime.strptime(str(start_date),"%Y-%m-%d")
        el =datetime.timestamp(e)
        elT = datetime.utcfromtimestamp(el).strftime("%Y-%m-%dT%H:%M:%S")+'.000Z'
        f = datetime.strptime(str(end_date),"%Y-%m-%d")
        fl =datetime.timestamp(f)
        flT = datetime.utcfromtimestamp(fl).strftime("%Y-%m-%dT%H:%M:%S")+'.000Z'


        df_dev = []
        for dev in onc.getDevices({
            'locationCode': 'BIIP',
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
                'locationCode': 'BIIP'
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
        result1 = onc.getListByDevice(filt, allPages=True)
        df = pd.DataFrame(result1)
        if len(df) > 0:
            st.markdown("There are {} files".format(len(df)) + ' from ' + filt['deviceCode'] 
                    + ' between '   + parse(filt['dateFrom']).strftime('%Y %b %d')
            + ' and ' + parse(filt['dateTo']).strftime('%Y %b %d'))
            with st.expander("Data:"):
                st.write(df)
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
                                    .strip('-spect').strip('-spect-small').strip('-LPF-spect').strip('-LPF-spect-thumb')
                                    .strip('-HPF-spect').strip('-HPF-spect-thumb').split('_')[1])   
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
            
                    
            option = st.selectbox(
                'How would you like to visualize the data availability:?',
                ('Line only', 'Bar only', 'Both'))
            
            if option == 'Line only':
                fig = px.scatter(df, x="files", y="UTC time",
                                 title='Data Availabiltiy Plot for {} of the entire deployment (Please enlarge the plot for better visualization)'.format(deviceZ),
                                 template='plotly_white'
                )
                fig.update_layout(yaxis=dict(title=''), xaxis=dict(title='', showgrid=False, gridcolor='grey',
                      tickvals=[],),hovermode="y unified")
                fig.update_traces(connectgaps=False,hovertemplate=None)


                st.plotly_chart(fig)

            elif option=='Bar only':
                df_dt = pd.to_datetime(df_dt)
                dm = df_dt.dt.strftime('%m-%d')
                dav = dm.value_counts().sort_index()


                fig1 = plt.figure(figsize = (4,2))

                ax = plt.axes()
                ax.barh(dav.index,dav,color=sns.color_palette("tab10"),align ='center')
                # Remove axes splines
                for s in ['top', 'bottom', 'left', 'right']:
                    ax.spines[s].set_visible(False)
                    # Remove x, y Ticks
                ax.xaxis.set_ticks_position('none')
                ax.yaxis.set_ticks_position('none')

                plt.yticks(fontsize=5)
                plt.ylabel("day",size = 4)

                ax.legend()        
 
                ax.get_xaxis().set_visible(False)

                ax.set_title('Data Available Per day',
                         loc ='left',fontsize=5 )
            # Add annotation to bars
                for p in ax.patches:
                    left, bottom, width, height = p.get_bbox().bounds
                    ax.annotate(str(int(width)), xy=(left+width/2, bottom+height/2), 
                                ha='center', va='center', size = 3)
            
                # save image, display it, and delete after usage.
                plt.savefig('x',dpi=200)
                st.image('x.png')
                os.remove('x.png')
                        
            else:
                fig = px.scatter(df, x="files", y="UTC time",
                                 title='Data Availabiltiy Plot for {} of the entire deployment (Please enlarge the plot for better visualization)'.format(deviceZ),
                                 template='plotly_white'
                )
                fig.update_layout(yaxis=dict(title=''), xaxis=dict(title='', showgrid=False, gridcolor='grey',
                      tickvals=[],),hovermode="y unified")
                fig.update_traces(connectgaps=False,hovertemplate=None)
                
                df_dt = pd.to_datetime(df_dt)
                dm = df_dt.dt.strftime('%m-%d')
                dav = dm.value_counts().sort_index()


                fig1 = plt.figure(figsize = (4,2))

                ax = plt.axes()
                ax.barh(dav.index,dav,color=sns.color_palette("tab10"),align ='center')
                # Remove axes splines
                for s in ['top', 'bottom', 'left', 'right']:
                    ax.spines[s].set_visible(False)
                    # Remove x, y Ticks
                ax.xaxis.set_ticks_position('none')
                ax.yaxis.set_ticks_position('none')

                plt.yticks(fontsize=5)
                plt.ylabel("day",size = 4)

                ax.legend()        
 
                ax.get_xaxis().set_visible(False)

                ax.set_title('Data Available Per day',
                         loc ='left',fontsize=5 )
            # Add annotation to bars
                for p in ax.patches:
                    left, bottom, width, height = p.get_bbox().bounds
                    ax.annotate(str(int(width)), xy=(left+width/2, bottom+height/2), 
                                ha='center', va='center', size = 3)
            
                # save image, display it, and delete after usage.
                plt.savefig('x',dpi=200)
                st.image('x.png')
                os.remove('x.png')
                st.plotly_chart(fig)

        else:
            st.markdown("No data found, try other extension, please.")
    elif opt=='Douglas Channel - Hartley Bay':
        filters1 = {
            'locationCode': 'HBIP',
            'deviceCategoryCode': 'HYDROPHONE',
            }
        resultX = onc.getLocations(filters1)
        za = pd.DataFrame(resultX)
        st.markdown(za.description.values[0])


        df_dep = []
        for deployment in onc.getDeployments(filters={'locationCode': 'HBIP', 'deviceCategoryCode': 'HYDROPHONE'}):
            df_dep.append([deployment['locationCode'], deployment['begin'], deployment['end']])

        npl = np.array(df_dep)
        locationC = pd.DataFrame(npl[:,0])
        deplF = pd.DataFrame(npl[:,1])
        deplT = pd.DataFrame(npl[:,2])

        df_dep = pd.concat([locationC,deplF,deplT],axis=1)
        df_dep.columns=["Location Code", "Deployed from", "Deployed to"]


        st.write("There are {} deployments.".format(df_dep.shape[0]))
        df_dep["Deployed from"] = pd.to_datetime(df_dep["Deployed from"]).apply(lambda y: y.date())
        df_dep["Deployed to"] = pd.to_datetime(df_dep["Deployed to"]).apply(lambda y: y.date())
        fe = df_dep.style.hide_index()
        st.write(fe.to_html(), unsafe_allow_html=True)

        start_date = st.sidebar.date_input("Select Start Date")
        end_date = st.sidebar.date_input("Select End Date")

        e = datetime.strptime(str(start_date),"%Y-%m-%d")
        el =datetime.timestamp(e)
        elT = datetime.utcfromtimestamp(el).strftime("%Y-%m-%dT%H:%M:%S")+'.000Z'
        f = datetime.strptime(str(end_date),"%Y-%m-%d")
        fl =datetime.timestamp(f)
        flT = datetime.utcfromtimestamp(fl).strftime("%Y-%m-%dT%H:%M:%S")+'.000Z'


        df_dev = []
        for dev in onc.getDevices({
            'locationCode': 'HBIP',
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
                'locationCode': 'HBIP'
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
        result1 = onc.getListByDevice(filt, allPages=True)
        df = pd.DataFrame(result1)
        if len(df) > 0:
            st.markdown("There are {} files".format(len(df)) + ' from ' + filt['deviceCode'] 
                    + ' between '   + parse(filt['dateFrom']).strftime('%Y %b %d')
            + ' and ' + parse(filt['dateTo']).strftime('%Y %b %d'))
            with st.expander("Data:"):
                st.write(df)
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
                                    .strip('-spect').strip('-spect-small').strip('-LPF-spect').strip('-LPF-spect-thumb')
                                    .strip('-HPF-spect').strip('-HPF-spect-thumb').split('_')[1])   
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
            
                    
            option = st.selectbox(
                'How would you like to visualize the data availability:?',
                ('Line only', 'Bar only', 'Both'))
            
            if option == 'Line only':
                fig = px.scatter(df, x="files", y="UTC time",
                                 title='Data Availabiltiy Plot for {} of the entire deployment (Please enlarge the plot for better visualization)'.format(deviceZ),
                                 template='plotly_white'
                )
                fig.update_layout(yaxis=dict(title=''), xaxis=dict(title='', showgrid=False, gridcolor='grey',
                      tickvals=[],),hovermode="y unified")
                fig.update_traces(connectgaps=False,hovertemplate=None)


                st.plotly_chart(fig)

            elif option=='Bar only':
                df_dt = pd.to_datetime(df_dt)
                dm = df_dt.dt.strftime('%m-%d')
                dav = dm.value_counts().sort_index()


                fig1 = plt.figure(figsize = (4,2))

                ax = plt.axes()
                ax.barh(dav.index,dav,color=sns.color_palette("tab10"),align ='center')
                # Remove axes splines
                for s in ['top', 'bottom', 'left', 'right']:
                    ax.spines[s].set_visible(False)
                    # Remove x, y Ticks
                ax.xaxis.set_ticks_position('none')
                ax.yaxis.set_ticks_position('none')

                plt.yticks(fontsize=5)
                plt.ylabel("day",size = 4)

                ax.legend()        
 
                ax.get_xaxis().set_visible(False)

                ax.set_title('Data Available Per day',
                         loc ='left',fontsize=5 )
            # Add annotation to bars
                for p in ax.patches:
                    left, bottom, width, height = p.get_bbox().bounds
                    ax.annotate(str(int(width)), xy=(left+width/2, bottom+height/2), 
                                ha='center', va='center', size = 3)
            
                # save image, display it, and delete after usage.
                plt.savefig('x',dpi=200)
                st.image('x.png')
                os.remove('x.png')
                        
            else:
                fig = px.scatter(df, x="files", y="UTC time",
                                 title='Data Availabiltiy Plot for {} of the entire deployment (Please enlarge the plot for better visualization)'.format(deviceZ),
                                 template='plotly_white'
                )
                fig.update_layout(yaxis=dict(title=''), xaxis=dict(title='', showgrid=False, gridcolor='grey',
                      tickvals=[],),hovermode="y unified")
                fig.update_traces(connectgaps=False,hovertemplate=None)
                
                df_dt = pd.to_datetime(df_dt)
                dm = df_dt.dt.strftime('%m-%d')
                dav = dm.value_counts().sort_index()


                fig1 = plt.figure(figsize = (4,2))

                ax = plt.axes()
                ax.barh(dav.index,dav,color=sns.color_palette("tab10"),align ='center')
                # Remove axes splines
                for s in ['top', 'bottom', 'left', 'right']:
                    ax.spines[s].set_visible(False)
                    # Remove x, y Ticks
                ax.xaxis.set_ticks_position('none')
                ax.yaxis.set_ticks_position('none')

                plt.yticks(fontsize=5)
                plt.ylabel("day",size = 4)

                ax.legend()        
 
                ax.get_xaxis().set_visible(False)

                ax.set_title('Data Available Per day',
                         loc ='left',fontsize=5 )
            # Add annotation to bars
                for p in ax.patches:
                    left, bottom, width, height = p.get_bbox().bounds
                    ax.annotate(str(int(width)), xy=(left+width/2, bottom+height/2), 
                                ha='center', va='center', size = 3)
            
                # save image, display it, and delete after usage.
                plt.savefig('x',dpi=200)
                st.image('x.png')
                os.remove('x.png')
                st.plotly_chart(fig)

        else:
            st.markdown("No data found, try other extension, please.")   
    elif opt=='Conception Bay - Holyrood Bay Underwater Network':
        filters1 = {
            'locationCode': 'HRBIP',
            'deviceCategoryCode': 'HYDROPHONE',
            }
        resultX = onc.getLocations(filters1)
        za = pd.DataFrame(resultX)
        st.markdown(za.description.values[0])


        df_dep = []
        for deployment in onc.getDeployments(filters={'locationCode': 'HRBIP', 'deviceCategoryCode': 'HYDROPHONE'}):
            df_dep.append([deployment['locationCode'], deployment['begin'], deployment['end']])

        npl = np.array(df_dep)
        locationC = pd.DataFrame(npl[:,0])
        deplF = pd.DataFrame(npl[:,1])
        deplT = pd.DataFrame(npl[:,2])

        df_dep = pd.concat([locationC,deplF,deplT],axis=1)
        df_dep.columns=["Location Code", "Deployed from", "Deployed to"]


        st.write("There are {} deployments.".format(df_dep.shape[0]))
        df_dep["Deployed from"] = pd.to_datetime(df_dep["Deployed from"]).apply(lambda y: y.date())
        df_dep["Deployed to"] = pd.to_datetime(df_dep["Deployed to"]).apply(lambda y: y.date())
        fe = df_dep.style.hide_index()
        st.write(fe.to_html(), unsafe_allow_html=True)

        start_date = st.sidebar.date_input("Select Start Date")
        end_date = st.sidebar.date_input("Select End Date")

        e = datetime.strptime(str(start_date),"%Y-%m-%d")
        el =datetime.timestamp(e)
        elT = datetime.utcfromtimestamp(el).strftime("%Y-%m-%dT%H:%M:%S")+'.000Z'
        f = datetime.strptime(str(end_date),"%Y-%m-%d")
        fl =datetime.timestamp(f)
        flT = datetime.utcfromtimestamp(fl).strftime("%Y-%m-%dT%H:%M:%S")+'.000Z'


        df_dev = []
        for dev in onc.getDevices({
            'locationCode': 'HRBIP',
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
                'locationCode': 'HRBIP'
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
        result1 = onc.getListByDevice(filt, allPages=True)
        df = pd.DataFrame(result1)
        if len(df) > 0:
            st.markdown("There are {} files".format(len(df)) + ' from ' + filt['deviceCode'] 
                    + ' between '   + parse(filt['dateFrom']).strftime('%Y %b %d')
            + ' and ' + parse(filt['dateTo']).strftime('%Y %b %d'))
            with st.expander("Data:"):
                st.write(df)
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
                                    .strip('-spect').strip('-spect-small').strip('-LPF-spect').strip('-LPF-spect-thumb')
                                    .strip('-HPF-spect').strip('-HPF-spect-thumb').split('_')[1])   
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
            
                    
            option = st.selectbox(
                'How would you like to visualize the data availability:?',
                ('Line only', 'Bar only', 'Both'))
            
            if option == 'Line only':
                fig = px.scatter(df, x="files", y="UTC time",
                                 title='Data Availabiltiy Plot for {} of the entire deployment (Please enlarge the plot for better visualization)'.format(deviceZ),
                                 template='plotly_white'
                )
                fig.update_layout(yaxis=dict(title=''), xaxis=dict(title='', showgrid=False, gridcolor='grey',
                      tickvals=[],),hovermode="y unified")
                fig.update_traces(connectgaps=False,hovertemplate=None)


                st.plotly_chart(fig)

            elif option=='Bar only':
                df_dt = pd.to_datetime(df_dt)
                dm = df_dt.dt.strftime('%m-%d')
                dav = dm.value_counts().sort_index()


                fig1 = plt.figure(figsize = (4,2))

                ax = plt.axes()
                ax.barh(dav.index,dav,color=sns.color_palette("tab10"),align ='center')
                # Remove axes splines
                for s in ['top', 'bottom', 'left', 'right']:
                    ax.spines[s].set_visible(False)
                    # Remove x, y Ticks
                ax.xaxis.set_ticks_position('none')
                ax.yaxis.set_ticks_position('none')

                plt.yticks(fontsize=5)
                plt.ylabel("day",size = 4)

                ax.legend()        
 
                ax.get_xaxis().set_visible(False)

                ax.set_title('Data Available Per day',
                         loc ='left',fontsize=5 )
            # Add annotation to bars
                for p in ax.patches:
                    left, bottom, width, height = p.get_bbox().bounds
                    ax.annotate(str(int(width)), xy=(left+width/2, bottom+height/2), 
                                ha='center', va='center', size = 3)
            
                # save image, display it, and delete after usage.
                plt.savefig('x',dpi=200)
                st.image('x.png')
                os.remove('x.png')
                        
            else:
                fig = px.scatter(df, x="files", y="UTC time",
                                 title='Data Availabiltiy Plot for {} of the entire deployment (Please enlarge the plot for better visualization)'.format(deviceZ),
                                 template='plotly_white'
                )
                fig.update_layout(yaxis=dict(title=''), xaxis=dict(title='', showgrid=False, gridcolor='grey',
                      tickvals=[],),hovermode="y unified")
                fig.update_traces(connectgaps=False,hovertemplate=None)
                
                df_dt = pd.to_datetime(df_dt)
                dm = df_dt.dt.strftime('%m-%d')
                dav = dm.value_counts().sort_index()


                fig1 = plt.figure(figsize = (4,2))

                ax = plt.axes()
                ax.barh(dav.index,dav,color=sns.color_palette("tab10"),align ='center')
                # Remove axes splines
                for s in ['top', 'bottom', 'left', 'right']:
                    ax.spines[s].set_visible(False)
                    # Remove x, y Ticks
                ax.xaxis.set_ticks_position('none')
                ax.yaxis.set_ticks_position('none')

                plt.yticks(fontsize=5)
                plt.ylabel("day",size = 4)

                ax.legend()        
 
                ax.get_xaxis().set_visible(False)

                ax.set_title('Data Available Per day',
                         loc ='left',fontsize=5 )
            # Add annotation to bars
                for p in ax.patches:
                    left, bottom, width, height = p.get_bbox().bounds
                    ax.annotate(str(int(width)), xy=(left+width/2, bottom+height/2), 
                                ha='center', va='center', size = 3)
            
                # save image, display it, and delete after usage.
                plt.savefig('x',dpi=200)
                st.image('x.png')
                os.remove('x.png')
                st.plotly_chart(fig)

        else:
            st.markdown("No data found, try other extension, please.")
    elif opt=='Cambridge Bay':
        filters1 = {
            'locationCode': 'CBYIP',
            'deviceCategoryCode': 'HYDROPHONE',
            }
        resultX = onc.getLocations(filters1)
        za = pd.DataFrame(resultX)
        st.markdown(za.description.values[0])


        df_dep = []
        for deployment in onc.getDeployments(filters={'locationCode': 'CBYIP', 'deviceCategoryCode': 'HYDROPHONE'}):
            df_dep.append([deployment['locationCode'], deployment['begin'], deployment['end']])

        npl = np.array(df_dep)
        locationC = pd.DataFrame(npl[:,0])
        deplF = pd.DataFrame(npl[:,1])
        deplT = pd.DataFrame(npl[:,2])

        df_dep = pd.concat([locationC,deplF,deplT],axis=1)
        df_dep.columns=["Location Code", "Deployed from", "Deployed to"]


        st.write("There are {} deployments.".format(df_dep.shape[0]))
        df_dep["Deployed from"] = pd.to_datetime(df_dep["Deployed from"]).apply(lambda y: y.date())
        df_dep["Deployed to"] = pd.to_datetime(df_dep["Deployed to"]).apply(lambda y: y.date())
        fe = df_dep.style.hide_index()
        st.write(fe.to_html(), unsafe_allow_html=True)

        start_date = st.sidebar.date_input("Select Start Date")
        end_date = st.sidebar.date_input("Select End Date")

        e = datetime.strptime(str(start_date),"%Y-%m-%d")
        el =datetime.timestamp(e)
        elT = datetime.utcfromtimestamp(el).strftime("%Y-%m-%dT%H:%M:%S")+'.000Z'
        f = datetime.strptime(str(end_date),"%Y-%m-%d")
        fl =datetime.timestamp(f)
        flT = datetime.utcfromtimestamp(fl).strftime("%Y-%m-%dT%H:%M:%S")+'.000Z'


        df_dev = []
        for dev in onc.getDevices({
            'locationCode': 'CBYIP',
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
                'locationCode': 'CBYIP'
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
        result1 = onc.getListByDevice(filt, allPages=True)
        df = pd.DataFrame(result1)
        if len(df) > 0:
            st.markdown("There are {} files".format(len(df)) + ' from ' + filt['deviceCode'] 
                    + ' between '   + parse(filt['dateFrom']).strftime('%Y %b %d')
            + ' and ' + parse(filt['dateTo']).strftime('%Y %b %d'))
            with st.expander("Data:"):
                st.write(df)
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
                                    .strip('-spect').strip('-spect-small').strip('-LPF-spect').strip('-LPF-spect-thumb')
                                    .strip('-HPF-spect').strip('-HPF-spect-thumb').split('_')[1])   
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
            
                    
            option = st.selectbox(
                'How would you like to visualize the data availability:?',
                ('Line only', 'Bar only', 'Both'))
            
            if option == 'Line only':
                fig = px.scatter(df, x="files", y="UTC time",
                                 title='Data Availabiltiy Plot for {} of the entire deployment (Please enlarge the plot for better visualization)'.format(deviceZ),
                                 template='plotly_white'
                )
                fig.update_layout(yaxis=dict(title=''), xaxis=dict(title='', showgrid=False, gridcolor='grey',
                      tickvals=[],),hovermode="y unified")
                fig.update_traces(connectgaps=False,hovertemplate=None)


                st.plotly_chart(fig)

            elif option=='Bar only':
                df_dt = pd.to_datetime(df_dt)
                dm = df_dt.dt.strftime('%m-%d')
                dav = dm.value_counts().sort_index()


                fig1 = plt.figure(figsize = (4,2))

                ax = plt.axes()
                ax.barh(dav.index,dav,color=sns.color_palette("tab10"),align ='center')
                # Remove axes splines
                for s in ['top', 'bottom', 'left', 'right']:
                    ax.spines[s].set_visible(False)
                    # Remove x, y Ticks
                ax.xaxis.set_ticks_position('none')
                ax.yaxis.set_ticks_position('none')

                plt.yticks(fontsize=5)
                plt.ylabel("day",size = 4)

                ax.legend()        
 
                ax.get_xaxis().set_visible(False)

                ax.set_title('Data Available Per day',
                         loc ='left',fontsize=5 )
            # Add annotation to bars
                for p in ax.patches:
                    left, bottom, width, height = p.get_bbox().bounds
                    ax.annotate(str(int(width)), xy=(left+width/2, bottom+height/2), 
                                ha='center', va='center', size = 3)
            
                # save image, display it, and delete after usage.
                plt.savefig('x',dpi=200)
                st.image('x.png')
                os.remove('x.png')
                        
            else:
                fig = px.scatter(df, x="files", y="UTC time",
                                 title='Data Availabiltiy Plot for {} of the entire deployment (Please enlarge the plot for better visualization)'.format(deviceZ),
                                 template='plotly_white'
                )
                fig.update_layout(yaxis=dict(title=''), xaxis=dict(title='', showgrid=False, gridcolor='grey',
                      tickvals=[],),hovermode="y unified")
                fig.update_traces(connectgaps=False,hovertemplate=None)
                
                df_dt = pd.to_datetime(df_dt)
                dm = df_dt.dt.strftime('%m-%d')
                dav = dm.value_counts().sort_index()


                fig1 = plt.figure(figsize = (4,2))

                ax = plt.axes()
                ax.barh(dav.index,dav,color=sns.color_palette("tab10"),align ='center')
                # Remove axes splines
                for s in ['top', 'bottom', 'left', 'right']:
                    ax.spines[s].set_visible(False)
                    # Remove x, y Ticks
                ax.xaxis.set_ticks_position('none')
                ax.yaxis.set_ticks_position('none')

                plt.yticks(fontsize=5)
                plt.ylabel("day",size = 4)

                ax.legend()        
 
                ax.get_xaxis().set_visible(False)

                ax.set_title('Data Available Per day',
                         loc ='left',fontsize=5 )
            # Add annotation to bars
                for p in ax.patches:
                    left, bottom, width, height = p.get_bbox().bounds
                    ax.annotate(str(int(width)), xy=(left+width/2, bottom+height/2), 
                                ha='center', va='center', size = 3)
            
                # save image, display it, and delete after usage.
                plt.savefig('x',dpi=200)
                st.image('x.png')
                os.remove('x.png')
                st.plotly_chart(fig)

        else:
            st.markdown("No data found, try other extension, please.")
    elif opt=='Chatham Sound - Digby Island':
        filters1 = {
            'locationCode': 'DIIP',
            'deviceCategoryCode': 'HYDROPHONE',
            }
        resultX = onc.getLocations(filters1)
        za = pd.DataFrame(resultX)
        st.markdown(za.description.values[0])


        df_dep = []
        for deployment in onc.getDeployments(filters={'locationCode': 'DIIP', 'deviceCategoryCode': 'HYDROPHONE'}):
            df_dep.append([deployment['locationCode'], deployment['begin'], deployment['end']])

        npl = np.array(df_dep)
        locationC = pd.DataFrame(npl[:,0])
        deplF = pd.DataFrame(npl[:,1])
        deplT = pd.DataFrame(npl[:,2])

        df_dep = pd.concat([locationC,deplF,deplT],axis=1)
        df_dep.columns=["Location Code", "Deployed from", "Deployed to"]


        st.write("There are {} deployments.".format(df_dep.shape[0]))
        df_dep["Deployed from"] = pd.to_datetime(df_dep["Deployed from"]).apply(lambda y: y.date())
        df_dep["Deployed to"] = pd.to_datetime(df_dep["Deployed to"]).apply(lambda y: y.date())
        fe = df_dep.style.hide_index()
        st.write(fe.to_html(), unsafe_allow_html=True)

        start_date = st.sidebar.date_input("Select Start Date")
        end_date = st.sidebar.date_input("Select End Date")

        e = datetime.strptime(str(start_date),"%Y-%m-%d")
        el =datetime.timestamp(e)
        elT = datetime.utcfromtimestamp(el).strftime("%Y-%m-%dT%H:%M:%S")+'.000Z'
        f = datetime.strptime(str(end_date),"%Y-%m-%d")
        fl =datetime.timestamp(f)
        flT = datetime.utcfromtimestamp(fl).strftime("%Y-%m-%dT%H:%M:%S")+'.000Z'


        df_dev = []
        for dev in onc.getDevices({
            'locationCode': 'DIIP',
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
                'locationCode': 'DIIP'
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
        result1 = onc.getListByDevice(filt, allPages=True)
        df = pd.DataFrame(result1)
        if len(df) > 0:
            st.markdown("There are {} files".format(len(df)) + ' from ' + filt['deviceCode'] 
                    + ' between '   + parse(filt['dateFrom']).strftime('%Y %b %d')
            + ' and ' + parse(filt['dateTo']).strftime('%Y %b %d'))
            with st.expander("Data:"):
                st.write(df)
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
                                    .strip('-spect').strip('-spect-small').strip('-LPF-spect').strip('-LPF-spect-thumb')
                                    .strip('-HPF-spect').strip('-HPF-spect-thumb').split('_')[1])   
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
            
                    
            option = st.selectbox(
                'How would you like to visualize the data availability:?',
                ('Line only', 'Bar only', 'Both'))
            
            if option == 'Line only':
                fig = px.scatter(df, x="files", y="UTC time",
                                 title='Data Availabiltiy Plot for {} of the entire deployment (Please enlarge the plot for better visualization)'.format(deviceZ),
                                 template='plotly_white'
                )
                fig.update_layout(yaxis=dict(title=''), xaxis=dict(title='', showgrid=False, gridcolor='grey',
                      tickvals=[],),hovermode="y unified")
                fig.update_traces(connectgaps=False,hovertemplate=None)


                st.plotly_chart(fig)

            elif option=='Bar only':
                df_dt = pd.to_datetime(df_dt)
                dm = df_dt.dt.strftime('%m-%d')
                dav = dm.value_counts().sort_index()


                fig1 = plt.figure(figsize = (4,2))

                ax = plt.axes()
                ax.barh(dav.index,dav,color=sns.color_palette("tab10"),align ='center')
                # Remove axes splines
                for s in ['top', 'bottom', 'left', 'right']:
                    ax.spines[s].set_visible(False)
                    # Remove x, y Ticks
                ax.xaxis.set_ticks_position('none')
                ax.yaxis.set_ticks_position('none')

                plt.yticks(fontsize=5)
                plt.ylabel("day",size = 4)

                ax.legend()        
 
                ax.get_xaxis().set_visible(False)

                ax.set_title('Data Available Per day',
                         loc ='left',fontsize=5 )
            # Add annotation to bars
                for p in ax.patches:
                    left, bottom, width, height = p.get_bbox().bounds
                    ax.annotate(str(int(width)), xy=(left+width/2, bottom+height/2), 
                                ha='center', va='center', size = 3)
            
                # save image, display it, and delete after usage.
                plt.savefig('x',dpi=200)
                st.image('x.png')
                os.remove('x.png')
                        
            else:
                fig = px.scatter(df, x="files", y="UTC time",
                                 title='Data Availabiltiy Plot for {} of the entire deployment (Please enlarge the plot for better visualization)'.format(deviceZ),
                                 template='plotly_white'
                )
                fig.update_layout(yaxis=dict(title=''), xaxis=dict(title='', showgrid=False, gridcolor='grey',
                      tickvals=[],),hovermode="y unified")
                fig.update_traces(connectgaps=False,hovertemplate=None)
                
                df_dt = pd.to_datetime(df_dt)
                dm = df_dt.dt.strftime('%m-%d')
                dav = dm.value_counts().sort_index()


                fig1 = plt.figure(figsize = (4,2))

                ax = plt.axes()
                ax.barh(dav.index,dav,color=sns.color_palette("tab10"),align ='center')
                # Remove axes splines
                for s in ['top', 'bottom', 'left', 'right']:
                    ax.spines[s].set_visible(False)
                    # Remove x, y Ticks
                ax.xaxis.set_ticks_position('none')
                ax.yaxis.set_ticks_position('none')

                plt.yticks(fontsize=5)
                plt.ylabel("day",size = 4)

                ax.legend()        
 
                ax.get_xaxis().set_visible(False)

                ax.set_title('Data Available Per day',
                         loc ='left',fontsize=5 )
            # Add annotation to bars
                for p in ax.patches:
                    left, bottom, width, height = p.get_bbox().bounds
                    ax.annotate(str(int(width)), xy=(left+width/2, bottom+height/2), 
                                ha='center', va='center', size = 3)
            
                # save image, display it, and delete after usage.
                plt.savefig('x',dpi=200)
                st.image('x.png')
                os.remove('x.png')
                st.plotly_chart(fig)

        else:
            st.markdown("No data found, try other extension, please.")
    elif opt=='Douglas Channel - Kitamaat Village':
        filters1 = {
            'locationCode': 'KVIP',
            'deviceCategoryCode': 'HYDROPHONE',
            }
        resultX = onc.getLocations(filters1)
        za = pd.DataFrame(resultX)
        st.markdown(za.description.values[0])


        df_dep = []
        for deployment in onc.getDeployments(filters={'locationCode': 'KVIP', 'deviceCategoryCode': 'HYDROPHONE'}):
            df_dep.append([deployment['locationCode'], deployment['begin'], deployment['end']])

        npl = np.array(df_dep)
        locationC = pd.DataFrame(npl[:,0])
        deplF = pd.DataFrame(npl[:,1])
        deplT = pd.DataFrame(npl[:,2])

        df_dep = pd.concat([locationC,deplF,deplT],axis=1)
        df_dep.columns=["Location Code", "Deployed from", "Deployed to"]


        st.write("There are {} deployments.".format(df_dep.shape[0]))
        df_dep["Deployed from"] = pd.to_datetime(df_dep["Deployed from"]).apply(lambda y: y.date())
        df_dep["Deployed to"] = pd.to_datetime(df_dep["Deployed to"]).apply(lambda y: y.date())
        fe = df_dep.style.hide_index()
        st.write(fe.to_html(), unsafe_allow_html=True)

        start_date = st.sidebar.date_input("Select Start Date")
        end_date = st.sidebar.date_input("Select End Date")

        e = datetime.strptime(str(start_date),"%Y-%m-%d")
        el =datetime.timestamp(e)
        elT = datetime.utcfromtimestamp(el).strftime("%Y-%m-%dT%H:%M:%S")+'.000Z'
        f = datetime.strptime(str(end_date),"%Y-%m-%d")
        fl =datetime.timestamp(f)
        flT = datetime.utcfromtimestamp(fl).strftime("%Y-%m-%dT%H:%M:%S")+'.000Z'


        df_dev = []
        for dev in onc.getDevices({
            'locationCode': 'KVIP',
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
                'locationCode': 'KVIP'
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
        result1 = onc.getListByDevice(filt, allPages=True)
        df = pd.DataFrame(result1)
        if len(df) > 0:
            st.markdown("There are {} files".format(len(df)) + ' from ' + filt['deviceCode'] 
                    + ' between '   + parse(filt['dateFrom']).strftime('%Y %b %d')
            + ' and ' + parse(filt['dateTo']).strftime('%Y %b %d'))
            with st.expander("Data:"):
                st.write(df)
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
                                    .strip('-spect').strip('-spect-small').strip('-LPF-spect').strip('-LPF-spect-thumb')
                                    .strip('-HPF-spect').strip('-HPF-spect-thumb').split('_')[1])   
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
            
                    
            option = st.selectbox(
                'How would you like to visualize the data availability:?',
                ('Line only', 'Bar only', 'Both'))
            
            if option == 'Line only':
                fig = px.scatter(df, x="files", y="UTC time",
                                 title='Data Availabiltiy Plot for {} of the entire deployment (Please enlarge the plot for better visualization)'.format(deviceZ),
                                 template='plotly_white'
                )
                fig.update_layout(yaxis=dict(title=''), xaxis=dict(title='', showgrid=False, gridcolor='grey',
                      tickvals=[],),hovermode="y unified")
                fig.update_traces(connectgaps=False,hovertemplate=None)


                st.plotly_chart(fig)

            elif option=='Bar only':
                df_dt = pd.to_datetime(df_dt)
                dm = df_dt.dt.strftime('%m-%d')
                dav = dm.value_counts().sort_index()


                fig1 = plt.figure(figsize = (4,2))

                ax = plt.axes()
                ax.barh(dav.index,dav,color=sns.color_palette("tab10"),align ='center')
                # Remove axes splines
                for s in ['top', 'bottom', 'left', 'right']:
                    ax.spines[s].set_visible(False)
                    # Remove x, y Ticks
                ax.xaxis.set_ticks_position('none')
                ax.yaxis.set_ticks_position('none')

                plt.yticks(fontsize=5)
                plt.ylabel("day",size = 4)

                ax.legend()        
 
                ax.get_xaxis().set_visible(False)

                ax.set_title('Data Available Per day',
                         loc ='left',fontsize=5 )
            # Add annotation to bars
                for p in ax.patches:
                    left, bottom, width, height = p.get_bbox().bounds
                    ax.annotate(str(int(width)), xy=(left+width/2, bottom+height/2), 
                                ha='center', va='center', size = 3)
            
                # save image, display it, and delete after usage.
                plt.savefig('x',dpi=200)
                st.image('x.png')
                os.remove('x.png')
                        
            else:
                fig = px.scatter(df, x="files", y="UTC time",
                                 title='Data Availabiltiy Plot for {} of the entire deployment (Please enlarge the plot for better visualization)'.format(deviceZ),
                                 template='plotly_white'
                )
                fig.update_layout(yaxis=dict(title=''), xaxis=dict(title='', showgrid=False, gridcolor='grey',
                      tickvals=[],),hovermode="y unified")
                fig.update_traces(connectgaps=False,hovertemplate=None)
                
                df_dt = pd.to_datetime(df_dt)
                dm = df_dt.dt.strftime('%m-%d')
                dav = dm.value_counts().sort_index()


                fig1 = plt.figure(figsize = (4,2))

                ax = plt.axes()
                ax.barh(dav.index,dav,color=sns.color_palette("tab10"),align ='center')
                # Remove axes splines
                for s in ['top', 'bottom', 'left', 'right']:
                    ax.spines[s].set_visible(False)
                    # Remove x, y Ticks
                ax.xaxis.set_ticks_position('none')
                ax.yaxis.set_ticks_position('none')

                plt.yticks(fontsize=5)
                plt.ylabel("day",size = 4)

                ax.legend()        
 
                ax.get_xaxis().set_visible(False)

                ax.set_title('Data Available Per day',
                         loc ='left',fontsize=5 )
            # Add annotation to bars
                for p in ax.patches:
                    left, bottom, width, height = p.get_bbox().bounds
                    ax.annotate(str(int(width)), xy=(left+width/2, bottom+height/2), 
                                ha='center', va='center', size = 3)
            
                # save image, display it, and delete after usage.
                plt.savefig('x',dpi=200)
                st.image('x.png')
                os.remove('x.png')
                st.plotly_chart(fig)

        else:
            st.markdown("No data found, try other extension, please.")
else:
    st.error("Get a token  from  https://data.oceannetworks.ca/Profile")
