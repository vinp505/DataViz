"""
Helper module with html related functions, primarily used to render plots on the webpage.
Due to the nature of such functions not being in the scope of our Data Science education,
AI help was needed to generate working code, which is properly labeled.
"""

# -------------------------------------------------------------------------------

import base64
from io import StringIO
import regex as re

# -------------------------------------------------------------------------------

def get_aligned_text_row(text: list | str, alignments: list | str, left_padding="6.5%", right_padding="3.5%", font_size= "16", margin_top= "20", margin_bottom= "20", line_width = None, line_thickness= None, line_fade=True):
    """Helper function to generate and align text. Used for some plot markers."""

    # convert to list even when single string
    if isinstance(text, str):
        text = [text]
    if isinstance(alignments, str):
        alignments = [alignments]

    # one alignment per text
    assert len(text) == len(alignments)
    
    # !! Gemini code
    # --------------

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
    # --------------

    return html

def get_open_scrollable_svg_html(fig, height=500, padding_topbottom= "10", padding_leftright = "20"):
    """Encase a plot in a scrollable html element. Used to plot complete heatmap and barchart."""
    
    # !! Gemini code - mostly
    # --------------

    # convert matplotlib figure into svg format
    imgdata = StringIO()
    fig.savefig(imgdata, format="svg", bbox_inches="tight")
    imgdata.seek(0)
    svg_string = imgdata.getvalue()

    # encode in base 64 for html code
    b64 = base64.b64encode(svg_string.encode('utf-8')).decode("utf-8")

    html = f"""
    <div style="
        height: {height}px; 
        overflow-y: auto;
        border-left: 3.5px solid #000000;
        border-radius: 8px;
        background-color: #FAF9F6;
        padding: {padding_topbottom}px {padding_leftright}px;
        box-sizing: border-box;
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
    # --------------

    return html

def get_open_scrollable_svg_html_inverted(fig, height=500):
    """
    Encase a plot in a scrollable html element, starting from the bottom of the image. 
    Used to plot the complete linechart.
    """
    
    # !! Gemini code
    # --------------
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
    # --------------

    return html

def get_svg_html(fig):
    """Saves a Matplotlib figure as an SVG string and returns it as a Base64 HTML tag."""

    # !! Gemini code
    # --------------

    # 1. Save figure to an in-memory text buffer instead of disk
    imgdata = StringIO()
    fig.savefig(imgdata, format="svg", bbox_inches="tight")
    imgdata.seek(0)
    svg_string = imgdata.getvalue()
    
    # 2. Encode the SVG XML string to Base64
    b64 = base64.b64encode(svg_string.encode('utf-8')).decode("utf-8")
    
    # 3. Create a responsive HTML img tag
    html = f'<div style="text-align: center;"><img src="data:image/svg+xml;base64,{b64}" style="width: 100%; height: auto;"/></div>'
    # --------------

    return html