import matplotlib.pyplot as plt
import numpy as np
import base64
import matplotlib.colors as mcolors
from io import StringIO
import regex as re

def get_aligned_text_row(text: list | str, alignments: list | str, left_padding="6.5%", right_padding="3.5%", font_size= "16", margin_top= "20", margin_bottom= "20", line_width = None, line_thickness= None, line_fade=True):
    """Generates a horizontally aligned row of text elements with zero markdown indentation risk."""
    if isinstance(text, str):
        text = [text]
    if isinstance(alignments, str):
        alignments = [alignments]
    assert len(text) == len(alignments)
    items_list = []
    for i, t in enumerate(text):
        # Determine the line's margin and gradient direction based on alignment
        if alignments[i] == "right":
            direction = "to left"
            margin_style = "margin: 4px 0 0 auto;"
        elif alignments[i] == "center":
            direction = "to right"
            margin_style = "margin: 4px auto 0 auto;"
        else: # "left"
            direction = "to right"
            margin_style = "margin: 4px 0 0 0;"
            
        # Apply either a fading linear-gradient or a solid background color
        if line_fade:
            background_style = f"background: linear-gradient({direction}, #000000, transparent);"
        else:
            background_style = f"background-color: #000000;"
            
        # Build the line HTML block if a width is specified
        line_html = f'<div style="width: {line_width}; height: {line_thickness}; {background_style} {margin_style}"></div>' if line_width else ''
        
        # Wrap the text and the line in a vertical flex block
        item = f"""
        <div style="flex: 1; text-align: {alignments[i]}; font-family: sans-serif; font-weight: bold; font-size: {font_size}px; color: #000000; display: flex; flex-direction: column;">
            <span>{t}</span>
            {line_html}
        </div>
        """
        items_list.append(item)
        
    # Flatten the HTML into a single line to prevent Streamlit Markdown bugs
    items_html = "".join(items_list).replace("\n", "").replace("  ", "")
    
    # Wrap in the main flex container
    html = f'<div style="display: flex; justify-content: space-between; width: 100%; padding-left: {left_padding}; padding-right: {right_padding}; box-sizing: border-box; margin-bottom: {margin_bottom}px; margin-top: {margin_top}px;">{items_html}</div>'
    html = html.replace("\n", "").replace("  ", "")
    
    return html

def get_open_scrollable_svg_html(fig, height=500, padding_topbottom= "10", padding_leftright = "20"):
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
        border-left: 3.5px solid #000000;
        border-radius: 8px;
        background-color: #FAF9F6;
        padding: {padding_topbottom}px {padding_leftright}px;             /* Adds a clean 15px gap on all sides */
        box-sizing: border-box;    /* Prevents padding from increasing container height */
    ">
        <img src="data:image/svg+xml;base64,{b64}" style="width: 100%; height: auto; display: block;"/>
    </div>

    <div style="
            position: absolute; 
            left: -30px; 
            top: 50%; 
            transform: translateY(-50%); 
            font-size: 24px; 
            color: #000000; 
            pointer-events: none; 
            opacity: 1;
            user-select: none;
        ">
            ⬍
        </div>
    """
    return html

def get_open_scrollable_svg_html_inverted(fig, height=500):
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
        border-left: 3.5px solid #000000;
        border-radius: 8px;
        background-color: #FAF9F6;
    ">
        <img src="data:image/svg+xml;base64,{b64}" style="width: 100%; height: auto; display: block;"/>
    </div>

    <div style="
            position: absolute; 
            left: -30px; 
            top: 50%; 
            transform: translateY(-50%); 
            font-size: 24px; 
            color: #000000; 
            pointer-events: none; 
            opacity: 1;
            user-select: none;
        ">
            ⬍
        </div>
    """
    return html

def get_interactive_svg_html(fig):
    """Saves a Matplotlib figure as an SVG and wraps it with svg-pan-zoom.js inside an HTML document."""
    # 1. Save figure to an in-memory text buffer
    imgdata = StringIO()
    fig.savefig(imgdata, format="svg", bbox_inches="tight")
    imgdata.seek(0)
    svg_string = imgdata.getvalue()
    
    # 2. Extract only the raw <svg>...</svg> XML tags (ignoring XML metadata)
    svg_match = re.search(r'<svg.*</svg>', svg_string, re.DOTALL)
    svg_clean = svg_match.group(0) if svg_match else svg_string

    # 3. Inject an ID attribute so our JS library can select it, and set full scale
    svg_clean = re.sub(
        r'<svg', 
        '<svg id="interactive-svg" style="width: 100%; height: 100%;"', 
        svg_clean, 
        count=1
    )
    
    # 4. Build the complete HTML page with the svg-pan-zoom CDN script
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <!-- Load the lightweight panning/zooming library -->
        <script src="https://cdn.jsdelivr.net/npm/svg-pan-zoom@3.6.1/dist/svg-pan-zoom.min.js"></script>
        <style>
            html, body {{
                margin: 0;
                padding: 0;
                width: 100%;
                height: 100%;
                overflow: hidden;
                background-color: #FAF9F6; /* Matches your warm background */
            }}
            #container {{
                width: 100%;
                height: 100%;
                border: 2px solid #E1D6B6;
                border-radius: 8px;
                box-sizing: border-box;
            }}
        </style>
    </head>
    <body>
        <div id="container">
            {svg_clean}
        </div>
        <script>
            window.onload = function() {{
                // Initialize the pan-zoom behavior on our SVG
                var panZoomInstance = svgPanZoom('#interactive-svg', {{
                    zoomEnabled: true,
                    controlIconsEnabled: true, // Shows subtle on-screen zoom overlay controls
                    fit: true,
                    center: true,
                    minZoom: 0.1,
                    maxZoom: 30,
                    zoomScaleSensitivity: 0.2 // Controls scroll wheel sensitivity (soft zoom)
                }});
                
                // Recalculate dimensions cleanly if the user resizes their browser
                window.addEventListener('resize', function() {{
                    panZoomInstance.resize();
                    panZoomInstance.fit();
                    panZoomInstance.center();
                }});
            }};
        </script>
    </body>
    </html>
    """
    return html_content

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

    # ── layout ──────────────────────────────────────────────────────────────
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
    red, grey, green = '#FAAC68', FACE, '#5A9CB5'
    cmap = mcolors.LinearSegmentedColormap.from_list('RdGrGn', [red, grey, green])

    im = ax.imshow(
        sector_mom.values,
        aspect='auto', cmap=cmap,
        vmin=-vlim, vmax=vlim,
        interpolation='none',
    )

    # ── y-axis ───────────────────────────────────────────────────────────────
    # ax.set_yticks(range(n_sectors))
    # ax.set_yticklabels(sector_mom.index, fontsize=10, va='center',
    #                    fontfamily='monospace')
    # ax.tick_params(axis='y', length=0, pad=6)

    # ── x-axis (top) ─────────────────────────────────────────────────────────
    # step = 365
    # tick_pos = list(range(0, n_mo, step))
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
    
    # ax.vlines(x= len(dates)-11, ymin= -0.5, ymax= 30, colors= 'black', linewidth= 2)
    # ax.set_xticks(tick_pos)
    # ax.set_xticklabels(
    #     x_labels,
    #     fontsize=8, ha='center', rotation=0, color='#444444'
    # )
    # ax.set_xticklabels(
    #     [dates[i].strftime('%y') for i in tick_pos],
    #     fontsize=8, ha='center', rotation=0, color='#444444'
    # )
    ax.xaxis.set_ticks_position('top')
    ax.xaxis.set_label_position('top')
    ax.tick_params(axis='x', length=0, pad=3)

    # ── thin row separators ───────────────────────────────────────────────────
    for i in range(1, n_sectors):
        ax.axhline(i - 0.5, color=FACE, linewidth=1.2, zorder=3)

    # ── spines off ───────────────────────────────────────────────────────────
    for sp in ax.spines.values():
        sp.set_visible(False)

    # ── header (all elements expressed in absolute inches above T) ────────────
    # yin converts inches-above-T → figure fraction (always > T, never touches heatmap)
    #def yin(inches): return T + inches / fig_h

    #L = 0.18   # left margin (matches subplots_adjust left)

    # title: 1.2 in above T
    # fig.text(L, yin(1.20), 'Sector Heatmap',
    #          fontsize=16, fontweight='bold', va='bottom', ha='left', color='#1a1a1a')

    # subtitle: 0.82 in above T
    # date_range = f"{dates[0].strftime('%b %Y')} – {dates[-1].strftime('%b %Y')}"
    # fig.text(L, yin(0.82), f'1-month % change in avg sector close price  ·  {date_range}',
    #          fontsize=9, va='bottom', ha='left', color='#666666')

    # colorbar: 0.55 in above T, anchored to the RIGHT side of the figure
    # cbar_bottom = yin(0.55)
    # cbar_h_frac = 0.20 / fig_h
    # cbar_ax = fig.add_axes([0.63, cbar_bottom, 0.32, cbar_h_frac])
    # cb = fig.colorbar(im, cax=cbar_ax, orientation='horizontal')
    # cb.set_ticks([-vlim, 0, vlim])
    # cb.set_ticklabels([f'−{vlim:.0f}%', '0', f'+{vlim:.0f}%'])
    # cb.ax.tick_params(labelsize=7.5, length=0)
    # cb.outline.set_visible(False)

    # ── footer ───────────────────────────────────────────────────────────────
    # fig.text(L, 0.008,
    #          f'Source: InflAdj_Data_90th_2019_2025.csv  ·  {n_sectors} sectors  ·  30 trading-day rolling return',
    #          fontsize=7.5, color='#aaaaaa', va='bottom', ha='left')

    # out = save_path or 'heatmap_sector_averages.png'
    # plt.savefig(out, dpi=150, bbox_inches='tight', facecolor=FACE)
    # print(f'Saved → {out}')
    #plt.show()
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
        

        colors = ["#5A9CB5" if diff_Q[j] > 0 else "#FAAC68" for j in range(len(diff_Q))]
        
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