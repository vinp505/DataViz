import matplotlib.pyplot as plt
import numpy as np
import base64
from io import StringIO

def get_svg_html(fig):
    """Saves a Matplotlib figure as an SVG string and returns it as a Base64 HTML tag."""
    # 1. Save figure to an in-memory text buffer instead of disk
    imgdata = StringIO()
    fig.savefig(imgdata, format="svg", bbox_inches="tight")
    imgdata.seek(0)
    svg_string = imgdata.getvalue()
    
    # 2. Encode the SVG XML string to Base64
    b64 = base64.b64encode(svg_string.encode('utf-8')).decode("utf-8")
    
    # 3. Create a responsive HTML img tag
    html = f'<div style="text-align: center;"><img src="data:image/svg+xml;base64,{b64}" style="width: 100%; height: auto;"/></div>'
    return html

def get_scrollable_svg_html(fig, height=500):
    """Saves a figure as SVG and wraps it in a scrollable HTML container."""
    imgdata = StringIO()
    fig.savefig(imgdata, format="svg", bbox_inches="tight")
    imgdata.seek(0)
    svg_string = imgdata.getvalue()
    
    b64 = base64.b64encode(svg_string.encode('utf-8')).decode("utf-8")
    
    # Wrap the image in a container with a fixed height and a vertical scrollbar
    html = f"""
    <div style="
        height: {height}px; 
        overflow-y: auto; 
        border: 2px solid #E1D6B6; 
        border-radius: 8px;
        background-color: #FAF9F6;
    ">
        <img src="data:image/svg+xml;base64,{b64}" style="width: 100%; height: auto; display: block;"/>
    </div>
    """
    return html

def get_scrollable_svg_html_inverted(fig, height=500):
    """Saves a figure as SVG and wraps it in a scrollable container initialized at the bottom."""
    imgdata = StringIO()
    fig.savefig(imgdata, format="svg", bbox_inches="tight")
    imgdata.seek(0)
    svg_string = imgdata.getvalue()
    
    b64 = base64.b64encode(svg_string.encode('utf-8')).decode("utf-8")
    
    # By using flex-direction: column-reverse, the scrollbar starts at the bottom
    html = f"""
    <div style="
        height: {height}px; 
        overflow-y: auto; 
        display: flex;
        flex-direction: column-reverse;
        border: 2px solid #E1D6B6; 
        border-radius: 8px;
        background-color: #FAF9F6;
    ">
        <img src="data:image/svg+xml;base64,{b64}" style="width: 100%; height: auto; display: block;"/>
    </div>
    """
    return html

def generate_week_lineplot_title(color_list):

    fig, axes = plt.subplots(1, 4, facecolor= '#FAF9F6', figsize= (64, 3))
    for i, ax in enumerate(axes.flatten()):

        ax.axis('off')
        
        if i <= 3:
            ax.set_xlim(-5, 5)
            ax.set_ylim(-1, 1)
            ax.text(x= 0, y= -0.8, s= f"Stock {i+1}", c= '#000000', ha= 'center', weight= 550, size= 50)
            #ax.text(x= 0, y= -0.8, s= f"Stock {i+1}", c= color_list[i], ha= 'center', weight= 550, size= 50)
            ax.hlines(y= -1, xmin= -1.5, xmax= 1.5, colors= 'black', linewidth= 8, clip_on= False)
    
    return fig

def generate_week_lineplot(df_list, color_list, seed):
    
    fig, axes = plt.subplots(1, 4, facecolor= "#FAF9F6", figsize= (64, 16))

    w = seed  # np.random.randint(14, 1759)
    df_week_list = []
    close_min, close_max = np.inf, -np.inf
    stock_min_peak, stock_max_peak = None, None
    close_min_final, close_max_final = np.inf, -np.inf
    stock_min_final, stock_max_final = 0, 0

    for i, df in enumerate(df_list):
        df_week = df.iloc[w-14 : w].copy()
        baseline = df_week['close'].values[0]
        df_week['week close (%)'] = ((df_week['close'] - baseline) / baseline) * 100
        
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
            
        df_week_list.append(df_week)
    

    for i, ax in enumerate(axes):

        ax.axis('off')

        ax.set_ylim(close_min - 1, close_max + 1)
        #ax.set_xlim(-2, len(df_week))

        df_week = df_week_list[i]

        # ROUND VALS TO INTEGERS
        #ax.text(x= len(df_week)/2, y = close_max + abs(close_max*0.2), s= f"Stock {i+1}", c= color_list[i%4], ha= 'center', weight= 550, size= 50)
        ax.hlines(y = round(close_min*0.8, 0)/2, xmin= -1, xmax = len(df_week), linewidth= 3, colors= '#C8C8C7', clip_on=False)
        ax.hlines(y = round(close_min*0.8, 0), xmin= -1, xmax = len(df_week), linewidth= 3, colors= '#C8C8C7')
        ax.hlines(y = round(close_max*0.8, 0)/2, xmin= -1, xmax = len(df_week), linewidth= 3, colors= '#C8C8C7')
        ax.hlines(y = round(close_max*0.8, 0), xmin= -1, xmax = len(df_week), linewidth= 3, colors= '#C8C8C7')


        if close_min*0.4 < -0.8 or (close_max - close_min) < 15:
            ax.text(x=len(df_week)+2.3, y=round(close_min*0.8, 0) - abs(close_min)*0.01, s=f"{(close_min*0.8):.0f}%", c= '#C8C8C7', ha='center', weight= 550, size= 35)
        
        if close_max*0.4 > 0.8 or (close_max - close_min) < 15:
            ax.text(x=len(df_week)+2.3, y=round(close_max*0.8, 0) - abs(close_max)*0.01, s=f"{'+' * (float(close_max) > 0)}{(close_max*0.8):.0f}%", c= '#C8C8C7', ha='center', weight= 550, size= 35)
        ax.text(x= len(df_week)+2.3, y= -0.1, s= '0%', c= 'black', ha='center', weight= 550, size= 35)
            
        ax.hlines(y= 0, xmin= -1, xmax= len(df_week), linewidth= 5, colors= 'black')
        ax.scatter([0, 13], [0, df_week['week close (%)'].values[-1]], c= color_list[i], s= 300, zorder= 5)
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
        ax.text(x=-15, y=5, s="0%", c= 'black', ha='center', weight= 550) #, ha='center', family='serif', fontname='Arial')
        ax.text(x=-15, y=55, s=" +50%", c= '#C8C8C7', ha='center', weight= 550)
        ax.text(x=-15, y=105, s="+100%", c= '#C8C8C7', ha='center', weight= 550)
        ax.text(x=-15, y=155, s="+150%", c= '#C8C8C7', ha='center', weight= 550)
        ax.text(x=-15, y=-45, s=" -50%", c= '#C8C8C7', ha='center', weight= 550)
        ax.text(x=-15, y=-95, s="-100%", c= '#C8C8C7', ha='center', weight= 550)

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