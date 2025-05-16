import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np

# --- Page Config ---
st.set_page_config(page_title="Algorithmic Trading Hub", layout="wide", initial_sidebar_state="expanded")

# --- Hide Deploy Button ---
hide_streamlit_style = """
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    button[kind="icon"] {display: none !important;}  /* Hides deploy/share button */
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# --- Sidebar Navigation ---
st.sidebar.title("📌 Navigation")
section = st.sidebar.radio(
    "Go to section:",
    [
        "Welcome",
        "About Algorithmic Trading",
        "Website Uses",
        "Algorithms Used",
        "Live Market Chart",
        "Strategy Backtest",
        "Contact Us"
    ]
)

# --- Show Top Bar only on Welcome page ---
if section == "Welcome":
    col1, col2, col3 = st.columns([0.6, 6, 2])

    with col1:
        logo = Image.open("logo.png")
        st.image(logo, width=570)

    with col2:
        st.markdown(
            "<h2 style='color: black; font-weight:bold; margin: 0; padding-top: 10px;'>ALGORITHMIC TRADING HUB</h2>",
            unsafe_allow_html=True,
        )

    with col3:
        col_login, col_signup = st.columns([1, 1])
        with col_login:
            if st.button("Login"):
                st.markdown("<p style='margin: 0;'>🔐 Login functionality coming soon!</p>", unsafe_allow_html=True)
        with col_signup:
            if st.button("Sign Up"):
                st.markdown("<p style='margin: 0;'>📝 Signup functionality coming soon!</p>", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.title("Welcome!")
    st.write("Explore cutting-edge trading strategies powered by data and automation.")

elif section == "About Algorithmic Trading":
    st.header("💡 About Algorithmic Trading")
    st.write("""
    Algorithmic trading, also known as algo trading or automated trading, uses computer programs to follow a defined set of instructions for placing a trade. 
    The speed, precision, and data-handling capacity of these systems surpass human traders, making them ideal for today's fast-paced financial markets.

    Benefits include:
    - Faster execution
    - Reduced human error
    - Ability to backtest and optimize strategies
    - Operate 24/7 without fatigue
    """)

elif section == "Website Uses":
    st.header("🌐 Website Uses")
    st.markdown("""
    - 📊 Demonstrate and visualize trading strategies  
    - 🔍 Backtest algorithms with historical data  
    - ⚙️ Monitor real-time signals and analytics  
    - 📈 Analyze trends with interactive charts  
    - 📚 Provide educational resources on algorithmic trading  
    """)

elif section == "Algorithms Used":
    st.header("🧠 Algorithms Used")
    st.markdown("""
    - **Mean Reversion:** Profits from price returning to average  
    - **Momentum Trading:** Follows asset trends  
    - **Statistical Arbitrage:** Exploits pricing inefficiencies  
    - **Machine Learning Models:** Random Forests, XGBoost, LSTM  
    - **Pairs Trading:** Trades correlated asset pairs  
    """)

elif section == "Live Market Chart":
    st.header("📉 Live Market Chart (Simulated)")
    chart_data = pd.DataFrame(
        np.random.randn(100, 1).cumsum() + 100,
        columns=["Price"],
        index=pd.date_range(start="2025-01-01", periods=100)
    )
    st.line_chart(chart_data)

elif section == "Strategy Backtest":
    st.header("🧪 Strategy Backtest (SMA Crossover)")

    prices = pd.Series(np.random.randn(200).cumsum() + 100)
    short_window = st.slider("Short Moving Average Window", 5, 50, 20)
    long_window = st.slider("Long Moving Average Window", 10, 100, 50)

    signals = pd.DataFrame(index=prices.index)
    signals["price"] = prices
    signals["short_ma"] = prices.rolling(window=short_window).mean()
    signals["long_ma"] = prices.rolling(window=long_window).mean()
    signals["signal"] = 0
    signals["signal"][short_window:] = np.where(
        signals["short_ma"][short_window:] > signals["long_ma"][short_window:], 1, 0
    )
    signals["positions"] = signals["signal"].diff()

    st.line_chart(signals[["price", "short_ma", "long_ma"]])

elif section == "Contact Us":
    st.header("📬 Contact Us")

    with st.form("contact_form"):
        name = st.text_input("Your Name")
        email = st.text_input("Your Email")
        message = st.text_area("Your Message")
        submitted = st.form_submit_button("Send")
        if submitted:
            st.success(f"Thank you, {name}! We will get back to you at {email}.")

# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("© 2025 Algorithmic Trading Hub", unsafe_allow_html=True)
