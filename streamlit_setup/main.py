import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import streamlit.components.v1 as components
import time

from load_data import lineplot_load_data, heatmap_load_data, barplot_load_data
from generate_plot import get_aligned_text_row, generate_week_lineplot, generate_final_lineplot, get_svg_html, generate_week_lineplot_title, get_scrollable_svg_html_inverted, generate_heatmap, get_scrollable_svg_html, get_interactive_svg_html, get_open_scrollable_svg_html_inverted, get_open_scrollable_svg_html, generate_barplot

st.set_page_config(layout="wide")

st.markdown("""
    <style>
    div[data-testid="stButton"] button {
        background-color: #BF8755 !important; /* Button background color */
        color: #FAF9F6 !important;               /* Text color inside the box */
        border: 2px solid #BF8755 !important;  /* Optional: Border color */
        border-radius: 6px !important;         /* Corner roundness */
        font-weight: bold !important;
        transition: background-color 0.5s ease, border-color 0.5s ease !important;
    }
    
    /* 2. Style when Hovering over the Button Box */
    div[data-testid="stButton"] button:hover {
        background-color: #D38949 !important; /* Hover background color (Red) */
        border-color: #D38949 !important;     /* Hover border color */
        color: #FAF9F6 !important;
    }
            
    /* Ensure the disabled state looks clean */
    div[data-testid="stButton"] button:disabled {
        color: #FAF9F6 !important;
        background-color: #E6DCD2 !important;
        border-color: #E6DCD2 !important;
        text-decoration: none !important;
    }

    .stSelectbox div[data-baseweb="select"] > div:first-child {
        border-color: #BF8755 !important; /* Your custom border color (e.g. Teal) */
    }

    /* 2. Border color on Hover */
    .stSelectbox div[data-baseweb="select"]:hover > div:first-child {
        border-color: #D38949 !important; /* Hover border color (e.g. Red) */
    }

    /* 3. Border color when Focused (Clicked / Dropdown is open) */
    .stSelectbox div[data-baseweb="select"] > div:focus-within {
        border-color: #D38949 !important;
        box-shadow: 0 0 0 1px #D38949 !important; /* Optional: Highlights the border halo */
    }
                 
    /* Force elements to maintain 100% opacity during a rerun */
    div[data-stale="true"] {
        opacity: 1.0 !important;
        filter: none !important;
    }
            
    </style>
""", unsafe_allow_html=True)

if "final_lineplot_html" not in st.session_state:
    st.session_state["final_lineplot_html"] = None
if "weekly_lineplot_html" not in st.session_state:
    st.session_state["weekly_lineplot_html"] = None

if "weekly_dates_html" not in st.session_state:
    st.session_state["weekly_dates_html"] = None
if "heatmap_html" not in st.session_state:
    st.session_state["heatmap_html"] = None
if "barplots_html" not in st.session_state:
    st.session_state["barplots_html"] = []
if "barplots_idx" not in st.session_state:
    st.session_state["barplots_idx"] = 0

if "weekly_plot_counter" not in st.session_state:
    st.session_state["weekly_plot_counter"] = 0

if "current_seed" not in st.session_state:
    st.session_state["current_seed"] = 42

if "finalized" not in st.session_state:
    st.session_state["finalized"] = False
if "final_order" not in st.session_state:
    st.session_state["final_order"] = []

# list_records = ["max_peak_history", "min_peak_history", "max_final_history", "min_final_history"]

# for m in list_records:
#     if m not in st.session_state:
#         st.session_state[m] = [0] * 4


st.title("Zooming Out: How Time and Category Granularity can affect the perception of Stock Data", anchor= False)
st.subheader("A Data Visualization Project by ...", anchor= False)
st.write("Add introduction")

st.space(20)
st.header("P1 — Individual Stocks", anchor= False)
#st.write("Stocks are volatile, and putting your trust in a single title requires confidence.\nBelow are plots summarizing the performance of four selected stocks across a randomly selected 2-week period, together with a button to change the time window.\nFeel free to create as many snapshot as you need to take a responsible decision: order the plots in the drop down menu from what you think it's the most profitable stock to the most harmful. Once you are happy with your selection, click the button on the side to reveal the complete line plots for each of the stocks.")
st.write("Add paragraph about: 1. concept 2. plot 3. game")

st.space(10)
st.subheader("P1.1 — Weekly Stock Data", anchor= False)

df_list, color_list, name_list, x_ticks, x_labels = lineplot_load_data()

col1, col2, col3 = st.columns([3, 2, 7], vertical_alignment="center")

text_list = ['Stock 1', 'Stock 2', 'Stock 3', 'Stock 4']
cols = st.columns([1, 1, 1, 1], vertical_alignment= "center")
for text, col, lpad in zip(text_list, cols, ["38.5%", "41%", "44%", "47%"]):
    with col:
        text_html = get_aligned_text_row(text, alignments= 'left', left_padding= lpad, font_size= "19", margin_bottom= "0")
        st.markdown(text_html, unsafe_allow_html=True)

reloaded = False
with col2:
    if st.button("Re-Generate Snapshot Plots") or st.session_state['weekly_plot_counter'] == 0:
        reloaded= True
        st.session_state["current_seed"] = np.random.randint(14, 1759)
        
        st.session_state["weekly_plot_counter"] += 1

        fig, stock_min_final, stock_max_final, stock_min_peak, stock_max_peak, date_beginning, date_end = generate_week_lineplot(df_list, color_list, st.session_state["current_seed"])



with col1:
    if st.session_state["weekly_dates_html"] == None or reloaded:
        date_range = f"<span style='color: #000000; font-weight: bold;'>{date_beginning} → {date_end}</span>"
        final_html = f"""
            <p style='text-align: center; font-size: 16px; margin: 0; position: relative; top: -8px'>
                <span style='color: black;margin-right: 20px;'>Date range:</span>
                {date_range}
            </p>
            """
        st.session_state["weekly_dates_html"] = final_html
        st.markdown(st.session_state["weekly_dates_html"], unsafe_allow_html=True)
    
    else:
        st.markdown(st.session_state["weekly_dates_html"], unsafe_allow_html=True)

plot_placeholder = st.empty()

plot_placeholder.markdown(
    """
    <style>
    @keyframes pulse {
        0% { opacity: 0.6; }
        50% { opacity: 1.0; }
        100% { opacity: 0.6; }
    }
    .loading-skeleton {
        width: 100%;
        height: 378px; /* Adjust this to match your plot's relative height */
        background-color: #FAF9F6; /* Your warm gray secondary background */
        border: 2px dashed #B7B1A1;
        border-radius: 8px;
        margin-bottom: 8.5px;
        margin-top: 0px;
        display: flex;
        justify-content: center;
        align-items: center;
        color: #B7B1A1;
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
)

if reloaded:
    st.session_state["weekly_lineplot_html"] = get_svg_html(fig)
    plot_placeholder.write(st.session_state["weekly_lineplot_html"], unsafe_allow_html=True)
    plt.close(fig)

elif  st.session_state["weekly_lineplot_html"] is not None:
    plot_placeholder.write(st.session_state["weekly_lineplot_html"], unsafe_allow_html=True)

# st.subheader("Accumulated Stats")
# st.write(f"Total Plots Generated: {st.session_state['plot_counter']}")
# st.write("stock 1 | stock 2 | stock 3 | stock 4")

# for m in list_records:
#     st.write(f"{m}: {' | '.join(map(str, st.session_state[m]))}")

st.space(3)
col1, col2, col3, col4 = st.columns([1.5, 5.5, 1.5, 2], vertical_alignment="center")

with col1:
    if not st.session_state["finalized"]:
        st.markdown("**Select the stocks in order:**")
    else:
        st.markdown("<span style='color: #C8C8C7; font-weight: bold;'>Select the stocks in order:</span>", unsafe_allow_html=True)
with col2:
    if not st.session_state["finalized"]:
        sub_col1, sub_col2, sub_col3, sub_col4, sub_col5, sub_col6 = st.columns(
            [0.5, 1, 1, 1, 1, 0.5], 
            vertical_alignment="center"
        )
        stock_options = ['Stock 1', 'Stock 2', 'Stock 3', 'Stock 4']
        
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

        user_order = [choice1, choice2, choice3, choice4]
    else:
        formatted_stocks = [
            f"""<span style='
                background-color: {color_list[int(stock[-1])-1]};
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
        
        st.markdown(final_html, unsafe_allow_html=True)
        user_order = st.session_state["final_order"]

with col4:
    if st.button("Submit & Unlock Complete Plot", disabled=st.session_state["finalized"]):
        if len(user_order) < 4:
            st.toast("Select all 4 stocks in the  \ndesired order before submitting.", icon="⚠️")
        elif len(set(user_order)) < 4:
            st.toast("Select each stock exactly  \nonce before submitting.", icon="⚠️")
        else:
            st.session_state["final_order"] = user_order
            st.session_state["finalized"] = True
            st.rerun()

if st.session_state["finalized"]:

    col1, col2, col3, col4 = st.columns([1.5, 5.5, 1.5, 2], vertical_alignment="center")

    with col2:

        formatted_stocks = [
            f"""<span style='
                background-color: {color_list[int(stock[-1])-1]};
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
        st.markdown(final_html, unsafe_allow_html=True)

    
    st.space(10)
    st.subheader("P1.2 — Complete Stock Data", anchor= False)
    st.write("Add text based on wether the guess was correct + mention to scroll up")
    if st.session_state["final_lineplot_html"] is None:
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
                height: 500px; /* Matched to the scrollable container height */
                background-color: #FAF9F6; 
                border: 2px dashed #B7B1A1;
                border-radius: 8px;
                display: flex;
                justify-content: center;
                align-items: center;
                color: #B7B1A1;
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

        fig = generate_final_lineplot(df_list, color_list, name_list, x_ticks, x_labels)
        
        st.session_state["final_lineplot_html"] = get_open_scrollable_svg_html_inverted(fig, height= 450)
        plot_placeholder_2.write(st.session_state["final_lineplot_html"], unsafe_allow_html=True)
        plt.close(fig)
        
        st.space(10)
        with st.spinner("Check out the lineplot ..."):
            time.sleep(10)

    else:
        st.write(st.session_state["final_lineplot_html"], unsafe_allow_html=True)
    
    st.space(20)
    st.header("P2 — MoM Industry Heatmap", anchor= False)
    st.write("Add text")

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

    if st.session_state["heatmap_html"] is None:
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
                height: 700px; /* Matched to the scrollable container height */
                background-color: #FAF9F6; 
                border: 2px dashed #B7B1A1;
                border-radius: 8px;
                display: flex;
                justify-content: center;
                align-items: center;
                color: #B7B1A1;
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

        df_mom = heatmap_load_data()
        fig = generate_heatmap(df_mom)
        
        st.session_state["heatmap_html"] = get_open_scrollable_svg_html(fig, 700)
        plot_placeholder_3.write(st.session_state["heatmap_html"], unsafe_allow_html=True)
        plt.close(fig)

        st.space(10)
        with st.spinner("Check out the heatmap ..."):
            time.sleep(10)
    
    else:
        st.write(st.session_state["heatmap_html"], unsafe_allow_html=True)
    
    st.space(20)
    st.header("P3 — Quarterly Sector Evolution", anchor= False)
    st.write("Add text")

    button_text = "Show change from 2019" if not st.session_state['barplots_idx'] else "Hide change from 2019"
    if st.button(button_text):
        st.session_state['barplots_idx'] = 1 - st.session_state['barplots_idx']
        st.rerun()
    
    if st.session_state["barplots_html"] == []:
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
                border: 2px dashed #B7B1A1;
                border-radius: 8px;
                display: flex;
                justify-content: center;
                align-items: center;
                color: #B7B1A1;
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

        df_bar, bline = barplot_load_data()
        fig = generate_barplot(df_bar, bline, 0)
        fig_2019 = generate_barplot(df_bar, bline, 1)
        
        st.session_state["barplots_html"].append(get_open_scrollable_svg_html(fig, 550, padding_leftright= "0", padding_topbottom= "0"))
        st.session_state["barplots_html"].append(get_open_scrollable_svg_html(fig_2019, 550, padding_leftright= "0", padding_topbottom= "0"))
        plot_placeholder_4.write(st.session_state["barplots_html"][0], unsafe_allow_html=True)
        plt.close(fig)
        plt.close(fig_2019)

        st.space(10)
        with st.spinner("Check out the barplot ..."):
            time.sleep(10)
    
    else:
        st.write(st.session_state["barplots_html"][st.session_state["barplots_idx"]], unsafe_allow_html=True)

    


