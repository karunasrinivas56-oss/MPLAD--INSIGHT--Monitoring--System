"""
MPLAD INSIGHT - Authentication Module
Handles:
- Password hashing
- Registration
- Login
- Official ID validation
- Current user session
- Logout
- Password reset
"""

import hashlib
import streamlit as st

from backend.database import (
    get_user_by_email,
    get_user_by_official_id,
    add_user,
    get_user_by_id,
    update_user_password,
)


# ============================================================
# OFFICIAL ROLE PREFIXES
# ============================================================

OFFICIAL_ROLE_PREFIXES = {
    "Administrator": "ADM",
    "Project Officer": "PO",
    "MP Representative": "MP",
    "Monitoring Officer": "MO",
}


VALID_ROLES = [
    "Citizen",
    "Project Officer",
    "MP Representative",
    "Monitoring Officer",
    "Administrator",
]


# ============================================================
# PASSWORD FUNCTIONS
# ============================================================

def hash_password(password: str) -> str:
    """Hash password using SHA-256."""
    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


def check_password(password: str, hashed_password: str) -> bool:
    """Check entered password against stored hash."""
    return hash_password(password) == hashed_password


# ============================================================
# OFFICIAL ID VALIDATION
# ============================================================

def validate_official_id(
    official_id: str,
    role: str
) -> tuple[bool, str]:

    # --------------------------------------------------------
    # CITIZEN DOES NOT NEED OFFICIAL ID
    # --------------------------------------------------------

    if role == "Citizen":

        if official_id:
            return (
                False,
                "Citizen accounts must not have an Official ID."
            )

        return True, "Valid Citizen account"


    # --------------------------------------------------------
    # OFFICIAL ROLES REQUIRE OFFICIAL ID
    # --------------------------------------------------------

    if role not in OFFICIAL_ROLE_PREFIXES:
        return False, "Invalid role selected."


    if not official_id:
        return (
            False,
            f"Official ID is required for {role}."
        )


    official_id = official_id.strip().upper()

    expected_prefix = OFFICIAL_ROLE_PREFIXES[role]

    # Example:
    # PO-TG-001
    # MP-TG-001
    # MO-TG-001
    # ADM-TG-001

    if not official_id.startswith(
        expected_prefix + "-"
    ):
        return (
            False,
            f"Invalid Official ID for {role}. "
            f"It must start with {expected_prefix}-"
        )


    parts = official_id.split("-")

    if len(parts) != 3:
        return (
            False,
            "Invalid Official ID format. "
            "Example: PO-TG-001"
        )


    if not parts[1]:
        return False, "State code is required."


    if not parts[2].isdigit():
        return (
            False,
            "Official ID number must contain digits."
        )


    return True, "Valid Official ID"


# ============================================================
# REGISTER
# ============================================================

def register(
    name: str,
    email: str,
    password: str,
    role: str,
    constituency: str,
    official_id: str | None = None,
) -> tuple[bool, str]:

    name = name.strip()
    email = email.strip().lower()
    password = password.strip()
    constituency = constituency.strip()

    # --------------------------------------------------------
    # BASIC VALIDATION
    # --------------------------------------------------------

    if not name:
        return False, "Name is required."

    if not email:
        return False, "Email is required."

    if not password:
        return False, "Password is required."

    if role not in VALID_ROLES:
        return False, "Invalid role selected."

    if not constituency:
        return False, "Constituency is required."


    # --------------------------------------------------------
    # EMAIL DUPLICATE CHECK
    # --------------------------------------------------------

    existing_email_user = get_user_by_email(email)

    if existing_email_user:
        return False, "Email is already registered."


    # --------------------------------------------------------
    # CITIZEN
    # --------------------------------------------------------

    if role == "Citizen":

        # Citizen MUST NOT have Official ID.
        official_id = None

        is_valid, message = validate_official_id(
            official_id,
            role
        )

        if not is_valid:
            return False, message


    # --------------------------------------------------------
    # OFFICIAL ROLES
    # --------------------------------------------------------

    else:

        if official_id:
            official_id = official_id.strip().upper()

        is_valid, message = validate_official_id(
            official_id,
            role
        )

        if not is_valid:
            return False, message


        # ----------------------------------------------------
        # OFFICIAL ID DUPLICATE CHECK
        # ----------------------------------------------------

        existing_official_user = get_user_by_official_id(
            official_id
        )

        if existing_official_user:
            return (
                False,
                "Official ID is already registered."
            )


    # --------------------------------------------------------
    # HASH PASSWORD
    # --------------------------------------------------------

    hashed_password = hash_password(password)


    # --------------------------------------------------------
    # CREATE USER
    # --------------------------------------------------------

    user = add_user(
        name=name,
        email=email,
        password=hashed_password,
        role=role,
        constituency=constituency,
        official_id=official_id,
    )


    if user is None:
        return (
            False,
            "Registration failed. Please try again."
        )


    return True, "Registration successful."


# ============================================================
# LOGIN
# ============================================================

def login(
    email: str,
    password: str
) -> tuple[bool, str]:

    email = email.strip().lower()

    # --------------------------------------------------------
    # BASIC VALIDATION
    # --------------------------------------------------------

    if not email or not password:
        return (
            False,
            "Please enter email and password."
        )


    # --------------------------------------------------------
    # FIND USER BY EMAIL
    #
    # IMPORTANT:
    # Email is ONLY used to find the DB user.
    # Role is NEVER decided from email.
    # --------------------------------------------------------

    user = get_user_by_email(email)

    if user is None:
        return (
            False,
            "Email is not registered."
        )


    # --------------------------------------------------------
    # PASSWORD CHECK
    # --------------------------------------------------------

    if not check_password(
        password,
        user["password"]
    ):
        return (
            False,
            "Incorrect password."
        )


    # --------------------------------------------------------
    # GET ROLE FROM DATABASE
    # --------------------------------------------------------

    role = user.get("role")

    official_id = user.get("official_id")


    # --------------------------------------------------------
    # CITIZEN RULE
    # --------------------------------------------------------

    if role == "Citizen":

        # Citizen must NEVER have Official ID.
        official_id = None


    # --------------------------------------------------------
    # OFFICIAL ROLE RULE
    # --------------------------------------------------------

    elif role in OFFICIAL_ROLE_PREFIXES:

        if not official_id:
            return (
                False,
                "Official ID is missing for this official account."
            )

        official_id = official_id.strip().upper()

        is_valid, message = validate_official_id(
            official_id,
            role
        )

        if not is_valid:
            return False, message


    else:

        return (
            False,
            "Invalid role assigned to this account."
        )


    # --------------------------------------------------------
    # IMPORTANT:
    # FETCH FRESH USER FROM DATABASE
    #
    # This prevents stale role/details in session.
    # --------------------------------------------------------

    fresh_user = get_user_by_id(
        user["id"]
    )

    if fresh_user is None:
        return (
            False,
            "User account could not be loaded."
        )


    # --------------------------------------------------------
    # SESSION STATE
    # --------------------------------------------------------

    st.session_state["authenticated"] = True

    st.session_state["user_id"] = fresh_user["id"]

    st.session_state["user"] = fresh_user

    st.session_state["role"] = fresh_user.get(
        "role"
    )

    st.session_state["constituency"] = fresh_user.get(
        "constituency"
    )


    # --------------------------------------------------------
    # OFFICIAL ID
    # --------------------------------------------------------

    if fresh_user.get("role") == "Citizen":

        st.session_state["official_id"] = None

    else:

        st.session_state["official_id"] = (
            fresh_user.get("official_id")
        )


    return True, "Login successful."


# ============================================================
# GET CURRENT USER
# ============================================================

def get_current_user():

    user_id = st.session_state.get(
        "user_id"
    )

    if not user_id:
        return None


    # Always get latest data from database.
    user = get_user_by_id(user_id)


    if user is None:
        return None


    # --------------------------------------------------------
    # Keep session synchronized with DB
    # --------------------------------------------------------

    st.session_state["user"] = user

    st.session_state["role"] = user.get(
        "role"
    )

    st.session_state["constituency"] = user.get(
        "constituency"
    )


    if user.get("role") == "Citizen":

        st.session_state["official_id"] = None

    else:

        st.session_state["official_id"] = (
            user.get("official_id")
        )


    return user


# ============================================================
# LOGOUT
# ============================================================

def logout():

    session_keys = [
        "authenticated",
        "user_id",
        "user",
        "role",
        "official_id",
        "constituency",
    ]

    for key in session_keys:

        st.session_state.pop(
            key,
            None
        )


# ============================================================
# RESET PASSWORD
# ============================================================

def reset_password(
    email: str,
    new_password: str
) -> tuple[bool, str]:

    email = email.strip().lower()
    new_password = new_password.strip()


    if not email:
        return False, "Email is required."


    if not new_password:
        return False, "New password is required."


    user = get_user_by_email(email)

    if user is None:
        return (
            False,
            "Email is not registered."
        )


    hashed_password = hash_password(
        new_password
    )


    success = update_user_password(
        user["id"],
        hashed_password
    )


    if not success:
        return (
            False,
            "Password update failed."
        )


    return True, "Password updated successfully."