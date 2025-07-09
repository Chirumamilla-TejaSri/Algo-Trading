# signup.py

import streamlit as st
from PIL import Image
from users import create_user_table, register_user, user_exists

create_user_table()

def render_signup_form():
    # Background color and label style
    st.markdown("""
        <style>
        [data-testid="stAppViewContainer"] {
            background-color: black;
        }
        .signup-title {
            font-size: 28px;
            font-weight: bold;
            color: #00bfff;
        }
        label, .stTextInput>div>label {
            color: white !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Layout
    col1, col2 = st.columns(2)

    with col1:
        st.image("assests/Login.jpg", use_column_width=True)

    with col2:
        st.markdown('<div class="signup-title">📝 Sign Up</div>', unsafe_allow_html=True)

        # --- Input fields ---
        name_input = st.text_input("Full Name")
        email_input = st.text_input("Email")
        password_input = st.text_input("Password", type="password")
        confirm_input = st.text_input("Confirm Password", type="password")

        # --- Button ---
        if st.button("Sign Up"):
            name = name_input.strip()
            email = email_input.strip()
            password = password_input
            confirm = confirm_input

            if name == "" or email == "" or password == "" or confirm == "":
                st.warning("⚠️ Please fill all fields.")
            elif password != confirm:
                st.error("❌ Passwords do not match.")
            elif user_exists(email):
                st.error("❌ Email already registered.")
            else:
                register_user(name, email, password)
                st.success("✅ Signup successful! Redirecting to login...")
                st.session_state.page = "login"
                st.rerun()

        # --- Login link ---
        if st.button("Already have an account? Login"):
            st.session_state.page = "login"
            st.rerun()
