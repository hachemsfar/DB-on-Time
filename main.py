#Library to create dashboard
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from collections import defaultdict
import glob
from datetime import datetime
from neuralprophet import NeuralProphet

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
    st.image("companylogos.PNG")
    st.header("Deutsche Bahn Data Analysis")



        

def prediction():
    st.header("Prediction")
 
page_names_to_funcs = {
"Data Visualization": data_visualization,
"Prediction": prediction
}

demo_name = st.sidebar.selectbox("Choose the App", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()
