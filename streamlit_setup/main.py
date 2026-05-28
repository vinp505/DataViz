"""
Main script to render and effectively run the webpage.
"""

# -------------------------------------------------------------------------------

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

from load_data import lineplot_load_data, heatmap_load_data, barplot_load_data
from generate_plot import generate_week_lineplot, generate_final_lineplot, generate_heatmap, generate_barplot
from html_functions import get_aligned_text_row, get_svg_html, get_open_scrollable_svg_html_inverted, get_open_scrollable_svg_html
from pathlib import Path

current_dir = Path(__file__).resolve().parent

# -------------------------------------------------------------------------------

st.set_page_config(layout="wide")

# !! Gemini code skeleton - parameters (mainly colors) manually set
# -----------------------
st.markdown("""
    <style>
    div[data-testid="stButton"] button {
        background-color: #BF8755 !important;
        color: #FAF9F6 !important;
        border: 2px solid #BF8755 !important;
        border-radius: 6px !important;
        font-weight: bold !important;
        transition: background-color 0.5s ease, border-color 0.5s ease !important;
    }
    
    .stApp, .stApp *:not(input):not(textarea) {
        user-select: none !important;
        -webkit-user-select: none !important; /* Safari */
    }
            
    /* Button Hover */
    div[data-testid="stButton"] button:hover {
        background-color: #D38949 !important;
        border-color: #D38949 !important;
        color: #FAF9F6 !important;
    }
            
    /* Button Disabled */
    div[data-testid="stButton"] button:disabled {
        color: #FAF9F6 !important;
        background-color: #E6DCD2 !important;
        border-color: #E6DCD2 !important;
        text-decoration: none !important;
    }
    
    .st-key-toggle_2019 button {
        width: 200px !important;
    }
            
    .stSelectbox div[data-baseweb="select"] > div:first-child {
        border-color: #BF8755 !important;
    }

    .stSelectbox div[data-baseweb="select"]:hover > div:first-child {
        border-color: #D38949 !important;
    }

    .stSelectbox div[data-baseweb="select"] > div:focus-within {
        border-color: #D38949 !important;
        box-shadow: 0 0 0 1px #D38949 !important;
    }

    div[data-stale="true"] {
        opacity: 1.0 !important;
        filter: none !important;
    }
            
    </style>
""", unsafe_allow_html=True)
# -----------------------


# initialize various session state parameters

# plot caching
if "final_lineplot_html" not in st.session_state:
    st.session_state["final_lineplot_html"] = None
if "weekly_lineplot_html" not in st.session_state:
    st.session_state["weekly_lineplot_html"] = None
if "heatmap_html" not in st.session_state:
    st.session_state["heatmap_html"] = None
if "cbar_html" not in st.session_state:
    st.session_state["cbar_html"] = None
if "barplots_html" not in st.session_state:
    st.session_state["barplots_html"] = []

# helpers
if "current_seed" not in st.session_state:  
    st.session_state["current_seed"] = 42  # seed to extract random period for lineplot snapshot
if "weekly_dates_html" not in st.session_state:
    st.session_state["weekly_dates_html"] = None  # store date range of random extracted lineplot period
if "barplots_idx" not in st.session_state:
    st.session_state["barplots_idx"] = 0  # id of barplot to display (with / without change from 2019)

# not really needed - count how many times the lineplot snapshot has been re-generated
if "weekly_plot_counter" not in st.session_state:
    st.session_state["weekly_plot_counter"] = 0  

# status tracking for the initial 'minigame'
if "finalized" not in st.session_state:
    st.session_state["finalized"] = False
if "final_order" not in st.session_state:
    st.session_state["final_order"] = []

# overall title and introduction
# text formatted by Gemini
st.markdown(
    "<div style='text-align: center; font-size: 40px; font-weight: bold; font-family: sans-serif; color: black; margin-bottom: 10px;'>Zooming Out:</div>", 
    unsafe_allow_html=True
)
st.markdown(
    "<div style='text-align: center; font-size: 32px; font-weight: bold; font-family: sans-serif; color: black; margin-bottom: 25px;'>How Time and Category Granularity can affect the perception of Stock Data.</div>", 
    unsafe_allow_html=True
)
st.markdown(
    "<div style='text-align: center; font-size: 18px; font-weight: bold; font-family: sans-serif; color: black; margin-bottom: 15px;'>A Data Visualization Project by Bartosz Kochanski, Lukáš Trstenský, and Vincenzo Piras.</div>", 
    unsafe_allow_html=True
)
st.space(5)

# text formatted by Gemini
st.markdown(
    """
    <p style="font-family: sans-serif; font-size: 16px; color: black; line-height: 1.5; margin: 0;">
        Using 2025-inflation-adjusted historic stock market data spanning from the beginning of 2019 to the end of 2025, four visualization sections follow.<br/>
        The components of this webpage represent the path from subjective, narrow-context feelings to broader, objective realities, with the goal of bridging the mental gap between an individual trader looking at their personal portfolio performance and the overarching trends of the market.
    </p>
    """,
    unsafe_allow_html=True
)

# text formatted by Gemini
st.markdown(
    """
    <p style="font-family: sans-serif; font-size: 14px; color: #8C8C8C; line-height: 1.5; margin: 0;">
        The page is meant to be viewed in the standard 16:9 ratio, and interactive elements such as buttons must not be pressed before the relative plot has loaded.
    </p>
    """,
    unsafe_allow_html=True
)

# Gemini code - manually added data source link
html_link = """
<p style="font-family: sans-serif; font-size: 16px; color: black;">
    📊 
    <a href="https://huggingface.co/datasets/defeatbeta/yahoo-finance-data" target="_blank" style="color: #1E88E5; text-decoration: underline;">
        data source
    </a> 
</p>
"""
st.markdown(html_link, unsafe_allow_html=True)

# SECT1 - Individual Stocks // Snapshot and Complete Lineplot
# -----------------------------------------------------------

st.space(20)
st.header("P1 — Individual Stocks — percentage change in value over time", anchor= False)

# text formatted by Gemini
st.markdown(
    """
    <p style="font-family: sans-serif; font-size: 16px; color: black; line-height: 1.5; margin: 0;">
        With the use of multiple single-stock line charts, the section showcases the inherent difficulty in accurately assessing long-term performances when presented with short-term data.
    </p>
    """,
    unsafe_allow_html=True
)

# SUBSECT - Lineplot Snapshot and Minigame
st.space(10)
st.subheader("P1.1 — Weekly Stock Data", anchor= False)

# text formatted by Gemini
st.markdown(
    """
    <p style="font-family: sans-serif; font-size: 16px; color: black; line-height: 1.5; margin: 0;">
        Below there are four snapshot line plots, each encoding the 14-days relative performance of the associated stock: the first day of the time window serves as a baseline, and the percentage change from this initial value is reported on the y-axis.
        The time frame is chosen at random, and is reported above the charts, together with a button to perform the date sampling, and subsequent plotting, again.
        The goal is to assess the apparent reliability and profitability of each title over the long-term with the help of the random snapshot plots.
        Submit the stocks ordered from worst to best, based on what their overall performance evolution from 2019 might have been, to reveal the complete line plot.
    </p>
    """,
    unsafe_allow_html=True
)

st.space(3)

# obtain data (cached), and various needed values
df_list, color_list, name_list, x_ticks, x_labels = lineplot_load_data()
 
col1, col2, col3 = st.columns([3, 2, 7], vertical_alignment="center")

# plot and align titles for subplots
text_list = ['Stock 1', 'Stock 2', 'Stock 3', 'Stock 4']
cols = st.columns([1, 1, 1, 1], vertical_alignment= "center")
for text, col, lpad in zip(text_list, cols, ["38.5%", "41%", "44%", "47%"]):
    with col:
        text_html = get_aligned_text_row(text, alignments= 'left', left_padding= lpad, font_size= "19", margin_bottom= "0")
        st.markdown(text_html, unsafe_allow_html=True)

# re-generate plot if button is clicked or if wepage has just been started
reloaded = False
with col2:
    if st.button("Re-Generate Snapshot Plots") or st.session_state['weekly_plot_counter'] == 0:
        
        # update parameters
        reloaded= True
        st.session_state["current_seed"] = np.random.randint(14, 1759)
        st.session_state["weekly_plot_counter"] += 1

        # plot graph (fig, date_beginning, date_end are needed, remaining variables' use was discarded)
        fig, stock_min_final, stock_max_final, stock_min_peak, stock_max_peak, date_beginning, date_end = generate_week_lineplot(df_list, color_list, st.session_state["current_seed"])

# plot date range, update when needed
with col1:
    if st.session_state["weekly_dates_html"] == None or reloaded:

        # !! HTML generated by Gemini
        # ---------------------------
        date_range = f"<span style='color: #000000; font-weight: bold;'>{date_beginning} → {date_end}</span>"
        final_html = f"""
            <p style='text-align: center; font-size: 16px; margin: 0; position: relative; top: -8px'>
                <span style='color: black;margin-right: 20px;'>Date range:</span>
                {date_range}
            </p>
            """
        # ---------------------------

        # store current date range, and display it
        st.session_state["weekly_dates_html"] = final_html
        st.markdown(st.session_state["weekly_dates_html"], unsafe_allow_html=True)
    
    # display cached dates if the plot wasn't updated
    else:
        st.markdown(st.session_state["weekly_dates_html"], unsafe_allow_html=True)

st.space(3)
# placeholder for the lineplot snapshot, visible when the graph is loading (almost never :>)
plot_placeholder = st.empty()
plot_placeholder.markdown(
    # !! Gemini code skeleton - parameters manually set
    # -----------------------
    """
    <style>
    @keyframes pulse {
        0% { opacity: 0.6; }
        50% { opacity: 1.0; }
        100% { opacity: 0.6; }
    }
    .loading-skeleton {
        width: 100%;
        height: 378px;
        background-color: #FAF9F6;
        border: 2px dashed #BF8755;
        border-radius: 8px;
        margin-bottom: 8.5px;
        margin-top: 0px;
        display: flex;
        justify-content: center;
        align-items: center;
        color: #BF8755;
        font-family: sans-serif;
        font-weight: bold;
        animation: pulse 1.5s infinite ease-in-out;
    }
    </style>
    <div class="loading-skeleton">
        Generating visualization...
    </div>
    """,
    unsafe_allow_html=True
    # -----------------------
)

# plot linechart snapshot in the placeholder skeleton - newly generated, or cached
if reloaded:
    st.session_state["weekly_lineplot_html"] = get_svg_html(fig)
    plot_placeholder.write(st.session_state["weekly_lineplot_html"], unsafe_allow_html=True)
    plt.close(fig)

elif  st.session_state["weekly_lineplot_html"] is not None:
    plot_placeholder.write(st.session_state["weekly_lineplot_html"], unsafe_allow_html=True)


# 'minigame' section

st.space(3)
col1, col2, col3, col4 = st.columns([1.5, 5.5, 1.5, 2], vertical_alignment="center")

# info text: black if user hasn't submitted an order, gray otherwise
with col1:
    if not st.session_state["finalized"]:
        st.markdown("**Select the stocks in order:**")
    else:
        # !! Gemini code
        st.markdown("<span style='color: #C8C8C7; font-weight: bold;'>Select the stocks in order:</span>", unsafe_allow_html=True)

# input / display user selection
with col2:

    # minigame still on: plot clickable fields
    if not st.session_state["finalized"]:

        sub_col1, sub_col2, sub_col3, sub_col4, sub_col5, sub_col6 = st.columns(
            [0.5, 1, 1, 1, 1, 0.5], 
            vertical_alignment="center"
        )
        stock_options = ['Stock 1', 'Stock 2', 'Stock 3', 'Stock 4']
        
        # !! Gemini code skeleton - parameters manually set
        # -----------------------
        with sub_col1:
            st.markdown("<p style='text-align: right; font-weight: bold; margin: 0; position: relative; top: -8px;'>Worst → </p>", unsafe_allow_html=True)
        with sub_col2:
            choice1 = st.selectbox("1st", options=stock_options, label_visibility="collapsed", key="s1")
        with sub_col3:
            choice2 = st.selectbox("2nd", options=stock_options, label_visibility="collapsed", key="s2")
        with sub_col4:
            choice3 = st.selectbox("3rd", options=stock_options, label_visibility="collapsed", key="s3")
        with sub_col5:
            choice4 = st.selectbox("4th", options=stock_options, label_visibility="collapsed", key="s4")
        with sub_col6:
            st.markdown("<p style='text-align: left; font-weight: bold; margin: 0; position: relative; top: -8px;'> → Best</p>", unsafe_allow_html=True)
        # -----------------------
        user_order = [choice1, choice2, choice3, choice4]
    
    # minigame over: display user's submitted order
    else:

        color_list_desat = ['#A8C2D9', '#E4B4B6', '#B5D9C4', '#F5E0A5']
        
        # !! HTML generated by Gemini
        # ---------------------------
        formatted_stocks = [
            f"""<span style='
                background-color: {color_list_desat[int(stock[-1])-1]};
                color: black;
                border: 2px solid black;
                padding: 3px 8px;
                margin: 0 4px;
                border-radius: 4px;
                display: inline-block;
                font-weight: bold;
            '>{stock}</span>"""
            for stock in st.session_state['final_order']
        ]
        
        order_sequence = "<span style='color: #000000; font-weight: bold;'> → </span>".join(formatted_stocks)
        
        final_html = f"""
        <p style='text-align: center; font-size: 16px; margin: 0; position: relative; top: -8px'>
            <span style='color: black;margin-right: 20px;'>Submitted order:</span>
            <span style='font-weight: bold; color: black;'>Worst → </span> 
            {order_sequence} 
            <span style='font-weight: bold; color: black;'> → Best</span>
        </p>
        """
        # ---------------------------

        # display submission
        st.markdown(final_html, unsafe_allow_html=True)
        user_order = st.session_state["final_order"]

# handle the button logic
with col4:
    if st.button("Submit & Unlock Complete Plot", disabled=st.session_state["finalized"]):

        # make sure only valid combinations are accepted
        if len(user_order) < 4:
            st.toast("Select all 4 stocks in the  \ndesired order before submitting.", icon="⚠️")
        elif len(set(user_order)) < 4:
            st.toast("Select each stock exactly  \nonce before submitting.", icon="⚠️")
        else:

            # cache valid submission
            st.session_state["final_order"] = user_order
            st.session_state["finalized"] = True
            st.rerun()

# only display other plots if the minigame is over
if st.session_state["finalized"]:

    col1, col2, col3, col4 = st.columns([1.5, 5.5, 1.5, 2], vertical_alignment="center")

    # plot correct order underneath the user's submission
    with col2:

        color_list_desat = ['#A8C2D9', '#E4B4B6', '#B5D9C4', '#F5E0A5']

        # !! HTML generated by Gemini
        # ---------------------------
        formatted_stocks = [
            f"""<span style='
                background-color: {color_list_desat[int(stock[-1])-1]};
                color: black;
                border: 2px solid black;
                padding: 3px 8px;
                margin: 0 4px;
                border-radius: 4px;
                display: inline-block;
                font-weight: bold;
            '>{stock}</span>"""
            for stock in ['Stock 4', 'Stock 3', 'Stock 2', 'Stock 1']
        ]
        
        order_sequence = "<span style='color: #000000; font-weight: bold;'> → </span>".join(formatted_stocks)
        
        final_html = f"""
        <p style='text-align: center; font-size: 16px; margin: 0; position: relative; top: -8px'>
            <span style='color: black;margin-right: 40px;'>Correct order:</span>
            <span style='font-weight: bold; color: black;'>Worst → </span> 
            {order_sequence} 
            <span style='font-weight: bold; color: black;'> → Best</span>
        </p>
        """   
        # ---------------------------

        st.markdown(final_html, unsafe_allow_html=True)

    # SUBSECT - Complete Lineplot
    st.space(10)
    st.subheader("P1.2 — Complete Stock Data", anchor= False)

    if st.session_state['final_order'] == ['Stock 4', 'Stock 3', 'Stock 2', 'Stock 1']:
        
        # text formatted by Gemini
        st.markdown(
            """
            <p style="font-family: sans-serif; font-size: 16px; color: black; line-height: 1.5; margin: 0;">
                Congratulations, you correctly identified best and worst performing stocks over the long-term.
            </p>
            """,
            unsafe_allow_html=True
        )
    
    else:

        # text formatted by Gemini
        st.markdown(
            """
            <p style="font-family: sans-serif; font-size: 16px; color: black; line-height: 1.5; margin: 0;">
                The stocks were not ordered correctly, but good effort trying to read through the chaotic snapshots.
            </p>
            """,
            unsafe_allow_html=True
        )
    
    # text formatted by Gemini
    st.markdown(
            """
            <p style="font-family: sans-serif; font-size: 16px; color: black; line-height: 1.5; margin: 0;">
                What follows is the line plot containing the complete historic data for the four stocks.
                It starts from the worst performing title, and it is possible to scroll upwards to observe the trends for the more successful companies.
            </p>
            """,
            unsafe_allow_html=True
        )
    
    st.space(3)

    # generate lineplot on first run
    if st.session_state["final_lineplot_html"] is None:

        # !! Gemini code skeleton - parameters manually set
        # -----------------------
        plot_placeholder_2 = st.empty()
        plot_placeholder_2.markdown(
            """
            <style>
            @keyframes pulse {
                0% { opacity: 0.6; }
                50% { opacity: 1.0; }
                100% { opacity: 0.6; }
            }
            .loading-skeleton {
                width: 100%;
                height: 450px;
                background-color: #FAF9F6; 
                border: 2px dashed #BF8755;
                border-radius: 8px;
                display: flex;
                justify-content: center;
                align-items: center;
                color: #BF8755;
                font-family: sans-serif;
                font-weight: bold;
                animation: pulse 1.5s infinite ease-in-out;
                margin-top: 20px;
                margin-bottom: 20px;
            }
            </style>
            <div class="loading-skeleton">
                Generating visualization...
            </div>
            """,
            unsafe_allow_html=True
        )
        # -----------------------

        # generate lineplot
        fig = generate_final_lineplot(df_list, color_list, name_list, x_ticks, x_labels)
        
        # store the html code for the plot in the parameters, display it on the placeholder
        st.session_state["final_lineplot_html"] = get_open_scrollable_svg_html_inverted(fig, height= 450)
        plot_placeholder_2.write(st.session_state["final_lineplot_html"], unsafe_allow_html=True)
        plt.close(fig)
        
        # wait before loading other plots (mindfulness!)
        st.space(10)
        with st.spinner("Check out the lineplot ..."):
            time.sleep(10)

    # if the plot was already generated, display the cached code
    else:
        st.write(st.session_state["final_lineplot_html"], unsafe_allow_html=True)

# -----------------------------------------------------------

# SECT2 - MoM Industry Evolution // Heatmap
# -----------------------------------------------------------

    st.space(20)
    st.header("P2 — Industry Heatmap — MoM percentage change in average value across industries", anchor= False)
    
    # text formatted by Gemini
    st.markdown(
        """
        <p style="font-family: sans-serif; font-size: 16px; color: black; line-height: 1.5; margin: 0;">
            The following heatmap highlights the Month-over-Month (MoM) waves of gains and losses across industries, presenting the slightly broader context effecting individual stocks.<br/>
            MoM values encode the percentage change in stock value compared to 30 days prior: a positive value means the title price went up, compared to the past month.
        </p>
        """,
        unsafe_allow_html=True
    )

    # text formatted by Gemini
    st.markdown(
        """
        <p style="font-family: sans-serif; font-size: 14px; color: #8C8C8C; line-height: 1.5; margin: 0;">
            Titles below the 20th percentile value for industry-specific average trading volume (amount of stocks traded) and 2019 starting stock price were discarded.
        </p>
        """,
        unsafe_allow_html=True
    )


    # x axis labels, manually aligned with the plot

    years = ["2019", "2020", "2021", "2022", "2023", "2024", "2025"]
    col1, col2, col3, col4, col5, col6, col7, _ = st.columns([1, 1, 1, 1, 1, 1, 1, 0.5], vertical_alignment="center")
    lpad_list = ["13.6%", "4.58%", "9.5%", "14%", "18%", "21.35%", "25.75%"]
    linelen_list = ["195px", "220px", "220px", "220px", "220px", "220px", "218px"]

    for text, col, lpad, linelen in zip(years, [col1, col2, col3, col4, col5, col6, col7], lpad_list, linelen_list):
        text_html = get_aligned_text_row(text, alignments="left", 
                                         left_padding= lpad, right_padding= "0%", font_size= "16", 
                                         margin_bottom= "0", line_thickness= "2px", line_width= linelen)
        with col:
            st.write(text_html, unsafe_allow_html= True)

    # on the first run, generate the heatmap
    if st.session_state["heatmap_html"] is None:
        
        # !! Gemini code skeleton - parameters manually set
        # -----------------------
        plot_placeholder_3 = st.empty()
        plot_placeholder_3.markdown(
            """
            <style>
            @keyframes pulse {
                0% { opacity: 0.6; }
                50% { opacity: 1.0; }
                100% { opacity: 0.6; }
            }
            .loading-skeleton {
                width: 100%;
                height: 700px;
                background-color: #FAF9F6; 
                border: 2px dashed #BF8755;
                border-radius: 8px;
                display: flex;
                justify-content: center;
                align-items: center;
                color: #BF8755;
                font-family: sans-serif;
                font-weight: bold;
                animation: pulse 1.5s infinite ease-in-out;
                margin-top: 20px;
                margin-bottom: 20px;
            }
            </style>
            <div class="loading-skeleton">
                Generating visualization...
            </div>
            """,
            unsafe_allow_html=True
        )
        # -----------------------

        # load data (cached), generate plot
        df_mom = heatmap_load_data()
        fig, cbar = generate_heatmap(df_mom)
        
        # store the html code for the plot in the parameters, display it on the placeholder
        st.session_state["heatmap_html"] = get_open_scrollable_svg_html(fig, 700, border_radius= '20')
        plot_placeholder_3.write(st.session_state["heatmap_html"], unsafe_allow_html=True)
        plt.close(fig)

        # cache and display colorbar
        st.session_state["cbar_html"] = get_svg_html(cbar)
        col00, col0, col1, col2, col3, col4 = st.columns([0.5, 0.5, 2, 1, 1, 1], vertical_alignment="center")
        with col3:
            st.write(st.session_state["cbar_html"], unsafe_allow_html= True)

        # mindfulness blabla
        st.space(10)
        with st.spinner("Check out the heatmap ..."):
            time.sleep(10)
    
    # if the plot was already generated, display the cached code
    else:
        
        st.write(st.session_state["heatmap_html"], unsafe_allow_html=True)
        
        col00, col0, col1, col2, col3, col4 = st.columns([0.5, 0.5, 2, 1, 1, 1], vertical_alignment="center")
        with col3:
            st.write(st.session_state["cbar_html"], unsafe_allow_html= True)

# -----------------------------------------------------------

# SECT3 -  Quarterly Sector Evolution // Barplot
# -----------------------------------------------------------

    st.space(20)
    st.header("P3 — Sector Evolution — quarterly percentage change in average value across sectors", anchor= False)
    
    # text formatted by Gemini
    st.markdown(
        """
        <p style="font-family: sans-serif; font-size: 16px; color: black; line-height: 1.5; margin: 0;">
            The barplot presents quarterly sector performance, now showing broader market trends.<br/>
            Negative quarters likely indicate systematic regression in price, rather than a temporary independent negative moment for specific industries or stocks, adding more context to long-term performance analysis.<br/>
            Each bar represents the change, in percentage, of the mean price across all sector-specific stocks from the last day of the previous quarter to the last day of the current quarter: positive values indicate that the average company is worth more at the end of the given quarter than it was at the end of the previous.<br/>
            After observing the graph, it is possible to add the sector-specific mean price percentage change from the beginning of 2019 for each quarter by clicking the button.<br/>
            It is then possible to compare the perceived overall health and profitability of a sector on a quarterly basis with its long-term trends: are 3-month periods enough to determine the extended reliability of a sector?
        </p>
        """,
        unsafe_allow_html=True
    )

    # text generated by Gemini
    st.markdown(
        """
        <p style="font-family: sans-serif; font-size: 14px; color: #8C8C8C; line-height: 1.5; margin: 0;">
            Titles below the 20th percentile value for sector-specific average trading volume (amount of stocks traded) and 2019 starting stock price were discarded.
        </p>
        """,
        unsafe_allow_html=True
    )
    
    st.space(3)

    # button to control wether to show change from 2019 on the plot, initial state is 'not displayed'
    col1, _ = st.columns([3, 7], vertical_alignment="center")
    button_text = "Show change from 2019" if not st.session_state['barplots_idx'] else "Hide change from 2019"
    with col1:
        if st.button(button_text, key="toggle_2019"):

            # flip the barplot idx (0 to 1 / 1 to 0)
            st.session_state['barplots_idx'] = 1 - st.session_state['barplots_idx']
            st.rerun()
    
    st.space(1)

    # if no code for the barplots is cached, create both versions (with and without 2019 change)
    if st.session_state["barplots_html"] == []:
        
        # !! Gemini code skeleton - parameters manually set
        # -----------------------
        plot_placeholder_4 = st.empty()
        plot_placeholder_4.markdown(
            """
            <style>
            @keyframes pulse {
                0% { opacity: 0.6; }
                50% { opacity: 1.0; }
                100% { opacity: 0.6; }
            }
            .loading-skeleton {
                width: 100%;
                height: 550px; /* Matched to the scrollable container height */
                background-color: #FAF9F6; 
                border: 2px dashed #BF8755;
                border-radius: 8px;
                display: flex;
                justify-content: center;
                align-items: center;
                color: #BF8755;
                font-family: sans-serif;
                font-weight: bold;
                animation: pulse 1.5s infinite ease-in-out;
                margin-top: 20px;
                margin-bottom: 20px;
            }
            </style>
            <div class="loading-skeleton">
                Generating visualization...
            </div>
            """,
            unsafe_allow_html=True
        )
        # -----------------------

        # load data (cached), generate the two barplots
        df_bar, bline = barplot_load_data()
        fig = generate_barplot(df_bar, bline, 0)
        fig_2019 = generate_barplot(df_bar, bline, 1)
        
        # store them in the parameter (list), idx 0 stores plot not showing change from 2019, idx 1 stores the other
        st.session_state["barplots_html"].append(get_open_scrollable_svg_html(fig, 550, padding_leftright= "0", padding_topbottom= "0"))
        st.session_state["barplots_html"].append(get_open_scrollable_svg_html(fig_2019, 550, padding_leftright= "0", padding_topbottom= "0"))
        
        # plot figure 0 in the placeholder
        plot_placeholder_4.write(st.session_state["barplots_html"][0], unsafe_allow_html=True)
        plt.close(fig)
        plt.close(fig_2019)

        # lochness
        st.space(10)
        with st.spinner("Check out the barplot ..."):
            time.sleep(10)
    
    # if already cached, display the plot corresponding to the current idx
    else:
        st.write(st.session_state["barplots_html"][st.session_state["barplots_idx"]], unsafe_allow_html=True)

# -----------------------------------------------------------

# SECT4 - 2019-2025 Market Evolution // Animated Spiral
# -----------------------------------------------------------

    st.space(20)
    st.header("P4 — 2019-2025 Market Evolution — overall percentage change in average value animated spiral", anchor= False)
    
    # text formatted by Gemini
    st.markdown(
        """
        <p style="font-family: sans-serif; font-size: 16px; color: black; line-height: 1.5; margin: 0;">
            The spiral facilitates the comparison of daily aggregate stock trends and performance across years using a continuous line, allowing for animation.<br/>
            It shows the highs and lows of trading both inside individual years, and over multiple years.
            This provides full long-term context about the gains or losses of sectors and industries in any period of time, while also serving as a point of comparison between the performance of one’s own portfolio and the average market performance.
        </p>
        """,
        unsafe_allow_html=True
    )

    # text formatted by Gemini
    st.markdown(
        """
        <p style="font-family: sans-serif; font-size: 14px; color: #8C8C8C; line-height: 1.5; margin: 0;">
            Titles below the 20th percentile value for global average trading volume (amount of stocks traded) and 2019 starting stock price were discarded.
        </p>
        """,
        unsafe_allow_html=True
    )

    st.space(3)

    col1, col2, col3 = st.columns([2, 5, 2], vertical_alignment="center")
    
    with col2:
        st.video(
            current_dir / "spiral-vol20-price20.mp4",
            autoplay=True,
            loop=True,
            muted=True,
            start_time=0
        )

    st.space(30)
    st.markdown(
        """
        <p style='text-align: center; color: #BF8755; font-size: 15px; font-weight: bold; font-family: sans-serif; margin-top: 30px; margin-bottom: 30px;'>
            Thanks for reading.
        </p>
        """, 
        unsafe_allow_html=True
    )