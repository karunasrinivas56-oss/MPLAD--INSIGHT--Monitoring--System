
import sqlite3
import os


DB_PATH = "mplad.db"


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_db_connection():
    """Create and return database connection."""

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    return conn


# =========================================================
# DEMO PROJECT DATA
# 10 CONSTITUENCIES × 4 PROJECTS = 40 PROJECTS
# =========================================================

DEMO_PROJECTS = [

    # =====================================================
    # WARANGAL
    # =====================================================

    (
        "Warangal Main Road Improvement",
        "Roads",
        "Warangal",
        4500000,
        3600000,
        12,
        10,
        "In Progress",
        0,
        ""
    ),

    (
        "Warangal Government School Renovation",
        "Education",
        "Warangal",
        2800000,
        3640000,
        10,
        13,
        "In Progress",
        1,
        "Moderate Cost Overrun (1.30x) | Moderate Timeline Delay (1.30x)"
    ),

    (
        "Warangal Urban PHC Upgrade",
        "Healthcare",
        "Warangal",
        3200000,
        5120000,
        12,
        18,
        "Stalled",
        1,
        "Severe Expenditure Overrun (1.60x) | Critical Timeline Delay (1.50x)"
    ),

    (
        "Warangal Drinking Water Scheme",
        "Water & Sanitation",
        "Warangal",
        5000000,
        4750000,
        14,
        14,
        "Completed",
        0,
        ""
    ),

    # =====================================================
    # KARIMNAGAR
    # =====================================================

    (
        "Karimnagar Rural Road Development",
        "Roads",
        "Karimnagar",
        4200000,
        3360000,
        12,
        10,
        "In Progress",
        0,
        ""
    ),

    (
        "Karimnagar ZP School Infrastructure",
        "Education",
        "Karimnagar",
        3000000,
        3900000,
        10,
        13,
        "Stalled",
        1,
        "Moderate Cost Overrun (1.30x) | Moderate Timeline Delay (1.30x)"
    ),

    (
        "Karimnagar Community Health Centre",
        "Healthcare",
        "Karimnagar",
        3500000,
        5600000,
        12,
        18,
        "In Progress",
        1,
        "Severe Expenditure Overrun (1.60x) | Critical Timeline Delay (1.50x)"
    ),

    (
        "Karimnagar Village Water Supply",
        "Water & Sanitation",
        "Karimnagar",
        4600000,
        4370000,
        14,
        14,
        "Completed",
        0,
        ""
    ),

    # =====================================================
    # NIZAMABAD
    # =====================================================

    (
        "Nizamabad Internal Roads Project",
        "Roads",
        "Nizamabad",
        4800000,
        3840000,
        12,
        10,
        "In Progress",
        0,
        ""
    ),

    (
        "Nizamabad Government School Upgrade",
        "Education",
        "Nizamabad",
        2600000,
        3380000,
        10,
        13,
        "In Progress",
        1,
        "Moderate Cost Overrun (1.30x) | Moderate Timeline Delay (1.30x)"
    ),

    (
        "Nizamabad Primary Health Centre",
        "Healthcare",
        "Nizamabad",
        3400000,
        5440000,
        12,
        18,
        "Stalled",
        1,
        "Severe Expenditure Overrun (1.60x) | Critical Timeline Delay (1.50x)"
    ),

    (
        "Nizamabad Drinking Water Expansion",
        "Water & Sanitation",
        "Nizamabad",
        5200000,
        4940000,
        14,
        14,
        "Completed",
        0,
        ""
    ),

    # =====================================================
    # KHAMMAM
    # =====================================================

    (
        "Khammam Municipal Road Upgrade",
        "Roads",
        "Khammam",
        5000000,
        4000000,
        12,
        10,
        "In Progress",
        0,
        ""
    ),

    (
        "Khammam Government School Development",
        "Education",
        "Khammam",
        2900000,
        3770000,
        10,
        13,
        "In Progress",
        1,
        "Moderate Cost Overrun (1.30x) | Moderate Timeline Delay (1.30x)"
    ),

    (
        "Khammam Area Hospital Improvement",
        "Healthcare",
        "Khammam",
        3800000,
        6080000,
        12,
        18,
        "Stalled",
        1,
        "Severe Expenditure Overrun (1.60x) | Critical Timeline Delay (1.50x)"
    ),

    (
        "Khammam Rural Water Supply",
        "Water & Sanitation",
        "Khammam",
        4700000,
        4465000,
        14,
        14,
        "Completed",
        0,
        ""
    ),

    # =====================================================
    # NALGONDA
    # =====================================================

    (
        "Nalgonda Rural Road Improvement",
        "Roads",
        "Nalgonda",
        4300000,
        3440000,
        12,
        10,
        "In Progress",
        0,
        ""
    ),

    (
        "Nalgonda School Building Renovation",
        "Education",
        "Nalgonda",
        2700000,
        3510000,
        10,
        13,
        "In Progress",
        1,
        "Moderate Cost Overrun (1.30x) | Moderate Timeline Delay (1.30x)"
    ),

    (
        "Nalgonda PHC Modernization",
        "Healthcare",
        "Nalgonda",
        3300000,
        5280000,
        12,
        18,
        "Stalled",
        1,
        "Severe Expenditure Overrun (1.60x) | Critical Timeline Delay (1.50x)"
    ),

    (
        "Nalgonda Drinking Water Project",
        "Water & Sanitation",
        "Nalgonda",
        4900000,
        4655000,
        14,
        14,
        "Completed",
        0,
        ""
    ),

    # =====================================================
    # MAHABUBNAGAR
    # =====================================================

    (
        "Mahabubnagar District Road Works",
        "Roads",
        "Mahabubnagar",
        4600000,
        3680000,
        12,
        10,
        "In Progress",
        0,
        ""
    ),

    (
        "Mahabubnagar School Infrastructure Project",
        "Education",
        "Mahabubnagar",
        3100000,
        4030000,
        10,
        13,
        "In Progress",
        1,
        "Moderate Cost Overrun (1.30x) | Moderate Timeline Delay (1.30x)"
    ),

    (
        "Mahabubnagar Health Centre Expansion",
        "Healthcare",
        "Mahabubnagar",
        3600000,
        5760000,
        12,
        18,
        "Stalled",
        1,
        "Severe Expenditure Overrun (1.60x) | Critical Timeline Delay (1.50x)"
    ),

    (
        "Mahabubnagar Drinking Water Scheme",
        "Water & Sanitation",
        "Mahabubnagar",
        5400000,
        5130000,
        14,
        14,
        "Completed",
        0,
        ""
    ),

    # =====================================================
    # MEDAK
    # =====================================================

    (
        "Medak Village Road Development",
        "Roads",
        "Medak",
        4100000,
        3280000,
        12,
        10,
        "In Progress",
        0,
        ""
    ),

    (
        "Medak Government School Improvement",
        "Education",
        "Medak",
        2500000,
        3250000,
        10,
        13,
        "In Progress",
        1,
        "Moderate Cost Overrun (1.30x) | Moderate Timeline Delay (1.30x)"
    ),

    (
        "Medak Community Health Centre",
        "Healthcare",
        "Medak",
        3000000,
        4800000,
        12,
        18,
        "Stalled",
        1,
        "Severe Expenditure Overrun (1.60x) | Critical Timeline Delay (1.50x)"
    ),

    (
        "Medak Rural Water Supply",
        "Water & Sanitation",
        "Medak",
        4400000,
        4180000,
        14,
        14,
        "Completed",
        0,
        ""
    ),

    # =====================================================
    # ADILABAD
    # =====================================================

    (
        "Adilabad Road Connectivity Project",
        "Roads",
        "Adilabad",
        4700000,
        3760000,
        12,
        10,
        "In Progress",
        0,
        ""
    ),

    (
        "Adilabad School Development Works",
        "Education",
        "Adilabad",
        2800000,
        3640000,
        10,
        13,
        "In Progress",
        1,
        "Moderate Cost Overrun (1.30x) | Moderate Timeline Delay (1.30x)"
    ),

    (
        "Adilabad Primary Health Centre Upgrade",
        "Healthcare",
        "Adilabad",
        3500000,
        5600000,
        12,
        18,
        "In Progress",
        1,
        "Severe Expenditure Overrun (1.60x) | Critical Timeline Delay (1.50x)"
    ),

    (
        "Adilabad Drinking Water Programme",
        "Water & Sanitation",
        "Adilabad",
        4800000,
        4560000,
        14,
        14,
        "Completed",
        0,
        ""
    ),

    # =====================================================
    # HYDERABAD
    # =====================================================

    (
        "Hyderabad Urban Road Improvement",
        "Roads",
        "Hyderabad",
        6000000,
        4800000,
        12,
        10,
        "In Progress",
        0,
        ""
    ),

    (
        "Hyderabad Government School Modernization",
        "Education",
        "Hyderabad",
        4000000,
        5200000,
        10,
        13,
        "In Progress",
        1,
        "Moderate Cost Overrun (1.30x) | Moderate Timeline Delay (1.30x)"
    ),

    (
        "Hyderabad Urban Health Centre",
        "Healthcare",
        "Hyderabad",
        5500000,
        8800000,
        12,
        18,
        "Stalled",
        1,
        "Severe Expenditure Overrun (1.60x) | Critical Timeline Delay (1.50x)"
    ),

    (
        "Hyderabad Water & Sanitation Upgrade",
        "Water & Sanitation",
        "Hyderabad",
        6500000,
        6175000,
        14,
        14,
        "Completed",
        0,
        ""
    ),

    # =====================================================
    # SECUNDERABAD
    # =====================================================

    (
        "Secunderabad Road Development",
        "Roads",
        "Secunderabad",
        5800000,
        4640000,
        12,
        10,
        "In Progress",
        0,
        ""
    ),

    (
        "Secunderabad School Infrastructure",
        "Education",
        "Secunderabad",
        3800000,
        4940000,
        10,
        13,
        "In Progress",
        1,
        "Moderate Cost Overrun (1.30x) | Moderate Timeline Delay (1.30x)"
    ),

    (
        "Secunderabad Community Health Facility",
        "Healthcare",
        "Secunderabad",
        5200000,
        8320000,
        12,
        18,
        "Stalled",
        1,
        "Severe Expenditure Overrun (1.60x) | Critical Timeline Delay (1.50x)"
    ),

    (
        "Secunderabad Drinking Water Improvement",
        "Water & Sanitation",
        "Secunderabad",
        6200000,
        5890000,
        14,
        14,
        "Completed",
        0,
        ""
    )
]


# =========================================================
# DEMO ALLOCATION DISTRIBUTION
# =========================================================

SOCIAL_CATEGORIES = [
    "SC",
    "ST",
    "OBC",
    "General",
    "Other"
]

DOMAINS = [
    "Education",
    "Health",
    "Roads & Infrastructure",
    "Water & Sanitation",
    "Agriculture",
    "Other Development"
]

ALLOCATION_CATEGORIES = [
    "Infrastructure",
    "Education",
    "Healthcare",
    "Water & Sanitation",
    "Other"
]


def get_demo_allocation(index):
    """Return demo social category, domain and allocation category."""

    social_category = SOCIAL_CATEGORIES[
        index % len(SOCIAL_CATEGORIES)
    ]

    domain = DOMAINS[
        index % len(DOMAINS)
    ]

    allocation_category = ALLOCATION_CATEGORIES[
        index % len(ALLOCATION_CATEGORIES)
    ]

    return (
        social_category,
        domain,
        allocation_category
    )


# =========================================================
# SEED DEMO PROJECTS
# =========================================================

def seed_demo_projects(cursor):
    """
    Add the 40 demo projects without deleting existing data.

    Existing demo projects are updated only for allocation fields.

    User-created projects are NOT modified.
    """

    for index, project in enumerate(DEMO_PROJECTS):

        (
            title,
            category,
            constituency,
            estimated_budget,
            actual_expenditure,
            timeline_months,
            actual_months,
            status,
            anomaly_flag,
            anomaly_reason
        ) = project

        (
            social_category,
            domain,
            allocation_category
        ) = get_demo_allocation(index)

        existing = cursor.execute("""
            SELECT id
            FROM projects
            WHERE title = ?
            AND LOWER(TRIM(constituency))
                = LOWER(TRIM(?))
        """, (
            title,
            constituency
        )).fetchone()

        if existing:

            cursor.execute("""
                UPDATE projects
                SET
                    social_category = ?,
                    domain = ?,
                    allocation_category = ?
                WHERE id = ?
            """, (
                social_category,
                domain,
                allocation_category,
                existing["id"]
            ))

            continue

        cursor.execute("""
            INSERT INTO projects
            (
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
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
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
        ))


# =========================================================
# DEFAULT DEMO USERS
# =========================================================

DEFAULT_USERS = [

    (
        "Admin User",
        "admin@mplad.in",
        "admin123",
        "Administrator",
        "Central",
        "ADM-TG-001"
    ),

    (
        "Officer Kumar",
        "officer@mplad.in",
        "officer123",
        "Project Officer",
        "Warangal",
        "PO-TG-001"
    ),

    (
        "Citizen Rao",
        "citizen@mplad.in",
        "citizen123",
        "Citizen",
        "Warangal",
        None
    ),

    (
        "MP Sharma",
        "mp@mplad.in",
        "mp123",
        "MP Representative",
        "Warangal",
        "MP-TG-001"
    ),

    (
        "Auditor Verma",
        "auditor@mplad.in",
        "auditor123",
        "Monitoring Officer",
        "Central",
        "MO-TG-001"
    )
]


# =========================================================
# SYNC DEMO USER DETAILS
# =========================================================

def sync_demo_users(cursor):
    """
    Ensure the five demo accounts always have their
    correct demo roles and official IDs.

    This does NOT delete users.
    This does NOT modify user-created accounts.
    """

    for (
        name,
        email,
        password,
        role,
        constituency,
        official_id
    ) in DEFAULT_USERS:

        existing = cursor.execute("""
            SELECT id
            FROM users
            WHERE LOWER(TRIM(email)) = ?
        """, (
            email.lower().strip(),
        )).fetchone()

        if existing:

            cursor.execute("""
                UPDATE users
                SET
                    name = ?,
                    role = ?,
                    constituency = ?,
                    official_id = ?
                WHERE id = ?
            """, (
                name,
                role,
                constituency,
                official_id,
                existing["id"]
            ))

        else:

            cursor.execute("""
                INSERT INTO users
                (
                    name,
                    email,
                    password,
                    role,
                    constituency,
                    official_id
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                name,
                email,
                password,
                role,
                constituency,
                official_id
            ))


# =========================================================
# INITIALIZE DATABASE
# =========================================================

def init_database():
    """Create all required tables and seed demo data."""

    conn = get_db_connection()
    cursor = conn.cursor()

    # =====================================================
    # USERS
    # =====================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            constituency TEXT,
            official_id TEXT
        )
    """)

    # =====================================================
    # MIGRATE EXISTING USERS TABLE
    # =====================================================

    columns = [
        row["name"]
        for row in cursor.execute(
            "PRAGMA table_info(users)"
        ).fetchall()
    ]

    if "official_id" not in columns:

        cursor.execute("""
            ALTER TABLE users
            ADD COLUMN official_id TEXT
        """)

    # =====================================================
    # UNIQUE OFFICIAL ID INDEX
    # =====================================================

    cursor.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS idx_users_official_id
        ON users(official_id)
        WHERE official_id IS NOT NULL
    """)

    # =====================================================
    # PROJECTS
    # =====================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            constituency TEXT NOT NULL,
            estimated_budget REAL NOT NULL,
            actual_expenditure REAL DEFAULT 0.0,
            timeline_months INTEGER NOT NULL,
            actual_months INTEGER DEFAULT 0,
            status TEXT DEFAULT 'Proposed',
            anomaly_flag INTEGER DEFAULT 0,
            anomaly_reason TEXT DEFAULT '',
            social_category TEXT DEFAULT 'Other',
            domain TEXT DEFAULT 'Other Development',
            allocation_category TEXT DEFAULT 'Other'
        )
    """)

    # =====================================================
    # MIGRATE EXISTING PROJECTS TABLE
    # =====================================================

    project_columns = [
        row["name"]
        for row in cursor.execute(
            "PRAGMA table_info(projects)"
        ).fetchall()
    ]

    if "social_category" not in project_columns:

        cursor.execute("""
            ALTER TABLE projects
            ADD COLUMN social_category TEXT
            DEFAULT 'Other'
        """)

    if "domain" not in project_columns:

        cursor.execute("""
            ALTER TABLE projects
            ADD COLUMN domain TEXT
            DEFAULT 'Other Development'
        """)

    if "allocation_category" not in project_columns:

        cursor.execute("""
            ALTER TABLE projects
            ADD COLUMN allocation_category TEXT
            DEFAULT 'Other'
        """)

    # =====================================================
    # CITIZEN REPORTS
    # =====================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS citizen_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER NOT NULL,
            citizen_name TEXT NOT NULL,
            issue_type TEXT NOT NULL,
            description TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (project_id)
            REFERENCES projects(id)
        )
    """)

    # =====================================================
    # AUDIT LOGS
    # =====================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT NOT NULL,
            user_role TEXT NOT NULL,
            action TEXT NOT NULL,
            project_id INTEGER,
            details TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # =====================================================
    # FIX / SYNC DEMO USERS
    # =====================================================

    sync_demo_users(cursor)

    # =====================================================
    # OLD OFFICIAL ID MIGRATION
    # =====================================================

    cursor.execute("""
        UPDATE users
        SET official_id = 'ADM-TG-001'
        WHERE LOWER(TRIM(email)) = 'admin@mplad.in'
    """)

    cursor.execute("""
        UPDATE users
        SET official_id = 'PO-TG-001'
        WHERE LOWER(TRIM(email)) = 'officer@mplad.in'
    """)

    cursor.execute("""
        UPDATE users
        SET official_id = NULL
        WHERE LOWER(TRIM(email)) = 'citizen@mplad.in'
    """)

    cursor.execute("""
        UPDATE users
        SET official_id = 'MP-TG-001'
        WHERE LOWER(TRIM(email)) = 'mp@mplad.in'
    """)

    cursor.execute("""
        UPDATE users
        SET official_id = 'MO-TG-001'
        WHERE LOWER(TRIM(email)) = 'auditor@mplad.in'
    """)

    # =====================================================
    # SEED / UPDATE 40 DEMO PROJECTS
    # =====================================================

    seed_demo_projects(cursor)

    conn.commit()
    conn.close()


# =========================================================
# GET USER BY EMAIL
# =========================================================

def get_user_by_email(email):
    """Get user by email."""

    if not email:
        return None

    email = email.strip().lower()

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM users
        WHERE LOWER(TRIM(email)) = ?
    """, (email,))

    row = cursor.fetchone()

    conn.close()

    if row is None:
        return None

    return dict(row)


# =========================================================
# GET USER BY OFFICIAL ID
# =========================================================

def get_user_by_official_id(official_id):
    """Get user by official ID."""

    if not official_id:
        return None

    official_id = official_id.strip().upper()

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM users
        WHERE UPPER(TRIM(official_id)) = ?
    """, (official_id,))

    row = cursor.fetchone()

    conn.close()

    if row is None:
        return None

    return dict(row)


# =========================================================
# GET USER BY ID
# =========================================================

def get_user_by_id(user_id):
    """Get user by ID."""

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM users
        WHERE id = ?
    """, (user_id,))

    row = cursor.fetchone()

    conn.close()

    if row is None:
        return None

    return dict(row)


# =========================================================
# ADD USER
# =========================================================

def add_user(
    name,
    email,
    password,
    role,
    constituency,
    official_id=None
):
    """Register a new user."""

    name = name.strip() if name else ""
    email = email.strip().lower() if email else ""
    constituency = constituency.strip() if constituency else ""

    if official_id:
        official_id = official_id.strip().upper()

    conn = get_db_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            INSERT INTO users
            (
                name,
                email,
                password,
                role,
                constituency,
                official_id
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            name,
            email,
            password,
            role,
            constituency,
            official_id
        ))

        conn.commit()

        user_id = cursor.lastrowid

        cursor.execute("""
            SELECT *
            FROM users
            WHERE id = ?
        """, (user_id,))

        row = cursor.fetchone()

        if row is None:
            return None

        return dict(row)

    except sqlite3.IntegrityError:

        return None

    finally:

        conn.close()


# =========================================================
# UPDATE USER PASSWORD
# =========================================================

def update_user_password(
    user_id,
    new_password
):
    """Update user's password."""

    conn = get_db_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            UPDATE users
            SET password = ?
            WHERE id = ?
        """, (
            new_password,
            user_id
        ))

        conn.commit()

        return cursor.rowcount > 0

    except sqlite3.Error:

        return False

    finally:

        conn.close()


# =========================================================
# ADD PROJECT
# =========================================================

def add_project(
    title,
    category,
    constituency,
    estimated_budget,
    timeline_months,
    actual_expenditure=0.0,
    actual_months=0,
    status="Proposed",
    anomaly_flag=0,
    anomaly_reason="",
    social_category="Other",
    domain="Other Development",
    allocation_category="Other"
):
    """Add a new MPLAD project."""

    conn = get_db_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            INSERT INTO projects
            (
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
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
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
        ))

        conn.commit()

        return cursor.lastrowid

    except sqlite3.Error:

        return None

    finally:

        conn.close()


# =========================================================
# GET ALL PROJECTS
# =========================================================

def get_all_projects():
    """Return all projects as dictionaries."""

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM projects
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]


# =========================================================
# GET PROJECT BY ID
# =========================================================

def get_project_by_id(project_id):
    """Return project by ID."""

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM projects
        WHERE id = ?
    """, (project_id,))

    row = cursor.fetchone()

    conn.close()

    if row is None:
        return None

    return dict(row)


# =========================================================
# GET PROJECTS BY CONSTITUENCY
# =========================================================

def get_projects_by_constituency(
    constituency
):
    """Return all projects belonging to a constituency."""

    if not constituency:
        return []

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM projects
        WHERE LOWER(TRIM(constituency))
              = LOWER(TRIM(?))
        ORDER BY id DESC
    """, (constituency,))

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]


# =========================================================
# GET ANOMALY PROJECTS BY CONSTITUENCY
# =========================================================

def get_anomaly_projects_by_constituency(
    constituency
):
    """Return anomaly projects for a constituency."""

    if not constituency:
        return []

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM projects
        WHERE LOWER(TRIM(constituency))
              = LOWER(TRIM(?))
          AND anomaly_flag = 1
        ORDER BY id DESC
    """, (constituency,))

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]


# =========================================================
# UPDATE PROJECT
# =========================================================

def update_project(
    project_id,
    actual_expenditure=None,
    actual_months=None,
    status=None,
    anomaly_flag=None,
    anomaly_reason=None
):
    """Update project information."""

    conn = get_db_connection()
    cursor = conn.cursor()

    try:

        fields = []
        values = []

        if actual_expenditure is not None:

            fields.append(
                "actual_expenditure = ?"
            )

            values.append(
                actual_expenditure
            )

        if actual_months is not None:

            fields.append(
                "actual_months = ?"
            )

            values.append(
                actual_months
            )

        if status is not None:

            fields.append(
                "status = ?"
            )

            values.append(
                status
            )

        if anomaly_flag is not None:

            fields.append(
                "anomaly_flag = ?"
            )

            values.append(
                anomaly_flag
            )

        if anomaly_reason is not None:

            fields.append(
                "anomaly_reason = ?"
            )

            values.append(
                anomaly_reason
            )

        if not fields:

            return False

        values.append(project_id)

        query = f"""
            UPDATE projects
            SET {", ".join(fields)}
            WHERE id = ?
        """

        cursor.execute(
            query,
            values
        )

        conn.commit()

        return cursor.rowcount > 0

    except sqlite3.Error:

        return False

    finally:

        conn.close()


# =========================================================
# ADD CITIZEN REPORT
# =========================================================

def add_citizen_report(
    project_id,
    citizen_name,
    issue_type,
    description
):
    """Add citizen complaint/report."""

    conn = get_db_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            INSERT INTO citizen_reports
            (
                project_id,
                citizen_name,
                issue_type,
                description
            )
            VALUES (?, ?, ?, ?)
        """, (
            project_id,
            citizen_name,
            issue_type,
            description
        ))

        conn.commit()

        return cursor.lastrowid

    except sqlite3.Error:

        return None

    finally:

        conn.close()


# =========================================================
# GET CITIZEN REPORTS
# =========================================================

def get_citizen_reports():
    """Return all citizen reports."""

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM citizen_reports
        ORDER BY created_at DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]


# =========================================================
# GET REPORTS FOR PROJECT
# =========================================================

def get_reports_by_project(
    project_id
):
    """Return citizen reports for a project."""

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM citizen_reports
        WHERE project_id = ?
        ORDER BY created_at DESC
    """, (project_id,))

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]


# =========================================================
# AUDIT LOG
# =========================================================

def log_action(
    user_name,
    user_role,
    action,
    project_id=None,
    details=""
):
    """Store user activity in audit log."""

    conn = get_db_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            INSERT INTO audit_logs
            (
                user_name,
                user_role,
                action,
                project_id,
                details
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            user_name,
            user_role,
            action,
            project_id,
            details
        ))

        conn.commit()

        return True

    except sqlite3.Error:

        return False

    finally:

        conn.close()


# =========================================================
# GET AUDIT LOGS
# =========================================================

def get_audit_logs():
    """Return all audit logs."""

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM audit_logs
        ORDER BY timestamp DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]

