import streamlit as st
import time
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.figure_factory as ff



def preprocess_data_zomato(filepath):
    df = pd.read_csv(filepath)

    # Data cleaning
    df['Food2'].fillna('None', inplace=True)
    df['Quantity2'].fillna('None', inplace=True)
    df = df.replace('Manchurian', 'Manchuria')
    df = df.replace('The pancake co', 'The Pancake co')
    df = df.replace("L Pino'z", 'La Pinoz')
    df = df.replace("La Pinozo", 'La Pinoz')
    df = df.replace("The Good Bowl", 'Good Bowl')
    df = df.replace("The Nomads Cafe", 'Nomads Cafe')
    df.iloc[50, df.columns.get_loc('Date ')] = '10/20/24'
    df['Date '] = pd.to_datetime(df['Date '])

    return df

def preprocess_data_both(filepath):
    df = pd.read_csv(filepath)

    # Data cleaning
    df['Food2'].fillna('None', inplace=True)
    df['Quantity2'].fillna('None', inplace=True)
    df = df.replace('Manchurian', 'Manchuria')
    df = df.replace('The pancake co', 'The Pancake co')
    df = df.replace("L Pino'z", 'La Pinoz')
    df = df.replace("La Pinozo", 'La Pinoz')
    df = df.replace("The Good Bowl", 'Good Bowl')
    df = df.replace("The Nomads Cafe", 'Nomads Cafe')
    df.iloc[94, df.columns.get_loc('Date ')] = '10/20/24'
    df['Date '] = pd.to_datetime(df['Date '])

    return df

def preprocess_data_swiggy(filepath):
    df = pd.read_csv(filepath)

    # Data cleaning
    df['Food2'].fillna('None', inplace=True)
    df['Quantity2'].fillna('None', inplace=True)
    df = df.replace('Manchurian', 'Manchuria')
    df = df.replace('The pancake co', 'The Pancake co')
    df = df.replace("L Pino'z", 'La Pinoz')
    df = df.replace("La Pinozo", 'La Pinoz')
    df = df.replace("The Good Bowl", 'Good Bowl')
    df = df.replace("The Nomads Cafe", 'Nomads Cafe')
    # df.iloc[50, df.columns.get_loc('Date ')] = '10/20/24'
    df['Date '] = pd.to_datetime(df['Date '])

    return df

# Function to generate a donut chart with custom colors
def generate_donut_chart(platform_counts):
    color_map = {
        'Zomato': 'red',  # Set Zomato to red
        'Swiggy': 'orange'  # Set Swiggy to orange
    }

    fig = px.pie(
        platform_counts,
        values=platform_counts.values,
        names=platform_counts.index,
        title='Platform Distribution',
        hole=0.4,  # Creates a donut chart (hole in the middle)
        color=platform_counts.index,  # Assign color mapping
        color_discrete_map=color_map  # Apply custom colors
    )
    fig.update_layout(height=480)
    return fig

def generate_payment_pie_chart(df):
    mode_of_payment_counts = df['Mode of Payment'].value_counts()

    color_map = {
        'UPI': 'red',  # Set Zomato to red
        'COD': 'orange'  # Set Swiggy to orange
    }

    fig = px.pie(
        names=mode_of_payment_counts.index,
        values=mode_of_payment_counts.values,
        title='Mode of Payment Distribution',
        hole=0.3,  # Optional: Slightly hollow for a donut effect
        color=mode_of_payment_counts.index,  # Assign color mapping
        color_discrete_map=color_map
    )

    return fig




# def generate_scatter_plot(df):
#     fig = px.scatter(
#         df, 
#         x=df.index, 
#         y="Price", 
#         title="Price vs Index",
#         labels={"x": "Index", "Price": "Price"},
#         size="Price",      # Marker size is proportional to Price
#         size_max=20        # Optional: cap the maximum marker size
#     )

#     fig.update_layout(
#         hovermode="closest",
#         plot_bgcolor="rgba(0,0,0,0)",  # Transparent background
#         paper_bgcolor="rgba(0,0,0,0)"
#     )

#     # Update the trace for additional marker styling
#     fig.update_traces(
#         marker=dict(opacity=0.7, line=dict(width=2, color="black")),
#         hoverinfo="text"
#     )

#     return fig

import plotly.express as px

def generate_scatter_plot(df):
    # Create scatter plot with category orders so that trace order is [Zomato, Swiggy]
    fig = px.scatter(
        df, 
        x=df.index, 
        y="Price", 
        color="Platform",
        category_orders={"Platform": ["Zomato", "Swiggy"]},
        color_discrete_map={"Zomato": "red", "Swiggy": "orange"},
        title="Price vs Index",
        labels={"x": "Index", "Price": "Price"},
        size="Price",      
        size_max=20
    )
    
    fig.update_layout(
        hovermode="closest",
        plot_bgcolor="rgba(0,0,0,0)",  
        paper_bgcolor="rgba(0,0,0,0)"
    )
    
    # Update the trace for additional marker styling
    fig.update_traces(
        marker=dict(opacity=0.7, line=dict(width=2, color="black")),
        hoverinfo="text"
    )
    
    # Add dropdown filter for platform with toggler at bottom-right corner
    fig.update_layout(
        updatemenus=[
            {
                "active": 0,
                "buttons": [
                    {
                        "label": "All",
                        "method": "update",
                        "args": [{"visible": [True, True]},
                                 {"title": "Price vs Index - All Platforms"}]
                    },
                    {
                        "label": "Zomato",
                        "method": "update",
                        "args": [{"visible": [True, False]},
                                 {"title": "Price vs Index - Zomato Only"}]
                    },
                    {
                        "label": "Swiggy",
                        "method": "update",
                        "args": [{"visible": [False, True]},
                                 {"title": "Price vs Index - Swiggy Only"}]
                    }
                ],
                "direction": "down",
                "showactive": True,
                "x": 1,
                "xanchor": "right",
                "y": 0,
                "yanchor": "bottom"
            }
        ]
    )
    
    return fig




def generate_price_histogram(df):
    # Separate data for each platform
    df_zomato = df[df["Platform"] == "Zomato"]["Price"]
    df_swiggy = df[df["Platform"] == "Swiggy"]["Price"]
    
    # Create a distribution plot with two datasets
    fig = ff.create_distplot(
        [df_zomato, df_swiggy],       # List of arrays of data
        group_labels=["Zomato", "Swiggy"],  # Names for each dataset
        bin_size=20,                 # Bin size for histogram
        curve_type="kde",            # Add KDE curve
        colors=["red", "orange"]     # Color scheme for each dataset
    )

    fig.update_layout(
        title="Price Distribution by Platform",
        xaxis_title="Price",
        yaxis_title="Density",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )

    return fig



def generate_day_distribution_plot(df):
    day_counts = df.groupby(['Day', 'Platform']).size().reset_index(name='Count')

    # Create the bar chart with separate bars for each platform
    fig = px.bar(
        day_counts,
        x='Day',
        y='Count',
        color='Platform',  # Different color for Zomato & Swiggy
        barmode='group',  # Grouped bars
        labels={'Day': 'Day', 'Count': 'Order Count'},
        title="Order Distribution by Day for Zomato and Swiggy",
        color_discrete_map={'Zomato': 'red', 'Swiggy': 'orange'}  # Custom colors
    )

    # Update layout for aesthetics
    fig.update_layout(
        xaxis_title="Day",
        yaxis_title="Order Count",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )

    return fig
    

def generate_meal_distribution_plot(df):
    grouped = df.groupby(["Meal", "Platform"]).size().reset_index(name="Count")

    # Create a grouped bar chart (two columns per Meal, one for each platform)
    fig = px.bar(
        grouped,
        x="Meal",
        y="Count",
        color="Platform",
        barmode="group",  # side-by-side bars
        labels={"Meal": "Meal", "Count": "Order Count"},
        title="Distribution of Meals by Platform",
        # Optionally, set a custom color mapping:
        color_discrete_map={"Zomato": "red", "Swiggy": "orange"}
    )

    fig.update_layout(
        xaxis_title="Meal",
        yaxis_title="Order Count",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )

    return fig

    

def generate_box_plot_price(df):
    fig = px.box(
        df,
        x="Platform",
        y="Price",
        color="Platform",  # Color by platform
        color_discrete_map={"Zomato": "red", "Swiggy": "orange"},
        title="Box Plot of Price by Platform",
        labels={"Platform": "Platform", "Price": "Price"}
    )
    
    # Optional: Update the layout for a cleaner look
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )
    
    return fig


def generate_day_timeslot_heatmap_px(df):
    # Ensure 'Time' is datetime
    df["Time"] = pd.to_datetime(df["Time"])
    
    # Extract the hour and create 3-hour bins
    df["Hour"] = df["Time"].dt.hour
    df["TimeSlot"] = pd.cut(
        df["Hour"],
        bins=range(0, 25, 3),
        right=False,
        labels=[
            '00:00-02:59', '03:00-05:59', '06:00-08:59', '09:00-11:59',
            '12:00-14:59', '15:00-17:59', '18:00-20:59', '21:00-23:59'
        ]
    )
    
    # Ensure 'Day' is ordered correctly
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    df["Day"] = pd.Categorical(df["Day"], categories=days_order, ordered=True)
    
    # Group by Day and TimeSlot, count orders, and unstack to create a pivot table
    heatmap_data = df.groupby(["Day", "TimeSlot"]).size().unstack(fill_value=0)
    heatmap_data = heatmap_data.reindex(days_order)  # Ensure correct day order

    # Create the heatmap using Plotly Express' imshow
    fig = px.imshow(
        heatmap_data,
        labels={
            "x": "Time Slots (3-hour intervals)",
            "y": "Day of the Week",
            "color": "Order Count"
        },
        x=heatmap_data.columns,
        y=heatmap_data.index,
        color_continuous_scale='YlOrRd',
        text_auto=True,
        aspect="auto",
        title="Order Frequency Heatmap (Time vs. Day)"
    )

    fig.update_xaxes(side="bottom")
    
    
    return fig



def generate_cdf_plot(df):
    df_zomato = df[df["Platform"] == "Zomato"]
    df_swiggy = df[df["Platform"] == "Swiggy"]
    
    # Compute cumulative data for Zomato
    sorted_prices_zomato = np.sort(df_zomato["Price"])
    cumulative_percentage_zomato = np.arange(1, len(sorted_prices_zomato) + 1) / len(sorted_prices_zomato) * 100
    
    # Compute cumulative data for Swiggy
    sorted_prices_swiggy = np.sort(df_swiggy["Price"])
    cumulative_percentage_swiggy = np.arange(1, len(sorted_prices_swiggy) + 1) / len(sorted_prices_swiggy) * 100
    
    # Create the figure and add traces for each platform
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=sorted_prices_zomato,
        y=cumulative_percentage_zomato,
        mode="lines",
        line=dict(color="red", width=2),
        name="Zomato"
    ))
    
    fig.add_trace(go.Scatter(
        x=sorted_prices_swiggy,
        y=cumulative_percentage_swiggy,
        mode="lines",
        line=dict(color="orange", width=2),
        name="Swiggy"
    ))
    
    fig.update_layout(
        title="Cumulative Percentage of Orders by Price",
        xaxis_title="Price (Rs)",
        yaxis_title="Percentage of Orders ≤ Price",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        hovermode="x"
    )
    
    return fig

def generate_meal_popularity_heatmap(df):
    # Ensure 'Day' is a categorical variable with the correct order
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    df['Day'] = pd.Categorical(df['Day'], categories=days_order, ordered=True)
    
    # Group by 'Meal' and 'Day' to calculate order frequency and pivot the result
    heatmap_data_freq = df.groupby(['Meal', 'Day']).size().unstack(fill_value=0)
    
    # Create a heatmap using Plotly Express' imshow
    fig = px.imshow(
        heatmap_data_freq,
        text_auto=True,
        color_continuous_scale='YlOrRd',
        labels={"x": "Day of the Week", "y": "Meal Type", "color": "Order Count"},
        x=heatmap_data_freq.columns,
        y=heatmap_data_freq.index,
        title="Meal Type Popularity Heatmap (Order Frequency)"
    )
    
    # Update layout for a clean appearance (x-axis labels on the bottom)
    fig.update_layout(
        xaxis={"side": "bottom"},
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )
    
    return fig

# Custom CSS for a polished look
st.markdown(
    """
    <style>
        body {
            font-family: 'Arial', sans-serif;
        }
        .main-title {
            font-size: 36px;
            font-weight: bold;
            color: #FF4B4B;
            text-align: center;
            padding: 10px;
        }
        .subheader {
            font-size: 20px;
            font-weight: bold;
            color: #555;
            text-align: center;
            margin-bottom: 20px;
        }
        .popular-opinion {
            background: linear-gradient(135deg, #ffe5b4, #ffb4b4); 
            padding: 15px;
            border-radius: 10px;
            border-left: 5px solid #FF4B4B;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
            text-align: center;
            font-size: 18px;
        }
        .counter-container {
            text-align: center;
            margin: 30px 0;
        }
        .counter-box {
            font-size: 24px;
            font-weight: bold;
            color: #fff;
            padding: 10px 20px;
            border-radius: 10px;
            display: inline-block;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.2);
            transition: 0.3s ease-in-out;
        }
        .orders {
            background: #FF4B4B;
        }
        .spent {
            background: #FFA500;
        }
        .footer-box {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 10px;
            border-left: 5px solid #FF4B4B;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
            text-align: center;
            font-size: 18px;
            color: #555;
            margin-bottom:20px;
        }
        .hover-container {
        transition: transform 0.3s ease-in-out;
        }
        .hover-container:hover {
            transform: scale(1.05); /* Slightly enlarges on hover */
        }

       
    </style>
    """,
    unsafe_allow_html=True,
)



st.markdown(
    """
    <style>
        .lottie-container {
            margin: 30px 0;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            background-color: white; /* White background */
            padding: 20px;
            border-radius: 10px; /* Optional rounded corners */
        }

        .lottie-container2 {
            margin: 30px 0;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            background: linear-gradient(135deg, #ffe5b4, #ffb4b4); 
            padding: 20px;
            border-radius: 10px;
            border-left: 5px solid #FF4B4B;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        }
    </style>

    <div class="lottie-container2">
        <div class="main-title">Zomato Vs. Swiggy</div>
        <div class="subheader">Let's Check Out Who My Favourite Is!</div>
        
    </div>

    <div class = "lottie-container">
    <iframe src="https://lottie.host/embed/d350818b-0e21-4e25-ae05-2d3ddc0bae42/0VJml39b7L.lottie" 
                width= 100% height=100% style="border: none;">
        </iframe>
    </div>
    """,
    unsafe_allow_html=True
)


st.markdown("<br><br>", unsafe_allow_html=True)


df_zomato = preprocess_data_zomato("./zomato.csv")  # Replace with your actual CSV file
df_swiggy = preprocess_data_swiggy("./swiggy.csv")
df = preprocess_data_both("./both.csv")

total_zomato = len(df_zomato)
total_swiggy = len(df_swiggy)

# Create two columns side-by-side for the counters
col1, col2 = st.columns(2)

# Create empty placeholders for the animated numbers
zomato_placeholder = col1.empty()
swiggy_placeholder = col2.empty()

# Animate Zomato counter in red
for i in range(1, total_zomato + 1, max(1, total_zomato // 100)):
    zomato_placeholder.markdown(
        f"""
        <div style="font-size: 32px; font-weight: bold; color: red; text-align: center;">
            {i}
        </div>
        """,
        unsafe_allow_html=True,
    )
    time.sleep(0.01)

# Animate Swiggy counter in orange
for i in range(1, total_swiggy + 1, max(1, total_swiggy // 100)):
    swiggy_placeholder.markdown(
        f"""
        <div style="font-size: 32px; font-weight: bold; color: orange; text-align: center;">
            {i}
        </div>
        """,
        unsafe_allow_html=True,
    )
    time.sleep(0.005)

# Ensure final numbers are displayed
zomato_placeholder.markdown(
    f"""
    <div style="font-size: 32px; font-weight: bold; color: red; text-align: center;">
        {total_zomato}
    </div>
    """,
    unsafe_allow_html=True,
)
swiggy_placeholder.markdown(
    f"""
    <div style="font-size: 32px; font-weight: bold; color: orange; text-align: center;">
        {total_swiggy}
    </div>
    """,
    unsafe_allow_html=True,
)

# Create a new row of two columns for the descriptive text boxes
text_col1, text_col2 = st.columns(2)

text_col1.markdown(
    """
   <div style="font-size: 22px; font-weight: bold; color: orange; text-align: center;">
        <p style="color: red;">
            Total orders on Zomato
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

text_col2.markdown(
   """
   <div style="font-size: 22px; font-weight: bold; color: orange; text-align: center;">
        <p style="color: orange;">
            Total orders on Swiggy
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


st.markdown("<br><br>", unsafe_allow_html=True)
# Load data


# Count occurrences of each platform
platform_counts = df['Platform'].value_counts()

# Layout using columns for side-by-side alignment
col1, col2 = st.columns([1, 1])  # Adjust width ratio as needed

with col1:
    st.markdown(
        """
        <div style="margin-top: 20px;  height: 400px; padding: 15px; background: #f8f9fa; border-radius: 10px; border-left: 5px solid #FF4B4B; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);">
            <h4 style="color: #FF4B4B;">Zomato Trumps Swiggy!</h4>
            <p style="font-size: 16px; color: #333;">
                Over the years, I've primarily ordered from <b>Zomato</b> and <b>Swiggy</b>. 
                The pie chart on the right represents my overall platform usage. 
                While both platforms serve my cravings, <b>Zomato</b> seems to be my go-to more often! 🍽️
                The reason, you ask? Well back in 2023, Zomato's Gold Membership was given for only ₹60 while Swiggy One was more pricey, hence the bias toawards Zomato.
                However today, both fall within the same price range, hence I actively use both apps today.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.plotly_chart(generate_donut_chart(platform_counts), use_container_width=True)

st.markdown("<br><br>", unsafe_allow_html=True)






# Initialize slide state
if "slide" not in st.session_state:
    st.session_state["slide"] = 1

# Create three columns (left button, content, right button)
col_left, col_content, col_right = st.columns([1, 10, 1])

# Left Arrow (Previous)
with col_left:
    if st.button("◀", key="prev") and st.session_state["slide"] > 1:
        st.session_state["slide"] -= 1

# Right Arrow (Next)
with col_right:
    if st.button("▶", key="next") and st.session_state["slide"] < 4:
        st.session_state["slide"] += 1

# Show content based on slide number
with col_content:
    if st.session_state["slide"] == 1:
        # Scatter Plot Section
        # col1, col2 = st.columns([1.5, 1])

        # with col2:
            

        # with col1:
            st.plotly_chart(generate_scatter_plot(df), use_container_width=True)
            st.markdown(
                """
                <div style=" padding: 15px; background-color: #f8f9fa; border-radius: 10px; border-right: 5px solid #FF4B4B; height: 100%;">
                    <p style="color: black;"> The above plots reveals that most orders land in the same price range,
                      with both Zomato and Swiggy used regularly for everyday meals. 
                      The occasional high-priced outliers on Zomato indicates a tendency to place more costly items on Zomato, 
                      but overall my spending pattern appears to be consistent across both platforms.</p>
                </div>
                """,
                unsafe_allow_html=True
            )

    elif st.session_state["slide"] == 3:
        # CDF Plot Section
        # col1, col2 = st.columns([1, 1.5])

        # with col1:
       

        # with col2:
            st.plotly_chart(generate_cdf_plot(df), use_container_width=True)
            st.markdown(
               """
                <div style=" padding: 15px; background-color: #f8f9fa; border-radius: 10px; border-right: 5px solid #FF4B4B; height: 100%;">
                    <p style="color: black;"> The above plots reveals that most orders land in the same price range,
                      with both Zomato and Swiggy used regularly for everyday meals. 
                      The occasional high-priced outliers on Zomato indicates a tendency to place more costly items on Zomato, 
                      but overall my spending pattern appears to be consistent across both platforms.</p>
                </div>
                """,
                unsafe_allow_html=True
            )

    elif st.session_state["slide"] == 4:  # Adjust the slide number as needed
       
            st.plotly_chart(generate_price_histogram(df), use_container_width=True)

        
    elif st.session_state['slide'] == 2:
        st.plotly_chart(generate_box_plot_price(df), use_container_width=True)
        st.markdown(
                """
                <div style=" padding: 15px; background-color: #f8f9fa; border-radius: 10px; border-right: 5px solid #FF4B4B; height: 100%;">
                    <p style="color: black;"> The above plots reveals that most orders land in the same price range,
                      with both Zomato and Swiggy used regularly for everyday meals. 
                      The occasional high-priced outliers on Zomato indicates a tendency to place more costly items on Zomato, 
                      but overall my spending pattern appears to be consistent across both platforms.</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        



st.markdown("<br><br>", unsafe_allow_html=True)



st.markdown("<br><br>", unsafe_allow_html=True)
# Initialize slide state
if "slide_food" not in st.session_state:
    st.session_state["slide_food"] = 1

# Create three columns (left button, content, right button)
col_left, col_content, col_right = st.columns([1, 10, 1])

# Left Arrow (Previous)
with col_left:
    if st.button("◀", key="prev_food") and st.session_state["slide_food"] > 1:
        st.session_state["slide_food"] -= 1

# Right Arrow (Next)
with col_right:
    if st.button("▶", key="next_food") and st.session_state["slide_food"] < 2:
        st.session_state["slide_food"] += 1

# Show content based on slide number
with col_content:
    if st.session_state["slide_food"] == 1:
        # col1, col2 = st.columns([1.5, 1])

        # with col1:
        st.plotly_chart(generate_day_distribution_plot(df), use_container_width=True)

        # with col2:
        st.markdown(
                """
                <div style="margin-top: 30px; padding: 15px; background-color: #f8f9fa; border-radius: 10px; border-right: 5px solid #FF4B4B; height: 100%;">
                    <p style="color: black;">
                    Both platforms were used throughout the week and on different times of the day, indicating no single “dominant” platform—just a slight day-to-day preference that could be driven by coupons, offers, or just a personal routine.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

    elif st.session_state["slide_food"] == 2:
        # col1, col2 = st.columns([1.5, 1])

        # with col1:
        st.plotly_chart(generate_meal_distribution_plot(df), use_container_width=True)

        # with col2:
        st.markdown(
                 """
                <div style="margin-top: 30px; padding: 15px; background-color: #f8f9fa; border-radius: 10px; border-right: 5px solid #FF4B4B; height: 100%;">
                    <p style="color: black;">
                    Both platforms were used throughout the week and on different times of the day, indicating no single “dominant” platform—just a slight day-to-day preference that could be driven by coupons, offers, or just a personal routine.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
        



