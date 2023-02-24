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
    st.image("https://lirp.cdn-website.com/f98d10fa/dms3rep/multi/opt/d1c2e6ba-b890-4754-9d49-cd3ac8b84a69-640w.png")
    st.header("Our Team")
    st.image("faces.PNG")
    st.header("Technologies Used:")
    st.image("logos.PNG")
    st.header("Data Sources:")
    st.image("companylogos.PNG")
    st.header("Volkshochschule Data Analysis")

    selected_years=st.multiselect('Choose Year(s)', ['2018', '2019', '2020'])
    State=st.selectbox('Pick State', ['DEU','BW', 'BY','BE','BB','HB','HH','HE','MV','NI','NW','RP','SL','SN','ST','SH','TH'])

    if selected_years:
        df_list=[]
        df3_list=[]
        Sprach_stat=defaultdict(list)
        Sprach_all=defaultdict(list)
        
        for year in selected_years:
            df=pd.read_excel(year+" VHS/male_female_"+year+".xlsx",decimal=",")
            df.columns = ['German State','Female','Male']
            df=df[df['German State']==State]
            df_list.append(df)
            
            df3=pd.read_excel(year+" VHS/VHS_Students_"+year+".xlsx",decimal=",")
            df3.columns = ['Language','nbre of courses','nbre of courses %','Total hours','Total hours %','Total students','Total students %']
            df3_list.append(df3)
            
            df2=pd.read_excel(year+" VHS/Deutsch_course "+year+".xlsx",decimal=",",header=None)
            df2=df2.fillna(method='ffill')
            df2.columns = ['German State','nbre of courses','Total hours','Total students']

            for i in df2['German State'].unique():
                Sprach_all['German State'].append(i)
                Sprach_all['total_students'].append(df2[df2['German State']==i]['Total students'].iloc[0])
                
        
        for year in ['2018', '2019', '2020']:
            df2=pd.read_excel(year+" VHS/Deutsch_course "+year+".xlsx",decimal=",",header=None)
            df2=df2.fillna(method='ffill')
            df2.columns = ['German State','nbre of courses','Total hours','Total students']
            df2=df2[df2['German State']==State]
            Sprach_stat['nbre_courses'].append(df2['nbre of courses'].iloc[0])
            Sprach_stat['nbre_courses_per'].append(df2['nbre of courses'].iloc[1])
            Sprach_stat['total_students'].append(df2['Total students'].iloc[0])
            Sprach_stat['total_students_per'].append(df2['Total students'].iloc[1])

        
        df=pd.concat(df_list)
        df3=pd.concat(df3_list)
        
        for i in df3.columns:
            if "%" in i:
                df3[i]=df3[i]*100
        df3=df3.groupby("Language").mean()
        df3.sort_values('nbre of courses %',ascending=False,inplace=True)

        fig,ax=plt.subplots(figsize=(11,7))
        ax.pie([df['Female'].mean(),df['Male'].mean()], labels=['Female','Male'], autopct='%1.1f%%',shadow=True, startangle=90)
        ax.set_title("Male/Female Percentage for Language Course:"+State)
        st.pyplot(fig)
        
        fig1,ax1=plt.subplots(figsize=(11,7))
        ax1.bar(['2018', '2019', '2020'],Sprach_stat['nbre_courses'], color='g', label='cos')
        ax1.set_title("# Languages courses offered by VHS:")
        st.pyplot(fig1)
        st.success("Due to Corona, VHS offered %"+str(round(100*(Sprach_stat['total_students'][-2]-Sprach_stat['total_students'][-1])/Sprach_stat['total_students'][-2],2))+" less courses than the previous year")

        fig1,ax1=plt.subplots(figsize=(11,7))
        ax1.bar(['2018', '2019', '2020'],Sprach_stat['total_students'], color='r', label='sin')
        ax1.set_title("# Students enrolled at VHS:")
        st.pyplot(fig1)
        st.success("Due to Corona, The # of students enrolled Decreased by %"+str(round(100*(Sprach_stat['nbre_courses'][-2]-Sprach_stat['nbre_courses'][-1])/Sprach_stat['nbre_courses'][-2],2))+" than the previous year")

        st.subheader("Top States where the highest number of language learner")
        st.write(pd.DataFrame(Sprach_all).groupby("German State").sum().apply(lambda x: x.sort_values(ascending=False).head()))

        st.subheader("Statistic about each language course offered by VHS")
        st.write(df3[1:])
        st.subheader("Most popular Language courses offered by VHS")
        df4=df3[['nbre of courses %','Total hours %','Total students %']][1:].head(5)
        df5=df4.copy()
        df5.loc['Other languages']= 100-df4.sum()
        df4.loc['Total']= df4.sum()

        st.write(df4)

        fig,ax=plt.subplots(figsize=(11,7))
        ax.pie(df5['nbre of courses %'],labels=df5.index, autopct='%1.1f%%',shadow=True, startangle=90)
        ax.set_title("% of courses for each language")
        st.pyplot(fig)

        fig,ax=plt.subplots(figsize=(11,7))
        ax.pie(df5['Total hours %'],labels=df5.index, autopct='%1.1f%%',shadow=True, startangle=90)
        ax.set_title("% of hours allocated for each language")
        st.pyplot(fig)

        fig,ax=plt.subplots(figsize=(11,7))
        ax.pie(df5['Total students %'],labels=df5.index, autopct='%1.1f%%',shadow=True, startangle=90)
        ax.set_title("% of students for each language")
        st.pyplot(fig)


def prediction():
    st.header("Prediction")
    list_files=glob.glob("Prediction/*.csv")
    df_list=[]
    for i in list_files:
        df_list.append(pd.read_csv(i,encoding='latin1',sep=";",skiprows=7))
    df=pd.concat(df_list)
    df.columns=["semester","ID","University","Deutsche männlich","Deutsche weiblich","Deutsche Insgesamt","Ausländer männlich","Ausländer weiblich","Ausländer Insgesamt","Insgesamt männlich","Insgesamt weiblich","Insgesamt"]
    a=df['University'].unique().tolist()
    uni_filter = st.selectbox("Select the university:",  a )
    column_to_predict = st.selectbox("Select the column to predict:",["Deutsche männlich","Deutsche weiblich","Deutsche Insgesamt","Ausländer männlich","Ausländer weiblich","Ausländer Insgesamt","Insgesamt männlich","Insgesamt weiblich","Insgesamt"])
    future_filter = st.number_input('How many year to predict', 2, 23)

    df=df[df["University"]==uni_filter]
    df["year"]=df["semester"].apply(lambda x:datetime.strptime(x[3:].split("/")[0]+"-01-01 00:00", '%Y-%m-%d %H:%M'))
    df=df[["year",column_to_predict]].sort_values("year").reset_index().drop("index",axis=1)
    new_column = df[["year",column_to_predict]]
    new_column=new_column[new_column["year"]!="2020-01-01 00:00"]
    new_column.dropna(inplace=True)
    new_column.columns = ['ds', 'y']
    clicked=st.button('Predict')
    if clicked:
        n = NeuralProphet()
        model = n.fit(new_column, freq='Y')
        future = n.make_future_dataframe(new_column, periods=future_filter+1)
        forecast = n.predict(future)
        forecast['yhat1']=forecast['yhat1'].apply(lambda x:int(x))
        forecast=forecast[['ds','yhat1']]
        forecast.columns=['year',column_to_predict]
        forecast['year']=forecast['year'].apply(lambda x:str(x).split("-")[0])
        st.write(forecast[1:])

    st.header("Historical Data")
    df2=pd.concat(df_list)
    df2.columns=["semester","ID","University","Deutsche männlich","Deutsche weiblich","Deutsche Insgesamt","Ausländer männlich","Ausländer weiblich","Ausländer Insgesamt","Insgesamt männlich","Insgesamt weiblich","Insgesamt"]
    df2=df2[df2["University"]==uni_filter]
    df2.sort_values('semester',ascending=True,inplace=True)
    st.write(df2[["semester","University","Deutsche männlich","Deutsche weiblich","Deutsche Insgesamt","Ausländer männlich","Ausländer weiblich","Ausländer Insgesamt","Insgesamt männlich","Insgesamt weiblich","Insgesamt"]].reset_index().drop("index",axis=1))


    for j in ["Deutsche männlich","Deutsche weiblich","Deutsche Insgesamt","Ausländer männlich","Ausländer weiblich","Ausländer Insgesamt","Insgesamt männlich","Insgesamt weiblich","Insgesamt"]:
        df2[j] = df2[j].astype(float)
        
    fig,ax=plt.subplots(figsize=(11,7))
    df3=df2.fillna(df2.mean())
    ax.pie([df3['Deutsche männlich'].mean(),df3['Deutsche weiblich'].mean()], labels=['Male','Female'], autopct='%1.1f%%',shadow=True, startangle=90)
    ax.set_title("German: Male/Female Percentage @:"+uni_filter)
    st.pyplot(fig)

    fig,ax=plt.subplots(figsize=(11,7))
    df3=df2.fillna(df2.mean())
    ax.pie([df3['Ausländer männlich'].mean(),df3['Ausländer weiblich'].mean()], labels=['Male','Female'], autopct='%1.1f%%',shadow=True, startangle=90)
    ax.set_title("Auslander: Male/Female Percentage @:"+uni_filter)
    st.pyplot(fig)

    fig,ax=plt.subplots(figsize=(11,7))
    df3=df2.fillna(df2.mean())
    ax.pie([df3['Deutsche Insgesamt'].mean(),df3['Ausländer Insgesamt'].mean()], labels=['Deutsche','Ausländer'], autopct='%1.1f%%',shadow=True, startangle=90)
    ax.set_title("Deutsche/Ausländer Percentage @:"+uni_filter)
    st.pyplot(fig)
    
page_names_to_funcs = {
"Data Visualization": data_visualization,
"Prediction": prediction
}

demo_name = st.sidebar.selectbox("Choose the App", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()
