
"""
MPLAD Management System - Login Page
Handles user login and password reset.
"""

import streamlit as st

from backend.auth import (
    login,
    reset_password,
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="MPLAD - Login",
    page_icon="🏛️",
    layout="centered",
)


# ============================================================
# SESSION STATE
# ============================================================

if "show_reset_password" not in st.session_state:
    st.session_state.show_reset_password = False


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main {
        background-color: #f5f7fa;
    }

    .login-container {
        max-width: 500px;
        margin: auto;
        padding: 20px;
    }

    .title {
        text-align: center;
        font-size: 36px;
        font-weight: 700;
        color: #1f3c88;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 17px;
        color: #666666;
        margin-bottom: 30px;
    }

    .section-title {
        text-align: center;
        font-size: 25px;
        font-weight: 600;
        margin-bottom: 20px;
        color: #222222;
    }

    .info-box {
        background-color: #eef4ff;
        padding: 12px;
        border-radius: 8px;
        border-left: 5px solid #1f3c88;
        margin-bottom: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="title">🏛️ MPLAD INSIGHT</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">MPLAD Management & Monitoring System</div>',
    unsafe_allow_html=True,
)


# ============================================================
# LOGIN / RESET PASSWORD
# ============================================================

if not st.session_state.show_reset_password:

    st.markdown(
        '<div class="section-title">🔐 Login</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="info-box">
        Login to access your role-based MPLAD dashboard.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # LOGIN FORM
    # --------------------------------------------------------

    with st.form("login_form"):

        email = st.text_input(
            "📧 Email Address",
            placeholder="Enter your email",
        )

        password = st.text_input(
            "🔑 Password",
            type="password",
            placeholder="Enter your password",
        )

        login_button = st.form_submit_button(
            "🔐 Login",
            use_container_width=True,
        )

    # --------------------------------------------------------
    # LOGIN PROCESS
    # --------------------------------------------------------

    if login_button:

        if not email.strip():

            st.error("❌ Please enter your email address.")

        elif not password:

            st.error("❌ Please enter your password.")

        else:

            success, message = login(
                email.strip(),
                password,
            )

            if success:

                # ------------------------------------------------
                # Mark user as authenticated
                # ------------------------------------------------

                st.session_state.authenticated = True

                # ------------------------------------------------
                # Sync logged-in user details
                # ------------------------------------------------

                current_user = st.session_state.get("user")

                if current_user:

                    st.session_state.user_name = current_user.get(
                        "name",
                        "User",
                    )

                    st.session_state.user_role = current_user.get(
                        "role",
                        "Citizen",
                    )

                # ------------------------------------------------
                # Reload app
                # ------------------------------------------------

                st.rerun()

            else:

                st.error(f"❌ {message}")

    # --------------------------------------------------------
    # FORGOT PASSWORD
    # --------------------------------------------------------

    st.markdown("")

    if st.button(
        "🔑 Forgot Password?",
        use_container_width=True,
    ):

        st.session_state.show_reset_password = True
        st.rerun()

    # --------------------------------------------------------
    # REGISTER
    # --------------------------------------------------------

    st.markdown("")

    st.write("Don't have an account?")

    if st.button(
        "📝 Create New Account",
        use_container_width=True,
    ):

        st.switch_page("pages/register.py")


# ============================================================
# RESET PASSWORD PAGE
# ============================================================

else:

    st.markdown(
        '<div class="section-title">🔑 Reset Password</div>',
        unsafe_allow_html=True,
    )

    st.info(
        "Enter your registered email address and choose a new password."
    )

    # --------------------------------------------------------
    # RESET FORM
    # --------------------------------------------------------

    with st.form("reset_password_form"):

        reset_email = st.text_input(
            "📧 Registered Email",
            placeholder="Enter your registered email",
        )

        new_password = st.text_input(
            "🔑 New Password",
            type="password",
            placeholder="Enter new password",
        )

        confirm_password = st.text_input(
            "🔐 Confirm New Password",
            type="password",
            placeholder="Re-enter new password",
        )

        reset_button = st.form_submit_button(
            "🔄 Reset Password",
            use_container_width=True,
        )

    # --------------------------------------------------------
    # RESET PROCESS
    # --------------------------------------------------------

    if reset_button:

        if not reset_email.strip():

            st.error("❌ Please enter your email address.")

        elif not new_password:

            st.error("❌ Please enter a new password.")

        elif not confirm_password:

            st.error("❌ Please confirm your new password.")

        elif new_password != confirm_password:

            st.error("❌ Passwords do not match.")

        else:

            try:

                success, message = reset_password(
                    reset_email.strip(),
                    new_password,
                )

                if success:

                    st.success(
                        f"✅ {message}"
                    )

                    st.session_state.show_reset_password = False
                    st.rerun()

                else:

                    st.error(
                        f"❌ {message}"
                    )

            except Exception as e:

                st.error(
                    f"❌ Unable to reset password: {e}"
                )

    # --------------------------------------------------------
    # BACK TO LOGIN
    # --------------------------------------------------------

    st.markdown("")

    if st.button(
        "⬅️ Back to Login",
        use_container_width=True,
    ):

        st.session_state.show_reset_password = False
        st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center; color:#777;">
        <small>
        MPLAD INSIGHT • Secure Role-Based Monitoring System
        </small>
    </div>
    """,
    unsafe_allow_html=True,
)
