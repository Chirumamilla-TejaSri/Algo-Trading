import streamlit as st
from PIL import Image
from users import login_user, user_exists

def render_login_form():
    st.markdown("""
        <style>
        /* Background */
        [data-testid="stAppViewContainer"] {
            background-color: black;
        }

        /* Container padding to push content down */
        .form-container {
            padding-top: 80px;
        }

        /* Login heading */
        .login-title {
            font-size: 38px;
            font-weight: bold;
            color: #00bfff;
            margin-bottom: 25px;
        }

        /* Bigger label text */
        div[data-testid="stTextInput"] label {
            font-size: 20px;
            color: white;
            font-weight: bold;
        }

        /* Bigger input text */
        input {
            font-size: 18px !important;
            padding: 12px !important;
            color: white !important;
            background-color: #222 !important;
            border: 1px solid #555 !important;
            border-radius: 8px !important;
        }

        /* Buttons */
        .stButton > button {
            font-size: 20px !important;
            font-weight: bold;
            padding: 12px 28px !important;
            background-color: #00bfff !important;
            color: black !important;
            border: none !important;
            border-radius: 10px !important;
            transition: 0.3s ease;
        }

        .stButton > button:hover {
            background-color: #009acd !important;
            color: white !important;
            transform: scale(1.05);
        }

        /* Add some space between buttons */
        .stButton {
            margin-bottom: 12px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Pushes the form down
    st.markdown('<div class="form-container">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.image("assests/LoginPage.jpg", use_column_width=True)

    with col2:
        st.markdown('<div class="login-title">🔐 Login</div>', unsafe_allow_html=True)

        email_input = st.text_input("Email")
        password_input = st.text_input("Password", type="password")

        if st.button("Login"):
            email = email_input.strip()
            password = password_input

            if email == "" or password == "":
                st.warning("⚠️ Please enter both fields.")
            elif not user_exists(email):
                st.error("❌ Email not found.")
            elif not login_user(email, password):
                st.error("❌ Incorrect password.")
            else:
                st.success("✅ Login successful!")
                st.session_state.login_success = True
                st.rerun()

        if st.button("Don't have an account? Sign Up"):
            st.session_state.page = "signup"
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
