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
    
    # iterate through axes
    for i, ax in enumerate(axes):
        
        # axis settings
        ax.axis('off')
        ax.set_ylim(close_min - 1, close_max + 1)

        # obtain correct dataset
        df_week = df_week_list[i]

        # round 40% and 80% of min and max values to integers and add the relative line
        ax.hlines(y = round(close_min*0.8, 0)/2, xmin= -1, xmax = len(df_week), linewidth= 3, colors= '#C8C8C7', clip_on=False)
        ax.hlines(y = round(close_min*0.8, 0), xmin= -1, xmax = len(df_week), linewidth= 3, colors= '#C8C8C7')
        ax.hlines(y = round(close_max*0.8, 0)/2, xmin= -1, xmax = len(df_week), linewidth= 3, colors= '#C8C8C7')
        ax.hlines(y = round(close_max*0.8, 0), xmin= -1, xmax = len(df_week), linewidth= 3, colors= '#C8C8C7')
        
        # add labels with % in between plots (if lines aren't too close to eachother)
        if i < 3:
            if close_min*0.4 < -0.8 or (close_max - close_min) < 15:
                ax.text(x=len(df_week)+2.3, y=round(close_min*0.8, 0) - abs(close_min)*0.01, s=f"{(close_min*0.8):.0f}%", c= '#C8C8C7', ha='center', weight= 550, size= 30)
            
            if close_max*0.4 > 0.8 or (close_max - close_min) < 15:
                ax.text(x=len(df_week)+2.3, y=round(close_max*0.8, 0) - abs(close_max)*0.01, s=f"{'+' * (float(close_max) > 0)}{(close_max*0.8):.0f}%", c= '#C8C8C7', ha='center', weight= 550, size= 30)
            ax.text(x= len(df_week)+2.3, y= -0.1, s= '0%', c= 'black', ha='center', weight= 550, size= 30)

        # add 0 line     
        ax.hlines(y= 0, xmin= -1, xmax= len(df_week), linewidth= 5, colors= 'black')

        # scatter for end points + arrow on 0 line
        ax.scatter([0, 13], [0, df_week['week close (%)'].values[-1]], c= color_list[i%4], s= 300, zorder= 5)
        ax.scatter([14], [0], c= '#000000', s= 300, marker= '>', zorder= 4)

        # main data plotting
        ax.plot(range(len(df_week)), df_week['week close (%)'], c= color_list[i], linewidth= 10)

    # obtain dates of time period
    date_1, date_2 = df_week['report_date'].values[0], df_week['report_date'].values[-1]
    
    return fig, stock_min_final, stock_max_final, stock_min_peak, stock_max_peak, date_1, date_2

# -------------------------------------------------------------------------------

def generate_final_lineplot(df_list, color_list, name_list, x_ticks, x_labels):

    # axes with proper ratio (Apple goes off scale)
    fig, axes = plt.subplots(4, 1, gridspec_kw={'height_ratios': [1.85, 1, 1, 1]}, facecolor= '#FAF9F6')
    fig.set_figheight(32)
    fig.set_figwidth(20)

    # iterate through axes
    for i, ax in enumerate(axes):
        
        # text for the major horizontal lines
        ax.text(x= 211, y= 170, s= f'Stock {i+1}: ', c= 'black', ha= 'right', size= 'large', weight= 550)
        ax.text(x= 215, y= 170, s= name_list[i], c= color_list[i], ha= 'left', size= 'x-large', weight= 'heavy')
        ax.text(x=-15, y=5, s="0%", c= 'black', ha='center', weight= 550, size= 8) #, ha='center', family='serif', fontname='Arial')
        ax.text(x=-15, y=55, s=" +50%", c= '#C8C8C7', ha='center', weight= 550, size= 8)
        ax.text(x=-15, y=105, s="+100%", c= '#C8C8C7', ha='center', weight= 550, size= 8)
        ax.text(x=-15, y=155, s="+150%", c= '#C8C8C7', ha='center', weight= 550, size= 8)
        ax.text(x=-15, y=-45, s=" -50%", c= '#C8C8C7', ha='center', weight= 550, size= 8)
        ax.text(x=-15, y=-95, s="-100%", c= '#C8C8C7', ha='center', weight= 550, size= 8)


        # horizontal lines for major and minor ticks

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


        # dashed lines for the margins of the graph

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
        

        # set custom axis parameters for Apple, extra line
        if df_list[i]['symbol'].values[0] == 'AAPL':
            ax.set_ylim(-150, 500)
            ax.hlines(y=400, xmin=-100, xmax=0, colors='#C8C8C7', linestyles= 'dashed', linewidth= 1.3)
            ax.hlines(y=400, xmin=1759, xmax=1900, colors='#C8C8C7', linestyles= 'dashed', linewidth= 1.3)
            ax.hlines(y=400, xmin=0, xmax=1759, colors='#C8C8C7', linewidth= 1.3)
            ax.text(x=-15, y=405, s=" +400%", c= '#C8C8C7', ha='center', weight= 550)

        else:
            ax.set_ylim(-150, 200)
        
        # plot values, adjust axis
        ax.plot(df_list[i]['report_date'], df_list[i]['close (%)'], c= color_list[i], linewidth= 2.5)
        ax.axis('off')
        ax.set_xlim(left= -50, right= 1809)
        
        # add x-axis labels and ticks
        for x, label in zip(x_ticks, x_labels):
            
            # plot years lower than months
            if len(label) > 2:
                size = 'medium'
                ymin = -137
                y = -138
            else:
                size = 'small'
                ymin = -125
                y = -127
            
            # add vertical line for the ticks, and text for the labels
            ax.vlines(x=x, ymin=ymin, ymax=-120, colors='black')
            ax.text(
                x=x, 
                y=y, 
                s=label,
                ha='center',
                va='top', weight= 550, size= size)
    
    return fig

# -------------------------------------------------------------------------------

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
    norm = mcolors.Normalize(vmin=-vlim, vmax=vlim)


    im = ax.imshow(
        sector_mom.values,
        aspect='auto', cmap=cmap,
        vmin=-vlim, vmax=vlim,
        interpolation='none',
    )

    if True:
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

    #colorbar
    colorbar, ax  = plt.subplots(figsize=(5, 0.35) , facecolor = FACE)
    colorbar.subplots_adjust(left=0, right=1, top=1, bottom=0)

    cb = colorbar.colorbar(
        plt.cm.ScalarMappable(norm=norm, cmap=cmap),
        cax=ax,
        orientation='horizontal',
    )
    cb.set_ticks([])
    cb.outline.set_visible(False)
    cb.ax.text(0, 0.5, f'{-vlim:.1f}% ', transform=cb.ax.transAxes,
               ha='right', va='center', fontsize=18, fontweight='bold')
    cb.ax.text(1, 0.5, f' {vlim:.1f}%', transform=cb.ax.transAxes,
               ha='left', va='center', fontsize=18, fontweight='bold')

    return fig, colorbar

# -------------------------------------------------------------------------------

def generate_barplot(df, avg_close, ticks_2019: bool = False):

    # obtain baseline values in $
    baseline_sector_avg = {item[0][1] : item[1] for item in avg_close['average close'].items()}
    
    # more data
    quarters = set([k[0] for k in df['average close'].keys()])
    sectors = [k[1] for k in df['average close'].keys()]
    values = df['average close'].values
    unique_sectors = sorted(baseline_sector_avg.keys())
    unique_sectors = unique_sectors[:8] + ['Real Estate', 'Technology', 'Utilities']
    
    # main plot definition
    fig, axes = plt.subplots(11, 1, figsize= (24, 80), facecolor= '#FAF9F6')
    fig.subplots_adjust(
        top=0.98, 
        bottom=0.02, 
        hspace=0.08
    )

    # for each sector
    for i, sec in enumerate(unique_sectors):

        ax = axes[i]
        ax.set_ylim(-60, 60)

        # horizontal tick lines
        ax.hlines(y=10, xmin=-0.7, xmax=27.7, colors='#E1E1DD', linewidth= 0.8, zorder= 0)
        ax.hlines(y=20, xmin=-0.7, xmax=27.7, colors='#C8C8C7', linewidth= 1.3, zorder= 0)
        ax.hlines(y=30, xmin=-0.7, xmax=27.7, colors='#E1E1DD', linewidth= 0.8, zorder= 0)
        ax.hlines(y=40, xmin=-0.7, xmax=27.7, colors='#C8C8C7', linewidth= 1.3, zorder= 0)
        ax.hlines(y=50, xmin=-0.7, xmax=27.7, colors='#E1E1DD', linewidth= 0.8, zorder= 0)
        ax.hlines(y=-10, xmin=-0.7, xmax=27.7, colors='#E1E1DD', linewidth= 0.8, zorder= 0)
        ax.hlines(y=-20, xmin=-0.7, xmax=27.7, colors='#C8C8C7', linewidth= 1.3, zorder= 0)
        ax.hlines(y=-30, xmin=-0.7, xmax=27.7, colors='#E1E1DD', linewidth= 0.8, zorder= 0)
        ax.hlines(y=-40, xmin=-0.7, xmax=27.7, colors='#C8C8C7', linewidth= 1.3, zorder= 0)


        # relative text (mirrored, both at left and right margins)
        
        ax.text(x= -1.4, y=1, s="0%", c= 'black', ha='left', weight= 550)
        ax.text(x= -1.8, y=19.2, s="+20%", c= '#C8C8C7', ha='left', weight= 550)
        ax.text(x= -1.8, y=39.2, s="+40%", c= '#C8C8C7', ha='left', weight= 550)
        ax.text(x= -1.8, y=-20.8, s="-20%", c= '#C8C8C7', ha='left', weight= 550)
        ax.text(x= -1.8, y=-40.8, s="-40%", c= '#C8C8C7', ha='left', weight= 550)

        ax.text(x= 28.8, y=19.2, s="+20%", c= '#C8C8C7', ha='right', weight= 550)
        ax.text(x= 28.8, y=39.2, s="+40%", c= '#C8C8C7', ha='right', weight= 550)
        ax.text(x= 28.8, y=-20.8, s="-20%", c= '#C8C8C7', ha='right', weight= 550)
        ax.text(x= 28.8, y=-40.8, s="-40%", c= '#C8C8C7', ha='right', weight= 550)

        # obtain sector values
        sec_values = [values[i] for i in range(len(sectors)) if sectors[i] == sec]

        # convert sector values in % change from sector baseline
        sec_values_lday_perc = [((values[i] - baseline_sector_avg[sec]) / baseline_sector_avg[sec]) * 100 for i in range(len(sectors)) if sectors[i] == sec]
        
        # convert sector values in % change from previous quarter value
        diff_Q = [0] + [((sec_values[i] - sec_values[i-1]) / sec_values[i-1]) * 100 for i in range(1, len(sec_values))]
        
        colors = ["#4C98CE" if diff_Q[j] > 0 else "#D06A4C" for j in range(len(diff_Q))]
        
        # plot quarterly change bars
        bars2 = ax.bar(range(len(diff_Q)), diff_Q, color= colors)
        
        # plot horizontal lines for change from baseline if needed
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

        # x ticks and labels: quarter number, and overarching year
        for x, yr in [(1, '2019'), (5, '2020'), (9, '2021'), (13, '2022'), (17, '2023'), (21, '2024'), (25, '2025')]:
            
            ax.hlines(y=-51.7, xmin= x-1.05, xmax= x+2.05, colors= 'black', linewidth= 1.6, zorder= 4)

            ax.text(
                x=x+0.5, 
                y=-53, 
                s=yr,
                ha='center',
                va='top', size= 'large', weight= 550, zorder= 4)

        # 0 line and x-axis line
        ax.hlines(y=0, xmin=-1.3, xmax=28.3, colors='black', linewidth= 1.6, zorder= 4)
        ax.hlines(y=-47, xmin=-1.3, xmax=28.3, colors='black', linewidth= 1.6, zorder= 4)
        
        # add sector name
        ax.text(x=0, y=+34, s=sec, c= 'black', ha='left', size= 'x-large', weight= 'heavy')
        ax.axis('off')
        
    return fig

# -------------------------------------------------------------------------------

def plot_spiral(data_path="datasets/df_spiral.csv", vol_pct=20, price_pct=20):
    import pandas as pd
    from matplotlib.collections import LineCollection
    from adjustText import adjust_text
    import matplotlib.patheffects as path_effects
    import matplotlib.colors as mcolors
    from matplotlib.animation import FuncAnimation
    # Loading data
    if data_path is None:
        data = f"data/global_vol{vol_pct}_price{price_pct}.csv"
        save_path = f"figs/spiral-vol{vol_pct}-price{price_pct}.mp4"

        df = pd.read_csv(data)

        # Grouping to get average close per day
        df = df.loc[:, ["report_date", "close (%)", "close"]].groupby("report_date").mean()

        # Daily change
        df.reset_index(inplace=True)
        df["change_day"] = df["close"] - df["close"].shift(1, fill_value=0)
        df.loc[0, "change_day"] = 0
        df["report_date"] = pd.to_datetime(df["report_date"])

        # AI helped make this code
        # ------------------------------------------------------------
        # Yearly Change
        df['Target_Date'] = df['report_date'] - pd.DateOffset(years=1)

        df_lookup = df[['report_date', 'close']].rename(
            columns={'report_date': 'Matched_Date', 'close': 'close_1yr_ago'}
        )

        df = pd.merge_asof(
            df,
            df_lookup,
            left_on='Target_Date',
            right_on='Matched_Date',
            direction='backward',
            tolerance=pd.Timedelta(days=4)
        )
        df.drop(columns=["Target_Date", "Matched_Date"], inplace=True)

        # Monthly change
        df['Target_Date'] = df['report_date'] - pd.DateOffset(months=1)

        df_lookup = df[['report_date', 'close']].rename(
            columns={'report_date': 'Matched_Date', 'close': 'close_1mo_ago'}
        )

        df = pd.merge_asof(
            df,
            df_lookup,
            left_on='Target_Date',
            right_on='Matched_Date',
            direction='backward',
            tolerance=pd.Timedelta(days=4)
        )
        df.drop(columns=["Target_Date", "Matched_Date"], inplace=True)
        # ------------------------------------------------------------

        df["change_year"] = df["close"] - df["close_1yr_ago"]
        df["change_month"] = df["close"] - df["close_1mo_ago"]

        # Close since beginning
        df["close (%)"] = (df["close"] - df.loc[0,"close"]) / df.loc[0,"close"] * 100

        # Seperate month and day for rotation of data point
        df['month'] = pd.DatetimeIndex(df['report_date']).month
        df["day"] = pd.DatetimeIndex(df['report_date']).day

        # Rotation prep based on month 
        month_to_degree = {m: (m - 1) * 30 for m in range(1, 13)}
        df["month_rotation"] = df["month"].map(month_to_degree.get)

        # Get max and min day of month
        df['report_date'] = pd.to_datetime(df['report_date'])
        df['year'] = df['report_date'].dt.year

        month_bounds = df.groupby(['year', 'month'])['day'].agg(['min', 'max']).reset_index()
        month_bounds.rename(columns={'min': 'min_day', 'max': 'max_day'}, inplace=True)

        df = df.merge(month_bounds, on=['year', 'month'])

        # AI helped make this code
        # ------------------------------------------------------------
        # Get month progress from 0 to 1 and compute the total rotation for datapoint based on month and month progress
        df['day_progress'] = (df['day'] - df['min_day']) / (df['max_day'] - df['min_day']).replace(0, 1)
        df['day_degrees'] = df['month'].map(month_to_degree) + (df['day_progress'] * 30)
        # ------------------------------------------------------------

        # Cleanup
        df = df.drop(columns=['min_day', 'max_day', 'day_progress'])

        # Compute the zero point, so that distance from centre not negative and add a little spacing
        shift_zero = abs(df["close (%)"].min()) + 5
        shift_zero = (int(shift_zero/10)+1)*10 # Round up to the tens to add more spacing
        df["distance_from_center"] = df["close (%)"] + shift_zero # distance from centre

        # compute the vector positions of points based on distance from centre and rotation 
        from numpy import cos, sin, radians
        df["x"] = df["distance_from_center"] * sin(radians(df["day_degrees"]))
        df["y"] = df["distance_from_center"] * cos(radians(df["day_degrees"]))
        # get continous time
        df["cont_time"] = df.index
    else:
        df = pd.read_csv(data_path)
        month_to_degree = {m: (m - 1) * 30 for m in range(1, 13)}
        shift_zero = abs(df["close (%)"].min()) + 5
        shift_zero = (int(shift_zero/10)+1)*10
        save_path = f"spiral-vol{vol_pct}-price{price_pct}.mp4"
        df["report_date"] = pd.to_datetime(df["report_date"])

    #Plot Settings
    plt.rc('font', family='sans-serif', serif=["Open Sans"])
    
    minor_line_settings = ("#C8C8C7", 0.8, 1, "-") 
    major_line_settings = ("#000000", 1.3, 1, "-") 
    data_line_settings = ("twilight_shifted", 2.5, (0.75, 1), "-") 
    facecolor ="#FAF9F6"
    text_outline_settings = (facecolor, 1.5) 
    step = 1  # Step through frames to set animation speed
    color_base = df["change_day"] # base of cmap
    # Colors for cmap
    red = "#D06A4C"
    grey="#898989"
    green = "#4C98CE"


    # Dynamic color settings
    GREY_COLOR_RGB = mcolors.to_rgb("#E1E3E4")  # Faded color
    WINDOW_SIZE = 300                    # The sliding window in days/rows

    x = df["x"].values
    y = df["y"].values

    # AI helped make this code
    # ------------------------------------------------------------
    # Reshape points for LineCollection
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    # ------------------------------------------------------------

    # Setup cmap for daily gain or losses
    colors_list = [red, grey, green]
    cmap = mcolors.LinearSegmentedColormap.from_list("RdGrGn", colors_list)
    norm = mcolors.CenteredNorm(halfrange=2)
    
    # Compute colors and assign to segments
    rgba_values = cmap(norm(color_base))
    segment_colors = rgba_values[:-1]

    # Setup Axes
    fig, ax = plt.subplots(figsize=(13, 10), facecolor=facecolor)
    ax_bar = fig.add_axes([0.88, 0.05, 0.03, 0.9], facecolor=facecolor )

    # Draw static elements; get max distance and month angles
    max_dist = df['distance_from_center'].max()
    angles = list(month_to_degree.values())

    # AI helped make this code
    # ------------------------------------------------------------
    # Helper for rotating vector based on degree
    def rotate_vector(vector, angle_degrees):
        theta = np.radians(angle_degrees)
        c, s = np.cos(theta), np.sin(theta)
        R = np.array(((c, -s), (s, c)))
        return vector @ R.T
    # ------------------------------------------------------------

    # Get radii for rings
    radii = np.arange(-round(shift_zero, -1), round(max_dist, -1), 10) + shift_zero
    radii = radii[radii > 0]
    raddi_to_idx = {r: i for i, r in enumerate(radii)}

    # Setup for  Month labeling
    month_texts = []
    months = ['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D']

    # Month axis ring index and last displayed ring index
    ring_num = raddi_to_idx[round(df[df["x"] == 0]["y"].max(), -1) + shift_zero] - 2
    last_ring = -2

    # AI helped make this code
    # ------------------------------------------------------------
    # plot month lines and labels
    for i, angle in enumerate(angles):
        start_point = np.array([0, 0]) # Start line in centre
        end_point = rotate_vector(np.array([0, radii[last_ring-1]+2]), -angle) # end line at last ring and rotate
        
        ax.plot([start_point[0], end_point[0]], [start_point[1], end_point[1]], 
                color=minor_line_settings[0], alpha=minor_line_settings[2], 
                lw=minor_line_settings[1], linestyle=minor_line_settings[3], zorder=0, clip_on=False)
        
        # Month text
        text_point = rotate_vector(np.array([0, radii[ring_num]+3]), -angle) 
        
        t = ax.text(text_point[0], text_point[1], str(months[i]), color=major_line_settings[0],
                    fontsize=10, fontweight='bold', alpha=major_line_settings[2], ha='center', va='center')
        t.set_path_effects([path_effects.Stroke(linewidth=text_outline_settings[1], foreground=text_outline_settings[0]), path_effects.Normal()]) # Add outline for better visibility
        month_texts.append(t)
        
    # Add percentage labels    
    for i, r in enumerate(radii[:last_ring]):
        x_val, y_val = rotate_vector(np.array([0, r+3]), -angles[2]+angles[1]/2)
        label = f"{int(round(r - shift_zero))}%"
        if (r == 0 + shift_zero) or i == ring_num: # zero line and last line
            t = ax.text(x_val, y_val, label, color=major_line_settings[0], fontsize=8, fontweight='bold',
                        alpha=major_line_settings[2], ha='center', va='center')
        elif (r == -10 + shift_zero) or (r == 10 + shift_zero) or (i == ring_num-1) or (i == ring_num+1): # one before and after highlighted rings
            t = ax.text(x_val, y_val, label, color=minor_line_settings[0], fontsize=8, fontweight='bold',
                        alpha=minor_line_settings[2], ha='center', va='center')
        t.set_path_effects([path_effects.Stroke(linewidth=text_outline_settings[1], foreground=text_outline_settings[0]), path_effects.Normal()]) # Add outline for better visibility
    
    # Plot rings
    for i, r in enumerate(radii[:last_ring]):
        use_major = (r == radii[ring_num]) # Major when month axis ring
        circle = plt.Circle((0, 0), r, color=major_line_settings[0] if use_major else minor_line_settings[0],
                            fill=False, linestyle=major_line_settings[3] if use_major else minor_line_settings[3],
                            linewidth=major_line_settings[1] if use_major else minor_line_settings[1],
                            alpha=major_line_settings[2] if use_major else minor_line_settings[2], zorder=0, clip_on=False)
        ax.add_patch(circle)

    circle = plt.Circle((0, 0), shift_zero, color=major_line_settings[0], fill=False,
                        linestyle=major_line_settings[3], linewidth=major_line_settings[1],
                        alpha=major_line_settings[2], zorder=0, clip_on=False) # Zero ring
    ax.add_patch(circle)
    # ------------------------------------------------------------

    # Initialize line collection
    lc = LineCollection(segments[0:0], colors=segment_colors[0:0])
    lc.set_linewidth(data_line_settings[1])
    ax.add_collection(lc)
    lc.set_path_effects([
        path_effects.withStroke(linewidth=5, foreground=text_outline_settings[0])
    ]) # Add outline for visibility

    # Prepare year annotations
    first_year_indices = df.drop_duplicates(subset='year', keep='first').index
    texts = []
    annotation_objects = []

    # AI helped make this code
    # ------------------------------------------------------------
    for idx in first_year_indices:
        year = df.loc[idx, 'year']
        val = df.loc[idx, "change_year"]
        x_pos = df.loc[idx, 'x']
        x_pos_text = df.loc[idx, 'x'] + 1.5
        y_pos = df.loc[idx, 'y']
        y_pos_text = df.loc[idx+3, 'y'] if (idx+3) in df.index else df.loc[idx, 'y']
        alpha = rgba_values[:, 3][idx]
        point_color = cmap(norm(val)) if idx > 0 else cmap(norm(0))

        tick_length = 4
        tick_line, = ax.plot([x_pos, x_pos], [y_pos - tick_length/2, y_pos + tick_length/2], 
                            color=point_color, lw=1.5, zorder=10, alpha=alpha)
        
        t = ax.text(x_pos_text, y_pos_text, str(year), color=point_color, fontsize=10, fontweight='bold', alpha=alpha)
        t.set_path_effects([path_effects.Stroke(linewidth=text_outline_settings[1], foreground=text_outline_settings[0]), path_effects.Normal()]) # Add outline for better visibility
        
        texts.append(t)
        annotation_objects.append({'idx': idx, 'tick': tick_line, 'text': t, 'arrow': None})

    adjust_text(texts, ax=ax) # Adjust positions to prevent overlap

    for ann in annotation_objects: # Set annotations invisible
        ann['tick'].set_visible(False)
        ann['text'].set_visible(False)
    # ------------------------------------------------------------


    # Set view limits and posititons
    outer_limit = radii[last_ring-1]
    ax.set_xlim(-outer_limit+1, outer_limit+1)
    ax.set_ylim(-outer_limit+1, outer_limit+1)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.subplots_adjust(left=0.01, right=0.84, top=0.98, bottom=0.02)

    # Configure side bar
    bar_data = df["close (%)"].values
    max_abs_val = max(abs(bar_data.min()), abs(bar_data.max()))

    # AI helped make this code
    # ------------------------------------------------------------
    # Format bar axis bounds and aesthetics
    ax_bar.set_xlim(-0.8, 1.2)
    ax_bar.set_ylim(-max_abs_val * 1.15, max_abs_val * 1.15)
    ax_bar.spines['top'].set_visible(False)
    ax_bar.spines['right'].set_visible(True)
    ax_bar.spines['right'].set_color(minor_line_settings[0])
    ax_bar.spines['left'].set_visible(False)
    ax_bar.spines['bottom'].set_visible(False)
    ax_bar.get_xaxis().set_visible(False)
    ax_bar.tick_params(axis='y', labelsize=8, colors=minor_line_settings[0]) # y-axis ticks
    ax_bar.yaxis.tick_right()
    ax_bar.yaxis.set_label_position("right")

    # Zero reference line
    ax_bar.axhline(0, color=major_line_settings[0], linewidth=0.8, linestyle=major_line_settings[3], zorder=2) # Zero line

    # Initialize dynamic bar, range markers, and labels
    bar_rect = ax_bar.bar(0, 0, width=2, color=major_line_settings[0], zorder=1)[0]
    line_min, = ax_bar.plot([-1, 1], [0, 0], color=red, linestyle=major_line_settings[3], linewidth=major_line_settings[1], zorder=3)
    line_max, = ax_bar.plot([-1, 1], [0, 0], color=green, linestyle=major_line_settings[3], linewidth=major_line_settings[1], zorder=3)

    # Static layout text containers to display numerical values alongside markers
    text_min = ax_bar.text(-1, 0, '', color=red, fontsize=8, fontweight='bold', va='center', ha='right')
    text_max = ax_bar.text(-1, 0, '', color=green, fontsize=8, fontweight='bold', va='center', ha='right')

    # Heler to get dynamic colors
    def get_dynamic_colors(frame, base_colors, grey_rgb, window):
        current_colors = base_colors[:frame].copy()
        if frame == 0:
            return current_colors
        
        start_idx = max(0, frame - window)
        if start_idx > 0:
            current_colors[:start_idx, :3] = grey_rgb # Grey from line start to beginning of color
            
        gradient_len = frame - start_idx
        if gradient_len > 0:
            factors = np.ones((gradient_len, 1)) # Setup factors array as full color
            if gradient_len > 100:
                factors[:-100] = np.linspace(0, 1, gradient_len - 100).reshape(-1, 1) # Make grafient factors for first one hundred
            original_rgb = current_colors[start_idx:frame, :3] # Get original colors
            blended_rgb = (1 - factors) * np.array(grey_rgb) + factors * original_rgb # blend grey to color
            current_colors[start_idx:frame, :3] = blended_rgb 
            
        return current_colors # return new dynamic color array

    final_dot = ax.scatter([], [], s=20, zorder=5) # Highlight the current point


    # Aimation update
    def update(frame):
        current_segments = segments[:frame]
        
        # Generate the sliding dynamic colors for this frame
        current_colors = get_dynamic_colors(
            frame=frame, 
            base_colors=segment_colors, 
            grey_rgb=GREY_COLOR_RGB, 
            window=WINDOW_SIZE
        )

        # Set line segments
        lc.set_segments(current_segments)
        lc.set_colors(current_colors[1:])
        
        # Update side bar statistics
        idx = min(frame, len(bar_data) - 1)
        current_val = bar_data[idx]
        
        # Compute running historical boundaries up to current frame
        historical_subset = bar_data[:idx + 1]
        hist_min = historical_subset.min()
        hist_min_idx = historical_subset.argmin()
        hist_max = historical_subset.max()
        hist_max_idx = historical_subset.argmax()
        
        # Update the bar metrics
        bar_rect.set_height(current_val)
        bar_rect.set_color(cmap(norm(current_val)))
        
        # Position and adjust horizontal threshold lines
        line_min.set_ydata([hist_min, hist_min])
        line_max.set_ydata([hist_max, hist_max])
        
        # Update text values next to thresholds
        text_min.set_position((-1, hist_min))
        text_min.set_text(f"""Min\n{hist_min:+.1f}%\n{df.loc[hist_min_idx, 'report_date'].strftime("%d/%m/%Y")}""")
        
        text_max.set_position((-1, hist_max))
        text_max.set_text(f"""Max\n{hist_max:+.1f}%\n{df.loc[hist_max_idx, 'report_date'].strftime("%d/%m/%Y")}""")
        
        # Toggle year markers
        for ann in annotation_objects:
            is_visible = (frame >= ann['idx'])
            ann['tick'].set_visible(is_visible)
            ann['text'].set_visible(is_visible)

    # Configure the animation steps
    frames_indices = list(range(1, len(segments) + 1, step))
    if frames_indices[-1] != len(segments):
        frames_indices.append(len(segments))

    ani = FuncAnimation(
        fig, update, 
        frames=frames_indices, 
        interval=20, 
        blit=False, 
        repeat=False
    ) # create animation
    # ------------------------------------------------------------


    ani.save(save_path, writer='ffmpeg', dpi=300) # Save animation as video
