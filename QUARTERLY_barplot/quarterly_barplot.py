""" Script to create, display, and save the Quarterly Barplot."""

# ---------------------------------------------------------------

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import re

mpl.rcParams['pdf.fonttype'] = 42

# ---------------------------------------------------------------

# load data
df = pd.read_csv("../InflAdj_Data_2019_2025-20th-20th.csv")

# obtain Quarter of Year for each entry
df['report_quarter'] = pd.to_datetime(df['report_date']).dt.to_period('Q')

# fill in missing values
df['sector'] =df['sector'].fillna("Other")

# filter missing symbols out (can impact sorting and final data)
df = df[~(df['symbol'].isna())]

# last day average dataset
df_lday = df.copy()

# shift report quarter
df_lday['report_quarter_shifted-TEMP'] = df_lday['report_quarter'].shift(-1)

# primarily sort by symbol, for each symbol sort by date
df_lday.sort_values(by= ['symbol', 'report_date'], axis= 0, inplace= True)

# return True if current day is the last of its quarter (next quarter is different)
def last_Qday(row):
    return row['report_quarter'] != row['report_quarter_shifted-TEMP']

# boolean column -> True = needed for plot
df_lday['last_Qday'] = df_lday.apply(last_Qday, axis= 1)

# removed lagged report date
df_lday.drop('report_quarter_shifted-TEMP', axis= 1, inplace= True)

# only store last days of quarters
df_lday_only = df_lday[df_lday['last_Qday'] == True]

# obtain average close % for each sector for each quarter
df_grouped_lday = df_lday_only.groupby(by= ['report_quarter', 'sector']).agg({'close (%)' : 'mean'})
df_grouped_lday.rename({'close (%)' : 'average close (%)'}, axis= 1, inplace= True)

# quarter names and sectors
quarters = set([k[0] for k in df_grouped_lday['average close (%)'].keys()])
sectors = [k[1] for k in df_grouped_lday['average close (%)'].keys()]

# part of the values to be plotted
values_lday = df_grouped_lday['average close (%)'].values

# reordered sectors
unique_sectors = sorted([s for s in df['sector'].unique()])
unique_sectors = unique_sectors[:8] + ['Real Estate', 'Technology', 'Utilities', 'Other']

# ---------------------------------------------------------------

# height ratios are to give less space for the title
fig, axes = plt.subplots(13, 1, figsize= (24, 136), gridspec_kw={'height_ratios': [0.2] + [1] * 12})

# work on title axis
ax_t = axes[0]
ax_t.axis('off')

# for comodity
ax_t.set_xlim(0, 100)
ax_t.set_ylim(0, 100)

# main title
ax_t.text(
            x=50, 
            y=80, 
            s='HOW THE SECTORS SHIFT',
            ha='center',
            va='top', size= 60, weight= 550, zorder= 4)

# description - main
ax_t.text(
            x=50, 
            y=15, 
            s='SECTOR AVERAGE CLOSE % —  INCREASE \u2503 DECREASE  FROM THE PREVIOUS QUARTER',
            ha='center',
            va='top', size= 24, weight= 550, zorder= 4)

# description - additional info (smaller)
ax_t.text(
            x=34, 
            y=-20, 
            s='... across all Sector-specific stocks\non the last day of the Quarter',
            ha='right',
            va='top', size= 16, weight= 400, zorder= 4, c= '#C8C8C7')

# description - utility
ax_t.text(
            x=37, 
            y=13, 
            s='████████  █████████',
            ha='left',
            va='top', size= 24, weight= 550, zorder= 4, c= 'white')

# description - colored text
ax_t.text(
            x=42.7, 
            y=10.5, 
            s='INCREASE',
            ha='center',
            va='top', size= 24, weight= 550, zorder= 4, c= '#4A9090')

# description - colored text
ax_t.text(
            x=55.4, 
            y=10.5, 
            s='DECREASE',
            ha='center',
            va='top', size= 24, weight= 550, zorder= 4, c= '#D06A4C')

# description - 2nd main
ax_t.text(
            x=42, 
            y=-25, 
            s='+++ ACCOMPANIED BY THE',
            ha='left',
            va='top', size= 24, weight= 550, zorder= 4, c= '#000000')

# description - decorated text
ax_t.text(
            x=70.3, 
            y=-28, 
            s='CHANGE FROM 2019',
            ha='left',
            va='top', size= 20, weight= 550, zorder= 4, c= '#000000')
ax_t.hlines(y=-24, xmin= 70.3, xmax= 87.3, colors= '#000000', linewidth= 3.3, zorder= 4, clip_on=False)

# description - additional info (smaller)
ax_t.text(
            x=89.5, 
            y=-31, 
            s='/01/02',
            ha='center',
            va='top', size= 16, weight= 400, zorder= 4, c= '#C8C8C7')

# iterate through sectors
for i, sec in enumerate(unique_sectors, 1):

    # obtain and bound axis
    ax = axes[i]
    ax.set_ylim(-60, 60)

    
    # main y-axis ticks (horizontal lines)
    
    ax.hlines(y=10, xmin=-0.7, xmax=27.7, colors='#E1E1DD', linewidth= 0.8, zorder= 0)
    ax.hlines(y=20, xmin=-0.7, xmax=27.7, colors='#C8C8C7', linewidth= 1.3, zorder= 0)
    ax.hlines(y=30, xmin=-0.7, xmax=27.7, colors='#E1E1DD', linewidth= 0.8, zorder= 0)
    ax.hlines(y=40, xmin=-0.7, xmax=27.7, colors='#C8C8C7', linewidth= 1.3, zorder= 0)
    ax.hlines(y=50, xmin=-0.7, xmax=27.7, colors='#E1E1DD', linewidth= 0.8, zorder= 0)
    
    ax.hlines(y=-10, xmin=-0.7, xmax=27.7, colors='#E1E1DD', linewidth= 0.8, zorder= 0)
    ax.hlines(y=-20, xmin=-0.7, xmax=27.7, colors='#C8C8C7', linewidth= 1.3, zorder= 0)
    ax.hlines(y=-30, xmin=-0.7, xmax=27.7, colors='#E1E1DD', linewidth= 0.8, zorder= 0)
    ax.hlines(y=-40, xmin=-0.7, xmax=27.7, colors='#C8C8C7', linewidth= 1.3, zorder= 0)

    # left labels for the ticks
    ax.text(x= -1.4, y=1, s="0%", c= 'black', ha='left', weight= 550)
    ax.text(x= -1.8, y=19.2, s="+20%", c= '#C8C8C7', ha='left', weight= 550)
    ax.text(x= -1.8, y=39.2, s="+40%", c= '#C8C8C7', ha='left', weight= 550)
    ax.text(x= -1.8, y=-20.8, s="-20%", c= '#C8C8C7', ha='left', weight= 550)
    ax.text(x= -1.8, y=-40.8, s="-40%", c= '#C8C8C7', ha='left', weight= 550)

    # right labels for the ticks
    ax.text(x= 28.8, y=19.2, s="+20%", c= '#C8C8C7', ha='right', weight= 550)
    ax.text(x= 28.8, y=39.2, s="+40%", c= '#C8C8C7', ha='right', weight= 550)
    ax.text(x= 28.8, y=-20.8, s="-20%", c= '#C8C8C7', ha='right', weight= 550)
    ax.text(x= 28.8, y=-40.8, s="-40%", c= '#C8C8C7', ha='right', weight= 550)

    # only obtain values relative to the current sector
    sec_values_lday = [values_lday[i] for i in range(len(sectors)) if sectors[i] == sec]
    
    # compute difference with the previous quarter
    diff_Q = [0] + [sec_values_lday[i] - sec_values_lday[i-1] for i in range(1, len(sec_values_lday))]
    
    # plot bars with proper colors
    colors = ["#4A9090" if diff_Q[j] > 0 else "#D06A4C" for j in range(len(diff_Q))]
    bars2 = ax.bar(range(len(diff_Q)), diff_Q, color= colors)
    
    # add horizontal 'ticks'
    for i, val in enumerate(sec_values_lday):
        
        # store number of quarter
        q = str(i%4+1)

        # low opacity if out of bounds
        a = 0.4 if val > 90 else 1.0
        
        # plot the thick dash
        ax.hlines(y=val, xmin= i-0.33, xmax= i+0.3, colors= 'black', linewidth= 3.3, clip_on=False, alpha= a)
        
        # add text to x-axis ticks
        ax.text(
            x=i, 
            y=-48.5, 
            s='Q' + q,
            ha='center',
            va='top', size= 'medium', weight= 550, zorder= 4)

    # iterate through years to complete x-axis labeling
    for x, yr in [(1, '2019'), (5, '2020'), (9, '2021'), (13, '2022'), (17, '2023'), (21, '2024'), (25, '2025')]:
        
        # horizontal line to encompass the relative four quarters
        ax.hlines(y=-51.8, xmin= x-1.05, xmax= x+2.05, colors= 'black', linewidth= 1.6, zorder= 4)
        
        # year text for x-axis ticks
        ax.text(
            x=x+0.5, 
            y=-53, 
            s=yr,
            ha='center',
            va='top', size= 'large', weight= 550, zorder= 4)
    
    # main horizontal black lines
    ax.hlines(y=0, xmin=-1.3, xmax=28.3, colors='black', linewidth= 1.6, zorder= 4)
    ax.hlines(y=-47, xmin=-1.3, xmax=28.3, colors='black', linewidth= 1.6, zorder= 4)
    
    # plot name of sector
    ax.text(x=0, y=+34, s=sec, c= 'black', ha='left', size= 'x-large', weight= 'heavy')
    ax.axis('off')


# save figure and strip the absolute width attribute to make the svg responsive

fig.savefig("quarterly_barplot_lastday.svg", bbox_inches= 'tight', dpi= 600)

with open("quarterly_barplot_lastday.svg", "r") as f:
    svg_data = f.read()
svg_data = re.sub(r'width="[^"]+"', '', svg_data, count=1)

with open("quarterly_barplot_lastday.svg", "w") as f:
    f.write(svg_data)

print(f"Plot saved as [quarterly_barplot_lastday.svg] in QUARTERLY_barplot/")

# ---------------------------------------------------------------

# group dataframe by report quarter first, sector second, and compute average close %
df_grouped = df.groupby(by= ['report_quarter', 'sector']).agg({'close (%)' : 'mean'})
df_grouped.rename({'close (%)' : 'average close (%)'}, axis= 1, inplace= True)

# quarter names and sectors
quarters = set([k[0] for k in df_grouped['average close (%)'].keys()])
sectors = [k[1] for k in df_grouped['average close (%)'].keys()]

# part of the values to be plotted
values = df_grouped['average close (%)'].values

# reordered sectors
unique_sectors = sorted([s for s in df['sector'].unique()])
unique_sectors = unique_sectors[:8] + ['Real Estate', 'Technology', 'Utilities', 'Other']

# ---------------------------------------------------------------

# height ratios are to give less space for the title
fig, axes = plt.subplots(13, 1, figsize= (24, 136), gridspec_kw={'height_ratios': [0.2] + [1] * 12})

# work on title axis
ax_t = axes[0]
ax_t.axis('off')

# for comodity
ax_t.set_xlim(0, 100)
ax_t.set_ylim(0, 100)

# main title
ax_t.text(
            x=50, 
            y=80, 
            s='HOW THE SECTORS SHIFT',
            ha='center',
            va='top', size= 60, weight= 550, zorder= 4)

# description - main
ax_t.text(
            x=50, 
            y=15, 
            s='SECTOR AVERAGE CLOSE % —  INCREASE \u2503 DECREASE  FROM THE PREVIOUS QUARTER',
            ha='center',
            va='top', size= 24, weight= 550, zorder= 4)

# description - additional info (smaller)
ax_t.text(
            x=34, 
            y=-20, 
            s='... across all Sector-specific stocks\nover all days of the Quarter',
            ha='right',
            va='top', size= 16, weight= 400, zorder= 4, c= '#C8C8C7')

# description - utility
ax_t.text(
            x=37, 
            y=13, 
            s='████████  █████████',
            ha='left',
            va='top', size= 24, weight= 550, zorder= 4, c= 'white')

# description - colored text
ax_t.text(
            x=42.7, 
            y=10.5, 
            s='INCREASE',
            ha='center',
            va='top', size= 24, weight= 550, zorder= 4, c= '#4A9090')

# description - colored text
ax_t.text(
            x=55.4, 
            y=10.5, 
            s='DECREASE',
            ha='center',
            va='top', size= 24, weight= 550, zorder= 4, c= '#D06A4C')

# description - 2nd main
ax_t.text(
            x=42, 
            y=-25, 
            s='+++ ACCOMPANIED BY THE',
            ha='left',
            va='top', size= 24, weight= 550, zorder= 4, c= '#000000')

# description - decorated text
ax_t.text(
            x=70.3, 
            y=-28, 
            s='CHANGE FROM 2019',
            ha='left',
            va='top', size= 20, weight= 550, zorder= 4, c= '#000000')
ax_t.hlines(y=-24, xmin= 70.3, xmax= 87.3, colors= '#000000', linewidth= 3.3, zorder= 4, clip_on=False)

# description - additional info (smaller)
ax_t.text(
            x=89.5, 
            y=-31, 
            s='/01/02',
            ha='center',
            va='top', size= 16, weight= 400, zorder= 4, c= '#C8C8C7')

# iterate through sectors
for i, sec in enumerate(unique_sectors, 1):

    # obtain and bound axis
    ax = axes[i]
    ax.set_ylim(-60, 60)

    
    # main y-axis ticks (horizontal lines)
    
    ax.hlines(y=10, xmin=-0.7, xmax=27.7, colors='#E1E1DD', linewidth= 0.8, zorder= 0)
    ax.hlines(y=20, xmin=-0.7, xmax=27.7, colors='#C8C8C7', linewidth= 1.3, zorder= 0)
    ax.hlines(y=30, xmin=-0.7, xmax=27.7, colors='#E1E1DD', linewidth= 0.8, zorder= 0)
    ax.hlines(y=40, xmin=-0.7, xmax=27.7, colors='#C8C8C7', linewidth= 1.3, zorder= 0)
    ax.hlines(y=50, xmin=-0.7, xmax=27.7, colors='#E1E1DD', linewidth= 0.8, zorder= 0)
    
    ax.hlines(y=-10, xmin=-0.7, xmax=27.7, colors='#E1E1DD', linewidth= 0.8, zorder= 0)
    ax.hlines(y=-20, xmin=-0.7, xmax=27.7, colors='#C8C8C7', linewidth= 1.3, zorder= 0)
    ax.hlines(y=-30, xmin=-0.7, xmax=27.7, colors='#E1E1DD', linewidth= 0.8, zorder= 0)
    ax.hlines(y=-40, xmin=-0.7, xmax=27.7, colors='#C8C8C7', linewidth= 1.3, zorder= 0)

    # left labels for the ticks
    ax.text(x= -1.4, y=1, s="0%", c= 'black', ha='left', weight= 550)
    ax.text(x= -1.8, y=19.2, s="+20%", c= '#C8C8C7', ha='left', weight= 550)
    ax.text(x= -1.8, y=39.2, s="+40%", c= '#C8C8C7', ha='left', weight= 550)
    ax.text(x= -1.8, y=-20.8, s="-20%", c= '#C8C8C7', ha='left', weight= 550)
    ax.text(x= -1.8, y=-40.8, s="-40%", c= '#C8C8C7', ha='left', weight= 550)

    # right labels for the ticks
    ax.text(x= 28.8, y=19.2, s="+20%", c= '#C8C8C7', ha='right', weight= 550)
    ax.text(x= 28.8, y=39.2, s="+40%", c= '#C8C8C7', ha='right', weight= 550)
    ax.text(x= 28.8, y=-20.8, s="-20%", c= '#C8C8C7', ha='right', weight= 550)
    ax.text(x= 28.8, y=-40.8, s="-40%", c= '#C8C8C7', ha='right', weight= 550)

    # only obtain values relative to the current sector
    sec_values = [values[i] for i in range(len(sectors)) if sectors[i] == sec]
    
    # compute difference with the previous quarter
    diff_Q = [0] + [sec_values[i] - sec_values[i-1] for i in range(1, len(sec_values))]
    
    # plot bars with proper colors
    colors = ["#4A9090" if diff_Q[j] > 0 else "#D06A4C" for j in range(len(diff_Q))]
    bars2 = ax.bar(range(len(diff_Q)), diff_Q, color= colors)
    
    # add horizontal 'ticks'
    for i, val in enumerate(sec_values):
        
        # store number of quarter
        q = str(i%4+1)

        # low opacity if out of bounds
        a = 0.4 if val > 90 else 1.0
        
        # plot the thick dash
        ax.hlines(y=val, xmin= i-0.33, xmax= i+0.3, colors= 'black', linewidth= 3.3, clip_on=False, alpha= a)
        
        # add text to x-axis ticks
        ax.text(
            x=i, 
            y=-48.5, 
            s='Q' + q,
            ha='center',
            va='top', size= 'medium', weight= 550, zorder= 4)

    # iterate through years to complete x-axis labeling
    for x, yr in [(1, '2019'), (5, '2020'), (9, '2021'), (13, '2022'), (17, '2023'), (21, '2024'), (25, '2025')]:
        
        # horizontal line to encompass the relative four quarters
        ax.hlines(y=-51.8, xmin= x-1.05, xmax= x+2.05, colors= 'black', linewidth= 1.6, zorder= 4)
        
        # year text for x-axis ticks
        ax.text(
            x=x+0.5, 
            y=-53, 
            s=yr,
            ha='center',
            va='top', size= 'large', weight= 550, zorder= 4)
    
    # main horizontal black lines
    ax.hlines(y=0, xmin=-1.3, xmax=28.3, colors='black', linewidth= 1.6, zorder= 4)
    ax.hlines(y=-47, xmin=-1.3, xmax=28.3, colors='black', linewidth= 1.6, zorder= 4)
    
    # plot name of sector
    ax.text(x=0, y=+34, s=sec, c= 'black', ha='left', size= 'x-large', weight= 'heavy')
    ax.axis('off')


# save figure and strip the absolute width attribute to make the svg responsive

fig.savefig("quarterly_barplot_alldays.svg", bbox_inches= 'tight', dpi= 600)

with open("quarterly_barplot_alldays.svg", "r") as f:
    svg_data = f.read()
svg_data = re.sub(r'width="[^"]+"', '', svg_data, count=1)

with open("quarterly_barplot_alldays.svg", "w") as f:
    f.write(svg_data)

print(f"Plot saved as [quarterly_barplot_alldays.svg] in QUARTERLY_barplot/")