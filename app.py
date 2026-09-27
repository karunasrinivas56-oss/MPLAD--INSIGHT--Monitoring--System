"""
MPLAD Management System - Main Application Entry Point
Handles multi-role authentication and page routing via Streamlit Navigation
"""

import streamlit as st
from backend import database

st.set_page_config(
    page_title="MPLAD Management System",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize database
database.init_database()

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "user" not in st.session_state:
    st.session_state.user = None

if "user_name" not in st.session_state:
    st.session_state.user_name = "User"

if "user_role" not in st.session_state:
    st.session_state.user_role = "Citizen"


# -------------------------------
# NOT AUTHENTICATED
# -------------------------------
if not st.session_state.authenticated:

    login_page = st.Page(
        "pages/login.py",
        title="Login",
        icon="🔐",
        default=True
    )

    register_page = st.Page(
        "pages/register.py",
        title="Register",
        icon="📝"
    )

    pg = st.navigation(
        [login_page, register_page],
        position="hidden"
    )

    pg.run()


# -------------------------------
# AUTHENTICATED
# -------------------------------
else:

    # Sidebar user information
    with st.sidebar:

        st.markdown("---")

        col1, col2 = st.columns([3, 1])

        with col1:
            st.markdown(
                f"### 👤 {st.session_state.get('user_name', 'User')}\n"
                f"*{st.session_state.get('user_role', 'N/A')}*"
            )

        with col2:
            if st.button("🚪", help="Logout"):

                from backend.auth import logout

                logout()

                st.session_state.authenticated = False
                st.session_state.user = None

                st.rerun()

        st.markdown("---")


    # Pages
    home = st.Page(
        "pages/home.py",
        title="Home",
        icon="🏠",
        default=True
    )

    dashboard = st.Page(
        "pages/dashboard.py",
        title="Dashboard",
        icon="📊"
    )

    profile = st.Page(
        "pages/profile.py",
        title="Profile",
        icon="👤"
    )


    # Navigation
    pg = st.navigation(
        [home, dashboard, profile]
    )

    pg.run()