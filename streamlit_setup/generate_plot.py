"""
Module containing all functions needed to create matplotlib figures for the charts.
"""

# -------------------------------------------------------------------------------

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors

# -------------------------------------------------------------------------------

def generate_week_lineplot(df_list, color_list, seed):
    
    fig, axes = plt.subplots(1, 4, facecolor= "#FAF9F6", figsize= (64, 16))

    # seed will be passed from the session state parameters
    w = seed  # np.random.randint(14, 1759)
    
    # initialize list to store datasets
    df_week_list = []

    # store min and max change to properly calibrate axes range
    close_min, close_max = np.inf, -np.inf

    # extra - not used
    stock_min_peak, stock_max_peak = None, None
    close_min_final, close_max_final = np.inf, -np.inf
    stock_min_final, stock_max_final = 0, 0

    # iterate through datasets
    for i, df in enumerate(df_list):

        # only keep the 14 most recent datapoints up until the seed index
        df_week = df.iloc[w-14 : w].copy()

        # obtain baseline value
        baseline = df_week['close'].values[0]

        # new column: compute difference of each closing value in $ from baseline and turn it into % change 
        df_week['week close (%)'] = ((df_week['close'] - baseline) / baseline) * 100
        

        # obtain and store min and max % values

        cmin = df_week['week close (%)'].min()
        cmax = df_week['week close (%)'].max()

        if cmin < close_min:
            close_min = cmin
            stock_min_peak = i
        
        if cmax > close_max:
            close_max = cmax
            stock_max_peak = i

        fc_val = df_week['week close (%)'].values[-1]
        
        if fc_val < close_min_final:
            close_min_final = fc_val
            stock_min_final = i
        
        if fc_val > close_max_final:
            close_max_final = fc_val
            stock_max_final = i

        # store filtered dataset 
        df_week_list.append(df_week)
    

    for i, ax in enumerate(axes):

        ax.axis('off')
        ax.set_ylim(close_min - 1, close_max + 1)
        #ax.set_xlim(-2, len(df_week))
        #ax.vlines(x= len(df_week)/2, ymin= -100, ymax= 100, colors= 'black')
        df_week = df_week_list[i]

        # ROUND VALS TO INTEGERS
        #ax.text(x= len(df_week)/2, y = close_max + abs(close_max*0.2), s= f"Stock {i+1}", c= color_list[i%4], ha= 'center', weight= 550, size= 50)
        ax.hlines(y = round(close_min*0.8, 0)/2, xmin= -1, xmax = len(df_week), linewidth= 3, colors= '#C8C8C7', clip_on=False)
        ax.hlines(y = round(close_min*0.8, 0), xmin= -1, xmax = len(df_week), linewidth= 3, colors= '#C8C8C7')
        ax.hlines(y = round(close_max*0.8, 0)/2, xmin= -1, xmax = len(df_week), linewidth= 3, colors= '#C8C8C7')
        ax.hlines(y = round(close_max*0.8, 0), xmin= -1, xmax = len(df_week), linewidth= 3, colors= '#C8C8C7')
        #ax.vlines(x = len(df_week)/2, ymin=-100, ymax= 100, colors= 'black')
        if i < 3:
            if close_min*0.4 < -0.8 or (close_max - close_min) < 15:
                ax.text(x=len(df_week)+2.3, y=round(close_min*0.8, 0) - abs(close_min)*0.01, s=f"{(close_min*0.8):.0f}%", c= '#C8C8C7', ha='center', weight= 550, size= 30)
            
            if close_max*0.4 > 0.8 or (close_max - close_min) < 15:
                ax.text(x=len(df_week)+2.3, y=round(close_max*0.8, 0) - abs(close_max)*0.01, s=f"{'+' * (float(close_max) > 0)}{(close_max*0.8):.0f}%", c= '#C8C8C7', ha='center', weight= 550, size= 30)
            ax.text(x= len(df_week)+2.3, y= -0.1, s= '0%', c= 'black', ha='center', weight= 550, size= 30)
            
        ax.hlines(y= 0, xmin= -1, xmax= len(df_week), linewidth= 5, colors= 'black')
        ax.scatter([0, 13], [0, df_week['week close (%)'].values[-1]], c= color_list[i%4], s= 300, zorder= 5)
        ax.scatter([14], [0], c= '#000000', s= 300, marker= '>', zorder= 4)
        ax.plot(range(len(df_week)), df_week['week close (%)'], c= color_list[i], linewidth= 10)

    date_1, date_2 = df_week['report_date'].values[0], df_week['report_date'].values[-1]
    return fig, stock_min_final, stock_max_final, stock_min_peak, stock_max_peak, date_1, date_2


def generate_final_lineplot(df_list, color_list, name_list, x_ticks, x_labels):

    fig, axes = plt.subplots(4, 1, gridspec_kw={'height_ratios': [1.85, 1, 1, 1]}, facecolor= '#FAF9F6')
    fig.set_figheight(32)
    fig.set_figwidth(20)

    for i, ax in enumerate(axes):
        
        ax.text(x= 211, y= 170, s= f'Stock {i+1}: ', c= 'black', ha= 'right', size= 'large', weight= 550)
        ax.text(x= 215, y= 170, s= name_list[i], c= color_list[i], ha= 'left', size= 'x-large', weight= 'heavy')
        ax.text(x=-15, y=5, s="0%", c= 'black', ha='center', weight= 550, size= 8) #, ha='center', family='serif', fontname='Arial')
        ax.text(x=-15, y=55, s=" +50%", c= '#C8C8C7', ha='center', weight= 550, size= 8)
        ax.text(x=-15, y=105, s="+100%", c= '#C8C8C7', ha='center', weight= 550, size= 8)
        ax.text(x=-15, y=155, s="+150%", c= '#C8C8C7', ha='center', weight= 550, size= 8)
        ax.text(x=-15, y=-45, s=" -50%", c= '#C8C8C7', ha='center', weight= 550, size= 8)
        ax.text(x=-15, y=-95, s="-100%", c= '#C8C8C7', ha='center', weight= 550, size= 8)

        ax.hlines(y=0, xmin=0, xmax=1759, colors='black')
        ax.hlines(y=25, xmin=0, xmax=1759, colors='#E1E1DD', linewidth= 0.8)
        ax.hlines(y=50, xmin=0, xmax=1759, colors='#C8C8C7', linewidth= 1.3)
        ax.hlines(y=75, xmin=0, xmax=1759, colors='#E1E1DD', linewidth= 0.8)
        ax.hlines(y=100, xmin=0, xmax=1759, colors='#C8C8C7', linewidth= 1.3)
        ax.hlines(y=125, xmin=0, xmax=1759, colors='#E1E1DD', linewidth= 0.8)
        ax.hlines(y=150, xmin=0, xmax=1759, colors='#C8C8C7', linewidth= 1.3)

        ax.hlines(y=-25, xmin=0, xmax=1759, colors='#E1E1DD', linewidth= 0.8)
        ax.hlines(y=-50, xmin=0, xmax=1759, colors='#C8C8C7', linewidth= 1.3)
        ax.hlines(y=-75, xmin=0, xmax=1759, colors='#E1E1DD', linewidth= 0.8)
        ax.hlines(y=-100, xmin=0, xmax=1759, colors='#C8C8C7', linewidth= 1.3)
        ax.hlines(y=-120, xmin=-2, xmax=1759, colors='black')

        ax.hlines(y=0, xmin=-100, xmax=0, colors='black', linestyles= 'dashed')
        ax.hlines(y=25, xmin=-100, xmax=0, colors='#E1E1DD', linestyles= 'dashed', linewidth= 0.8)
        ax.hlines(y=50, xmin=-100, xmax=0, colors='#C8C8C7', linestyles= 'dashed', linewidth= 1.3)
        ax.hlines(y=75, xmin=-100, xmax=0, colors='#E1E1DD', linestyles= 'dashed', linewidth= 0.8)
        ax.hlines(y=100, xmin=-100, xmax=0, colors='#C8C8C7', linestyles= 'dashed', linewidth= 1.3)
        ax.hlines(y=125, xmin=-100, xmax=0, colors='#E1E1DD', linestyles= 'dashed', linewidth= 0.8)
        ax.hlines(y=150, xmin=-100, xmax=0, colors='#C8C8C7', linestyles= 'dashed', linewidth= 1.3)

        ax.hlines(y=-25, xmin=-100, xmax=0, colors='#E1E1DD', linestyles= 'dashed', linewidth= 0.8)
        ax.hlines(y=-50, xmin=-100, xmax=0, colors='#C8C8C7', linestyles= 'dashed', linewidth= 1.3)
        ax.hlines(y=-75, xmin=-100, xmax=0, colors='#E1E1DD', linestyles= 'dashed', linewidth= 0.8)
        ax.hlines(y=-100, xmin=-100, xmax=0, colors='#C8C8C7', linestyles= 'dashed', linewidth= 1.3)
        ax.hlines(y=-120, xmin=-100, xmax=0, colors='black', linestyles= 'dashed')
        

        ax.hlines(y=0, xmin=1759, xmax=1900, colors='black', linestyles= 'dashed')
        ax.hlines(y=25, xmin=1759, xmax=1900, colors='#E1E1DD', linestyles= 'dashed', linewidth= 0.8)
        ax.hlines(y=50, xmin=1759, xmax=1900, colors='#C8C8C7', linestyles= 'dashed', linewidth= 1.3)
        ax.hlines(y=75, xmin=1759, xmax=1900, colors='#E1E1DD', linestyles= 'dashed', linewidth= 0.8)
        ax.hlines(y=100, xmin=1759, xmax=1900, colors='#C8C8C7', linestyles= 'dashed', linewidth= 1.3)
        ax.hlines(y=125, xmin=1759, xmax=1900, colors='#E1E1DD', linestyles= 'dashed', linewidth= 0.8)
        ax.hlines(y=150, xmin=1759, xmax=1900, colors='#C8C8C7', linestyles= 'dashed', linewidth= 1.3)

        ax.hlines(y=-25, xmin=1759, xmax=1900, colors='#E1E1DD', linestyles= 'dashed', linewidth= 0.8)
        ax.hlines(y=-50, xmin=1759, xmax=1900, colors='#C8C8C7', linestyles= 'dashed', linewidth= 1.3)
        ax.hlines(y=-75, xmin=1759, xmax=1900, colors='#E1E1DD', linestyles= 'dashed', linewidth= 0.8)
        ax.hlines(y=-100, xmin=1759, xmax=1900, colors='#C8C8C7', linestyles= 'dashed', linewidth= 1.3)
        ax.hlines(y=-120, xmin=1759, xmax=1900, colors='black', linestyles= 'dashed')
        

        
        if df_list[i]['symbol'].values[0] == 'AAPL':
            ax.set_ylim(-150, 500)
            ax.hlines(y=400, xmin=-100, xmax=0, colors='#C8C8C7', linestyles= 'dashed', linewidth= 1.3)
            ax.hlines(y=400, xmin=1759, xmax=1900, colors='#C8C8C7', linestyles= 'dashed', linewidth= 1.3)
            ax.hlines(y=400, xmin=0, xmax=1759, colors='#C8C8C7', linewidth= 1.3)
            ax.text(x=-15, y=405, s=" +400%", c= '#C8C8C7', ha='center', weight= 550)

        else:
            ax.set_ylim(-150, 200)
        
        ax.plot(df_list[i]['report_date'], df_list[i]['close (%)'], c= color_list[i], linewidth= 2.5)
        ax.axis('off')
        ax.set_xlim(left= -50, right= 1809)
        
        for x, label in zip(x_ticks, x_labels):
            if len(label) > 2:
                size = 'medium'
                ymin = -137
                y = -138
            else:
                size = 'small'
                ymin = -125
                y = -127
            ax.vlines(x=x, ymin=ymin, ymax=-120, colors='black')
            ax.text(
                x=x, 
                y=y, 
                s=label,
                ha='center',
                va='top', weight= 550, size= size)
    
    return fig


def generate_heatmap(sector_mom):

    n_sectors, n_mo = sector_mom.shape
    dates = sector_mom.columns

    finite = sector_mom.values[np.isfinite(sector_mom.values)]
    vlim = round(float(np.percentile(np.abs(finite), 95)), 1) if len(finite) > 0 else 10.0

    # layout control, height, width etc
    cell_h   = 0.52
    fig_w    = max(18, n_mo * 0.032 + 4)
    fig_h    = max(7, n_sectors * cell_h + 3.6)   # +0.4 for extra header room
    header_h = 1.5                                  # fixed inches — enough for any fig_h
    footer_h = 0.45
    T = 1.0 - (header_h / fig_h)*3
    B = footer_h*3 / fig_h
    print(fig_w)
    FACE = "#FAF9F6"
    fig, ax = plt.subplots(figsize=(fig_w, fig_h), facecolor=FACE)
    fig.subplots_adjust(top= 1, bottom= 0, left=0, right=1)
    ax.set_facecolor(FACE)
    ax.axis("off")
    # ── colormap (unchanged) ─────────────────────────────────────────────────
    red, grey, green = '#D06A4C', FACE, '#4C98CE'
    cmap = mcolors.LinearSegmentedColormap.from_list('RdGrGn', [red, grey, green])

    im = ax.imshow(
        sector_mom.values,
        aspect='auto', cmap=cmap,
        vmin=-vlim, vmax=vlim,
        interpolation='none',
    )

    if False:
        tick_pos = [0]
        x_labels = ['2019']
        last_month = '12'
        for i, val in enumerate(dates):
                y, m, d = str(val).split('-')
                if m == '01' and last_month == '12':
                    tick_pos.append(i)
                    x_labels.append(y)

                # elif int(m) % 2 == 0 and int(last_month) % 2 == 1:
                #     tick_pos.append(i)
                #     x_labels.append(m)
                
                last_month = m

        for t in tick_pos[1:]:
            ax.vlines(x= t, ymin= -0.5, ymax= 30, colors= 'black', linewidth= 2)
    

    ax.xaxis.set_ticks_position('top')
    ax.xaxis.set_label_position('top')
    ax.tick_params(axis='x', length=0, pad=3)

    # thin row separators 
    for i in range(1, n_sectors):
        ax.axhline(i - 0.5, color=FACE, linewidth=1.2, zorder=3)

    # spines off
    for sp in ax.spines.values():
        sp.set_visible(False)

    return fig

def generate_barplot(df, avg_close, ticks_2019: bool = False):

    baseline_sector_avg = {item[0][1] : item[1] for item in avg_close['average close'].items()}
    quarters = set([k[0] for k in df['average close'].keys()])
    sectors = [k[1] for k in df['average close'].keys()]
    values = df['average close'].values
    unique_sectors = sorted(baseline_sector_avg.keys())
    unique_sectors = unique_sectors[:8] + ['Real Estate', 'Technology', 'Utilities']
    
    fig, axes = plt.subplots(11, 1, figsize= (24, 80), facecolor= '#FAF9F6')
    fig.subplots_adjust(
        top=0.98, 
        bottom=0.02, 
        hspace=0.08  # Adjust this to control the vertical spacing *between* the 11 subplots
    )

    for i, sec in enumerate(unique_sectors):

        ax = axes[i]
        ax.set_ylim(-60, 60)

        ax.hlines(y=10, xmin=-0.7, xmax=27.7, colors='#E1E1DD', linewidth= 0.8, zorder= 0)
        ax.hlines(y=20, xmin=-0.7, xmax=27.7, colors='#C8C8C7', linewidth= 1.3, zorder= 0)
        ax.hlines(y=30, xmin=-0.7, xmax=27.7, colors='#E1E1DD', linewidth= 0.8, zorder= 0)
        ax.hlines(y=40, xmin=-0.7, xmax=27.7, colors='#C8C8C7', linewidth= 1.3, zorder= 0)
        ax.hlines(y=50, xmin=-0.7, xmax=27.7, colors='#E1E1DD', linewidth= 0.8, zorder= 0)
        ax.hlines(y=-10, xmin=-0.7, xmax=27.7, colors='#E1E1DD', linewidth= 0.8, zorder= 0)
        ax.hlines(y=-20, xmin=-0.7, xmax=27.7, colors='#C8C8C7', linewidth= 1.3, zorder= 0)
        ax.hlines(y=-30, xmin=-0.7, xmax=27.7, colors='#E1E1DD', linewidth= 0.8, zorder= 0)
        ax.hlines(y=-40, xmin=-0.7, xmax=27.7, colors='#C8C8C7', linewidth= 1.3, zorder= 0)

        ax.text(x= -1.4, y=1, s="0%", c= 'black', ha='left', weight= 550)
        ax.text(x= -1.8, y=19.2, s="+20%", c= '#C8C8C7', ha='left', weight= 550)
        ax.text(x= -1.8, y=39.2, s="+40%", c= '#C8C8C7', ha='left', weight= 550)
        ax.text(x= -1.8, y=-20.8, s="-20%", c= '#C8C8C7', ha='left', weight= 550)
        ax.text(x= -1.8, y=-40.8, s="-40%", c= '#C8C8C7', ha='left', weight= 550)

        ax.text(x= 28.8, y=19.2, s="+20%", c= '#C8C8C7', ha='right', weight= 550)
        ax.text(x= 28.8, y=39.2, s="+40%", c= '#C8C8C7', ha='right', weight= 550)
        ax.text(x= 28.8, y=-20.8, s="-20%", c= '#C8C8C7', ha='right', weight= 550)
        ax.text(x= 28.8, y=-40.8, s="-40%", c= '#C8C8C7', ha='right', weight= 550)

        sec_values = [values[i] for i in range(len(sectors)) if sectors[i] == sec]
        sec_values_lday_perc = [((values[i] - baseline_sector_avg[sec]) / baseline_sector_avg[sec]) * 100 for i in range(len(sectors)) if sectors[i] == sec]
        diff_Q = [0] + [((sec_values[i] - sec_values[i-1]) / sec_values[i-1]) * 100 for i in range(1, len(sec_values))]
        

        colors = ["#4C98CE" if diff_Q[j] > 0 else "#D06A4C" for j in range(len(diff_Q))]
        
        bars2 = ax.bar(range(len(diff_Q)), diff_Q, color= colors)
        for i, val in enumerate(sec_values_lday_perc):
            q = str(i%4+1)

            if ticks_2019:
                c = "#484848" if (val > 90) or ((val < -45) and (val > -55)) else "#000000"
                ax.hlines(y=val, xmin= i-0.33, xmax= i+0.3, colors= c, linewidth= 3.3, clip_on=False)
            ax.text(
                x=i, 
                y=-48.2, 
                s='Q' + q,
                ha='center',
                va='top', size= 'medium', weight= 550, zorder= 4)

        for x, yr in [(1, '2019'), (5, '2020'), (9, '2021'), (13, '2022'), (17, '2023'), (21, '2024'), (25, '2025')]:
            ax.hlines(y=-51.7, xmin= x-1.05, xmax= x+2.05, colors= 'black', linewidth= 1.6, zorder= 4)

            ax.text(
                x=x+0.5, 
                y=-53, 
                s=yr,
                ha='center',
                va='top', size= 'large', weight= 550, zorder= 4)

        ax.hlines(y=0, xmin=-1.3, xmax=28.3, colors='black', linewidth= 1.6, zorder= 4)
        ax.hlines(y=-47, xmin=-1.3, xmax=28.3, colors='black', linewidth= 1.6, zorder= 4)
        ax.text(x=0, y=+34, s=sec, c= 'black', ha='left', size= 'x-large', weight= 'heavy')
        ax.axis('off')
        
    return fig