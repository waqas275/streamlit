#!/usr/bin/env python
# coding: utf-8

# In[6]:


import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px


# In[7]:


st.set_page_config(page_title = "avocado-dashboard",
                  page_icon = ":bar_charts:",
                  layout = "wide")



df = pd.read_csv("https://raw.githubusercontent.com/Waqas-test/streamlit/main/avocado.csv")

df['Date'] =  pd.to_datetime(df['Date'],infer_datetime_format=True)
df.sort_values(by=['Date'],inplace=True)
st.sidebar.header("Select Filters:")

#start_date, end_date = st.sidebar.select_slider(
 #   'Select a range of date wavelength',
 #   options=df["Date"],
  #  value=(df["Date"].min(), df["Date"].max()))
start_date = st.sidebar.date_input(
		    "Start Date",
		    df.Date.min())
end_date = st.sidebar.date_input(
		    "Start Date",
		    df.Date.max())

Type = st.sidebar.multiselect(
    "Select Type:",
        options = df["type"].unique(),
        default = df["type"].unique())

city = st.sidebar.multiselect(
    "Select the City:",
        options = df["region"].unique(),
        default = df["region"].unique())




df_selection = df.query("region == @city & Date >= @start_date & Date <= @end_date & type == @Type")

col1, col2, col3, col4 = st.columns(4)






st.subheader('AveragePrice over the Years')

chartdf = pd.pivot_table(df_selection, values='AveragePrice', index=['year'],aggfunc=np.mean)
with col1:
   st.header("Total Volume")
   st.subheader(int(df_selection["Total Volume"].sum()))
   st.bar_chart(chartdf)
with col2:
   st.header("Total Bags")
   st.subheader(int(df_selection["Total Bags"].sum()))
 
fig = px.bar(data_frame=chartdf, x=chartdf.index, y=chartdf["AveragePrice"]) 
fig.update_xaxes(type='category')  
st.plotly_chart(fig, use_container_width=True)
st.dataframe(df_selection)
