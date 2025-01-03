import streamlit as st
import pandas as pd
import re

#Funksionet ne stramlit deklarohen lart

def clean_rate(rate:str)->float:
    regex_pattern = r"[^\d.]+"                              #Largon çdo gje perveç numrave dhe pikave
    rate_str = re.sub(regex_pattern,"",str(rate))
    return float(rate_str)                                  #funksioni me pastru, pra, me largu dollarin
                     
def calculate_wage(hours:float, rate:float)->float:
    if hours <= 40:
         wage = rate * hours
    else:
        wage = (hours - 40) * 1.5 * rate + 40 * rate
    return wage

@st.cache_data      #funksione ndihmese i streamlit 
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

st.title('Calculate Wage Application')

uploaded_file = st.file_uploader('Upload Hours-Rate file!', type=['csv'])
if uploaded_file is None:                                                    #Nese nuk eshte ngarku file
    st.warning('Please upload a csv file to calculate the wage!')            #Shenoje kete paralajmerimin
else:
    df = pd.read_csv(uploaded_file)
    if 'Rate' not in df.columns or 'Hours' not in df.columns:
        st.error("Please rename your columns to correct format 'Rate' and 'Hours' not other")
    else:
        df['Rate'] = df['Rate'].apply(clean_rate)
        df['Wage'] = df.apply(lambda x: calculate_wage(x['Hours'], x['Rate']), axis=1)
        st.dataframe(df)   #me pa file qe e bonem upload

        csv = convert_df(df)
        st.download_button(
            "Press to Download",
            csv,
            "file.csv",
            "text/csv",
            key='download-csv'
        )


