# Data Visualization and Data-Driven Decision Making

Repository for the Data Visualization and Data-Driven Decision Making project.

*   **Interactive Webpage:** https://zoomingout-blv.streamlit.app/

---

## Directory Structure

The repository is organized as follows:

*   `figs/` — Contains the raw generated plots and visualizations.
*   `report/` — Contains the LaTeX source documents and project files for the final report.
*   `streamlit_setup/` — Contains the source code and configuration files for the Streamlit web application.

---

Follow these steps to run the interactive Streamlit webpage locally on your machine:

### 1. Install Dependencies
Ensure you have Python installed, then install the required packages using the requirements file:
```bash
pip install -r requirements.txt
```

### 2. Run the Webpage
Navigate into the `streamlit_setup/` directory and execute the Streamlit run command:
```bash
streamlit run main.py
```