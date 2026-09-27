import streamlit as st
import pandas as pd

from backend.auth import (
    get_current_user,
    logout,
)

from backend.permissions import check_permission

from backend.ml_engine import (
    evaluate_process_delays,
)

from backend.database import (
    get_db_connection,
    log_action,
    update_project,
    get_anomaly_projects_by_constituency,
)

from backend.report_generator import (
    generate_pdf_report,
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="MPLAD INSIGHT Dashboard",
    page_icon="🏛️",
    layout="wide",
)


# ============================================================
# AUTHENTICATION
# ============================================================

current_user = get_current_user()

if not current_user:

    st.warning(
        "Please login first."
    )

    st.stop()


# ============================================================
# CURRENT USER DETAILS
# ============================================================

user_id = current_user.get(
    "id",
    ""
)

user_name = current_user.get(
    "name",
    ""
)

user_email = current_user.get(
    "email",
    ""
)

user_role = current_user.get(
    "role",
    ""
)

user_constituency = current_user.get(
    "constituency",
    ""
)

user_official_id = current_user.get(
    "official_id",
    ""
)


# ============================================================
# DATABASE COLUMN SAFETY
# ============================================================

def ensure_user_columns():

    conn = get_db_connection()

    try:

        cur = conn.cursor()

        cur.execute(
            "PRAGMA table_info(users)"
        )

        user_columns = [
            row[1]
            for row in cur.fetchall()
        ]

        if "is_active" not in user_columns:

            cur.execute(
                """
                ALTER TABLE users
                ADD COLUMN is_active INTEGER DEFAULT 1
                """
            )

            conn.commit()

    finally:

        conn.close()


ensure_user_columns()


# ============================================================
# HEADER
# ============================================================

header_col1, header_col2 = st.columns(
    [4, 1]
)


with header_col1:

    st.title(
        "🏛️ MPLAD INSIGHT Dashboard"
    )

    st.write(
        f"Welcome, **{user_name}**"
    )

    if user_role == "Citizen":

        st.caption(
            f"Role: {user_role} | "
            f"Constituency: {user_constituency}"
        )

    else:

        st.caption(
            f"Role: {user_role} | "
            f"Official ID: {user_official_id} | "
            f"Constituency: {user_constituency}"
        )


with header_col2:

    if st.button(
        "Logout",
        key="logout_button",
    ):

        logout()

        st.rerun()


st.divider()


# ============================================================
# COMMON FUNCTIONS
# ============================================================

def load_projects():

    conn = get_db_connection()

    try:

        query = """
            SELECT

                id,

                title AS project_name,

                category,

                constituency,

                estimated_budget AS estimated_cost,

                actual_expenditure AS actual_spent,

                timeline_months,

                actual_months AS completed_months,

                status,

                anomaly_flag,

                anomaly_reason,

                social_category,

                domain,

                allocation_category

            FROM projects

            ORDER BY id DESC
        """

        df = pd.read_sql_query(
            query,
            conn
        )

    finally:

        conn.close()

    # --------------------------------------------------------
    # NUMERIC COLUMNS
    # --------------------------------------------------------

    numeric_columns = [
        "estimated_cost",
        "actual_spent",
        "timeline_months",
        "completed_months",
    ]

    for column in numeric_columns:

        if column not in df.columns:

            df[column] = 0

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        ).fillna(0)

    # --------------------------------------------------------
    # TEXT COLUMNS
    # --------------------------------------------------------

    text_columns = [
        "project_name",
        "category",
        "constituency",
        "status",
        "allocation_category",
        "social_category",
        "domain",
        "anomaly_reason",
    ]

    for column in text_columns:

        if column not in df.columns:

            df[column] = ""

        df[column] = (
            df[column]
            .fillna("")
            .astype(str)
            .str.strip()
        )

    # --------------------------------------------------------
    # ROLE BASED ACCESS
    # --------------------------------------------------------

    if user_role in [
        "Administrator",
        "Monitoring Officer",
        "Project Officer",
    ]:

        return df

    # --------------------------------------------------------
    # CITIZEN / MP CONSTITUENCY ACCESS
    # --------------------------------------------------------

    if "constituency" in df.columns:

        df = df[
            df["constituency"]
            .astype(str)
            .str.strip()
            .str.lower()
            ==
            str(user_constituency)
            .strip()
            .lower()
        ].copy()

    return df


# ============================================================
# PROJECT ACCESS CHECK
# ============================================================

def project_belongs_to_user(
    project_constituency
):

    if user_role in [
        "Administrator",
        "Monitoring Officer",
        "Project Officer",
    ]:

        return True

    return (
        str(project_constituency)
        .strip()
        .lower()
        ==
        str(user_constituency)
        .strip()
        .lower()
    )


# ============================================================
# RISK CALCULATION
# ============================================================

def calculate_risk(
    estimated_cost,
    actual_spent,
    timeline_months,
    completed_months,
):

    try:

        result = evaluate_process_delays(
            estimated_cost=estimated_cost,
            actual_spent=actual_spent,
            timeline_months=timeline_months,
            completed_months=completed_months,
        )

        return result

    except Exception:

        try:

            estimated_cost = float(
                estimated_cost
            )

            actual_spent = float(
                actual_spent
            )

            timeline_months = float(
                timeline_months
            )

            completed_months = float(
                completed_months
            )

        except Exception:

            estimated_cost = 0
            actual_spent = 0
            timeline_months = 0
            completed_months = 0

        # ----------------------------------------------------
        # BUDGET RATIO
        # ----------------------------------------------------

        if estimated_cost > 0:

            budget_ratio = (
                actual_spent
                /
                estimated_cost
            )

        else:

            budget_ratio = 0

        # ----------------------------------------------------
        # TIMELINE RATIO
        # ----------------------------------------------------

        if timeline_months > 0:

            timeline_ratio = (
                completed_months
                /
                timeline_months
            )

        else:

            timeline_ratio = 0

        # ----------------------------------------------------
        # RISK SCORE
        # ----------------------------------------------------

        risk_score = (
            budget_ratio * 0.6
            +
            timeline_ratio * 0.4
        )

        if risk_score >= 0.9:

            risk = "High"

        elif risk_score >= 0.7:

            risk = "Medium"

        else:

            risk = "Low"

        return {
            "risk_level": risk,
            "risk_score": round(
                risk_score,
                2
            ),
            "reason": "Fallback rule-based risk analysis",
        }


# ============================================================
# LOG ACTION HELPER
# ============================================================

def save_audit_log(
    action,
    project_id=None,
    details="",
):

    try:

        log_action(
            user_name,
            user_role,
            action,
            project_id,
            details,
        )

    except Exception as e:

        st.warning(
            f"Audit log could not be saved: {e}"
        )


# ============================================================
# REPORT CARD
# ============================================================
#
# IMPORTANT:
# Report details are NOT displayed on the dashboard.
# Only the PDF download button is displayed.
#
# The dashboard uses aliases:
# project_name
# estimated_cost
# actual_spent
# completed_months
#
# The PDF generator may use the original database names:
# title
# estimated_budget
# actual_expenditure
# actual_months
#
# Therefore we convert the project dictionary before
# sending it to generate_pdf_report().
#
# ============================================================

def show_report_card(
    project,
    show_download=True,
):

    project_id = project.get(
        "id"
    )

    if not show_download:

        return

    try:

        pdf_project = {
            "id": project.get(
                "id"
            ),

            "title": project.get(
                "project_name",
                "Unnamed Project"
            ),

            "category": project.get(
                "category",
                ""
            ),

            "constituency": project.get(
                "constituency",
                ""
            ),

            "estimated_budget": project.get(
                "estimated_cost",
                0
            ),

            "actual_expenditure": project.get(
                "actual_spent",
                0
            ),

            "timeline_months": project.get(
                "timeline_months",
                0
            ),

            "actual_months": project.get(
                "completed_months",
                0
            ),

            "status": project.get(
                "status",
                ""
            ),

            "anomaly_flag": project.get(
                "anomaly_flag",
                0
            ),

            "anomaly_reason": project.get(
                "anomaly_reason",
                ""
            ),

            "social_category": project.get(
                "social_category",
                ""
            ),

            "domain": project.get(
                "domain",
                ""
            ),

            "allocation_category": project.get(
                "allocation_category",
                ""
            ),
        }

        pdf_bytes = generate_pdf_report(
            pdf_project
        )

        st.download_button(
            label="📄 Download PDF Report",
            data=pdf_bytes,
            file_name=(
                f"project_{project_id}_report.pdf"
            ),
            mime="application/pdf",
            key=(
                f"download_report_"
                f"{user_role}_"
                f"{project_id}"
            ),
        )

    except Exception as e:

        st.error(
            f"Unable to generate PDF report: {e}"
        )


# ============================================================
# LOAD PROJECT DATA
# ============================================================

projects_df = load_projects()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title(
    "🏛️ MPLAD INSIGHT"
)

st.sidebar.write(
    f"**User:** {user_name}"
)

st.sidebar.write(
    f"**Role:** {user_role}"
)

if user_role != "Citizen":

    st.sidebar.write(
        f"**Official ID:** {user_official_id}"
    )

st.sidebar.write(
    f"**Constituency:** {user_constituency}"
)

st.sidebar.divider()


# ============================================================
# CITIZEN DASHBOARD
# ============================================================

if user_role == "Citizen":

    st.header(
        "👤 Citizen Dashboard"
    )

    st.write(
        "View public MPLAD projects and report project defects."
    )

    # --------------------------------------------------------
    # PUBLIC PROJECTS
    # --------------------------------------------------------

    st.subheader(
        "📋 Public Projects"
    )

    if projects_df.empty:

        st.info(
            "No projects found for your constituency."
        )

    else:

        citizen_display = [
            "id",
            "project_name",
            "category",
            "constituency",
            "domain",
            "estimated_cost",
            "actual_spent",
            "status",
        ]

        citizen_display = [
            col
            for col in citizen_display
            if col in projects_df.columns
        ]

        st.dataframe(
            projects_df[
                citizen_display
            ],
            use_container_width=True,
            hide_index=True,
        )

    # --------------------------------------------------------
    # CITIZEN PROJECT REPORT
    # --------------------------------------------------------

    st.subheader(
        "📄 Project Report"
    )

    if not projects_df.empty:

        citizen_report_id = st.selectbox(
            "Select Project",
            projects_df[
                "id"
            ].tolist(),
            format_func=lambda project_id: (
                projects_df.loc[
                    projects_df["id"] == project_id,
                    "project_name"
                ].iloc[0]
            ),
            key="citizen_report_project",
        )

        citizen_report_project = (
            projects_df[
                projects_df["id"]
                ==
                citizen_report_id
            ]
            .iloc[0]
            .to_dict()
        )

        show_report_card(
            citizen_report_project,
            show_download=True,
        )

    else:

        st.info(
            "No projects available for report."
        )

    # --------------------------------------------------------
    # ANOMALY PROJECTS
    # --------------------------------------------------------

    st.subheader(
        "⚠️ Projects Requiring Attention"
    )

    try:

        anomaly_projects = (
            get_anomaly_projects_by_constituency(
                user_constituency
            )
        )

        if anomaly_projects:

            anomaly_df = pd.DataFrame(
                anomaly_projects
            )

            st.dataframe(
                anomaly_df,
                use_container_width=True,
                hide_index=True,
            )

        else:

            st.success(
                "No anomaly projects reported."
            )

    except Exception:

        st.info(
            "No anomaly information available."
        )

    # --------------------------------------------------------
    # DEFECT REPORT
    # --------------------------------------------------------

    st.subheader(
        "🛠️ Report a Project Defect"
    )

    with st.form(
        "citizen_defect_form"
    ):

        if not projects_df.empty:

            project_options = (
                projects_df[
                    "project_name"
                ]
                .dropna()
                .tolist()
            )

            selected_project = st.selectbox(
                "Project",
                project_options,
            )

        else:

            selected_project = ""

        defect_description = st.text_area(
            "Describe the defect"
        )

        submit_defect = st.form_submit_button(
            "Submit Defect Report"
        )

        if submit_defect:

            if not defect_description.strip():

                st.error(
                    "Please describe the defect."
                )

            else:

                save_audit_log(
                    action="Citizen Defect Report",
                    details=(
                        f"Project: {selected_project}; "
                        f"Defect: {defect_description}"
                    ),
                )

                st.success(
                    "Defect report submitted successfully."
                )


# ============================================================
# PROJECT OFFICER DASHBOARD
# ============================================================

elif user_role == "Project Officer":

    st.header(
        "👨‍💼 Project Officer Dashboard"
    )

    st.write(
        "Submit project proposals and update project milestones."
    )

    # --------------------------------------------------------
    # SUBMIT PROJECT PROPOSAL
    # --------------------------------------------------------

    st.subheader(
        "➕ Submit New Project Proposal"
    )

    with st.form(
        "project_proposal_form"
    ):

        project_name = st.text_input(
            "Project Name"
        )

        project_constituency = st.selectbox(
            "Constituency",
            [
                "Warangal",
                "Karimnagar",
                "Nizamabad",
                "Khammam",
                "Nalgonda",
                "Mahabubnagar",
                "Medak",
                "Adilabad",
                "Hyderabad",
                "Secunderabad",
            ],
            index=0,
        )

        allocation_category = st.selectbox(
            "Allocation Category",
            [
                "Infrastructure",
                "Education",
                "Healthcare",
                "Water & Sanitation",
                "Other",
            ],
        )

        social_category = st.selectbox(
            "Social Category",
            [
                "General",
                "SC",
                "ST",
                "OBC",
                "Other",
            ],
        )

        domain = st.selectbox(
            "Domain",
            [
                "Education",
                "Health",
                "Roads & Infrastructure",
                "Water & Sanitation",
                "Agriculture",
                "Other Development",
            ],
        )

        category = st.selectbox(
            "Project Category",
            [
                "Roads",
                "Education",
                "Healthcare",
                "Water & Sanitation",
                "Other",
            ],
        )

        estimated_cost = st.number_input(
            "Estimated Cost",
            min_value=0.0,
            step=10000.0,
        )

        timeline_months = st.number_input(
            "Timeline (Months)",
            min_value=1,
            step=1,
        )

        submit_project = st.form_submit_button(
            "Submit Proposal"
        )

        if submit_project:

            if not project_name.strip():

                st.error(
                    "Project name is required."
                )

            elif estimated_cost <= 0:

                st.error(
                    "Estimated cost must be greater than 0."
                )

            else:

                conn = get_db_connection()

                try:

                    cur = conn.cursor()

                    cur.execute(
                        """
                        INSERT INTO projects (

                            title,
                            category,
                            constituency,

                            estimated_budget,
                            actual_expenditure,

                            timeline_months,
                            actual_months,

                            status,

                            anomaly_flag,
                            anomaly_reason,

                            social_category,
                            domain,
                            allocation_category

                        )
                        VALUES (
                            ?, ?, ?,
                            ?, ?,
                            ?, ?,
                            ?,
                            ?, ?,
                            ?, ?, ?
                        )
                        """,
                        (
                            project_name,
                            category,
                            project_constituency,

                            estimated_cost,
                            0,

                            timeline_months,
                            0,

                            "Proposed",

                            0,
                            "",

                            social_category,
                            domain,
                            allocation_category,
                        ),
                    )

                    conn.commit()

                    new_project_id = (
                        cur.lastrowid
                    )

                finally:

                    conn.close()

                save_audit_log(
                    action="Project Proposal Submitted",
                    project_id=new_project_id,
                    details=(
                        f"Project: {project_name}; "
                        f"Category: {category}; "
                        f"Constituency: {project_constituency}; "
                        f"Budget: {estimated_cost}"
                    ),
                )

                st.success(
                    "Project proposal submitted successfully."
                )

                st.rerun()

    # --------------------------------------------------------
    # EXISTING PROJECTS
    # --------------------------------------------------------

    st.subheader(
        "📋 Project Records"
    )

    if projects_df.empty:

        st.info(
            "No projects found."
        )

    else:

        st.dataframe(
            projects_df,
            use_container_width=True,
            hide_index=True,
        )

    # --------------------------------------------------------
    # PROJECT OFFICER REPORT
    # --------------------------------------------------------

    st.subheader(
        "📄 Project Report"
    )

    if not projects_df.empty:

        po_report_id = st.selectbox(
            "Select Project",
            projects_df[
                "id"
            ].tolist(),
            format_func=lambda project_id: (
                projects_df.loc[
                    projects_df["id"] == project_id,
                    "project_name"
                ].iloc[0]
            ),
            key="po_report_project",
        )

        po_report_project = (
            projects_df[
                projects_df["id"]
                ==
                po_report_id
            ]
            .iloc[0]
            .to_dict()
        )

        show_report_card(
            po_report_project,
            show_download=True,
        )

    else:

        st.info(
            "No projects available for report."
        )

    # --------------------------------------------------------
    # MILESTONE UPDATE
    # --------------------------------------------------------

    st.subheader(
        "🔄 Update Project Milestone"
    )

    if not projects_df.empty:

        project_ids = projects_df[
            "id"
        ].tolist()

        selected_id = st.selectbox(
            "Select Project",
            project_ids,
            key="po_selected_project",
        )

        selected_row = projects_df[
            projects_df["id"] == selected_id
        ].iloc[0]

        new_spent = st.number_input(
            "Actual Expenditure",
            min_value=0.0,
            value=float(
                selected_row.get(
                    "actual_spent",
                    0
                )
            ),
            step=10000.0,
            key="new_spent",
        )

        new_completed_months = st.number_input(
            "Completed Months",
            min_value=0,
            value=int(
                selected_row.get(
                    "completed_months",
                    0
                )
            ),
            step=1,
            key="new_completed_months",
        )

        status_options = [
            "Proposed",
            "In Progress",
            "Completed",
            "Delayed",
            "On Hold",
            "Stalled",
        ]

        current_status = selected_row.get(
            "status",
            "Proposed"
        )

        if current_status not in status_options:

            current_status = "Proposed"

        new_status = st.selectbox(
            "Project Status",
            status_options,
            index=status_options.index(
                current_status
            ),
            key="new_status",
        )

        if st.button(
            "Update Milestone",
            key="update_milestone",
        ):

            update_project(
                selected_id,
                actual_expenditure=new_spent,
                actual_months=new_completed_months,
                status=new_status,
            )

            save_audit_log(
                action="Project Milestone Updated",
                project_id=selected_id,
                details=(
                    f"Spent: {new_spent}; "
                    f"Completed Months: "
                    f"{new_completed_months}; "
                    f"Status: {new_status}"
                ),
            )

            st.success(
                "Project milestone updated successfully."
            )

            st.rerun()


# ============================================================
# MP REPRESENTATIVE DASHBOARD
# ============================================================

elif user_role == "MP Representative":

    st.header(
        "🏛️ MP Representative Dashboard"
    )

    st.write(
        f"Projects and fund monitoring for "
        f"**{user_constituency}** constituency."
    )

    # --------------------------------------------------------
    # CONSTITUENCY PROJECTS
    # --------------------------------------------------------

    constituency_projects = projects_df[
        projects_df["constituency"]
        .astype(str)
        .str.strip()
        .str.lower()
        ==
        str(user_constituency)
        .strip()
        .lower()
    ].copy()

    # --------------------------------------------------------
    # NUMERIC SAFETY
    # --------------------------------------------------------

    for column in [
        "estimated_cost",
        "actual_spent",
        "timeline_months",
        "completed_months",
    ]:

        constituency_projects[column] = pd.to_numeric(
            constituency_projects[column],
            errors="coerce"
        ).fillna(0)

    # --------------------------------------------------------
    # FUND CALCULATIONS
    # --------------------------------------------------------

    if constituency_projects.empty:

        total_budget = 0
        total_spent = 0

    else:

        total_budget = (
            constituency_projects[
                "estimated_cost"
            ].sum()
        )

        total_spent = (
            constituency_projects[
                "actual_spent"
            ].sum()
        )

    remaining_funds = (
        total_budget
        -
        total_spent
    )

    if total_budget > 0:

        utilization = (
            total_spent
            /
            total_budget
            *
            100
        )

    else:

        utilization = 0

    # --------------------------------------------------------
    # FUND SUMMARY
    # --------------------------------------------------------

    st.subheader(
        "💰 Constituency Fund Summary"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Total Project Budget",
            f"₹{total_budget:,.0f}"
        )

    with col2:

        st.metric(
            "Total Funds Spent",
            f"₹{total_spent:,.0f}"
        )

    with col3:

        st.metric(
            "Remaining Funds",
            f"₹{remaining_funds:,.0f}"
        )

    with col4:

        st.metric(
            "Fund Utilization",
            f"{utilization:.1f}%"
        )

    st.divider()

    # --------------------------------------------------------
    # PROJECT DETAILS
    # --------------------------------------------------------

    st.subheader(
        "📋 Project Details"
    )

    if constituency_projects.empty:

        st.warning(
            f"No projects found for "
            f"{user_constituency} constituency."
        )

    else:

        project_details = constituency_projects[
            [
                "id",
                "project_name",
                "category",
                "constituency",
                "domain",
                "social_category",
                "allocation_category",
                "estimated_cost",
                "actual_spent",
                "timeline_months",
                "completed_months",
                "status",
                "anomaly_flag",
                "anomaly_reason",
            ]
        ].copy()

        project_details[
            "remaining_funds"
        ] = (
            project_details[
                "estimated_cost"
            ]
            -
            project_details[
                "actual_spent"
            ]
        )

        project_details[
            "utilization_percent"
        ] = 0.0

        valid_budget = (
            project_details[
                "estimated_cost"
            ]
            > 0
        )

        project_details.loc[
            valid_budget,
            "utilization_percent"
        ] = (
            project_details.loc[
                valid_budget,
                "actual_spent"
            ]
            /
            project_details.loc[
                valid_budget,
                "estimated_cost"
            ]
            *
            100
        )

        st.dataframe(
            project_details,
            use_container_width=True,
            hide_index=True,
        )

    st.divider()

    # --------------------------------------------------------
    # PROJECT-WISE FUND UTILIZATION
    # --------------------------------------------------------

    st.subheader(
        "💵 Project-wise Fund Utilization"
    )

    if not constituency_projects.empty:

        fund_details = constituency_projects[
            [
                "project_name",
                "domain",
                "estimated_cost",
                "actual_spent",
            ]
        ].copy()

        fund_details[
            "remaining_funds"
        ] = (
            fund_details[
                "estimated_cost"
            ]
            -
            fund_details[
                "actual_spent"
            ]
        )

        fund_details[
            "utilization_percent"
        ] = 0.0

        valid_budget = (
            fund_details[
                "estimated_cost"
            ]
            > 0
        )

        fund_details.loc[
            valid_budget,
            "utilization_percent"
        ] = (
            fund_details.loc[
                valid_budget,
                "actual_spent"
            ]
            /
            fund_details.loc[
                valid_budget,
                "estimated_cost"
            ]
            *
            100
        )

        fund_details.columns = [
            "Project",
            "Domain",
            "Budget",
            "Spent",
            "Remaining",
            "Utilization %",
        ]

        st.dataframe(
            fund_details,
            use_container_width=True,
            hide_index=True,
        )

    # --------------------------------------------------------
    # DOMAIN-WISE ALLOCATION
    # --------------------------------------------------------

    st.subheader(
        "🏗️ Domain-wise Fund Allocation"
    )

    if not constituency_projects.empty:

        domain_summary = (
            constituency_projects
            .groupby(
                "domain",
                dropna=False
            )[
                "estimated_cost"
            ]
            .sum()
            .reset_index()
        )

        domain_summary.columns = [
            "Domain",
            "Allocated Amount",
        ]

        st.bar_chart(
            domain_summary.set_index(
                "Domain"
            )
        )

        st.dataframe(
            domain_summary,
            use_container_width=True,
            hide_index=True,
        )

    # --------------------------------------------------------
    # DOMAIN-WISE SPENDING
    # --------------------------------------------------------

    st.subheader(
        "📊 Domain-wise Spending"
    )

    if not constituency_projects.empty:

        domain_spending = (
            constituency_projects
            .groupby(
                "domain",
                dropna=False
            )[
                "actual_spent"
            ]
            .sum()
            .reset_index()
        )

        domain_spending.columns = [
            "Domain",
            "Spent Amount",
        ]

        st.bar_chart(
            domain_spending.set_index(
                "Domain"
            )
        )

        st.dataframe(
            domain_spending,
            use_container_width=True,
            hide_index=True,
        )

    # --------------------------------------------------------
    # SOCIAL CATEGORY ALLOCATION
    # --------------------------------------------------------

    st.subheader(
        "👥 Social Category-wise Allocation"
    )

    if not constituency_projects.empty:

        social_summary = (
            constituency_projects
            .groupby(
                "social_category",
                dropna=False
            )[
                "estimated_cost"
            ]
            .sum()
            .reset_index()
        )

        social_summary.columns = [
            "Social Category",
            "Allocated Amount",
        ]

        st.bar_chart(
            social_summary.set_index(
                "Social Category"
            )
        )

        st.dataframe(
            social_summary,
            use_container_width=True,
            hide_index=True,
        )

    # --------------------------------------------------------
    # ALLOCATION CATEGORY
    # --------------------------------------------------------

    st.subheader(
        "📌 Allocation Category-wise Funds"
    )

    if not constituency_projects.empty:

        allocation_summary = (
            constituency_projects
            .groupby(
                "allocation_category",
                dropna=False
            )[
                "estimated_cost"
            ]
            .sum()
            .reset_index()
        )

        allocation_summary.columns = [
            "Allocation Category",
            "Allocated Amount",
        ]

        st.bar_chart(
            allocation_summary.set_index(
                "Allocation Category"
            )
        )

        st.dataframe(
            allocation_summary,
            use_container_width=True,
            hide_index=True,
        )

    # --------------------------------------------------------
    # PROJECT STATUS
    # --------------------------------------------------------

    st.subheader(
        "📈 Project Status Summary"
    )

    if not constituency_projects.empty:

        status_summary = (
            constituency_projects[
                "status"
            ]
            .value_counts()
            .reset_index()
        )

        status_summary.columns = [
            "Status",
            "Projects",
        ]

        st.bar_chart(
            status_summary.set_index(
                "Status"
            )
        )

        st.dataframe(
            status_summary,
            use_container_width=True,
            hide_index=True,
        )

    # --------------------------------------------------------
    # MP PROJECT REPORT
    # --------------------------------------------------------

    st.subheader(
        "📄 Project Report"
    )

    if not constituency_projects.empty:

        mp_report_id = st.selectbox(
            "Select Project",
            constituency_projects[
                "id"
            ].tolist(),
            format_func=lambda project_id: (
                constituency_projects.loc[
                    constituency_projects["id"] == project_id,
                    "project_name"
                ].iloc[0]
            ),
            key="mp_report_project",
        )

        mp_report_project = (
            constituency_projects[
                constituency_projects["id"]
                ==
                mp_report_id
            ]
            .iloc[0]
            .to_dict()
        )

        show_report_card(
            mp_report_project,
            show_download=True,
        )

    else:

        st.info(
            "No projects available for report."
        )

    # --------------------------------------------------------
    # ANOMALY PROJECTS
    # --------------------------------------------------------

    st.subheader(
        "⚠️ Projects Requiring Attention"
    )

    anomaly_projects = constituency_projects[
        constituency_projects[
            "anomaly_flag"
        ]
        .astype(str)
        .str.lower()
        .isin(
            [
                "1",
                "true",
                "yes",
            ]
        )
    ].copy()

    if not anomaly_projects.empty:

        anomaly_display = anomaly_projects[
            [
                "id",
                "project_name",
                "anomaly_reason",
                "estimated_cost",
                "actual_spent",
                "status",
            ]
        ]

        st.dataframe(
            anomaly_display,
            use_container_width=True,
            hide_index=True,
        )

    else:

        st.success(
            "No flagged anomaly projects in this constituency."
        )

    # --------------------------------------------------------
    # MP ACTIONS
    # --------------------------------------------------------

    st.subheader(
        "⚡ MP Actions"
    )

    if not constituency_projects.empty:

        selected_project_id = st.selectbox(
            "Select Project",
            constituency_projects[
                "id"
            ].tolist(),
            key="mp_project_action",
        )

        mp_action = st.selectbox(
            "Action",
            [
                "Review Project",
                "Request Progress Update",
                "Raise Concern",
                "Recommend Monitoring",
            ],
            key="mp_action",
        )

        if st.button(
            "Submit MP Action",
            key="submit_mp_action",
        ):

            save_audit_log(
                action=f"MP Action: {mp_action}",
                project_id=selected_project_id,
                details=(
                    f"Constituency: "
                    f"{user_constituency}"
                ),
            )

            st.success(
                "MP action recorded successfully."
            )


# ============================================================
# MONITORING OFFICER DASHBOARD
# ============================================================

elif user_role == "Monitoring Officer":

    st.header(
        "🔍 Monitoring Officer Dashboard"
    )

    st.write(
        "Review financial, timeline and AI-based anomaly detection."
    )

    # --------------------------------------------------------
    # PROJECT SELECTION
    # --------------------------------------------------------

    if projects_df.empty:

        st.info(
            "No projects available for monitoring."
        )

    else:

        project_ids = projects_df[
            "id"
        ].tolist()

        selected_project_id = st.selectbox(
            "Select Project for Monitoring",
            project_ids,
            key="monitoring_project",
        )

        project_row = projects_df[
            projects_df["id"]
            ==
            selected_project_id
        ].iloc[0]

        project = project_row.to_dict()

        # ----------------------------------------------------
        # PROJECT INFORMATION
        # ----------------------------------------------------

        st.subheader(
            "📌 Project Information"
        )

        info1, info2, info3 = st.columns(3)

        with info1:

            st.write(
                f"**Project:** "
                f"{project.get('project_name', '')}"
            )

            st.write(
                f"**Project ID:** "
                f"{project.get('id', '')}"
            )

            st.write(
                f"**Category:** "
                f"{project.get('category', '')}"
            )

        with info2:

            st.write(
                f"**Constituency:** "
                f"{project.get('constituency', '')}"
            )

            st.write(
                f"**Estimated Cost:** "
                f"₹{float(project.get('estimated_cost', 0)):,.0f}"
            )

            st.write(
                f"**Domain:** "
                f"{project.get('domain', '')}"
            )

        with info3:

            st.write(
                f"**Actual Spent:** "
                f"₹{float(project.get('actual_spent', 0)):,.0f}"
            )

            st.write(
                f"**Status:** "
                f"{project.get('status', '')}"
            )

            st.write(
                f"**Social Category:** "
                f"{project.get('social_category', '')}"
            )

        # ----------------------------------------------------
        # FINANCIAL VERIFICATION
        # ----------------------------------------------------

        st.subheader(
            "💰 Financial Verification"
        )

        estimated_cost = float(
            project.get(
                "estimated_cost",
                0
            )
        )

        actual_spent = float(
            project.get(
                "actual_spent",
                0
            )
        )

        if estimated_cost > 0:

            spending_ratio = (
                actual_spent
                /
                estimated_cost
            )

        else:

            spending_ratio = 0

        if spending_ratio > 1:

            st.error(
                "Actual spending exceeds estimated "
                f"budget by "
                f"{(spending_ratio - 1) * 100:.1f}%."
            )

        elif spending_ratio > 0.9:

            st.warning(
                "Project has consumed more than "
                "90% of the estimated budget."
            )

        else:

            st.success(
                "Financial spending is within expected limits."
            )

        # ----------------------------------------------------
        # TIMELINE VERIFICATION
        # ----------------------------------------------------

        st.subheader(
            "⏱️ Timeline Verification"
        )

        timeline_months = float(
            project.get(
                "timeline_months",
                0
            )
        )

        completed_months = float(
            project.get(
                "completed_months",
                0
            )
        )

        if timeline_months > 0:

            timeline_ratio = (
                completed_months
                /
                timeline_months
            )

        else:

            timeline_ratio = 0

        if timeline_ratio > 1:

            st.error(
                "Project has exceeded the planned timeline."
            )

        elif timeline_ratio > 0.9:

            st.warning(
                "Project is close to its planned completion period."
            )

        else:

            st.success(
                "Project timeline is currently within limits."
            )

        # ----------------------------------------------------
        # RULE BASED RISK CHECK
        # ----------------------------------------------------

        st.subheader(
            "🧮 Rule / Risk Analysis"
        )

        risk_result = calculate_risk(
            estimated_cost,
            actual_spent,
            timeline_months,
            completed_months,
        )

        risk_level = risk_result.get(
            "risk_level",
            "Unknown"
        )

        risk_score = risk_result.get(
            "risk_score",
            0
        )

        risk_reason = risk_result.get(
            "reason",
            ""
        )

        risk_col1, risk_col2 = st.columns(2)

        with risk_col1:

            st.metric(
                "Risk Level",
                risk_level,
            )

        with risk_col2:

            st.metric(
                "Risk Score",
                risk_score,
            )

        if risk_reason:

            st.info(
                risk_reason
            )

        # ----------------------------------------------------
        # AI ANOMALY DETECTION PROCESS
        # ----------------------------------------------------

        st.subheader(
            "🤖 AI Anomaly Detection Process"
        )

        st.write(
            "The system evaluates project financial "
            "and timeline indicators."
        )

        process_col1, process_col2, process_col3 = st.columns(3)

        with process_col1:

            st.info(
                "1️⃣ INPUTS\n\n"
                "• Estimated Cost\n"
                "• Actual Spending\n"
                "• Planned Timeline\n"
                "• Completed Months\n"
                "• Project Status"
            )

        with process_col2:

            st.info(
                "2️⃣ AI / RULE ANALYSIS\n\n"
                "• Spending Pattern\n"
                "• Timeline Delay\n"
                "• Risk Score\n"
                "• Anomaly Detection"
            )

        with process_col3:

            if risk_level == "High":

                st.error(
                    "3️⃣ HIGH RISK\n\n"
                    "Project requires monitoring."
                )

            elif risk_level == "Medium":

                st.warning(
                    "3️⃣ MEDIUM RISK\n\n"
                    "Project needs review."
                )

            else:

                st.success(
                    "3️⃣ LOW RISK\n\n"
                    "No major anomaly detected."
                )

        # ----------------------------------------------------
        # WHY FLAGGED
        # ----------------------------------------------------

        st.subheader(
            "🔎 Why Was This Project Flagged?"
        )

        reasons = []

        if estimated_cost > 0:

            if actual_spent > estimated_cost:

                reasons.append(
                    "Actual expenditure exceeds "
                    "the approved estimate."
                )

            elif actual_spent >= (
                estimated_cost * 0.9
            ):

                reasons.append(
                    "Actual expenditure is close "
                    "to the approved estimate."
                )

        if timeline_months > 0:

            if completed_months > timeline_months:

                reasons.append(
                    "Project has exceeded "
                    "the planned timeline."
                )

            elif completed_months >= (
                timeline_months * 0.9
            ):

                reasons.append(
                    "Project is close to its "
                    "planned completion timeline."
                )

        anomaly_reason = project.get(
            "anomaly_reason",
            ""
        )

        if anomaly_reason:

            reasons.append(
                anomaly_reason
            )

        if not reasons:

            reasons.append(
                "No major rule-based anomaly "
                "indicators detected."
            )

        for reason in reasons:

            st.write(
                f"• {reason}"
            )

        # ----------------------------------------------------
        # HUMAN IN THE LOOP
        # ----------------------------------------------------

        st.subheader(
            "👤 Human-in-the-Loop Safety Review"
        )

        st.write(
            "AI only recommends the risk status. "
            "The Monitoring Officer makes the final decision."
        )

        ai_recommendation = risk_level

        st.info(
            f"AI Recommendation: "
            f"**{ai_recommendation}**"
        )

        human_decision = st.radio(
            "Monitoring Officer Decision",
            [
                "Accept",
                "Reject",
                "Edit",
            ],
            horizontal=True,
            key=f"human_decision_{selected_project_id}",
        )

        edited_risk = ai_recommendation

        if human_decision == "Edit":

            risk_options = [
                "Low",
                "Medium",
                "High",
            ]

            if ai_recommendation in risk_options:

                default_index = (
                    risk_options.index(
                        ai_recommendation
                    )
                )

            else:

                default_index = 0

            edited_risk = st.selectbox(
                "Edit Risk Level",
                risk_options,
                index=default_index,
                key=f"edited_risk_{selected_project_id}",
            )

        # ----------------------------------------------------
        # MONITORING ACTION
        # ----------------------------------------------------

        st.subheader(
            "⚡ Monitoring Action"
        )

        monitoring_action = st.selectbox(
            "Select Action",
            [
                "No Action",
                "Issue Notice",
                "Request Explanation",
                "Increase Monitoring",
                "Recommend Fund Review",
                "Block Funds",
            ],
            key=f"monitoring_action_{selected_project_id}",
        )

        if st.button(
            "Save Monitoring Decision",
            key=f"save_monitoring_{selected_project_id}",
        ):

            if human_decision == "Accept":

                final_risk = ai_recommendation

            elif human_decision == "Edit":

                final_risk = edited_risk

            else:

                final_risk = "Rejected"

            save_audit_log(
                action="Monitoring Decision",
                project_id=selected_project_id,
                details=(
                    f"AI Recommendation: "
                    f"{ai_recommendation}; "
                    f"Human Decision: "
                    f"{human_decision}; "
                    f"Final Risk: "
                    f"{final_risk}; "
                    f"Monitoring Action: "
                    f"{monitoring_action}"
                ),
            )

            st.success(
                "Monitoring decision saved successfully."
            )

        # ----------------------------------------------------
        # MONITORING PROJECT REPORT
        # ----------------------------------------------------

        st.subheader(
            "📄 Monitoring Report"
        )

        show_report_card(
            project,
            show_download=True,
        )


# ============================================================
# ADMINISTRATOR DASHBOARD
# ============================================================

elif user_role == "Administrator":

    st.header(
        "⚙️ Administrator Dashboard"
    )

    st.write(
        "Manage users and review system audit activity."
    )

    # --------------------------------------------------------
    # USER MANAGEMENT
    # --------------------------------------------------------

    st.subheader(
        "👥 User Management"
    )

    conn = get_db_connection()

    try:

        users_df = pd.read_sql_query(
            """
            SELECT
                id,
                name,
                email,
                role,
                constituency,
                official_id,
                is_active
            FROM users
            ORDER BY id
            """,
            conn,
        )

    finally:

        conn.close()

    if users_df.empty:

        st.info(
            "No users found."
        )

    else:

        st.dataframe(
            users_df,
            use_container_width=True,
            hide_index=True,
        )

    # --------------------------------------------------------
    # AUDIT LOGS
    # --------------------------------------------------------

    st.subheader(
        "📝 Audit Logs"
    )

    conn = get_db_connection()

    try:

        logs_df = pd.read_sql_query(
            """
            SELECT *
            FROM audit_logs
            ORDER BY id DESC
            """,
            conn,
        )

    except Exception:

        logs_df = pd.DataFrame()

    finally:

        conn.close()

    if logs_df.empty:

        st.info(
            "No audit logs available."
        )

    else:

        st.dataframe(
            logs_df,
            use_container_width=True,
            hide_index=True,
        )