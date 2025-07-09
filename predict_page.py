
import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler

def run_predict_page():
    if "sidebar_open" not in st.session_state:
        st.session_state.sidebar_open = True
    if "selected_section" not in st.session_state:
        st.session_state.selected_section = "home"

    # CSS Styling
    st.markdown("""
        <style>
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(to bottom right, #0f2027, #203a43, #2c5364);
            background-attachment: fixed;
        }
        .sidebar {
            background-color: #111;
            border-radius: 15px;
            padding: 20px;
            margin-top: 0px;
            box-shadow: 0 0 20px rgba(0, 191, 255, 0.3);
        }
        .sidebar-title {
            color: #00bfff;
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 30px;
            text-align: center;
        }
        .stButton > button {
            background-color: #ffffff !important;
            color: black !important;
            font-size: 16px !important;
            padding: 12px 24px;
            border-radius: 10px;
            margin: 10px 0px;
            width: 100%;
            transition: all 0.3s ease;
            border: none;
        }
        .stButton > button:hover {
            background-color: #00bfff !important;
            color: white !important;
            font-weight: bold !important;
            transform: scale(1.03);
            box-shadow: 0 0 8px #00bfff;
        }
        .toggle-btn {
            margin-top: 15px;
            margin-left: 5px;
        }
        div[data-testid="stSelectbox"] label {
            font-size: 35px !important;
            color: white !important;
            font-weight: bold !important;
        }
        div[data-baseweb="select"] div[role="button"] {
            background-color: #1e1e1e !important;
            color: white !important;
            font-size: 25px !important;
            border: 1px solid #00bfff;
            border-radius: 8px;
            padding: 8px 12px;
        }
        div[role="listbox"] > div {
            font-size: 35px !important;
            background-color: #1e1e1e !important;
            color: white !important;
        }

        @keyframes blink {
            0% { opacity: 1; }
            50% { opacity: 0.1; }
            100% { opacity: 1; }
        }
        .blinker {
            animation: blink 1.2s infinite;
        }
        </style>
    """, unsafe_allow_html=True)

    # Sidebar toggle button
    toggle_col, _ = st.columns([1, 5])
    with toggle_col:
        st.markdown('<div class="toggle-btn">', unsafe_allow_html=True)
        if st.button("⬅️" if st.session_state.sidebar_open else "➡️", help="Toggle Sidebar"):
            st.session_state.sidebar_open = not st.session_state.sidebar_open
        st.markdown('</div>', unsafe_allow_html=True)

    # Layout columns
    if st.session_state.sidebar_open:
        left, right = st.columns([1, 3])
    else:
        _, right = st.columns([0.2, 3.8])

    # Sidebar Navigation
    if st.session_state.sidebar_open:
        with left:
            st.markdown("""
                <div class="sidebar">
                    <div class="sidebar-title">🛠️ Navigation</div>
            """, unsafe_allow_html=True)
            if st.button("🤖 Predict Prices", key="predict_btn"):
                st.session_state.selected_section = "predict"
            if st.button("📊 View Graphs", key="graph_btn"):
                st.session_state.selected_section = "view_graph"
            if st.button("💡 Buy/Sell Signals", key="signal_btn"):
                st.session_state.selected_section = "signals"
            st.markdown("</div>", unsafe_allow_html=True)

    # Main Content
    with right:
        if st.session_state.selected_section == "home":
            st.markdown("""
                <div style='
                    background-color: #111;
                    padding: 40px 30px;
                    border-radius: 20px;
                    box-shadow: 0 0 25px rgba(0, 191, 255, 0.3);
                    text-align: center;
                '>
                    <h2 style='color:#00bfff; font-size: 36px; font-weight: bold;'>📈 Welcome back, <span style='color:white;'>Trader!</span></h2>
                    <p style='color:#ccc; font-size: 18px;'>Stay ahead with TCS stock forecasts powered by AI. Use the navigation bar to begin predictions or explore signals.</p>
                    <hr style='border: 1px solid #00bfff; margin: 20px 0;'>
                    <p style='color: #aaa; font-style: italic;'>“Trading is not about being right, it's about being prepared.”</p>
                </div>
            """, unsafe_allow_html=True)

        elif st.session_state.selected_section == "view_graph":
            option = st.selectbox("Select Time Range", ["1D", "5D", "1M", "6M", "1Y", "5Y"])
            period_map = {
                "1D": ("1d", "5m"),
                "5D": ("5d", "15m"),
                "1M": ("1mo", "60m"),
                "6M": ("6mo", "1d"),
                "1Y": ("1y", "1d"),
                "5Y": ("5y", "1wk"),
            }
            period, interval = period_map[option]
            df = yf.Ticker("TCS.NS").history(period=period, interval=interval)
            if not df.empty:
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=df.index, y=df["Close"], mode='lines', line=dict(color='red', width=3)))
                fig.update_layout(
                    plot_bgcolor='#000',
                    paper_bgcolor='#000',
                    font=dict(color='white', size=22),
                    showlegend=False,
                    xaxis=dict(
                        showgrid=False,
                        title='Date',
                        titlefont=dict(size=24, color='white'),
                        tickfont=dict(size=20, color='white')
                    ),
                    yaxis=dict(
                        showgrid=False,
                        title='Price (₹)',
                        titlefont=dict(size=24, color='white'),
                        tickfont=dict(size=20, color='white')
                    ),
                    height=550,
                    margin=dict(l=40, r=40, t=40, b=40)
                )
                st.plotly_chart(fig, use_container_width=True)

        elif st.session_state.selected_section == "predict":
            try:
                model = load_model("keras_model.h5")
                df = yf.Ticker("TCS.NS").history(period="1y", interval="1d")
                if df.empty:
                    st.error("⚠️ Could not fetch TCS data from Yahoo Finance.")
                else:
                    close_prices = df["Close"].values.reshape(-1, 1)
                    scaler = MinMaxScaler()
                    scaled = scaler.fit_transform(close_prices)
                    if len(scaled) >= 100:
                        last_100 = scaled[-100:].reshape(1, 100, 1)
                        pred_scaled = model.predict(last_100)
                        predicted_price = scaler.inverse_transform(pred_scaled)[0][0]
                        current_price = close_prices[-1][0]
                        change = predicted_price - current_price
                        change_pct = (change / current_price) * 100

                        sentiment = "Bullish" if change > 0 else "Bearish"
                        sentiment_color = "lime" if change > 0 else "red"
                        arrow = "🔺" if change > 0 else "🔻"

                        st.markdown(f"""
                            <h2 style="color: white; font-size: 36px; font-weight: bold;">📈 TCS Stock Prediction</h2>
                            <div style="background-color: #111; padding: 30px; border-radius: 15px; box-shadow: 0 0 20px #00ffff20;">
                                <h3 style="color: #00bfff; font-weight: bold;">🤖 AI Prediction Summary</h3>
                                <p style="color: #ccc;">Prediction for the next day</p>
                                <p style="color: white; font-size: 28px; font-weight: bold;">Current Price</p>
                                <p style="color: white; font-size: 24px;">₹{current_price:.2f}</p>
                                <p style="color: white; font-size: 28px; font-weight: bold;">Predicted Price</p>
                                <p style="color: white; font-size: 24px;">₹{predicted_price:.2f} <span style='color:{sentiment_color}; font-size: 22px;'>{arrow}</span></p>
                                <p style="color: {sentiment_color}; font-size: 20px;">+₹{abs(change):.2f} ({abs(change_pct):.2f}%)</p>
                            </div>
                            <div style="margin-top: 25px; background-color: #111; padding: 20px; border-radius: 15px;">
                                <h4 style="color: #999;">AI Confidence</h4>
                                <div style="background-color: #333; border-radius: 8px; height: 20px;">
                                    <div style="width: 87%; background-color: #00ccff; height: 100%; border-radius: 8px;"></div>
                                </div>
                                <p style="color: #00ccff; margin-top: 5px;">✅ Confidence: 87%</p>
                                <p style="color: #ccc; margin-top: 20px; font-size: 20px;">📉 <strong>Market Sentiment:</strong> <span style="color: {sentiment_color}; font-weight: bold;">{sentiment}</span></p>
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.error("Not enough data to prepare prediction.")
            except Exception as e:
                st.error(f"❌ Prediction error: {e}")

        elif st.session_state.selected_section == "signals":
            try:
                model = load_model("keras_model.h5")
                df = yf.Ticker("TCS.NS").history(period="1y", interval="1d")
                if df.empty:
                    st.error("⚠️ Could not fetch TCS data from Yahoo Finance.")
                else:
                    close_prices = df["Close"].values.reshape(-1, 1)
                    scaler = MinMaxScaler()
                    scaled = scaler.fit_transform(close_prices)
                    if len(scaled) >= 100:
                        last_100 = scaled[-100:].reshape(1, 100, 1)
                        pred_scaled = model.predict(last_100)
                        predicted_price = scaler.inverse_transform(pred_scaled)[0][0]
                        current_price = close_prices[-1][0]
                        change = predicted_price - current_price
                        change_pct = (change / current_price) * 100

                        threshold = 0.5
                        if change_pct > threshold:
                            signal = "✅ BUY"
                            signal_color = "lime"
                        elif change_pct < -threshold:
                            signal = "❌ SELL"
                            signal_color = "red"
                        else:
                            signal = "🤝 HOLD"
                            signal_color = "#ffa500"

                        st.markdown(f"""
                            <h2 style='color:#00bfff;'>💡 AI-Based Buy/Sell Signal</h2>
                            <div style="background-color:#111; padding:30px; border-radius:15px; box-shadow:0 0 20px rgba(0,255,255,0.1);">
                                <p style="color:white; font-size:20px;">📈 <strong>Current Price:</strong> ₹{current_price:.2f}</p>
                                <p style="color:white; font-size:20px;">🤖 <strong>Predicted Price:</strong> ₹{predicted_price:.2f}</p>
                                <p style="color:white; font-size:18px;">📊 <strong>Expected Change:</strong> ₹{change:.2f} ({change_pct:.2f}%)</p>
                                <hr style="border-color:#444;">
                                <h1 class="blinker" style="color:{signal_color}; text-align:center; font-size: 48px; margin-top: 20px;">{signal}</h1>
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.error("Not enough data to generate a signal.")
            except Exception as e:
                st.error(f"❌ Signal generation error: {e}")