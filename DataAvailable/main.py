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

st.set_page_config(layout='centered')

st.cache(suppress_st_warning=True)

#Create a new environment with the latest version of python:

#   `conda create -n streamlit python=3.10`
im = 'DataAvailable/image/onc_dataTeam_logo.png'



#Create a new environment with the latest version of python:

#im = 'DataAvailable/image/onc_dataTeam_logo.png'
st.sidebar.image(im,use_column_width=True)
st.get_option("theme.primaryColor")
st.get_option("theme.textColor")
# Remove whitespace from the top of the page and sidebar
st.markdown("""
        <style>
               .css-18e3th9 {
                    padding-top: 0rem;
                    padding-bottom: 10rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
               .css-1d391kg {
                    padding-top: 3.5rem;
                    padding-right: 1rem;
                    padding-bottom: 3.5rem;
                    padding-left: 1rem;
                }
        </style>
        """, unsafe_allow_html=True)
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


    col1, col2,_,_ = st.columns([3,1,2,1])

    with col2:
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
            col2.plotly_chart(fig0) 
    
    with col1:

        df_hy = []
        for location in onc.getLocations({'deviceCategoryCode': 'HYDROPHONE'}):
            df_hy.append(location['locationCode'])
    
        df_hy = pd.DataFrame({'Location code':df_hy})

        hyl = df_hy['Location code'].unique()

        deviceL = st.sidebar.selectbox("Select location:",hyl)


    
        filters1 = {
            'locationCode': deviceL,
            'deviceCategoryCode': 'HYDROPHONE',
            }
        resultX = onc.getLocations(filters1)
        za = pd.DataFrame(resultX)
        col1.markdown(za.description.values[0])


        df_dep = []
        for deployment in onc.getDeployments(filters={'locationCode': deviceL, 'deviceCategoryCode': 'HYDROPHONE'}):
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
        result1 = onc.getListByDevice(filt, allPages=True)
        df = pd.DataFrame(result1)
        if len(df) > 0:
            col1.markdown("There are {} files".format(len(df)) + ' from ' + filt['deviceCode'] 
                    + ' between '   + parse(filt['dateFrom']).strftime('%Y %b %d')
            + ' and ' + parse(filt['dateTo']).strftime('%Y %b %d'))
            with st.expander("Data:"):
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
                    df_dt =  df.files.apply(lambda x: x.strip('.mat').strip('-spect-small')
                                    .strip('-FFT-spect').strip('-FFT-spect-thumb').strip('FFT-spect-small').strip('-spect-thumb')
                                    .strip('-spect').strip('-spect-small')
                                    .strip('-HPF-spect').strip('-HPF-spect-thumb').split('_')[3])   
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

                fig1, ax = plt.subplots(figsize=(20, 15))

                ax.barh(dav.index,dav,color=sns.color_palette("tab10"),align ='center')
                # Remove axes splines
                for s in ['top', 'bottom', 'left', 'right']:
                    ax.spines[s].set_visible(False)
                    # Remove x, y Ticks
                ax.xaxis.set_ticks_position('none')
                ax.yaxis.set_ticks_position('none')

                plt.yticks(fontsize=30)
                plt.ylabel("day",size = 40)

                ax.legend()
                # Add x, y gridlines
                ax.grid(b = True, color ='grey',
                        linestyle ='-.', linewidth = 0.5,
                        alpha = 0.2)
 
                ax.get_xaxis().set_visible(False)

                ax.set_title('Data Available Per day',
                         loc ='left',fontsize=60 )
            # Add annotation to bars
                for p in ax.patches:
                    left, bottom, width, height = p.get_bbox().bounds
                    ax.annotate(str(int(width)), xy=(left+width/2, bottom+height/2), 
                                ha='center', va='center', size = 42)
                        
                st.pyplot(fig1)
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

                fig1, ax = plt.subplots(figsize=(20, 15))

                ax.barh(dav.index,dav,color=sns.color_palette("tab10"),align ='center')
                # Remove axes splines
                for s in ['top', 'bottom', 'left', 'right']:
                    ax.spines[s].set_visible(False)
                    # Remove x, y Ticks
                ax.xaxis.set_ticks_position('none')
                ax.yaxis.set_ticks_position('none')

                plt.yticks(fontsize=30)
                plt.ylabel("day",size = 40)

                ax.legend()
                # Add x, y gridlines
                ax.grid(b = True, color ='grey',
                        linestyle ='-.', linewidth = 0.5,
                        alpha = 0.2)
 
                ax.get_xaxis().set_visible(False)

                ax.set_title('Data Available Per day',
                         loc ='left',fontsize=60 )
            # Add annotation to bars
                for p in ax.patches:
                    left, bottom, width, height = p.get_bbox().bounds
                    ax.annotate(str(int(width)), xy=(left+width/2, bottom+height/2), 
                                ha='center', va='center', size = 42)
                
                st.plotly_chart(fig)
                st.pyplot(fig1)


        else:
            st.markdown("No data found, try other extension, please.")
else:
    st.error("Get a token  from  https://data.oceannetworks.ca/Profile")
