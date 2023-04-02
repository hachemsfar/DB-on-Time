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
    st.image("teamphoto.PNG")
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

    st.header("Histogram of Delay for Train Journeys in Germany ("+str(filter_date)+")")
   
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

    datatotal['delay?']=datatotal['Arrival Delay'].apply(lambda x: True if x>0 else False)
    if checked:
        st.header("Delay Percentage ("+str(filter_date)+")")
        fig5,ax5=plt.subplots(figsize=(11,7))
        ax5.pie(datatotal['delay?'].value_counts(), labels=['No Delay','Delay'], autopct='%1.1f%%',shadow=True, startangle=90)
        st.pyplot(fig5)
    else:
        st.header("Delay Percentage (all dataset)")
        fig5,ax5=plt.subplots(figsize=(11,7))
        ax5.pie(datatotal['delay?'].value_counts(), labels=['No Delay','Delay'], autopct='%1.1f%%',shadow=True, startangle=90)
        st.pyplot(fig5)

    if checked:
        st.header("Delay Percentage ("+str(filter_date_month)+")")
        datatotal_month['delay?']=datatotal_month['Arrival Delay'].apply(lambda x: True if x>0 else False)

        fig4,ax4=plt.subplots(figsize=(11,7))
        ax4.pie(datatotal_month['delay?'].value_counts(), labels=['No Delay','Delay'], autopct='%1.1f%%',shadow=True, startangle=90)
        st.pyplot(fig4)
            
        datatotal_month['day']=datatotal_month['date'].apply(lambda x:int(x.split('-')[2]))
        datatotal_month=datatotal_month.groupby(['day'])['Arrival Delay'].mean()
            
        st.header("Average Delay per day ("+str(filter_date_month)+")")

        fig3,ax3=plt.subplots(figsize=(11,7))  
        ax3.plot(datatotal_month.index,datatotal_month)
        st.pyplot(fig3)
            
    st.header("Heatmap about average delay per hour and station")
    datatotal['hour']=datatotal['Expected Arrival'].apply(lambda x:int(x.split(':')[0]))
                                                          
    datatotalgroup = datatotal[['Arrival Delay','Final Station','hour']].groupby(['Final Station','hour'], as_index=False).mean()
    #st.write(datatotalgroup)
            
    fig = plt.figure(figsize=(10, 4))
    datatotalgroup = pd.pivot_table(datatotalgroup.head(23),'Arrival Delay','Final Station','hour')
    sns.heatmap(datatotalgroup)
    st.pyplot(fig)


def prediction():
    st.header("Prediction")
    st.number_input('Arrival Delay', 0)
            
    st.number_input('day',0, 31)
    st.number_input('weekday',0, 6)
            
    st.number_input('hour departure',0, 23)
    st.number_input('minute departure',0, 59)
            
    st.number_input('hour arrival',0, 23)
    st.number_input('minute arrival',0, 59)
    
    L1=['Augsburg Hbf', 'Berlin Gesundbrunnen', 'Berlin Hbf', 'Berlin Hbf (tief)', 'Bremen Hbf', 'Dortmund Hbf', 'Dresden Hbf', 'Duisburg Hbf', 'Düsseldorf Hbf', 'Erfurt Hbf', 'Essen Hbf', 'Frankfurt(Main)Hbf', 'Freiburg(Breisgau) Hbf', 'Fulda', 'Göttingen', 'Hamburg Hbf', 'Hamburg-Altona', 'Hannover Hbf', 'Heidelberg Hbf', 'Karlsruhe Hbf', 'Köln Hbf', 'Köln Messe/Deutz Gl.11-12', 'Leipzig Hbf', 'Mainz Hbf', 'Mannheim Hbf', 'München Hbf', 'München Ost', 'Münster(Westf)Hbf', 'Nürnberg Hbf', 'Stuttgart Hbf']
    departure=st.selectbox('departure station', L1)
    List_departure=[0]*len(L1)
    List_departure[L1.index(departure)]=1

    L2=['Aachen Hbf', 'Amsterdam Centraal', 'Basel SBB', 'Berchtesgaden Hbf', 'Berlin Gesundbrunnen', 'Berlin Hbf', 'Berlin Ostbahnhof', 'Berlin Südkreuz', 'Berlin-Spandau', 'Bochum Hbf', 'Bologna Centrale', 'Bonn Hbf', 'Bonn-Bad Godesberg', 'Braunschweig Hbf', 'Bregenz', 'Bremen Hbf', 'Bremerhaven-Lehe', 'Bruxelles Midi', 'Budapest-Keleti', 'Chemnitz Hbf', 'Chur', 'Cottbus Hbf', 'Dortmund Hbf', 'Dresden Hbf', 'Duisburg Hbf', 'Düsseldorf Hbf', 'Emden Außenhafen', 'Emden Hbf', 'Erfurt Hbf', 'Essen Hbf', 'Flensburg', 'Frankfurt(M) Flughafen Fernbf', 'Frankfurt(Main)Hbf', 'Frankfurt(Main)Süd', 'Frankfurt(Main)West', 'Freiburg(Breisgau) Hbf', 'Friedberg(Hess)', 'Gera Hbf', 'Graz Hbf', 'Greifswald', 'Hamburg Dammtor', 'Hamburg Hbf', 'Hamburg-Altona', 'Hamburg-Harburg', 'Hannover Hbf', 'Heidelberg Hbf', 'Innsbruck Hbf', 'Interlaken Ost', 'Jena Paradies', 'Karlsruhe Hbf', 'Kassel-Wilhelmshöhe', 'Kiel Hbf', 'Klagenfurt Hbf', 'Koblenz Hbf', 'Konstanz', 'Köln Hbf', 'Köln Messe/Deutz Gl.11-12', 'Leipzig Hbf', 'Lübeck Hbf', 'Magdeburg Hbf', 'Mannheim Hbf', 'Marseille-St-Charles', 'Milano Porta Garibaldi', 'Mönchengladbach Hbf', 'München Hbf', 'Münster(Westf)Hbf', 'Norddeich', 'Norddeich Mole', 'Nürnberg Hbf', 'Oberstdorf', 'Offenburg', 'Oldenburg(Oldb)', 'Oldenburg(Oldb)Hbf', 'Ostseebad Binz', 'Paris Est', 'Paris Nord', 'Passau Hbf', 'Praha hl.n.', 'Rostock Hbf', 'Saarbrücken Hbf', 'Salzburg Hbf', 'Siegen', 'Singen(Hohentwiel)', 'Stralsund Hbf', 'Stuttgart Hbf', 'Tübingen Hbf', 'Ulm Hbf', 'Verona Porta Nuova', 'Warnemünde', 'Westerland(Sylt)', 'Wien Hbf', 'Wiesbaden Hbf', 'Wiesloch-Walldorf', 'Zürich HB']
    final=st.selectbox('final station',L2)
    List_final=[0]*len(L2)
    List_final[L2.index(final)]=1

            
page_names_to_funcs = {
"Data Visualization": data_visualization,
"Prediction": prediction
}

demo_name = st.sidebar.selectbox("Choose the App", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()
