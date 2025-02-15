import streamlit as st
import pandas as pd

# Set up the page configuration
st.set_page_config(page_title="Data Methodology & Analysis", layout="wide")

# Title of the page
st.title("Data Methodology & Analysis")

# -------------------------------------------------------------------------
# Data File Section
st.markdown("## Data File")

df = pd.read_csv("./both.csv")
st.markdown("### Data Preview")
st.dataframe(df)


# -------------------------------------------------------------------------
# Data Collection Section
st.markdown("## Data Collection")
st.markdown("""
- **Source:** Data was collected from my Zomato and Swiggy accounts.
- **Collection Method:** Since there wasn't a suitable web scraping tool, I had to manually enter the records.
- **Period Covered:** The dataset spans from 1/9/23 to 2/11/25, capturing different academic and vacation periods.
- **Attributes:** The dataset includes attributes like order price, date, platform (Zomato/Swiggy), meal type, cuisine type, food types,quantities,etc.
""")

# -------------------------------------------------------------------------
# Data Cleaning Section
st.markdown("## Data Cleaning")
st.markdown("""
- **Missing Values:** Missing were substituted using the string 'None'.
- **Standardization:** Column names and formats were standardized (e.g., date formats were converted to datetime, and categorical variables were properly ordered).
- **Error Correction:** Inconsistencies such as typos in restaurant or cuisine names were corrected.
""")

# -------------------------------------------------------------------------
# Data Pre-processing Section
st.markdown("## Data Pre-processing")
st.markdown("""
- **Data Transformation:** Dates were converted to datetime objects, and numerical fields (e.g., Price, Quantity) were cast to appropriate types.
- **Feature Engineering:** New features such as 'TimeSlot' (for 3-hour intervals) and cumulative counts were derived.
""")

# -------------------------------------------------------------------------
# Data Exploration Section
st.markdown("## Data Exploration")
st.markdown("""
- **Visualizations:** A variety of charts were created to uncover insights:
    - **Histograms & Box Plots:** To analyze price distributions, Day & Meal Distributions, Compare between platforms.
    - **Scatter Plots:** To compare ordering behavior across platforms.
    - **Heatmaps:** To identify ordering patterns by day and time.
    - **WordClouds:** To easily visualize the most common cuisines and restaurants.

""")


st.markdown(
    '<a href="https://colab.research.google.com/drive/1ajpdkMKEIWFTyFb2zplcGS5ZADaHf3PB?usp=sharing" target="_blank">Click here to redirect to EDA of data</a>',
    unsafe_allow_html=True
)
