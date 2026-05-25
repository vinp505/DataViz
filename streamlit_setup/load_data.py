import streamlit as st
import pandas as pd

@st.cache_data
def load_data():

    df = pd.read_csv("InflAdj_Data_2019_2025-20th-20th.csv")
    df_apple = df[df['symbol'] == 'AAPL']
    df_adm = df[df['symbol'] == 'ADM']
    df_aap = df[df['symbol'] == 'AAP']
    df_agco = df[df['symbol'] == 'AGCO']
    df_list = [df_apple, df_agco, df_adm, df_aap]
    color_list = ['#0066cc', '#C41230', '#00AA4B', '#FFCF06']
    name_list = ['Apple', 'AGCO', 'Archer Daniels Midland', 'Advance Auto Parts']

    x_ticks = []
    x_labels = []
    last_month = '12'
    for i, val in enumerate(df_apple['report_date'].values):
            y, m, d = val.split('-')
            if m == '01' and last_month == '12':
                x_ticks.append(i)
                x_labels.append(y)

            elif int(m) % 2 == 0 and int(last_month) % 2 == 1:
                x_ticks.append(i)
                x_labels.append(m)
            
            last_month = m
    return df_list, color_list, name_list, x_ticks, x_labels