import streamlit as st
import pandas as pd

@st.cache_data
def lineplot_load_data():

    df_list = []
    color_list = ['#0066cc', '#C41230', '#00AA4B', '#FFCF06']
    name_list = ['Apple', 'AGCO', 'Archer Daniels Midland', 'Advance Auto Parts']

    for symbol in ['AAPL', 'AGCO', 'ADM', 'AAP']:
        df = pd.read_csv(f"datasets/df_{symbol}.csv")
        df_list.append(df)

    x_ticks = []
    x_labels = []
    last_month = '12'
    for i, val in enumerate(df_list[0]['report_date'].values):
            y, m, d = val.split('-')
            if m == '01' and last_month == '12':
                x_ticks.append(i)
                x_labels.append(y)

            elif int(m) % 2 == 0 and int(last_month) % 2 == 1:
                x_ticks.append(i)
                x_labels.append(m)
            
            last_month = m
    
    return df_list, color_list, name_list, x_ticks, x_labels

@st.cache_data
def heatmap_load_data():
    return pd.read_csv("datasets/sector_mom.csv", index_col= 'industry')