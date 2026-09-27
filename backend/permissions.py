"""
MPLAD Management System - Role Permissions
"""

ROLE_PERMISSIONS = {
    "Citizen": [
        "VIEW_PUBLIC_PROJECTS",
        "SUBMIT_DEFECT_REPORT",
        "EXPORT_PDF",
    ],

    "Project Officer": [
        "VIEW_PUBLIC_PROJECTS",
        "SUBMIT_PROPOSAL",
        "UPDATE_MILESTONE",
        "RUN_PRE_CHECK",
        "EXPORT_PDF",
    ],

    "MP Representative": [
        "VIEW_PUBLIC_PROJECTS",
        "VIEW_CONSTITUENCY_ALLOCATION",
        "VIEW_SUBPLAN_METRICS",
        "APPROVE_PROJECT",
        "SEND_BACK_PROJECT",
        "REQUEST_CLARIFICATION",
        "HOLD_PROJECT",
        "EXPORT_PDF",
    ],

    "Monitoring Officer": [
        "VIEW_PUBLIC_PROJECTS",
        "VIEW_RAW_ML_SCORES",
        "ISSUE_NOTICE",
        "FREEZE_FUNDS",
        "TRIGGER_INSPECTION",
        "START_INVESTIGATION",
        "ESCALATE_CASE",
        "CLEAR_FLAG",
        "EXPORT_PDF",
    ],

    "Administrator": [
        "VIEW_PUBLIC_PROJECTS",
        "MANAGE_USERS",
        "VIEW_AUDIT_LOGS",
        "SYSTEM_MAINTENANCE",
        "EXPORT_PDF",
    ],
}


def check_permission(role, action):
    return action in ROLE_PERMISSIONS.get(role, [])