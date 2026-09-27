
"""
MPLAD INSIGHT - Demo / Prototype Report Generator

Generates project-wise audit/anomaly reports for the MPLAD
demo/prototype application.
"""

import io
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


def generate_pdf_report(project_data: dict) -> bytes:
    """
    Generate a detailed project-wise demo audit report.

    project_data must be a dictionary containing project information
    and, preferably, calculated anomaly/risk information.
    """

    buffer = io.BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Heading1"],
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#1f4037"),
        spaceAfter=8,
    )

    subtitle_style = ParagraphStyle(
        "ReportSubtitle",
        parent=styles["Normal"],
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#64748b"),
        spaceAfter=18,
    )

    section_style = ParagraphStyle(
        "Section",
        parent=styles["Heading2"],
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#1f4037"),
        spaceBefore=12,
        spaceAfter=8,
    )

    normal_style = ParagraphStyle(
        "NormalReport",
        parent=styles["Normal"],
        fontSize=9,
        leading=13,
    )

    header_style = ParagraphStyle(
        "TableHeader",
        parent=styles["Normal"],
        fontSize=9,
        leading=11,
        textColor=colors.white,
        fontName="Helvetica-Bold",
    )

    story = []

    generated_at = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    project_id = project_data.get("id", "N/A")
    title = project_data.get("title", "N/A")
    category = project_data.get("category", "N/A")
    constituency = project_data.get("constituency", "N/A")

    estimated_budget = float(
        project_data.get("estimated_budget", 0) or 0
    )

    actual_expenditure = float(
        project_data.get("actual_expenditure", 0) or 0
    )

    timeline_months = int(
        project_data.get("timeline_months", 0) or 0
    )

    actual_months = int(
        project_data.get("actual_months", 0) or 0
    )

    cost_ratio = project_data.get("cost_ratio")

    time_ratio = project_data.get("time_ratio")

    if cost_ratio is None:
        cost_ratio = (
            actual_expenditure / estimated_budget
            if estimated_budget > 0
            else 0
        )

    if time_ratio is None:
        time_ratio = (
            actual_months / timeline_months
            if timeline_months > 0
            else 0
        )

    risk_score = project_data.get("risk_score", 0)
    risk_level = project_data.get("risk_level", "Low")

    anomaly_flag = project_data.get("anomaly_flag", 0)

    anomaly_reason = project_data.get(
        "anomaly_reason",
        "No anomaly reason recorded."
    )

    action = project_data.get(
        "monitoring_action",
        "No enforcement action recorded."
    )

    status = project_data.get(
        "status",
        "N/A"
    )

    # ---------------------------------------------------------
    # MP REPRESENTATIVE ACTION DETAILS
    # ---------------------------------------------------------

    mp_action = project_data.get(
        "mp_action",
        "No action recorded"
    )

    mp_remarks = project_data.get(
        "mp_remarks",
        "No remarks recorded"
    )

    mp_action_timestamp = project_data.get(
        "mp_action_timestamp",
        ""
    )

    # ---------------------------------------------------------
    # TITLE
    # ---------------------------------------------------------

    story.append(
        Paragraph(
            "MPLAD INSIGHT",
            title_style
        )
    )

    story.append(
        Paragraph(
            "Demo / Prototype Audit & Anomaly Report",
            subtitle_style
        )
    )

    story.append(
        Paragraph(
            f"<b>Report Generated:</b> {generated_at}",
            normal_style
        )
    )

    story.append(Spacer(1, 12))

    # ---------------------------------------------------------
    # PROJECT DETAILS
    # ---------------------------------------------------------

    story.append(
        Paragraph(
            "1. Project Details",
            section_style
        )
    )

    project_table = [
        [
            Paragraph("Attribute", header_style),
            Paragraph("Value", header_style),
        ],
        [
            Paragraph("Project ID", normal_style),
            Paragraph(str(project_id), normal_style),
        ],
        [
            Paragraph("Project Title", normal_style),
            Paragraph(str(title), normal_style),
        ],
        [
            Paragraph("Constituency", normal_style),
            Paragraph(str(constituency), normal_style),
        ],
        [
            Paragraph("Category", normal_style),
            Paragraph(str(category), normal_style),
        ],
        [
            Paragraph("Status", normal_style),
            Paragraph(str(status), normal_style),
        ],
    ]

    table = Table(
        project_table,
        colWidths=[150, 380]
    )

    table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#1f4037"),
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.HexColor("#cbd5e1"),
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP",
                ),
                (
                    "PADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
            ]
        )
    )

    story.append(table)

    # ---------------------------------------------------------
    # FINANCIAL ANALYSIS
    # ---------------------------------------------------------

    story.append(
        Paragraph(
            "2. Financial Analysis",
            section_style
        )
    )

    financial_table = [
        [
            Paragraph("Metric", header_style),
            Paragraph("Value", header_style),
        ],
        [
            Paragraph("Estimated Budget", normal_style),
            Paragraph(
                f"INR {estimated_budget:,.2f}",
                normal_style
            ),
        ],
        [
            Paragraph("Actual Expenditure", normal_style),
            Paragraph(
                f"INR {actual_expenditure:,.2f}",
                normal_style
            ),
        ],
        [
            Paragraph("Cost Ratio", normal_style),
            Paragraph(
                f"{float(cost_ratio):.2f}x",
                normal_style
            ),
        ],
        [
            Paragraph("Cost Overrun", normal_style),
            Paragraph(
                f"{max(0, (float(cost_ratio) - 1) * 100):.2f}%",
                normal_style
            ),
        ],
    ]

    financial_table_obj = Table(
        financial_table,
        colWidths=[150, 380]
    )

    financial_table_obj.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#1f4037"),
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.HexColor("#cbd5e1"),
                ),
                (
                    "PADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
            ]
        )
    )

    story.append(financial_table_obj)

    # ---------------------------------------------------------
    # TIMELINE ANALYSIS
    # ---------------------------------------------------------

    story.append(
        Paragraph(
            "3. Timeline Analysis",
            section_style
        )
    )

    timeline_table = [
        [
            Paragraph("Metric", header_style),
            Paragraph("Value", header_style),
        ],
        [
            Paragraph("Allocated Timeline", normal_style),
            Paragraph(
                f"{timeline_months} months",
                normal_style
            ),
        ],
        [
            Paragraph("Actual Timeline", normal_style),
            Paragraph(
                f"{actual_months} months",
                normal_style
            ),
        ],
        [
            Paragraph("Time Ratio", normal_style),
            Paragraph(
                f"{float(time_ratio):.2f}x",
                normal_style
            ),
        ],
        [
            Paragraph("Time Delay", normal_style),
            Paragraph(
                f"{max(0, (float(time_ratio) - 1) * 100):.2f}%",
                normal_style
            ),
        ],
    ]

    timeline_table_obj = Table(
        timeline_table,
        colWidths=[150, 380]
    )

    timeline_table_obj.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#1f4037"),
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.HexColor("#cbd5e1"),
                ),
                (
                    "PADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
            ]
        )
    )

    story.append(timeline_table_obj)

    # ---------------------------------------------------------
    # RISK ANALYSIS
    # ---------------------------------------------------------

    story.append(
        Paragraph(
            "4. Anomaly / Risk Evaluation",
            section_style
        )
    )

    risk_table = [
        [
            Paragraph("Metric", header_style),
            Paragraph("Result", header_style),
        ],
        [
            Paragraph("Risk Score", normal_style),
            Paragraph(
                str(risk_score),
                normal_style
            ),
        ],
        [
            Paragraph("Risk Level", normal_style),
            Paragraph(
                str(risk_level),
                normal_style
            ),
        ],
        [
            Paragraph("Anomaly Detected", normal_style),
            Paragraph(
                "YES" if int(anomaly_flag) == 1 else "NO",
                normal_style
            ),
        ],
        [
            Paragraph("Why Flagged", normal_style),
            Paragraph(
                str(anomaly_reason),
                normal_style
            ),
        ],
    ]

    risk_table_obj = Table(
        risk_table,
        colWidths=[150, 380]
    )

    risk_table_obj.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#1f4037"),
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.HexColor("#cbd5e1"),
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP",
                ),
                (
                    "PADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
            ]
        )
    )

    story.append(risk_table_obj)

    # ---------------------------------------------------------
    # MP REPRESENTATIVE ACTION
    # ---------------------------------------------------------

    story.append(
        Paragraph(
            "5. MP Representative Action",
            section_style
        )
    )

    mp_table = [
        [
            Paragraph("Metric", header_style),
            Paragraph("Result", header_style),
        ],
        [
            Paragraph("MP Action", normal_style),
            Paragraph(
                str(mp_action),
                normal_style
            ),
        ],
        [
            Paragraph("MP Remarks", normal_style),
            Paragraph(
                str(mp_remarks),
                normal_style
            ),
        ],
        [
            Paragraph("Action Date / Time", normal_style),
            Paragraph(
                str(mp_action_timestamp)
                if mp_action_timestamp
                else "N/A",
                normal_style
            ),
        ],
    ]

    mp_table_obj = Table(
        mp_table,
        colWidths=[150, 380]
    )

    mp_table_obj.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#1f4037"),
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.HexColor("#cbd5e1"),
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP",
                ),
                (
                    "PADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
            ]
        )
    )

    story.append(mp_table_obj)

    # ---------------------------------------------------------
    # MONITORING ACTION
    # ---------------------------------------------------------

    story.append(
        Paragraph(
            "6. Monitoring Officer Action",
            section_style
        )
    )

    story.append(
        Paragraph(
            str(action),
            normal_style
        )
    )

    story.append(Spacer(1, 20))

    # ---------------------------------------------------------
    # DEMO DISCLAIMER
    # ---------------------------------------------------------

    story.append(
        Paragraph(
            "<b>Note:</b> This report is generated by the "
            "MPLAD INSIGHT demo/prototype application. "
            "The anomaly and risk evaluation is a deterministic "
            "rule-based evaluation for demonstration purposes "
            "and does not represent an official government report.",
            normal_style
        )
    )

    document.build(story)

    buffer.seek(0)

    return buffer.getvalue()