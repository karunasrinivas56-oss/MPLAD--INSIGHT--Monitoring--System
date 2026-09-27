
import streamlit as st
from backend.auth import get_current_user

st.title("👤 My Profile")

user = get_current_user()

if not user:
    st.warning("Please login first.")
    st.stop()

name = user.get("name", "N/A")
email = user.get("email", "N/A")
role = user.get("role", "N/A")
constituency = user.get("constituency", "N/A")
official_id = user.get("official_id")

if role == "Citizen":
    official_id = "Not Applicable"

st.subheader("Personal Information")

col1, col2 = st.columns(2)

with col1:
    st.text_input("Full Name", value=name, disabled=True)
    st.text_input("Role", value=role, disabled=True)

with col2:
    st.text_input("Email", value=email, disabled=True)
    st.text_input("Constituency", value=constituency, disabled=True)

st.subheader("Identification")

st.text_input(
    "Official ID",
    value=official_id or "Not Available",
    disabled=True
)

st.subheader("🔐 Permissions")

role_permissions = {
    "Citizen": [
        "View Public Projects",
        "Submit Defect Report"
    ],

    "Project Officer": [
        "View Public Projects",
        "Submit Proposal",
        "Update Milestone",
        "Run Pre Check"
    ],

    "MP Representative": [
        "View Public Projects",
        "View Constituency Allocation",
        "View Subplan Metrics"
    ],

    "Monitoring Officer": [
        "View Public Projects",
        "View Raw Risk Scores",
        "Issue Notice",
        "Freeze Funds",
        "Trigger Inspection",
        "Start Investigation",
        "Escalate Case",
        "Clear Flag",
        "Export PDF"
    ],

    "Administrator": [
        "View Public Projects",
        "Manage Users",
        "View Audit Logs",
        "System Maintenance"
    ]
}

permissions = role_permissions.get(role, [])

for permission in permissions:
    st.success("✅ " + permission)

st.subheader("📊 Access Scope")

if role == "Administrator":
    st.info("Access: All constituencies")
else:
    st.info(f"Access: {constituency} constituency projects")

st.caption("MPLAD Management System — Demo / Prototype")
