import streamlit as st
import time
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.figure_factory as ff
import re
import random
from collections import Counter
from wordcloud import WordCloud

def preprocess_data(filepath):
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

df = preprocess_data("./both.csv") 



def generate_restaurant_bar_chart(df):
    # Get top 10 restaurants by order count
    restaurant_counts = df['Restaurant'].value_counts().head(10).reset_index()
    restaurant_counts.columns = ['Restaurant', 'Count']
    
    # Create a bar chart using Plotly Express
    fig = px.bar(
        restaurant_counts,
        x='Restaurant',
        y='Count',
        title='Top 10 Restaurants',
        labels={'Restaurant': 'Restaurant', 'Count': 'Order Count'},
        color='Restaurant',
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    
    # Rotate x-axis labels for better readability and set theme
    fig.update_layout(
        xaxis_tickangle=45,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )
    
    return fig

def generate_animated_restaurant_bar_chart(df):
    # Ensure the "Date " column is datetime and sort by date
    df["Date "] = pd.to_datetime(df["Date "])
    df_sorted = df.sort_values("Date ")
    
    # Group by Date and Restaurant; count orders, then pivot so each column is a restaurant
    pivot = df_sorted.groupby(["Date ", "Restaurant"]).size().unstack(fill_value=0)
    
    # Compute cumulative counts so that each frame adds up over time
    cumulative = pivot.cumsum()
    
    # Add an initial row (one day before the earliest date) with zeros (starting with an empty state)
    initial_date = cumulative.index.min() - pd.Timedelta(days=1)
    zero_row = pd.DataFrame({col: 0 for col in cumulative.columns}, index=[initial_date])
    cumulative = pd.concat([zero_row, cumulative]).sort_index()
    
    # Reset index and convert from wide to long format
    cumulative_reset = cumulative.reset_index().rename(columns={"index": "Date "})
    df_long = cumulative_reset.melt(id_vars="Date ", var_name="Restaurant", value_name="Count")
    
    # Create a formatted date string for animation frames
    df_long["Date_str"] = df_long["Date "].dt.strftime("%Y-%m-%d")
    
    # Compute ranking for each date so we can sort dynamically (highest count gets rank 1)
    df_long["Rank"] = df_long.groupby("Date ")["Count"].rank(method="first", ascending=False)
    # Sort by date and then by rank
    df_long = df_long.sort_values(["Date ", "Rank"])
    
    # Create the animated horizontal bar chart using Plotly Express
    fig = px.bar(
        df_long,
        x="Count",
        y="Restaurant",
        color="Restaurant",
        orientation="h",
        animation_frame="Date_str",
        animation_group="Restaurant",
        range_x=[0, df_long["Count"].max() * 1.1],
        labels={"Count": "Order Count", "Restaurant": "Restaurant"},
        title="Cumulative Order Frequency by Restaurant Over Time"
    )
    
    # Update layout: reverse the y-axis so that the highest counts are at the top;
    # adjust margins for long restaurant names and the slider.
    fig.update_layout(
        yaxis={'autorange': "reversed"},
        margin=dict(l=150, b=150),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        transition={'duration': 100}
    )
    
    # For each animation frame, compute the ordering of restaurants by the current cumulative count
    # and update the frame's y-axis category order.
    for frame in fig.frames:
        # Collect counts from this frame; assume each trace corresponds to one restaurant.
        restaurant_counts = {}
        for trace in frame.data:
            # trace.name holds the restaurant name; trace.x is a list with the count
            if trace.x and len(trace.x) > 0:
                restaurant_counts[trace.name] = trace.x[0]
        # Sort restaurants in descending order (highest count first)
        sorted_restaurants = [r for r, _ in sorted(restaurant_counts.items(), key=lambda x: x[1], reverse=True)]
        # Set the category order for this frame's y-axis
        frame.layout = frame.layout or {}
        frame.layout["yaxis"] = {"categoryorder": "array", "categoryarray": sorted_restaurants}
    
    # Also update the main figure's y-axis using the final frame's order.
    if fig.frames:
        final_frame = fig.frames[-1]
        restaurant_counts = {}
        for trace in final_frame.data:
            if trace.x and len(trace.x) > 0:
                restaurant_counts[trace.name] = trace.x[0]
        sorted_restaurants = [r for r, _ in sorted(restaurant_counts.items(), key=lambda x: x[1], reverse=True)]
        # Update the main figure's y-axis with this ordering.
        fig.update_yaxes(categoryorder="array", categoryarray=sorted_restaurants)
    
    # Set the active slider to the last frame and update the main figure's traces
    if fig.frames:
        fig.layout.sliders[0].active = len(fig.frames) - 1
        final_frame = fig.frames[-1]
        for i, trace in enumerate(fig.data):
            trace.x = final_frame.data[i].x
            trace.y = final_frame.data[i].y
    
    return fig

def generate_animated_type_histogram(df):
    # Ensure "Date " is datetime and sort the DataFrame by date
    df["Date "] = pd.to_datetime(df["Date "])
    df_sorted = df.sort_values("Date ")

    # Explode the "Type" column: split comma-separated values and strip extra spaces
    df_sorted["Type"] = df_sorted["Type"].apply(lambda x: [t.strip() for t in x.split(',')])
    df_exploded = df_sorted.explode("Type")
    
    # Group by Date and Type and count occurrences
    pivot = df_exploded.groupby(["Date ", "Type"]).size().unstack(fill_value=0)
    
    # Compute cumulative counts so that each frame adds up over time
    cumulative = pivot.cumsum()
    
    # Add an initial row (one day before the earliest date) with zeros to start animation at 0
    initial_date = cumulative.index.min() - pd.Timedelta(days=1)
    zero_row = pd.DataFrame({col: 0 for col in cumulative.columns}, index=[initial_date])
    cumulative = pd.concat([zero_row, cumulative]).sort_index()
    
    # Reset index and convert from wide to long format
    cumulative_reset = cumulative.reset_index().rename(columns={"index": "Date "})
    df_long = cumulative_reset.melt(id_vars="Date ", var_name="Type", value_name="Count")
    
    # Create a formatted date string for the animation frame
    df_long["Date_str"] = df_long["Date "].dt.strftime("%Y-%m-%d")
    
    # Create the animated bar chart using Plotly Express
    fig = px.bar(
        df_long,
        x="Type",
        y="Count",
        color="Type",
        animation_frame="Date_str",
        animation_group="Type",
        range_y=[0, df_long["Count"].max() * 1.1],
        labels={"Count": "Count", "Type": "Cuisine Type"},
        title="Cumulative Histogram of Cuisine Types Over Time"
    )
    
    # Update layout: rotate x-axis labels, set transparent backgrounds, and speed up transitions
    fig.update_layout(
        xaxis_tickangle=45,
        margin=dict(b=150),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        transition={'duration': 100}  # Transition duration in milliseconds
    )
    
    # Set the active slider to the last frame and update trace data so the final frame is displayed on load
    if fig.frames:
        fig.layout.sliders[0].active = len(fig.frames) - 1
        final_frame = fig.frames[-1]
        # Update each trace in the main figure with data from the corresponding trace in the final frame
        for i, trace in enumerate(fig.data):
            trace.x = final_frame.data[i].x
            trace.y = final_frame.data[i].y

    return fig



def generate_animated_food_distribution_chart(df):
    # Ensure the "Date " column is datetime and sort by date
    df["Date "] = pd.to_datetime(df["Date "])
    df_sorted = df.sort_values("Date ")
    
    # Melt Food1 and Food2 columns into a long format; remove 'None' entries
    df_melted = df_sorted.melt(id_vars=["Date "], value_vars=["Food1", "Food2"], value_name="food")
    df_melted = df_melted[df_melted["food"] != "None"]
    
    # Group by Date and food; count occurrences and pivot
    pivot = df_melted.groupby(["Date ", "food"]).size().unstack(fill_value=0)
    
    # Compute cumulative counts over time (each date adds to the previous totals)
    cumulative = pivot.cumsum()
    
    # Add an initial row with zeros (to start the animation from an empty state)
    initial_date = cumulative.index.min() - pd.Timedelta(days=1)
    zero_row = pd.DataFrame({col: 0 for col in cumulative.columns}, index=[initial_date])
    cumulative = pd.concat([zero_row, cumulative]).sort_index()
    
    # Convert the cumulative DataFrame to long format
    cumulative_reset = cumulative.reset_index().rename(columns={"index": "Date "})
    df_long = cumulative_reset.melt(id_vars="Date ", var_name="food", value_name="Count")
    
    # Create a formatted date string for animation frames
    df_long["Date_str"] = df_long["Date "].dt.strftime("%Y-%m-%d")
    
    # Create the animated horizontal bar chart
    fig = px.bar(
        df_long,
        x="Count",
        y="food",
        color="food",
        orientation="h",
        animation_frame="Date_str",
        animation_group="food",
        range_x=[0, df_long["Count"].max() * 1.1],
        labels={"Count": "Order Count", "food": "Food Item"},
        title="Cumulative Food Order Frequency Over Time"
    )
    
    # Update layout: ensure a transparent background and adjust ordering of bars
    fig.update_layout(
        yaxis={'categoryorder': 'total ascending'},
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        transition={'duration': 100},
        margin=dict(b=150)  # Extra bottom margin if needed
    )
    
    # Set the active slider to the last frame and update traces to display the final data
    if fig.frames:
        fig.layout.sliders[0].active = len(fig.frames) - 1
        final_frame = fig.frames[-1]
        for i, trace in enumerate(fig.data):
            trace.x = final_frame.data[i].x
            trace.y = final_frame.data[i].y
            
    return fig


def generate_wordcloud_figure(corpus, width=800, height=400, title="Word Cloud"):
    # Generate the word cloud image from the corpus
    wc = WordCloud(width=width, height=height, background_color='white').generate(corpus)
    # Convert the WordCloud image to a NumPy array
    wc_array = wc.to_array()
    # Create an interactive Plotly figure using px.imshow
    fig = px.imshow(wc_array, title=title)
    # Hide axes for a cleaner look
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    # Set transparent backgrounds
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )
    return fig


def generate_animated_cumulative_cuisine_price_boxplot(df):
    # Convert and sort dates
    df["Date "] = pd.to_datetime(df["Date "])
    df_sorted = df.sort_values("Date ")
    
    # Expand the "Type" column: split comma-separated values and clean strings
    expanded_rows = []
    for idx, row in df_sorted.iterrows():
        types = row["Type"].split(',')
        for t in types:
            expanded_rows.append({
                "Cuisine": t.strip(),
                "Price": row["Price"],
                "Platform": str(row["Platform"]).strip().capitalize(),  # e.g., "swiggy" -> "Swiggy"
                "Date": row["Date "]
            })
    df_expanded = pd.DataFrame(expanded_rows)
    
    # Force Platform as categorical with fixed categories
    df_expanded["Platform"] = pd.Categorical(
        df_expanded["Platform"],
        categories=["Zomato", "Swiggy"],
        ordered=True
    )
    
    # Build cumulative dataset: for each day, include all orders up to that day.
    all_dates = pd.date_range(start=df_expanded["Date"].min(), end=df_expanded["Date"].max(), freq="D")
    cumulative_frames = []
    for d in all_dates:
        frame_df = df_expanded[df_expanded["Date"] <= d].copy()
        frame_df["Frame"] = d.strftime("%Y-%m-%d")
        cumulative_frames.append(frame_df)
    df_cumulative = pd.concat(cumulative_frames, ignore_index=True)
    
    # Get unique frames and cuisines from the cumulative data.
    unique_frames = df_cumulative["Frame"].unique()
    unique_cuisines = df_cumulative["Cuisine"].unique()
    platforms = ["Zomato", "Swiggy"]
    
    # Create a complete grid of all combinations (Frame x Cuisine x Platform)
    complete_index = pd.MultiIndex.from_product([unique_frames, unique_cuisines, platforms],
                                                  names=["Frame", "Cuisine", "Platform"])
    complete_df = pd.DataFrame(index=complete_index).reset_index()
    
    # Merge the complete grid with our cumulative data on (Frame, Cuisine, Platform)
    df_merged = pd.merge(complete_df, df_cumulative, on=["Frame", "Cuisine", "Platform"], how="left")
    # The "Price" from the cumulative data will be NaN for missing combinations.
    # We'll keep those rows so that Plotly always sees both platforms.
    
    # Create the animated box plot using Plotly Express.
    fig = px.box(
        df_merged,
        x="Cuisine",
        y="Price",
        color="Platform",
        animation_frame="Frame",
        category_orders={"Platform": ["Zomato", "Swiggy"]},
        color_discrete_map={"Zomato": "red", "Swiggy": "orange"},
        title="Box Plot of Cuisine vs. Price for Zomato and Swiggy (Cumulative)",
        labels={"Cuisine": "Cuisine Type", "Price": "Price"}
    )
    
    # Update layout for clarity: rotate x-axis labels and set transparent backgrounds.
    fig.update_layout(
        xaxis_tickangle=45,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )
    
    # Force the final frame to be displayed by default.
    if fig.frames:
        fig.layout.sliders[0].active = len(fig.frames) - 1
        final_frame = fig.frames[-1]
        for i, trace in enumerate(fig.data):
            trace.x = final_frame.data[i].x
            trace.y = final_frame.data[i].y
            
    return fig


def generate_cuisine_meal_heatmap(df):
    # Explode the 'Type' column into individual cuisines and strip whitespace
    df['Type'] = df['Type'].str.split(',')
    df_exploded = df.explode('Type')
    df_exploded['Type'] = df_exploded['Type'].str.strip()
    
    # Convert quantity columns to numeric and fill missing values with 0
    df_exploded['Quantity1'] = pd.to_numeric(df_exploded['Quantity1'], errors='coerce').fillna(0)
    df_exploded['Quantity2'] = pd.to_numeric(df_exploded['Quantity2'], errors='coerce').fillna(0)
    df_exploded['Total_Quantity'] = df_exploded['Quantity1'] + df_exploded['Quantity2']
    
    # Create a pivot table: index = 'Type', columns = 'Meal', values = sum of 'Total_Quantity'
    heatmap_data = df_exploded.pivot_table(
        index='Type',
        columns='Meal',
        values='Total_Quantity',
        aggfunc='sum',
        fill_value=0
    )
    
    # Create the heatmap using Plotly Express
    fig = px.imshow(
        heatmap_data,
        text_auto=True,  # Annotate the cells with values
        color_continuous_scale='YlGnBu',
        labels={"x": "Meal Type", "y": "Cuisine Type", "color": "Total Quantity"},
        title="Cuisine Type Popularity by Meal Type"
    )
    
    # Update layout for a clean, readable display
    fig.update_layout(
        xaxis=dict(tickangle=45),
        yaxis=dict(autorange="reversed"),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )
    
    fig.update_layout(width=800, height=600)

    return fig


def generate_top10_restaurant_boxplot(df):
    # Compute top 10 restaurants by frequency
    top10_restaurants = df['Restaurant'].value_counts().head(10).index.tolist()
    
    # Filter the DataFrame to only include rows for the top 10 restaurants
    df_top = df[df['Restaurant'].isin(top10_restaurants)]
    
    # Create a box plot using Plotly Express
    fig = px.box(
        df_top,
        x='Restaurant',
        y='Price',
        title='Box Plot of Price by Restaurant (Top 10)',
        labels={'Restaurant': 'Restaurant', 'Price': 'Price'},
        category_orders={'Restaurant': top10_restaurants}  # maintain the order from most frequent
    )
    
    # Update layout: rotate x-axis labels and use transparent background
    fig.update_layout(
        xaxis_tickangle=45,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )
    
    return fig

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
    </style>

    <div class="lottie-container">
        <div class="main-title">My Favourite Restaurants & Cuisines</div>
        <div class="subheader">Diving into the flavors and hotspots that keep me coming back for more!</div>
        <iframe src="https://lottie.host/embed/89a73ffa-66c7-483d-b481-f7581e7de7f5/F0u66iGpq8.lottie" 
                 width="100%" height="100%"style="border: none;">
         </iframe>
    </div>
    """,
    unsafe_allow_html=True
)


import streamlit as st

# Inject custom CSS for flip animation
st.markdown(
    """
    <style>
        @keyframes flipIn {
            0% {
                transform: rotateX(-90deg);
                opacity: 0;
            }
            100% {
                transform: rotateX(0deg);
                opacity: 1;
            }
        }
        .flip-widget {
            animation: flipIn 0.8s ease-out;
        }
        .restaurant-box {
            background-color: #f8f9fa;
            border-top: 5px solid #FF4B4B;
            padding: 10px;
            margin: 5px;
            border-radius: 10px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
            text-align: center;
            font-size: 20px;
            font-weight: bold;
            color: #333;
            height: 100px;
        }
    </style>
    """,
    unsafe_allow_html=True
)


food_corpus = (
    ' '.join(df[df['Food1'] != 'None']['Food1'].astype(str)) + ' ' +
    ' '.join(df[df['Food2'] != 'None']['Food2'].astype(str))
)
restaurant_corpus = ' '.join(df[df['Restaurant'] != 'None']['Restaurant'].astype(str))

# Generate word cloud figures
restaurant_wc_fig = generate_wordcloud_figure(restaurant_corpus, title="Restaurant Word Cloud")
food_wc_fig = generate_wordcloud_figure(food_corpus, title="Food Word Cloud")

st.plotly_chart(restaurant_wc_fig, use_container_width=True)

st.markdown("### My Top 5 Restaurants Are:")

# Replace these with your actual top restaurant names
top_restaurants = ["Haldiram's", "La Pinoz", "Pizza Hut", "90's Cafe Chapter 2", "Nomad's Cafe"]

# Create 5 columns for the top 5 restaurants
cols = st.columns(5)

for col, restaurant in zip(cols, top_restaurants):
    col.markdown(
        f"""
        <div class="flip-widget restaurant-box popular-opinion">
            {restaurant}
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<br><br>", unsafe_allow_html=True)



if "restaurant_slide" not in st.session_state:
    st.session_state["restaurant_slide"] = 1

# Create three columns for the slider navigation: left arrow, content, right arrow
col_left, col_content, col_right = st.columns([1, 10, 1])

# Left Arrow (Previous)
with col_left:
    if st.button("◀", key="prev_restaurant") and st.session_state["restaurant_slide"] > 1:
        st.session_state["restaurant_slide"] -= 1

# Right Arrow (Next)
with col_right:
    if st.button("▶", key="next_restaurant") and st.session_state["restaurant_slide"] < 3:
        st.session_state["restaurant_slide"] += 1

# Display content based on slide number
with col_content:
    if st.session_state["restaurant_slide"] == 2:
        st.markdown("### Sreya's Top Restaurants")
        st.plotly_chart(generate_restaurant_bar_chart(df), use_container_width=True)
    elif st.session_state["restaurant_slide"] == 1:
        st.markdown("### Restaurants' Frequencies Over Time")
        st.plotly_chart(generate_animated_restaurant_bar_chart(df), use_container_width=True)

    elif st.session_state["restaurant_slide"] == 3:
        st.markdown("### Box Plots for Top 10 Restaurants")
        st.plotly_chart(generate_top10_restaurant_boxplot(df), use_container_width=True)
        st.markdown(
    """
    <div style="margin-top: 30px; padding: 15px; background-color: #f8f9fa; 
                border-radius: 10px; border-right: 5px solid #FF4B4B; height: 100%;">
        <p style="color: black; font-size: 16px; line-height: 1.5;">
            The reason for the low variation in prices at many restaurants is simple: I tend to order the same favorite dish over and over again! 😋 
            Once I find a dish that consistently hits the spot, it becomes my go-to order—my little comfort zone (trust issues, you know! 🤷‍♂️).<br><br>
            So why do we see high variation in places like Pizza Hut and McDonald’s? 🤔 Because you can never go wrong with a cheesy pizza 🍕 or a juicy burger 🍔—variety keeps it fun and exciting!
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


st.markdown("<br>", unsafe_allow_html=True)

st.markdown("### My Top 3 Cuisines Are:")

# Replace these with your actual top restaurant names
top_cuisines = ["American", "North Indian", "Italian"]

# Create 5 columns for the top 5 restaurants
cols = st.columns(3)

for col, restaurant in zip(cols, top_cuisines):
    col.markdown(
        f"""
        <div class="flip-widget restaurant-box popular-opinion">
            {restaurant}
        </div>
        """,
        unsafe_allow_html=True
    )
st.markdown("<br><br>", unsafe_allow_html=True)
# st.plotly_chart(generate_animated_type_histogram(df), use_container_width=True)


# st.plotly_chart(generate_animated_cumulative_cuisine_price_boxplot(df), use_container_width=True)


# st.markdown(
#                 """
#                 <div style="margin-top: 30px; padding: 15px; background-color: #f8f9fa; border-radius: 10px; border-right: 5px solid #FF4B4B; height: 100%;">
#                     <p style="color: black;">
#                     While the prices of most of the cuisines are comaprable on both the platforms, we see broader dessert range in Zomato and a higher median for Italian cuisine in Zomato than Swiggy.
#                     The wider dessert range on Zomato hints at either specialized or premium dessert options that I occasionally splurge on (like birthday cakes), while 
#                     the similar pricing for most other cuisines indicates that the platforms can be used interchangeably.
#                     Italian cuisine can range from high-end to more casual, chain restaurant options.
#                     I might order a higher proportion of upscale Italian restaurants offering premium, artisanal dishes from Zomato, while I might use Swiggy to lean towards budget-friendly or standardized fare. 
#                     This maybe lead to a noticeable difference in prcing.
#                     </p>
#                 </div>
#                 """,
#                 unsafe_allow_html=True
#             )




# Initialize slider state for the two slides
if "analysis_slide" not in st.session_state:
    st.session_state["analysis_slide"] = 1

# Create three columns: left arrow, content, and right arrow
col_left, col_content, col_right = st.columns([1, 10, 1])

# Left Arrow (Previous)
with col_left:
    if st.button("◀", key="prev_analysis") and st.session_state["analysis_slide"] > 1:
        st.session_state["analysis_slide"] -= 1

# Right Arrow (Next)
with col_right:
    if st.button("▶", key="next_analysis") and st.session_state["analysis_slide"] < 3:
        st.session_state["analysis_slide"] += 1

# Show content based on the current slide
with col_content:
    if st.session_state["analysis_slide"] == 1:
        st.markdown("### Cumulative Distribution of Cuisine Types")
        st.plotly_chart(generate_animated_type_histogram(df), use_container_width=True)
        st.markdown(
    """
    <div style="margin-top: 30px; padding: 15px; background-color: #f8f9fa; 
                border-radius: 10px; border-right: 5px solid #FF4B4B; height: 100%;">
        <p style="color: black; font-size: 16px; line-height: 1.5;">
            Who doesn't love a good slice of cheesy pizza 🍕—yes, I even classify pizza as American (sue me! 😜). 
            But in my defense, we’re talking about the American version, not the authentic Italian one.
            And then there’s that big, juicy burger 🍔 that hits the spot every time. No wonder American cuisine is my go-to choice!
            <br><br>
            I'm also a fan of North Indian food, which comes in a close second—after all, we all crave the comfort of home.
            My love for Italian cuisine will last forever ❤️, but since it's a bit on the pricey side, I tend to lean towards American flavors.
            And as for desserts? Well, I never really had a sweet tooth, so the dip in dessert orders isn’t surprising. 
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

    elif st.session_state["analysis_slide"] == 2:
        st.markdown("### Cuisine vs. Price for Zomato & Swiggy")
        st.plotly_chart(generate_animated_cumulative_cuisine_price_boxplot(df), use_container_width=True)
        st.markdown(
            """
            <div style="margin-top: 30px; padding: 15px; background-color: #f8f9fa; 
                        border-radius: 10px; border-right: 5px solid #FF4B4B; height: 100%;">
                <p style="color: black;">
                    While the prices of most cuisines are comparable on both platforms, we observe a broader dessert range 
                    and a higher median for Italian cuisine on Zomato compared to Swiggy. The wider dessert range on Zomato 
                    hints at specialized or premium dessert options that I occasionally splurge on (like birthday cakes), while 
                    the similar pricing for most other cuisines indicates that the platforms can be used interchangeably. 
                    Additionally, Italian cuisine may vary due to diverse offerings, with Zomato featuring more upscale or 
                    artisanal options.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    elif st.session_state['analysis_slide'] == 3:
        st.plotly_chart(generate_cuisine_meal_heatmap(df), use_container_width=True)



st.markdown("<br><br>", unsafe_allow_html=True)
st.plotly_chart(generate_animated_food_distribution_chart(df), use_container_width=True)
st.markdown(
    """
    <div style="margin-top: 30px; padding: 15px; background-color: #f8f9fa; 
                border-radius: 10px; border-right: 5px solid #FF4B4B; height: 100%;">
        <p style="color: black; font-size: 16px; line-height: 1.5;">
            My Top 5 Food Items: <b>Pasta</b>, <b>Rice Bowls</b>, <b>Fries</b>, <b>Pizza</b>, and <b>Chaat</b>. 
            Based on my previous analysis, Pasta, Pizza, and Rice Bowls might seem a bit predictable – sometimes you just need that comforting classic! 🍝🍕🥘<br><br>
            And let’s be honest, we all crave a good snack to munch on, especially now that the mess has stopped serving snacks! 😢🍟 
            A tasty bite can brighten any day! 😋
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("<br><br>", unsafe_allow_html=True)


# Display the figures in Streamlit
st.markdown("<br>", unsafe_allow_html=True)
st.plotly_chart(food_wc_fig, use_container_width=True)

