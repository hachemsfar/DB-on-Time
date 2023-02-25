#Library to create dashboard
import streamlit as st
import pandas as pd
import zipfile
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from collections import defaultdict
from datetime import datetime
import io
import plotly.express as px

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            .row_heading.level0 {display:none}
            .blank {display:none}
            .dataframe {text-align: left !important}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)



def data_visualization():
    st.image("https://techlabs.org/static/tl-logo-cf3f70e8f5222649e6b06468adfae64c.png")
    st.header("Our Team")
    #st.image("faces.PNG")
    st.header("Technologies Used:")
    st.image("logos.png")
    st.header("Data Sources:")
    st.image("deutsche bahn.png")
    st.header("Deutsche Bahn Data Analysis")
    
    zf = zipfile.ZipFile('Mai-August_Departures-2.csv (1).zip') 
    data = pd.read_csv(zf.open('Mai-August_Departures-2.csv'),usecols=['Abfahrt','nach (Ankunft)','Abfahrtsbhf.','date','Zugnr.'])

    data['Final Station']=data['nach (Ankunft)'].apply(lambda x:x.split(' (')[0])
    data['Expected Arrival']=data['nach (Ankunft)'].apply(lambda x:x.split(' (an')[1].split(')')[0])
    data['Arrival Delay']=data['Abfahrt'].apply(lambda x:int(x.split('(')[1][:-1]) if('(' in x)  else 0)


    zf2 = zipfile.ZipFile('Mai-August_Arrivals-2.csv (1).zip') 
    data2 = pd.read_csv(zf2.open('Mai-August_Arrivals-2.csv'),usecols=['Ankunft','Zugnr.','von (Abfahrt)','Ankunftsbhf.','date'])
            
    data2['Departure Station']=data2['von (Abfahrt)'].apply(lambda x:x.split(' (')[0])
    data2['Expected Departure']=data2['von (Abfahrt)'].apply(lambda x:x.split(' (ab')[1].split(')')[0])
    data2['Departure Delay']=data2['Ankunft'].apply(lambda x:int(x.split('(')[1][:-1]) if('(' in x)  else 0)

            
    
    datatotal = data2.merge(data, left_on=['Zugnr.','date','Ankunftsbhf.'],right_on=['Zugnr.','date','Abfahrtsbhf.'])
    datatotal=datatotal.drop(['von (Abfahrt)', 'nach (Ankunft)'], axis=1)
    
    filter_date=st.date_input('Choose a date to analyse')
    trip_id=datatotal[datatotal['date']==str(filter_date)]['Zugnr.'].unique().tolist()
    trip_id_filter=st.multiselect('Pick one', trip_id)
                
    checked=st.checkbox('Filtering?')
    if checked:
        if trip_id_filter!=[]:
            datatotal=datatotal[datatotal['Zugnr.'].isin(trip_id_filter)]
            
        filter_date_month=str(filter_date)[:7]
        datatotal_month=datatotal[datatotal['date'].str.contains(str(filter_date_month))]
        datatotal=datatotal[datatotal['date']==str(filter_date)]

    st.write(datatotal)

    st.header("Summary of a DataFrame")
    buffer = io.StringIO()
    datatotal.info(buf=buffer)
    s = buffer.getvalue()
    st.text(s)

    st.header("Histogram of Delay for Train Journeys in Germany")
   
    fig1,ax1=plt.subplots(figsize=(11,7))
    ax1.hist(datatotal["Arrival Delay"], bins=50)
    ax1.set_xlabel("Arrival Delay (minutes)")
    ax1.set_ylabel("Frequency")
    st.pyplot(fig1)

    datatotal['date'] = pd.to_datetime(datatotal['date'])
    datatotal['day_of_week'] = datatotal['date'].dt.dayofweek

    fig2,ax2=plt.subplots(figsize=(11,7))
    fig2 = px.box(datatotal, y="Arrival Delay",x="day_of_week")
    st.plotly_chart(fig2)
            
    if checked:
        datatotal_month['delay?']=datatotal_month['Arrival Delay'].apply(lambda x: True if x>0 else False)

        fig4,ax4=plt.subplots(figsize=(11,7))
        ax.pie(datatotal_month['delay?'].value_counts(), labels=, autopct='%1.1f%%',shadow=True, startangle=90)
        st.pyplot(fig4)
            
        datatotal_month['day']=datatotal_month['date'].apply(lambda x:int(x.split('-')[2]))
        datatotal_month=datatotal_month.groupby(['day'])['Arrival Delay'].mean()

        fig3,ax3=plt.subplots(figsize=(11,7))  
        ax3.plot(datatotal_month.index,datatotal_month)
        st.pyplot(fig3)
 
                                                            
def prediction():
    st.header("Prediction")
 
page_names_to_funcs = {
"Data Visualization": data_visualization,
"Prediction": prediction
}

demo_name = st.sidebar.selectbox("Choose the App", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()
