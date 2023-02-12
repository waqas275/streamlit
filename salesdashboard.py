#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
import matplotlib.pyplot as plt

#template = pio.templates["plotly"]

# In[2]:


# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="wide")


# In[3]:
with st.spinner("plz wait"):
	@st.cache

	def cachesdata():

		df = pd.read_csv("https://raw.githubusercontent.com/waqas275/streamlit/main/SampleSales.csv")

		from datetime import datetime
		df['SalesChannel'] = df['SalesChannel'].str.upper()
		
		df['OrderDate'] = pd.to_datetime(df['OrderDate'])
		df['Quarter'] = df['OrderDate'].dt.to_period('Q')#.astype(str)
		df["OrderQuantity"] = pd.to_numeric(df["OrderQuantity"])
		df["UnitPrice"] = pd.to_numeric(df["UnitPrice"])
		df["UnitCost"] = pd.to_numeric(df["UnitCost"])
		df["Revenue"] = df["OrderQuantity"]*df["UnitPrice"]
		df["Profit"] = df["Revenue"] -  (df["OrderQuantity"]*df["UnitCost"])
		df["houseslab"] = pd.qcut(df["HouseholdIncome"], 8, labels=False)
		df["landslab"] = pd.qcut(df["LandArea"], 4, labels=["Q4","Q3","Q2","Q1"])
		df["popslab"] = pd.qcut(df["Population"], 8, labels=False)
		ndf = []

		for x in df.houseslab:
		    if x == 0:
		        y = str(int(df[df.houseslab == 0].HouseholdIncome.min()/1000))+"k to "+str(int(df[df.houseslab == 0].HouseholdIncome.max()/1000))+"k"
		        ndf.append(y)
		    if x == 1:
		        y = str(int(df[df.houseslab == 1].HouseholdIncome.min()/1000))+"k to "+str(int(df[df.houseslab == 1].HouseholdIncome.max()/1000))+"k"
		        ndf.append(y)
		    if x == 2:
		        y = str(int(df[df.houseslab == 2].HouseholdIncome.min()/1000))+"k to "+str(int(df[df.houseslab == 2].HouseholdIncome.max()/1000))+"k"
		        ndf.append(y)
		    if x == 3:
		        y = str(int(df[df.houseslab == 3].HouseholdIncome.min()/1000))+"k to "+str(int(df[df.houseslab == 3].HouseholdIncome.max()/1000))+"k"
		        ndf.append(y)
		    if x == 4:
		        y = str(int(df[df.houseslab == 4].HouseholdIncome.min()/1000))+"k to "+str(int(df[df.houseslab == 4].HouseholdIncome.max()/1000))+"k"
		        ndf.append(y)
		    if x == 5:
		        y = str(int(df[df.houseslab == 5].HouseholdIncome.min()/1000))+"k to "+str(int(df[df.houseslab == 5].HouseholdIncome.max()/1000))+"k"
		        ndf.append(y)
		    if x == 6:
		        y = str(int(df[df.houseslab == 6].HouseholdIncome.min()/1000))+"k to "+str(int(df[df.houseslab == 6].HouseholdIncome.max()/1000))+"k"
		        ndf.append(y)
		    if x == 7:
		        y = str(int(df[df.houseslab == 7].HouseholdIncome.min()/1000))+"k to "+str(int(df[df.houseslab == 7].HouseholdIncome.max()/1000))+"k"
		        ndf.append(y)
		df = pd.concat([df,pd.DataFrame(ndf, columns = ["HouseHoldSlabs"])],axis = 1)

		

		ndf2 = []

		for x1 in df.popslab:
		    if x1== 0:
		        y1 = str(round(df[df.popslab == 0].Population.min()/100000,2))+"m to "+str(round(df[df.popslab == 0].Population.max()/100000,2))+"m"
		        ndf2.append(y1)
		    if x1== 1:
		        y1 = str(round(df[df.popslab == 1].Population.min()/100000,2))+"m to "+str(round(df[df.popslab == 1].Population.max()/100000,2))+"m"
		        ndf2.append(y1)
		    if x1== 2:
		        y1 = str(round(df[df.popslab == 2].Population.min()/100000,2))+"m to "+str(round(df[df.popslab == 2].Population.max()/100000,2))+"m"
		        ndf2.append(y1)
		    if x1== 3:
		        y1 = str(round(df[df.popslab == 3].Population.min()/100000,2))+"m to "+str(round(df[df.popslab == 3].Population.max()/100000,2))+"m"
		        ndf2.append(y1)
		    if x1== 4:
		        y1 = str(round(df[df.popslab == 4].Population.min()/100000,2))+"m to "+str(round(df[df.popslab == 4].Population.max()/100000,2))+"m"
		        ndf2.append(y1)
		    if x1== 5:
		        y1 = str(round(df[df.popslab == 5].Population.min()/100000,2))+"m to "+str(round(df[df.popslab == 5].Population.max()/100000,2))+"m"
		        ndf2.append(y1)
		    if x1== 6:
		        y1 = str(round(df[df.popslab == 6].Population.min()/100000,2))+"m to "+str(round(df[df.popslab == 6].Population.max()/100000,2))+"m"
		        ndf2.append(y1)
		    if x1== 7:
		        y1 = str(round(df[df.popslab == 7].Population.min()/100000,2))+"m to "+str(round(df[df.popslab == 7].Population.max()/100000,2))+"m"
		        ndf2.append(y1)

		df = pd.concat([df,pd.DataFrame(ndf2, columns = ["PopulationSlabs"])],axis = 1)       

		return  df

	df = cachesdata()
# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")

start_date = st.sidebar.date_input(f'Start date >= {df.OrderDate.min()}', df.OrderDate.min())
end_date = st.sidebar.date_input(f'End date <= {df.OrderDate.max()}', df.OrderDate.max())



channel = st.sidebar.multiselect(
    "Select the Channel:",
    options=df["SalesChannel"].unique(),
    default=df["SalesChannel"].unique()
)


df_selection = df.query("SalesChannel == @channel & OrderDate >= @start_date & OrderDate <= @end_date")
#& OrderDate >= @start_date & OrderDate <= @end_date
#st.dataframe(df_selection)

# ---- MAINPAGE ----
st.header(":bar_chart: Sales Dashboard")
st.markdown("##")

# TOP KPI's
total_sales = int(df_selection["OrderQuantity"].sum())
average_discount = round(df_selection["DiscountApplied"].sum(), )
star_rating = ":star:" * 1
total_sale_by_USD = round(df_selection["Revenue"].sum(), )
profit = round(df_selection.Revenue.sum() - df_selection.UnitCost.sum(),)
left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader(f" :trophy: Units Sold {total_sales:,}")
with middle_column:
    st.subheader(f":chart_with_upwards_trend: Revenue {total_sale_by_USD:,} $")
with right_column:
    st.subheader(f":dart: Profit {profit:,} $")

st.markdown("""---""")


left_ch,mid_ch ,right_ch = st.columns(3)

pie = px.pie(data_frame=df_selection.groupby(['SalesChannel'])['OrderQuantity'].sum().reset_index(),
	names="SalesChannel", values="OrderQuantity", color="SalesChannel",title="Units Sold by Channel",
	labels = "OrderQuantity",hole=0.6, width = 370 , height= 350)
pie.update_traces({"textinfo":"value+percent",
					"textposition":"outside"})
with left_ch:
    st.plotly_chart(pie)
dfbar1 = pd.pivot_table(df_selection, values =['Profit',"Revenue"],index =["Quarter"], aggfunc={'Profit': np.sum,'Revenue': np.sum}).reset_index()
#fig1 = px.line(dfbar1,x=dfbar1.Quarter, y=f"{dfbar1.Revenue} & {dfbar1.Profit}",title="Quarterly Trend Quantity & Revenue",
 #            labels=dict(x="Quarter", y="Revenue"), width = 370 , height= 400)
#fig1.add_scatter(x=dfbar1.Quarter, y=dfbar1.Profit)
#fig1.update_layout({"showlegend":False})

dfbar2 = dfbar1.melt(id_vars=['Quarter']+list(dfbar1.keys()[3:6]), var_name='_')
fig1=px.line(dfbar2, x='Quarter', y='value', color='_' ,width = 370 , height= 350,title="Quarterly Trend Profit & Revenue",
	labels={
                     "Quarter": "Qtr",
                     "value": "USD"})

with right_ch:
	st.plotly_chart(fig1)

pie2 = px.pie(data_frame=df_selection.groupby(['Sales_Region'])['Revenue'].sum().reset_index(), 
	names="Sales_Region", values="Revenue", color="Sales_Region",title="Revenue by Region",
	labels = "Revenue",hole=0.6, width = 370 , height= 350)
pie2.update_traces({"textinfo":"value+percent",
					"textposition":"outside"})



#if chart == 'Revenue': 
#    st.plotly_chart(fig1)
#if chart == 'Continent Emissions': 
#    st.plotly_chart(fig2)
#if chart == 'Comparing continents': 
#    st.plotly_chart(fig3)


with mid_ch:
	
	st.plotly_chart(pie2)
st.markdown("""---""")


col_1 ,col_2 ,col_3, col_4 = st.columns(4)

with col_1:
	with st.expander("Select KPI for Map"):
		  mapradio = st.radio("Select the chart that you would like to display",
		  ('Revenue', 'Quantity', 'Profit'))


map1 = px.scatter_geo(data_frame=pd.pivot_table(df_selection, values =["OrderQuantity","Revenue","Latitude","Longitude","Profit"],index =["StateCode"], aggfunc={'OrderQuantity': np.sum,'Revenue': np.sum,"Latitude":np.max,"Longitude":np.max,"Profit":np.sum}).reset_index()
            , lat="Latitude", lon="Longitude", size='Revenue',locations="StateCode",locationmode = "USA-states",projection='albers usa', width = 580 , height= 400,title="Revenue by State",)
map1.update_traces({
    'mode': "markers",
    'fillcolor' : "green",
    'marker':{'color' : 'orange'}})
map1.update_layout({"paper_bgcolor":None})
map1.update_geos({"bgcolor":None,
				"showland": True,
				"showrivers":True,
				"scope":"usa",
				"showcoastlines":True,
				"showcountries":True,
				"showframe":True,
				"showlakes":True,
				"showsubunits":True,
				"subunitwidth": 0.3,
				"landcolor":"lightgrey"})

map2 = px.scatter_geo(data_frame=pd.pivot_table(df_selection, values =["OrderQuantity","Revenue","Latitude","Longitude","Profit"],index =["StateCode"], aggfunc={'OrderQuantity': np.sum,'Revenue': np.sum,"Latitude":np.max,"Longitude":np.max,"Profit":np.sum}).reset_index()
            , lat="Latitude", lon="Longitude", size='OrderQuantity',locations="StateCode",locationmode = "USA-states",projection='albers usa', width = 580 , height= 400,title="Quantity sold by State",)
map2.update_traces({
    'mode': "markers",
    'fillcolor' : "green",
    'marker':{'color' : 'red'}})
map2.update_layout({"paper_bgcolor":None})
map2.update_geos({"bgcolor":None,
				"showland": True,
				"showrivers":True,
				"scope":"usa",
				"showcoastlines":True,
				"showcountries":True,
				"showframe":True,
				"showlakes":True,
				"showsubunits":True,
				"subunitwidth": 0.3,
				"landcolor":"lightgrey"})

map3 = px.scatter_geo(data_frame=pd.pivot_table(df_selection, values =["OrderQuantity","Revenue","Latitude","Longitude","Profit"],index =["StateCode"], aggfunc={'OrderQuantity': np.sum,'Revenue': np.sum,"Latitude":np.max,"Longitude":np.max,"Profit":np.sum}).reset_index()
            , lat="Latitude", lon="Longitude", size='Profit',locations="StateCode",locationmode = "USA-states",projection='albers usa', width = 580 , height= 400,title="Profit by State",)
map3.update_traces({
    'mode': "markers",
    'fillcolor' : "green",
    'marker':{'color' : 'green'}})
map3.update_layout({"paper_bgcolor":None})
map3.update_geos({"bgcolor":None,
				"showland": True,
				"showrivers":True,
				"scope":"usa",
				"showcoastlines":True,
				"showcountries":True,
				"showframe":True,
				"showlakes":True,
				"showsubunits":True,
				"subunitwidth": 0.3,
				"landcolor":"lightgrey"})

col_11 ,col_22 = st.columns(2)

with col_11:
	if mapradio == 'Revenue':

		st.plotly_chart(map1)
	
	if mapradio == 'Quantity':
		st.plotly_chart(map2)
	if mapradio == 'Profit':
		st.plotly_chart(map3)

with col_22:
	st.dataframe(pd.pivot_table(df_selection, values =["OrderQuantity","Revenue","Profit"],
		index =["State"], 
		aggfunc={'OrderQuantity': np.sum,'Revenue': np.sum,"Profit":np.sum}).reset_index(), width=500, height=400, use_container_width=True)
st.markdown("""---""")
#icdf = pd.pivot_table(df_selection, values =["OrderQuantity","Revenue"],
#		index =["SalesTeam","Sales_Region","State"], 
#		aggfunc={'OrderQuantity': np.sum,'Revenue': np.sum}).reset_index()
#







#icchart = px.icicle(data_frame=icdf, path=[ 'Sales_Region','SalesTeam'],
#                values='Revenue', width=500, height=800,title="Sales by Region & Team")



#st.dataframe(pd.pivot_table(df_selection, values =["OrderQuantity","Revenue","Profit"],
#		index =["Sales_Region","State","SalesTeam"], 
#		aggfunc={'OrderQuantity': np.sum,'Revenue': np.sum,"Profit":np.sum}).reset_index(), width=500, height=800, use_container_width=True)
#st.markdown("""---""")

prdbar = pd.pivot_table(df_selection, values =["Revenue","Profit"],
		index =["Product"], 
		aggfunc={'Revenue': np.sum,"Profit":np.sum}).reset_index()

prdbar1 = prdbar.melt(id_vars=['Product']+list(prdbar.keys()[3:6]), var_name='_')
prdchart = px.bar(prdbar1, y='Product', x='value', color='_' ,width = 500 , height= 1200,title="Profit & Revenue by Product",
	labels={
                     "Product": "Product",
                     "value": "USD"},orientation="h")
prdchart.update_layout(yaxis={'categoryorder':'total ascending'})



teambar = pd.pivot_table(df_selection, values =["Revenue","Profit"],
		index =["SalesTeam"], 
		aggfunc={'Revenue': np.sum,"Profit":np.sum}).reset_index()

teambar1 = teambar.melt(id_vars=['SalesTeam']+list(teambar.keys()[3:6]), var_name='_')
teamchart = px.bar(teambar1, y='SalesTeam', x='value', color='_' ,width = 500 , height= 1200,title="Profit & Revenue by SalesTeam",
	labels={
                     "SalesTeam": "SalesTeam",
                     "value": "USD"},orientation="h",template="plotly_white")
teamchart.update_layout(yaxis={'categoryorder':'total ascending'})
l3col1, l3col2 = st.columns(2)

with l3col1:
	st.plotly_chart(prdchart)
with l3col2:
	st.plotly_chart(teamchart)


housechart = px.bar(pd.pivot_table(df_selection, values =["houseslab","Revenue","Profit"],
		index =["HouseHoldSlabs"], 
		aggfunc={'houseslab': np.max,'Revenue': np.sum,"Profit":np.sum}).reset_index().sort_values(by=['houseslab'], ascending=True), y="Revenue", x='HouseHoldSlabs',orientation="v",labels={
                     "Revenue": "Revenue",
                     "HouseHoldSlabs": "House hold Income range"},template="plotly_dark",title="Revenue by Household Income")

popchart = px.bar(pd.pivot_table(df_selection, values =["Population","Revenue","Profit"],
		index =["PopulationSlabs"], 
		aggfunc={'Population': np.sum,'Revenue': np.sum,"Profit":np.sum}).reset_index().sort_values(by=['Population'], ascending=True), y="Revenue", x='PopulationSlabs',orientation="v",labels={
                     "Revenue": "Revenue",
                     "PopulationSlabs": "PopulationSlabs"},title="Revenue by Population Distribution")


#popchart = px.bar(pd.pivot_table(df_selection, values =["Population","Revenue","Profit"],
#		index =["popslab"], 
#		aggfunc={'Population': np.mean,'Revenue': np.sum,"Profit":np.sum}).reset_index(), y="Revenue", x='popslab',orientation="v",labels={
 #                    "Revenue": "Revenue",
  #                   "popslab": "Population Quartile"})


l4col1,l4col2 = st.columns(2)


with l4col1:
	st.plotly_chart(housechart,use_container_width=True)
with l4col2:
	st.plotly_chart(popchart,use_container_width=True)

#if chart == 'Continent Emissions': 
#    st.plotly_chart(fig2)
#if chart == 'Comparing continents': 
#    st.plotly_chart(fig3)
#st.plotly_chart(map1)
