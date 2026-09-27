"""
Home Page - MPLAD INSIGHT
Intelligent Local Development Monitoring
"""

import streamlit as st

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Home - MPLAD INSIGHT",
    page_icon="🏠",
    layout="wide"
)

# ============================================================================
# USER SESSION CONTEXT
# ============================================================================

user_role = st.session_state.get("user_role", "Citizen")
user_name = st.session_state.get("user_name", "Karuna")

# ============================================================================
# CUSTOM STYLING
# ============================================================================

st.markdown(
    """
    <style>

    /* =========================================================
       GLOBAL PAGE
       ========================================================= */

    .stApp {
        background-color: #f8fafc;
    }

    .block-container {
        max-width: 1250px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    /* =========================================================
       HERO SECTION
       ========================================================= */

    .hero-container {
        background: linear-gradient(
            135deg,
            #1f4037 0%,
            #2f6f5e 50%,
            #99f2c8 100%
        );
        border-radius: 22px;
        padding: 45px;
        color: white;
        margin-bottom: 30px;
        box-shadow: 0 12px 30px rgba(0,0,0,0.15);
    }

    .hero-tag {
        background: rgba(255,255,255,0.18);
        padding: 7px 15px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 1px;
        display: inline-block;
        margin-bottom: 15px;
    }

    .hero-title {
        font-size: 46px;
        font-weight: 900;
        margin-bottom: 8px;
        letter-spacing: -1px;
    }

    .hero-line {
        font-size: 24px;
        font-weight: 500;
        margin-bottom: 18px;
        color: #e2e8f0;
    }

    .hero-line span {
        color: #ffffff;
        font-weight: 800;
    }

    .hero-description {
        font-size: 15px;
        max-width: 750px;
        line-height: 1.7;
        color: #f1f5f9;
    }

    /* =========================================================
       SECTION HEADINGS
       ========================================================= */

    .section-header {
        text-align: center;
        margin: 42px 0 22px 0;
    }

    .section-title {
        font-size: 27px;
        font-weight: 800;
        color: #1f4037;
    }

    .section-subtitle {
        font-size: 14px;
        color: #64748b;
        margin-top: 4px;
    }

    /* =========================================================
       WORKFLOW CARDS
       ========================================================= */

    .intel-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 22px 18px;
        text-align: center;
        min-height: 185px;
        box-shadow: 0 5px 12px rgba(0,0,0,0.04);
    }

    .intel-number {
        font-size: 12px;
        font-weight: 800;
        color: #99f2c8;
        background: #1f4037;
        width: 30px;
        height: 30px;
        line-height: 30px;
        border-radius: 50%;
        margin: 0 auto 10px auto;
    }

    .intel-icon {
        font-size: 29px;
        margin-bottom: 8px;
    }

    .intel-title {
        font-size: 15px;
        font-weight: 800;
        color: #1e293b;
        margin-bottom: 7px;
    }

    .intel-text {
        font-size: 12px;
        color: #64748b;
        line-height: 1.5;
    }

    /* =========================================================
       ANOMALY CARD
       ========================================================= */

    .anomaly-card {
        background: #ffffff;
        border-left: 6px solid #ef4444;
        border-radius: 15px;
        padding: 28px;
        box-shadow: 0 8px 22px rgba(0,0,0,0.06);
        margin: 20px 0;
    }

    .anomaly-label {
        color: #ef4444;
        font-weight: 800;
        font-size: 11px;
        letter-spacing: 1.5px;
        margin-bottom: 5px;
    }

    .anomaly-title {
        font-size: 24px;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 22px;
    }

    .money-label {
        font-size: 11px;
        color: #64748b;
        font-weight: 700;
        margin-bottom: 4px;
    }

    .money {
        font-size: 21px;
        font-weight: 900;
        color: #1f4037;
    }

    .risk-badge {
        background: #fef2f2;
        color: #dc2626;
        border: 1px solid #fca5a5;
        padding: 7px 13px;
        border-radius: 7px;
        font-weight: 800;
        font-size: 12px;
        display: inline-block;
        margin: 20px 0 12px 0;
    }

    .anomaly-note {
        font-size: 12px;
        color: #64748b;
        line-height: 1.6;
        background: #f8fafc;
        padding: 13px;
        border-radius: 9px;
        max-width: 900px;
    }

    /* =========================================================
       PROJECT JOURNEY
       ========================================================= */

    .journey-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 20px 12px;
        text-align: center;
        min-height: 120px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.03);
    }

    .journey-icon {
        font-size: 29px;
        margin-bottom: 7px;
    }

    .journey-title {
        font-size: 14px;
        font-weight: 800;
        color: #1f4037;
    }

    .journey-text {
        font-size: 12px;
        color: #64748b;
        margin-top: 4px;
    }

    /* =========================================================
       ROLE CARDS
       ========================================================= */

    .role-card {
        background: #ffffff;
        border-radius: 14px;
        border: 1px solid #e2e8f0;
        padding: 20px 16px;
        min-height: 170px;
        box-shadow: 0 5px 12px rgba(0,0,0,0.04);
    }

    .role-icon {
        font-size: 28px;
        margin-bottom: 7px;
    }

    .role-title {
        font-size: 15px;
        font-weight: 800;
        color: #1f4037;
        margin-bottom: 6px;
    }

    .role-text {
        font-size: 12px;
        color: #475569;
        line-height: 1.5;
    }

    /* =========================================================
       CTA
       ========================================================= */

    .cta-box {
        background: linear-gradient(
            135deg,
            #1f4037 0%,
            #111827 100%
        );
        border-radius: 18px;
        padding: 40px 25px;
        color: white;
        text-align: center;
        margin-top: 45px;
        box-shadow: 0 12px 30px rgba(0,0,0,0.12);
    }

    .cta-title {
        font-size: 26px;
        font-weight: 900;
        margin-bottom: 8px;
    }

    .cta-text {
        font-size: 14px;
        color: #e2e8f0;
        margin-bottom: 16px;
    }

    .quote {
        font-style: italic;
        color: #99f2c8;
        font-size: 14px;
        border-top: 1px solid rgba(255,255,255,0.15);
        padding-top: 14px;
        max-width: 700px;
        margin: auto;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================================
# HERO SECTION
# ============================================================================

st.markdown(
    """
    <div class="hero-container">
        <div class="hero-tag">INTELLIGENT LOCAL DEVELOPMENT MONITORING</div>
        <div class="hero-title">MPLAD INSIGHT</div>
        <div class="hero-line">From <span>Public Funds</span> to <span>Public Impact.</span></div>
        <div class="hero-description">
            An AI-powered monitoring platform designed to analyze development
            projects, identify unusual expenditure patterns, detect potential
            risks, and support transparent and accountable decision-making.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================================
# ACTIVE USER
# ============================================================================

st.success(f"👋 Active Session: **{user_name}** ({user_role})")

# ============================================================================
# HOW MPLAD INSIGHT WORKS
# ============================================================================

st.markdown(
    """
    <div class="section-header">
        <div class="section-title">How MPLAD Insight Works</div>
        <div class="section-subtitle">Turning project data into actionable monitoring intelligence</div>
    </div>
    """,
    unsafe_allow_html=True
)

c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.markdown(
        """
        <div class="intel-card">
            <div class="intel-number">01</div>
            <div class="intel-icon">📋</div>
            <div class="intel-title">Project Data</div>
            <div class="intel-text">Project, budget, expenditure, timeline and progress data.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c2:
    st.markdown(
        """
        <div class="intel-card">
            <div class="intel-number">02</div>
            <div class="intel-icon">💰</div>
            <div class="intel-title">Financial Analysis</div>
            <div class="intel-text">Analyzes spending patterns and project expenditure.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c3:
    st.markdown(
        """
        <div class="intel-card">
            <div class="intel-number">03</div>
            <div class="intel-icon">🤖</div>
            <div class="intel-title">AI Intelligence</div>
            <div class="intel-text">Machine learning identifies unusual project patterns.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c4:
    st.markdown(
        """
        <div class="intel-card">
            <div class="intel-number">04</div>
            <div class="intel-icon">🚨</div>
            <div class="intel-title">Risk Detection</div>
            <div class="intel-text">Flags projects that may require further review.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c5:
    st.markdown(
        """
        <div class="intel-card">
            <div class="intel-number">05</div>
            <div class="intel-icon">🎯</div>
            <div class="intel-title">Actionable Insight</div>
            <div class="intel-text">Helps authorized users prioritize monitoring actions.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================================================
# SMART ANOMALY DETECTION
# ============================================================================

st.markdown(
    """
    <div class="section-header">
        <div class="section-title">🧠 Smart Anomaly Detection</div>
        <div class="section-subtitle">Example of how the system identifies unusual expenditure</div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="anomaly-card">
        <div class="anomaly-label">AI-GENERATED RISK SIGNAL</div>
        <div class="anomaly-title">Community Hall Construction</div>
        <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:40px; max-width:750px;">
            <div>
                <div class="money-label">SIMILAR PROJECTS</div>
                <div class="money">₹8L – ₹12L</div>
            </div>
            <div>
                <div class="money-label">CURRENT PROJECT</div>
                <div class="money" style="color:#ef4444;">₹30L</div>
            </div>
            <div>
                <div class="money-label">AI RESULT</div>
                <div class="money">Potential Anomaly</div>
            </div>
        </div>
        <div class="risk-badge">🔴 REVIEW REQUIRED</div>
        <div class="anomaly-note">
            The system identifies that the expenditure is significantly higher
            than the expected range observed in comparable projects.
            This is an AI-generated risk signal and does not automatically mean
            fraud or wrongdoing. Human verification is required before any
            final decision or action.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================================
# PROJECT JOURNEY
# ============================================================================

st.markdown(
    """
    <div class="section-header">
        <div class="section-title">Project Journey</div>
        <div class="section-subtitle">Monitor a development project from proposal to impact</div>
    </div>
    """,
    unsafe_allow_html=True
)

j1, j2, j3, j4, j5 = st.columns(5)

journey_data = [
    ("📝", "Proposal", "Project proposed"),
    ("✅", "Approval", "Funds approved"),
    ("🏗️", "Execution", "Work implemented"),
    ("🔍", "Monitoring", "Progress analyzed"),
    ("🌱", "Impact", "Public benefit delivered")
]

for col, item in zip([j1, j2, j3, j4, j5], journey_data):
    with col:
        st.markdown(
            f"""
            <div class="journey-card">
                <div class="journey-icon">{item[0]}</div>
                <div class="journey-title">{item[1]}</div>
                <div class="journey-text">{item[2]}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

# ============================================================================
# ROLE-BASED ACCESS
# ============================================================================

st.markdown(
    """
    <div class="section-header">
        <div class="section-title">Role-Based Access</div>
        <div class="section-subtitle">Different responsibilities require different levels of access</div>
    </div>
    """,
    unsafe_allow_html=True
)

r1, r2, r3, r4, r5 = st.columns(5)

roles = [
    ("👤", "Citizen", "View public project information, progress and transparency alerts."),
    ("📋", "Project Officer", "Manage project execution, expenditure, progress and documentation."),
    ("🏛️", "MP Representative", "Review constituency projects, risks and monitoring insights."),
    ("🔎", "Monitoring Officer", "Verify AI risk alerts, investigate anomalies and take corrective action."),
    ("⚙️", "Administrator", "Manage users, projects, permissions and system-wide monitoring.")
]

for col, role in zip([r1, r2, r3, r4, r5], roles):
    with col:
        st.markdown(
            f"""
            <div class="role-card">
                <div class="role-icon">{role[0]}</div>
                <div class="role-title">{role[1]}</div>
                <div class="role-text">{role[2]}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

# ============================================================================
# FOOTER / CTA
# ============================================================================

st.markdown(
    """
    <div class="cta-box">
        <div class="cta-title">Every Rupee. Every Project. Every Impact.</div>
        <div class="cta-text">Intelligent monitoring for transparent, accountable and effective local development.</div>
        <div class="quote">“Data reveals the pattern. AI highlights the risk. Humans make the decision.”</div>
    </div>
    <p style="text-align:center; font-size:12px; color:#94a3b8; margin-top:20px;">
        MPLAD INSIGHT • Intelligent Local Development Monitoring
        <br>
        AI-assisted monitoring • Human-verified decisions • Public impact
    </p>
    """,
    unsafe_allow_html=True
)