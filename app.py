import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import random

# Set page configuration
st.set_page_config(
    page_title="Digital TFI Leap Card",
    page_icon="🚌",
    layout="wide",
)

# Initialize session state variables if they don't exist
if 'username' not in st.session_state:
    st.session_state.username = "Guest User"
    st.session_state.balance = 0.0
    st.session_state.has_card = False
    st.session_state.tourist_pass = None
    st.session_state.pass_expiry = None
    st.session_state.trips = []

# Simple CSS for styling
st.markdown("""
<style>
    .card {
        background-color: #0068c9;
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .header {
        color: #0068c9;
        font-size: 24px;
        font-weight: bold;
    }
    .tier {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("Digital TFI Leap Card")
page = st.sidebar.radio("Navigation", ["Home", "Digital Card", "Tourist Pass", "Data"])

# Display user info in sidebar
st.sidebar.markdown("---")
st.sidebar.subheader("User Info")
if st.session_state.has_card:
    st.sidebar.write(f"**Name:** {st.session_state.username}")
    st.sidebar.write(f"**Balance:** €{st.session_state.balance:.2f}")
else:
    st.sidebar.write("*No active card*")

if st.session_state.tourist_pass:
    st.sidebar.write(f"**Active Pass:** {st.session_state.tourist_pass}")
    st.sidebar.write(f"**Valid Until:** {st.session_state.pass_expiry}")

# Home page
if page == "Home":
    st.title("Welcome to Digital TFI Leap Card")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.write("""
        ## Modernizing Public Transport Payments & Enhancing Tourist Convenience
        
        The Digital TFI Leap Card solves key problems with the current physical card system:
        - No more lost or damaged cards
        - Easy top-up with auto-reload options
        - Full integration with Apple Pay and Google Pay
        - Simplified tourist access with tiered passes
        """)
        
        # Display sample image
        st.image("https://www.transportforireland.ie/wp-content/uploads/2020/12/TFI-Go-Image-1.jpg", 
                caption="TFI App Concept", width=600)
        
    with col2:
        st.subheader("Quick Access")
        if st.session_state.has_card:
            st.markdown(f"<p class='header'>Balance: €{st.session_state.balance:.2f}</p>", unsafe_allow_html=True)
            
            amount = st.selectbox("Top Up Amount (€)", [5, 10, 20, 50])
            if st.button("Top Up Card"):
                st.session_state.balance += amount
                st.success(f"Successfully topped up €{amount}")
                st.balloons()
        
        else:
            st.warning("You don't have a Digital Leap Card yet.")
            if st.button("Get Digital Card"):
                st.session_state.has_card = True
                st.session_state.balance = 20.00
                st.success("Successfully created your Digital Leap Card!")
                st.balloons()
        
        if st.session_state.tourist_pass:
            st.info(f"Active Tourist Pass: {st.session_state.tourist_pass}")
        
        st.markdown("---")
        st.subheader("Key Features")
        
        st.markdown("""
        - 📱 Digital Leap Card on your phone
        - 💳 Apple Pay & Google Pay support
        - 🔄 Auto top-up functionality
        - 📊 Travel insights and spending analytics
        - 🏰 Tiered tourist passes with attraction access
        """)

# Digital Card page
elif page == "Digital Card":
    st.title("Digital Leap Card")
    
    if st.session_state.has_card:
        # Display virtual card
        st.markdown(f"""
        <div class="card">
            <h3>TFI Leap Card</h3>
            <p>CARD **** **** **** 5678</p>
            <p>{st.session_state.username}</p>
            <h2>€{st.session_state.balance:.2f}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Add card to wallet options
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Add to Apple Wallet"):
                st.success("Card added to Apple Wallet!")
        with col2:
            if st.button("Add to Google Pay"):
                st.success("Card added to Google Pay!")
        
        # Auto top-up option
        st.subheader("Auto Top-Up Settings")
        auto_topup = st.checkbox("Enable Auto Top-Up")
        if auto_topup:
            col1, col2 = st.columns(2)
            with col1:
                threshold = st.number_input("Top up when below (€)", value=10.0, min_value=5.0)
            with col2:
                amount = st.selectbox("Amount to add (€)", [10, 20, 30, 50])
            st.success(f"Auto top-up set: Add €{amount} when balance falls below €{threshold}")
        
        # Recent transactions
        st.subheader("Recent Transactions")
        if len(st.session_state.trips) == 0:
            st.info("No recent transactions")
        else:
            trips_df = pd.DataFrame(st.session_state.trips[-5:], columns=["Date", "Route", "Cost"])
            st.table(trips_df)
        
        # Simulate a trip
        st.subheader("Simulate a Trip")
        col1, col2, col3 = st.columns(3)
        with col1:
            route = st.selectbox("Route", ["Dublin Bus 16", "Luas Red Line", "DART"])
        with col2:
            cost = st.number_input("Cost (€)", value=2.50, min_value=1.0, max_value=10.0)
        with col3:
            if st.button("Pay"):
                if st.session_state.balance >= cost:
                    st.session_state.balance -= cost
                    st.session_state.trips.append([datetime.now().strftime("%Y-%m-%d %H:%M"), route, cost])
                    st.success(f"Payment successful! Remaining balance: €{st.session_state.balance:.2f}")
                else:
                    st.error("Insufficient balance. Please top up your card.")
    else:
        st.warning("You don't have a Digital Leap Card yet.")
        
        # Card application form
        st.subheader("Get Your Digital Leap Card")
        
        username = st.text_input("Your Name", value=st.session_state.username)
        email = st.text_input("Email Address")
        
        col1, col2 = st.columns(2)
        with col1:
            card_type = st.selectbox("Card Type", ["Adult", "Student", "Child", "Senior"])
        with col2:
            initial_amount = st.selectbox("Initial Amount (€)", [5, 10, 20, 50])
        
        if st.button("Create Digital Card"):
            st.session_state.username = username
            st.session_state.has_card = True
            st.session_state.balance = initial_amount
            st.success(f"Successfully created your Digital Leap Card with €{initial_amount} balance!")
            st.balloons()

# Tourist Pass page
elif page == "Tourist Pass":
    st.title("TFI TravelPass+ for Tourists")
    
    if st.session_state.tourist_pass:
        # Display active pass
        st.success(f"You have an active {st.session_state.tourist_pass} valid until {st.session_state.pass_expiry}")
        
        # Transport access
        st.subheader("Transport Access")
        st.info("You have unlimited access to Dublin Bus, Luas, and DART until your pass expires.")
        
        # Option to cancel pass
        if st.button("Cancel Tourist Pass"):
            st.session_state.tourist_pass = None
            st.session_state.pass_expiry = None
            st.warning("Tourist pass has been cancelled")
    else:
        st.write("""
        ## Choose the Perfect Pass for Your Dublin Visit
        
        Our tiered pass system offers flexibility for all types of travelers. 
        Select the duration and level of access that suits your plans.
        """)
        
        # Basic tier
        st.markdown('<div class="tier">', unsafe_allow_html=True)
        st.markdown('<h3>1. TFI Basic (Transport Only)</h3>', unsafe_allow_html=True)
        st.markdown("""
        - Unlimited Dublin Bus, Luas, and DART access
        - Real-time route planner and transit alerts
        - No attractions included
        """)
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("24 Hours - €10"):
                st.session_state.tourist_pass = "TFI Basic (24h)"
                st.session_state.pass_expiry = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M")
                st.success("TFI Basic 24-hour pass activated!")
        with col2:
            if st.button("48 Hours - €18"):
                st.session_state.tourist_pass = "TFI Basic (48h)"
                st.session_state.pass_expiry = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d %H:%M")
                st.success("TFI Basic 48-hour pass activated!")
        with col3:
            if st.button("72 Hours - €25"):
                st.session_state.tourist_pass = "TFI Basic (72h)"
                st.session_state.pass_expiry = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d %H:%M")
                st.success("TFI Basic 72-hour pass activated!")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Explorer tier
        st.markdown('<div class="tier">', unsafe_allow_html=True)
        st.markdown('<h3>2. TFI Explorer (Most Popular)</h3>', unsafe_allow_html=True)
        st.markdown("""
        - Unlimited transport for the duration
        - Access to 3 attractions (Guinness Storehouse, Dublin Castle, EPIC Museum)
        - Discounts on tours & food
        """)
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("24 Hours - €35"):
                st.session_state.tourist_pass = "TFI Explorer (24h)"
                st.session_state.pass_expiry = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M")
                st.success("TFI Explorer 24-hour pass activated!")
        with col2:
            if st.button("48 Hours - €55"):
                st.session_state.tourist_pass = "TFI Explorer (48h)"
                st.session_state.pass_expiry = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d %H:%M")
                st.success("TFI Explorer 48-hour pass activated!")
        with col3:
            if st.button("72 Hours - €70"):
                st.session_state.tourist_pass = "TFI Explorer (72h)"
                st.session_state.pass_expiry = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d %H:%M") 
                st.success("TFI Explorer 72-hour pass activated!")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Premium tier
        st.markdown('<div class="tier">', unsafe_allow_html=True)
        st.markdown('<h3>3. TFI Plus (Premium)</h3>', unsafe_allow_html=True)
        st.markdown("""
        - Unlimited transport + Express Airport Transfer
        - Unlimited access to top 10 attractions
        - VIP fast-track entry & premium dining discounts
        """)
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("24 Hours - €70"):
                st.session_state.tourist_pass = "TFI Plus (24h)"
                st.session_state.pass_expiry = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M")
                st.success("TFI Plus 24-hour pass activated!")
        with col2:
            if st.button("48 Hours - €100"):
                st.session_state.tourist_pass = "TFI Plus (48h)"
                st.session_state.pass_expiry = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d %H:%M")
                st.success("TFI Plus 48-hour pass activated!")
        with col3:
            if st.button("72 Hours - €130"):
                st.session_state.tourist_pass = "TFI Plus (72h)"
                st.session_state.pass_expiry = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d %H:%M")
                st.success("TFI Plus 72-hour pass activated!")
        st.markdown('</div>', unsafe_allow_html=True)

# Data page
elif page == "Data":
    st.title("TFI Data Analytics")
    
    # Create some simple sample data
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    digital_usage = [40, 42, 45, 47, 50, 52, 55, 57, 60, 62, 65, 67]
    physical_usage = [60, 58, 55, 53, 50, 48, 45, 43, 40, 38, 35, 33]
    
    # Create a DataFrame
    data = pd.DataFrame({
        'Month': months,
        'Digital Card Usage (%)': digital_usage,
        'Physical Card Usage (%)': physical_usage
    })
    
    # Display a table of the data
    st.subheader("Digital vs Physical Card Usage")
    st.write(data)
    
    # Create a simple plot
    st.subheader("Digital Adoption Trend")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(months, digital_usage, marker='o', linewidth=2, color='#0068c9', label='Digital')
    ax.plot(months, physical_usage, marker='o', linewidth=2, color='#ff7f0e', label='Physical')
    ax.set_xlabel('Month')
    ax.set_ylabel('Usage (%)')
    ax.set_title('Digital vs Physical Card Usage Trend')
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Display the plot
    st.pyplot(fig)
    
    # Tourist pass data
    st.subheader("Tourist Pass Sales")
    
    # Create simple data for tourist passes
    tiers = ["TFI Basic", "TFI Explorer", "TFI Plus"]
    sales = [3500, 5000, 1500]
    
    # Create a DataFrame
    tourist_data = pd.DataFrame({
        'Tier': tiers,
        'Sales': sales
    })
    
    # Display the data
    st.write(tourist_data)
    
    # Create a simple bar chart
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(tiers, sales, color=['#1f77b4', '#2ca02c', '#d62728'])
    ax.set_xlabel('Tier')
    ax.set_ylabel('Number of Passes Sold')
    ax.set_title('Tourist Pass Sales by Tier')
    ax.grid(True, axis='y', linestyle='--', alpha=0.7)
    
    # Display the plot
    st.pyplot(fig)
    
    # Key insights
    st.subheader("Key Insights")
    
    st.write("""
    - Digital card adoption has increased by 27% over the past year
    - The Explorer tier is the most popular tourist pass
    - Weekend digital usage is 22% higher than weekday usage
    - 67% of tourists prefer digital passes over traditional cards
    """)
