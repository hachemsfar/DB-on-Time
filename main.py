#Library to create dashboard
import streamlit as st
import pandas as pd
import zipfile
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from collections import defaultdict
from datetime import datetime

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
    st.image("faces.PNG")
    st.header("Technologies Used:")
    st.image("logos.png")
    st.header("Data Sources:")
    st.image("deutsche bahn.png")
    st.header("Deutsche Bahn Data Analysis")
    
    zf = zipfile.ZipFile('Mai-August_Departures-2.csv (1).zip') 
    data = pd.read_csv(zf.open('Mai-August_Departures-2.csv'))

    zf2 = zipfile.ZipFile('Mai-August_Arrivals-2.csv (1).zip') 
    data2 = pd.read_csv(zf.open('Mai-August_Departures-2.csv'))

    #datatotal = data2.merge(data, on='Zugnr.')

    #datatotal['departure']=datatotal['von (Abfahrt)'].apply(lambda x:x.split('(ab ')[1].split(')')[0])
    #datatotal['Delay']=datatotal['Abfahrt'].apply(lambda x:int(x.split('(')[1][:-1]) if('(' in x)  else 0)

    st.write(data)
    st.write(data2)

def prediction():
    st.header("Prediction")
 
page_names_to_funcs = {
"Data Visualization": data_visualization,
"Prediction": prediction
}

demo_name = st.sidebar.selectbox("Choose the App", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()
