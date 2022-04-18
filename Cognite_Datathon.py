#!/usr/bin/env python
# coding: utf-8
# In[1]:
import pandas as pd
import numpy as np 
import streamlit as st
import plotly.express as px
# In[3]:
urlI = 'https://www.ndbc.noaa.gov/data/realtime2/KIKT.txt'
urlB = 'https://www.ndbc.noaa.gov/data/realtime2/KBQX.txt'
urlM = 'https://www.ndbc.noaa.gov/data/realtime2/KMIS.txt'
kikt = pd.read_csv(urlI, skiprows=[1], sep='\s+')
kapt = pd.read_csv(urlB, skiprows=[1], sep='\s+')
kmis = pd.read_csv(urlM, skiprows=[1], sep='\s+')
# In[4]:
# function for preprocessing 
def preproc_data(df):
    df = df.rename(columns={"#YY": "YR"})
    df['datetime'] = pd.to_datetime(df.YR.astype(str) + '-' + df.MM.astype(str) + '-' + df.DD.astype(str)                          + ' ' + df.hh.astype(str) + ':' + df.mm.astype(str))
    newdf = df[['datetime', 'WDIR', 'WSPD', 'GST', 'ATMP', 'DEWP', 'VIS']].sort_values(by=['datetime'])
    return newdf 
# In[5]:
# preprocessing all the dataframes 
kikt = preproc_data(kikt)
kapt = preproc_data(kapt)
kmis = preproc_data(kmis)
units = np.array(['datetime', 'degT', 'm/s', 'm/s', 'degC', 'degC', 'nmi'])  #units for the remaining columns 
# In[6]:
# function to interpolate where columns have MM
def interp_MM(df, column):
    dt = df['datetime'].to_numpy().astype(float)
    dt = (dt - np.min(dt))/(np.max(dt)-np.min(dt))
    x = dt[df[column] == 'MM']
    xp = dt[df[column] != 'MM']
    yp = df.loc[df[column]!= 'MM', column].to_numpy().astype(float)
    testing = np.interp(x, xp, yp) 
    
    df.loc[(df[column] == 'MM'), column] =  testing
    df[column] = df[column].astype(float)
    return df
# In[7]:
for i in kikt.columns[1:]:
    kikt = interp_MM(kikt, i)
    kapt = interp_MM(kapt, i)
    kmis = interp_MM(kmis, i)
# In[2]: Create dashboard
def pull_data(df):
    st.dataframe(df)
    return df
 
# In[3]:
## Source: https://share.streamlit.io/jkanner/streamlit-dataview/master/app.py/+/
st.sidebar.markdown("## Select Weather Station")
select_event = st.sidebar.selectbox('What dataset do you want?',
                                    ['KIKT', 'KAPT', 'KMIS'])
if  select_event == 'KIKT':
    df = kikt 
elif select_event == 'KAPT':
    df = kapt
elif select_event == 'KMIS':
    df = kmis
mindate = df['datetime'].iloc[0] 
maxdate = df['datetime'].iloc[-1] 
## Source: https://docs.streamlit.io/library/api-reference/widgets/st.date_input
st.sidebar.markdown("## Select Date")
select_date = st.sidebar.date_input("What date do you want?", value=mindate, min_value=mindate, max_value=maxdate, key=None, help=None, on_change=None, args=None, kwargs=None, disabled=False)
# In[2]:
st.title('Cognite Pakaa')
st.markdown("Station:  " + str(select_event) + "   Date:  " + str(select_date))
# In[4]: ## Graph Wind Speed
st.subheader('Wind Speed')
fig1 = df.loc[(df.datetime.dt.date == select_date), 'WSPD']
timestamp = df.loc[(df.datetime.dt.date == select_date), 'datetime'].dt.time
g1 = px.scatter(x=timestamp, y=fig1)
g1.update_layout(xaxis_title="Time (hh:mm:ss) on " + str(select_date), yaxis_title="Wind Speed (m/s)")
st.write(g1)
# In[4]: ## Graph Wind Direction
    
st.subheader('Wind Direction')
fig2 = df.loc[(df.datetime.dt.date == select_date), 'WDIR']
timestamp = df.loc[(df.datetime.dt.date == select_date), 'datetime'].dt.time
g2 = px.scatter(x=timestamp, y=fig2)
g2.update_layout(xaxis_title="Time (hh:mm:ss) on " + str(select_date), yaxis_title="Wind Direction (m/s)")
st.write(g2)
# In[5]: ## Show full data 
st.subheader('Source Data')
pull_data(df)
# In[ ]:
