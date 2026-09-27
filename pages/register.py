
"""
Registration page for MPLAD AI Anomaly & Fraud Detection System
"""

import time
import streamlit as st

from backend.auth import register


# ============================================================
# CONSTITUENCIES
# ============================================================

DATABASE_CONSTITUENCIES = [
    "Select Constituency",
    "Warangal",
    "Karimnagar",
    "Nizamabad",
    "Khammam",
    "Nalgonda",
    "Mahabubnagar",
    "Medak",
    "Adilabad",
    "Hyderabad",
    "Secunderabad"
]


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="MPLAD - Register",
    page_icon="📝",
    layout="centered",
)


# ============================================================
# LOGIN REDIRECT
# ============================================================

if st.session_state.get("authenticated", False):
    st.switch_page("pages/home.py")


# ============================================================
# CUSTOM STYLING
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background: linear-gradient(
            135deg,
            #1f4037 0%,
            #99f2c8 100%
        );

        background-attachment: fixed;
    }

    .register-container {
        max-width: 520px;
        margin: 30px auto 25px auto;
        padding: 38px;
        background: white;
        border-radius: 20px;
        box-shadow:
            0 15px 40px
            rgba(0, 0, 0, 0.18);
        border: 1px solid
            rgba(0, 0, 0, 0.05);
    }

    .register-title {
        text-align: center;
        font-size: 30px;
        font-weight: 700;
        color: #1f4037;
        margin-top: 0;
        margin-bottom: 6px;
    }

    .register-subtitle {
        text-align: center;
        color: #64748b;
        font-size: 13px;
        margin-bottom: 20px;
    }

    .section-title {
        color: #1f4037;
        font-size: 16px;
        font-weight: 700;
        margin-top: 14px;
        margin-bottom: 10px;
    }

    .role-info {
        background: #e6f4ea;
        border-left: 4px solid #1f4037;
        padding: 10px 12px;
        border-radius: 6px;
        font-size: 12px;
        color: #1f4037;
        margin-bottom: 15px;
    }

    .stTextInput > div > div > input,
    .stSelectbox > div > div {
        border-radius: 8px;
        border: 1px solid #cbd5e1;
    }

    .stButton > button {
        width: 100%;
        border-radius: 10px;
        height: 46px;
        font-weight: 600;
        font-size: 15px;
    }

    .login-link {
        text-align: center;
        margin-top: 18px;
        color: #64748b;
        font-size: 14px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# REGISTER FORM
# ============================================================

st.markdown(
    '<div class="register-container">',
    unsafe_allow_html=True
)

st.markdown(
    '<h1 class="register-title">'
    '📝 MPLAD INSIGHT'
    '</h1>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="register-subtitle">'
    'AI-Powered Anomaly, Fraud & Inefficiency Detection System'
    '</div>',
    unsafe_allow_html=True
)

st.markdown("---")


with st.form("register_form"):

    # ========================================================
    # SYSTEM ACCESS
    # ========================================================

    st.markdown(
        '<div class="section-title">'
        '🏛️ System Access & Region'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="role-info">
            Your <b>role</b> and <b>constituency</b>
            determine your access permissions and
            visibility in the system.
        </div>
        """,
        unsafe_allow_html=True
    )

    constituency = st.selectbox(
        "Constituency Name",
        options=DATABASE_CONSTITUENCIES,
        index=0,
        key="register_constituency",
        help="Select your assigned constituency",
    )

    role_options = [
        "Select Role",
        "Citizen",
        "Project Officer",
        "MP Representative",
        "Monitoring Officer",
        "Administrator",
    ]

    role = st.selectbox(
        "User Role",
        options=role_options,
        index=0,
        key="register_role",
        help="Select your system access role",
    )


    # ========================================================
    # OFFICIAL ID
    # ========================================================

    official_id = None

    official_roles = [
        "Administrator",
        "Project Officer",
        "MP Representative",
        "Monitoring Officer",
    ]

    if role in official_roles:

        st.markdown(
            '<div class="section-title">'
            '🪪 Official Identification'
            '</div>',
            unsafe_allow_html=True
        )

        official_id = st.text_input(
            "Official ID",
            placeholder="Example: PO-TG-001",
            max_chars=10,
            help=(
                "Enter your system-assigned official ID. "
                "Example: PO-TG-001"
            ),
        )

        st.caption(
            "🔐 Official roles require a valid official ID."
        )


    # ========================================================
    # PERSONAL INFORMATION
    # ========================================================

    st.markdown(
        '<div class="section-title">'
        '👤 Personal Information'
        '</div>',
        unsafe_allow_html=True
    )

    name = st.text_input(
        "Full Name",
        placeholder="Enter your full name",
    )

    email = st.text_input(
        "Email Address",
        placeholder="user@example.com",
    )


    # ========================================================
    # ACCOUNT SECURITY
    # ========================================================

    st.markdown(
        '<div class="section-title">'
        '🔐 Account Security'
        '</div>',
        unsafe_allow_html=True
    )

    password = st.text_input(
        "Password",
        type="password",
        placeholder="Enter password",
    )

    confirm_password = st.text_input(
        "Confirm Password",
        type="password",
        placeholder="Re-enter password",
    )

    st.markdown("<br>", unsafe_allow_html=True)

    register_button = st.form_submit_button(
        "📝 Create Account",
        use_container_width=True,
        type="primary",
    )


# ============================================================
# FORM SUBMISSION
# ============================================================

if register_button:

    # --------------------------------------------------------
    # REQUIRED FIELDS
    # --------------------------------------------------------

    if (
        not name.strip()
        or not email.strip()
        or not password
        or not confirm_password
        or role == "Select Role"
        or constituency == "Select Constituency"
    ):

        st.error(
            "❌ Please fill in all fields, "
            "select a valid constituency, "
            "and choose a role."
        )

    # --------------------------------------------------------
    # OFFICIAL ID REQUIRED
    # --------------------------------------------------------

    elif (
        role != "Citizen"
        and not official_id
    ):

        st.error(
            "❌ Official ID is required for this role."
        )

    # --------------------------------------------------------
    # PASSWORD MATCH
    # --------------------------------------------------------

    elif password != confirm_password:

        st.error(
            "❌ Passwords do not match."
        )

    # --------------------------------------------------------
    # REGISTER
    # --------------------------------------------------------

    else:

        success, message = register(
            name=name.strip(),
            email=email.strip(),
            password=password,
            role=role.strip(),
            constituency=constituency.strip(),
            official_id=(
                official_id.strip().upper()
                if official_id
                else None
            ),
        )

        if success:

            st.success(
                "✅ Account created successfully!"
            )

            if role == "Citizen":

                st.info(
                    f"Registered as **{role}** "
                    f"for **{constituency}** constituency."
                )

            else:

                st.info(
                    f"Registered as **{role}** "
                    f"with Official ID "
                    f"**{official_id.upper()}** "
                    f"for **{constituency}** constituency."
                )

            time.sleep(2)

            st.switch_page(
                "pages/login.py"
            )

        else:

            st.error(
                f"❌ {message}"
            )


# ============================================================
# LOGIN LINK
# ============================================================

st.markdown(
    "<br>",
    unsafe_allow_html=True
)

st.markdown(
    '<div class="login-link">'
    'Already have an account?'
    '</div>',
    unsafe_allow_html=True
)

if st.button(
    "🔐 Login Here",
    use_container_width=True
):

    st.switch_page(
        "pages/login.py"
    )


st.markdown(
    "</div>",
    unsafe_allow_html=True
)

