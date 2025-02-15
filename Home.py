import streamlit as st
import time
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.figure_factory as ff



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




def generate_scatter_plot(df):
    fig = px.scatter(
        df, 
        x=df.index, 
        y="Price", 
        title="Price vs Index",
        labels={"x": "Index", "Price": "Price"},
        size="Price",      # Marker size is proportional to Price
        size_max=20        # Optional: cap the maximum marker size
    )

    fig.update_layout(
        hovermode="closest",
        plot_bgcolor="rgba(0,0,0,0)",  # Transparent background
        paper_bgcolor="rgba(0,0,0,0)"
    )

    # Update the trace for additional marker styling
    fig.update_traces(
        marker=dict(opacity=0.7, line=dict(width=2, color="black")),
        hoverinfo="text"
    )

    return fig





def generate_price_histogram(df):
    fig = ff.create_distplot(
        [df["Price"]], 
        ["Price Distribution"], 
        bin_size=20, 
        curve_type='kde', 
        colors=['blue']
    )

    fig.update_layout(
        title="Price Distribution with Histogram and KDE Curve",
        xaxis_title="Price",
        yaxis_title="Density",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )

    return fig


def generate_day_distribution_plot(df):
    # day_counts = df['Day'].value_counts().reset_index()
    # day_counts.columns = ['Day', 'Count']  # Rename columns

    # fig = px.bar(
    #     day_counts, 
    #     x='Day', 
    #     y='Count', 
    #     labels={'Day': 'Day', 'Count': 'Order Count'}, 
    #     title="Distribution of Days",
    #     color='Day', 
    #     color_discrete_sequence=px.colors.qualitative.Set2
    # )

    # fig.update_layout(
    #     xaxis_title="Day",
    #     yaxis_title="Order Count",
    #     plot_bgcolor="rgba(0,0,0,0)",
    #     paper_bgcolor="rgba(0,0,0,0)"
    # )

    # return fig
    # Ensure the "Date " column is in datetime format and sort the DataFrame by date
    df["Date "] = pd.to_datetime(df["Date "])
    df_sorted = df.sort_values("Date ")
    
    # Define the desired day order
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    # Create a pivot table: rows are dates, columns are days, values are order counts
    pivot = df_sorted.groupby(["Date ", "Day"]).size().unstack(fill_value=0)
    
    # Reindex the columns to enforce the week order; missing days are filled with 0
    pivot = pivot.reindex(columns=day_order, fill_value=0)
    
    # Compute the cumulative sum along the date axis so counts accumulate over time
    cumulative = pivot.cumsum()
    
    # Add an initial row (one day before the earliest date) with zeros so animation starts at 0
    initial_date = cumulative.index.min() - pd.Timedelta(days=1)
    zero_row = pd.DataFrame({col: [0] for col in cumulative.columns}, index=[initial_date])
    cumulative = pd.concat([zero_row, cumulative]).sort_index()
    
    # Reset index and convert the DataFrame from wide to long format
    cumulative = cumulative.reset_index().rename(columns={"index": "Date "})
    cumulative_long = cumulative.melt(id_vars="Date ", var_name="Day", value_name="Count")
    
    # Create a formatted date string for the animation frame
    cumulative_long["Date_str"] = cumulative_long["Date "].dt.strftime("%Y-%m-%d")
    
    # Create the animated bar chart using Plotly Express with the specified day order
    fig = px.bar(
        cumulative_long,
        x="Day",
        y="Count",
        color="Day",
        category_orders={"Day": day_order},
        animation_frame="Date_str",
        range_y=[0, cumulative_long["Count"].max() + 5],
        labels={"Count": "Order Count", "Day": "Day"},
        title="Cumulative Order Frequency by Day Over Time"
    )
    
    # Update layout to match the theme
    fig.update_layout(
        xaxis_title="Day",
        yaxis_title="Order Count",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )

    if fig.frames:
        fig.layout.sliders[0].active = len(fig.frames) - 1
        final_frame = fig.frames[-1]
        # Update each trace in the main figure with the final frame's trace data
        for i, trace in enumerate(fig.data):
            trace.x = final_frame.data[i].x
            trace.y = final_frame.data[i].y


    fig.update_layout(transition={'duration': .1})

    
    return fig


def generate_meal_distribution_plot(df):
    # meal_counts = df['Meal'].value_counts().reset_index()
    # meal_counts.columns = ['Meal', 'Count']  # Rename columns

    # fig = px.bar(
    #     meal_counts, 
    #     x='Meal', 
    #     y='Count', 
    #     labels={'Meal': 'Meal', 'Count': 'Order Count'}, 
    #     title="Distribution of Meals",
    #     color='Meal', 
    #     color_discrete_sequence=px.colors.qualitative.Set2
    # )

    # fig.update_layout(
    #     xaxis_title="Meal",
    #     yaxis_title="Order Count",
    #     plot_bgcolor="rgba(0,0,0,0)",
    #     paper_bgcolor="rgba(0,0,0,0)"
    # )

    # return fig

    # def generate_animated_meal_distribution_plot(df):
    # Ensure "Date " is datetime and sort the data
        df["Date "] = pd.to_datetime(df["Date "])
        df_sorted = df.sort_values("Date ")
        
        # Group by Date and Meal, then count orders
        pivot = df_sorted.groupby(["Date ", "Meal"]).size().unstack(fill_value=0)
        
        # Compute cumulative sum along the date axis so counts accumulate over time
        cumulative = pivot.cumsum()
        
        # Add an initial row (one day before the earliest date) with zeros
        initial_date = cumulative.index.min() - pd.Timedelta(days=1)
        zero_row = pd.DataFrame({col: [0] for col in cumulative.columns}, index=[initial_date])
        cumulative = pd.concat([zero_row, cumulative]).sort_index()
        
        # Reset index and convert from wide to long format
        cumulative = cumulative.reset_index().rename(columns={"index": "Date "})
        cumulative_long = cumulative.melt(id_vars="Date ", var_name="Meal", value_name="Count")
        
        # Create a formatted date string for the animation frame
        cumulative_long["Date_str"] = cumulative_long["Date "].dt.strftime("%Y-%m-%d")
        
        # Create the animated bar chart using Plotly Express
        fig = px.bar(
            cumulative_long,
            x="Meal",
            y="Count",
            color="Meal",
            animation_frame="Date_str",
            animation_group="Meal",
            range_y=[0, cumulative_long["Count"].max() + 5],
            labels={"Count": "Order Count", "Meal": "Meal"},
            title="Cumulative Order Frequency by Meal Over Time"
        )
        
        # Update layout to match the theme and speed up animation
        fig.update_layout(
            xaxis_title="Meal",
            yaxis_title="Order Count",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            transition={'duration': 100}  # 100 ms transition between frames
        )

        if fig.frames:
            fig.layout.sliders[0].active = len(fig.frames) - 1
            final_frame = fig.frames[-1]
            # Update each trace in the main figure with the final frame's trace data
            for i, trace in enumerate(fig.data):
                trace.x = final_frame.data[i].x
                trace.y = final_frame.data[i].y
        
        # Return the figure's dictionary representation
        return fig.to_dict()



def generate_box_plot_price(df):
    fig = px.box(
        df,
        y='Price',
        title='Box Plot of Price',
        labels={'Price': 'Price'}
    )
    
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
    sorted_prices = np.sort(df["Price"])
    cumulative_percentage = np.arange(1, len(sorted_prices) + 1) / len(sorted_prices) * 100

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=sorted_prices, 
        y=cumulative_percentage,
        mode="lines",
        line=dict(color="blue", width=2),
        name="Cumulative %"
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


def generate_monthly_order_histogram(df):
    # Ensure the date column is datetime. Adjust the column name as needed.
    df["Date "] = pd.to_datetime(df["Date "])
    
    # Create a 'Month' column (as string in "YYYY-MM" format)
    df["Month"] = df["Date "].dt.to_period("M").astype(str)
    
    # Group by Month and count the number of orders
    monthly_counts = df["Month"].value_counts().sort_index().reset_index()
    monthly_counts.columns = ["Month", "Order Frequency"]
    
    # Create the bar chart (histogram) using Plotly Express
    fig = px.bar(
        monthly_counts,
        x="Month",
        y="Order Frequency",
        title="Monthly Order Frequency Histogram",
        labels={"Month": "Month", "Order Frequency": "Number of Orders"}
    )
    
    # Update layout for a clean look
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis_tickangle=45
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
    </style>

    <div class="lottie-container">
        <div class="main-title">Welcome to Sreya\'s Online Food Orders STORY!!</div>
        <div class="subheader">Author : Sreya Chitluru</div>
        <iframe src="https://lottie.host/embed/cc853e3d-5774-40ce-838a-23b8dae37606/svnqqQnno2.lottie" 
                width= 100% height=100% style="border: none;">
        </iframe>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("<br><br>", unsafe_allow_html=True)

# Popular Opinion Box
st.markdown(
    """
    <div class="popular-opinion">
        🍕 <b>Popular Opinion :</b> The College's Mess food is <b>insipid</b>.
    </div>
    """,
    unsafe_allow_html=True,
)

# Dynamic Counters
total_orders = 142
total_spent = 33228

orders_placeholder = st.empty()
spent_placeholder = st.empty()

# Order Count Animation
for i in range(1, total_orders + 1, max(1, total_orders // 100)):
    orders_placeholder.markdown(
        f"""
        <div class="counter-container">
            <p style="font-size: 20px; font-weight: bold;">Over the course of <b>three years</b>, I have placed a total orders of</p>
            <span class="counter-box orders">{i}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    time.sleep(0.01)

st.markdown("<br><br>", unsafe_allow_html=True)

# Spent Money Animation
for i in range(1, total_spent + 1, max(1, total_spent // 100)):
    spent_placeholder.markdown(
        f"""
        <div class="counter-container">
            <p style="font-size: 20px; font-weight: bold;">I have spent a total of</p>
            <span class="counter-box spent">₹{i}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    time.sleep(0.0005)

# Ensure final values are displayed
orders_placeholder.markdown(
    f"""
    <div class="counter-container">
        <p style="font-size: 20px; font-weight: bold;">Over the course of <b>three years</b>, I have placed a total orders of</p>
        <span class="counter-box orders">{total_orders}</span>
    </div>
    """,
    unsafe_allow_html=True,
)

spent_placeholder.markdown(
    f"""
    <div class="counter-container">
        <p style="font-size: 20px; font-weight: bold;">I have spent a total of</p>
        <span class="counter-box spent">₹{total_spent}</span>
    </div>
    """,
    unsafe_allow_html=True,
)

# Footer Box
st.markdown(
    """
    <div class="footer-box">
        🍽️ So, as you can imagine, my Zomato and Swiggy apps are a <b>goldmine</b> of data. 
        Let's delve into some of my favorite foods, cuisines, restaurants, and other interesting trends!
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<br><br>", unsafe_allow_html=True)
# Load data
df = preprocess_data("./both.csv")  # Replace with your actual CSV file

# Count occurrences of each platform
# platform_counts = df['Platform'].value_counts()

# # Layout using columns for side-by-side alignment
# col1, col2 = st.columns([1, 1])  # Adjust width ratio as needed

# with col1:
#     st.markdown(
#         """
#         <div style="margin-top: 20px;  height: 400px; padding: 15px; background: #f8f9fa; border-radius: 10px; border-left: 5px solid #FF4B4B; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);">
#             <h4 style="color: #FF4B4B;">Zomato Trumps Swiggy!</h4>
#             <p style="font-size: 16px; color: #333;">
#                 Over the years, I've primarily ordered from <b>Zomato</b> and <b>Swiggy</b>. 
#                 The pie chart on the right represents my overall platform usage. 
#                 While both platforms serve my cravings, <b>Zomato</b> seems to be my go-to more often! 🍽️
#                 The reason, you ask? Well back in 2023, Zomato's Gold Membership was given for only ₹60 while Swiggy One was more pricey, hence the bias toawards Zomato.
#                 However today, both fall within the same price range, hence I actively use both apps today.
#             </p>
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )

# with col2:
#     st.plotly_chart(generate_donut_chart(platform_counts), use_container_width=True)



col1, col2 = st.columns([1.5, 1])

            

with col1:
    st.plotly_chart(generate_payment_pie_chart(df), use_container_width=True)


with col2:
    st.markdown(
    """
            <div style="margin-top: 20px;  height: 350px; padding: 15px; background: #f8f9fa; border-radius: 10px; border-left: 5px solid #FF4B4B; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);">
            <h4 style="color: #FF4B4B;">UPI Crushes COD!</h4>
            <p style="font-size: 16px; color: #333;">
        As you can see, a whopping 88.7% of my payments were made via UPI – let's be honest, who even carries cash these days? 😏 The remaining 11.3% of cash payments 
        can likely be attributed to my initial trust issues with delivery apps. 👀
    </div>
    """,
    unsafe_allow_html=True,
)
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
                    <p style="color: black;">The Scatter Plot visualizes the price distribution of my orders. Most of them
                    fall within ₹100 to ₹300. Some outliers in ₹500-₹700 are birthday cakes, group orders, etc.</p>
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
                    <p style="color: black;">The Line Plot visualizes the CDF of price distribution of my orders. As you can see, 88% of the orders fall
                    within the price of ₹300</p>
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
    <div style=" padding: 15px; background-color: #f8f9fa; 
                border-radius: 10px; border-right: 5px solid #FF4B4B; height: 100%;">
        <p style="color: black; font-size: 16px; line-height: 1.5;">
            <b>So, what's the deal with my order prices?</b><br><br>
            Turns out, I typically spend around <b>₹150–₹250</b> on an order.
            But as you can see, I’ve got a few moments where 
            my spending shoots up beyond ₹400 (hello, group orders and premium treats! 🍕🍔).<br><br>
            In other words, my day-to-day orders are pretty consistent, 
            but every now and then, I like to <b>splurge</b>—because life’s too short not to indulge, right? 🥳
        </p>
    </div>
    """,
    unsafe_allow_html=True
)



st.markdown("<br><br>", unsafe_allow_html=True)


st.plotly_chart(generate_monthly_order_histogram(df), use_container_width=True)

st.markdown(
    """
    <div style=" padding: 15px; background-color: #f8f9fa; 
                border-radius: 10px; border-right: 5px solid #FF4B4B; height: 100%;">
        <p style="color: black; font-size: 16px; line-height: 1.5;">
       From the above histogram, it's pretty clear: as the mess food hits rock bottom, my online order frequency skyrockets! 🍕🍔  
            Meanwhile, the dips show up around vacation times—because, well, home food tops everything!  
            Here's hoping the new policy changes rescue our taste buds from another semester of lackluster meals 🍽️.  
            Until then, let the late-night munchies reign supreme! 🥳
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


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
    if st.button("▶", key="next_food") and st.session_state["slide_food"] < 4:
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
                    This chart reveals my online food ordering secrets! 🍕📦 
                    Thursday, Monday, and Friday seem to be my peak craving days - trust me, I am not a fan of 
                    Soya Chunks, Baingan, and Lauki. 
                    We see a dip on weekends because the mess food actually becomes tolerable 😄.
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
                    Here's the breakdown of my meal preferences! 🍽️  
                    Breakfast orders? Rare. Lunch? Desperate times (Lets admit it, no college student readily gets up to have breakfast, so we are mostly starving by lunch).  
                    Dinner? Oh, that’s where the magic happens—when the mess menu screams "skip me!"  
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
        
    elif st.session_state['slide_food'] == 4:
        st.plotly_chart(generate_day_timeslot_heatmap_px(df), use_container_width=True)
        
    elif st.session_state['slide_food'] == 3:
        st.plotly_chart(generate_meal_popularity_heatmap(df), use_container_width=True)


