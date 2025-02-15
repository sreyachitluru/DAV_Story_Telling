import streamlit as st

st.markdown("""
<h2 style="text-align: center; color: #FF4B4B;">Final Conclusions</h2>
""", unsafe_allow_html=True)


st.markdown("""
<div style="margin: 10px; padding: 15px; background-color: #f8f9fa; 
            border-radius: 10px; border-left: 5px solid #FF4B4B;  ">
    <h4 style="color: #FF4B4B;">Platform Preferences</h4>
    <p style="font-size: 16px; color: #333; line-height: 1.6;">
        My data shows that I lean on both <span style="color: red; font-weight: bold;">Zomato</span> and 
        <span style="color: orange; font-weight: bold;">Swiggy</span> for my orders. 
        <span style="color: red; font-weight: bold;">Zomato</span> occasionally treats me to premium, indulgent meals, 
        while <span style="color: orange; font-weight: bold;">Swiggy</span> often wins for consistent, value-driven orders.
    </p>
</div>
""", unsafe_allow_html=True)


st.markdown("""
<div style="margin: 10px; padding: 15px; background-color: #f8f9fa; 
            border-radius: 10px; border-left: 5px solid #FF4B4B; ">
    <h4 style="color: #FF4B4B;">Ordering & Price Trends</h4>
    <p style="font-size: 16px; color: #333; line-height: 1.6;">
        The majority of orders fall within a moderate price range (₹100–₹300), 
        with occasional splurges pushing orders above ₹500—likely for special occasions or group orders. 
        Moreover, order frequency tends to spike during busy college days and drop during vacations, 
        reflecting shifts in my daily routine and food quality at the mess.
    </p>
</div>
""", unsafe_allow_html=True)


st.markdown("""
<div style="margin: 10px; padding: 15px; background-color: #f8f9fa; 
            border-radius: 10px; border-left: 5px solid #FF4B4B;">
    <h4 style="color: #FF4B4B;">Cuisines, Day & Time Insights</h4>
    <p style="font-size: 16px; color: #333; line-height: 1.6;">
        The word clouds and heatmaps reveal a clear pattern in my favorite cuisines, 
        with a few go-to choices dominating. Peaks on specific days and times highlight when I’m most likely to order—often when the mess food goes from "meh" to "nope." 
        This consistent yet dynamic behavior ensures that I always have a reliable backup (or a treat!) when campus life gets hectic.
    </p>
</div>
""", unsafe_allow_html=True)

# A full-width summary box below the columns for an overall wrap-up
st.markdown("""
<div style="margin: 10px; padding: 15px; background-color: #f8f9fa; 
            border-radius: 10px; border-left: 5px solid #FF4B4B;">
    <h4 style="color: #FF4B4B;">Overall Insights</h4>
    <p style="font-size: 16px; color: #333; line-height: 1.6;">
        In summary, my ordering behavior reflects a balanced mix of consistency and indulgence. 
        Whether I’m opting for <span style="color: red; font-weight: bold;">Zomato’s</span> premium splurges 
        or <span style="color: orange; font-weight: bold;">Swiggy’s</span> reliable deals, 
        the trends are clear: I order more frequently when the mess falls short, 
        and I have a few favorite cuisines that never go out of style. 
        This dynamic pattern not only keeps my taste buds happy but also makes for an interesting data story!
    </p>
</div>
""", unsafe_allow_html=True)
