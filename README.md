# MPLAD INSIGHT – Monitoring System

## 📌 Overview

**MPLAD INSIGHT** is a role-based monitoring and transparency system designed to support the monitoring of development projects implemented under the **Members of Parliament Local Area Development Scheme (MPLADS)**.

The system provides different dashboards and functionalities based on user roles such as **Citizen, MP, Project Officer, Monitoring Officer, and Administrator**. It helps monitor project budgets, expenditures, timelines, anomalies, citizen-reported defects, and project status through a centralized platform.

The main objective is to improve **project monitoring, transparency, accountability, and early identification of potential cost or timeline irregularities**.

---

## 🎯 Problem Statement

Monitoring development projects manually can make it difficult to:

* Track project progress efficiently
* Compare estimated budgets with actual expenditure
* Identify unusual cost or timeline variations
* Provide role-specific access to project information
* Allow citizens to report project-related issues
* Maintain records of monitoring and administrative actions
* Generate project reports for review

MPLAD INSIGHT addresses these challenges through a centralized, role-based monitoring system.

---

## 💡 Proposed Solution

MPLAD INSIGHT provides a unified platform where authorized users can monitor and manage development projects.

The system:

* Maintains project and user information in a centralized database
* Provides dashboards according to user roles
* Monitors estimated and actual expenditure
* Monitors planned and actual project timelines
* Detects potential anomalies using rule-based analysis
* Provides risk-level information for projects
* Allows citizens to submit defect reports
* Maintains audit logs of important actions
* Generates downloadable project reports
* Supports transparency and accountability through controlled access

---

## 👥 User Roles

### 1. Citizen

Citizens can:

* View projects associated with their constituency
* View project status and relevant public information
* Receive anomaly alerts for applicable projects
* Submit defect or issue reports related to projects

### 2. MP / MP Representative

MP-related users can:

* View projects associated with their constituency
* Monitor project budgets and expenditure
* View category-wise allocation information
* Review project progress
* View relevant project risk information
* Monitor recent actions related to projects

### 3. Project Officer

Project Officers can:

* Add development project proposals
* Update project information
* Manage project details across constituencies
* Record estimated budget and planned timeline
* Record actual expenditure and project duration
* Maintain project categories and allocation information

### 4. Monitoring Officer

Monitoring Officers can:

* Monitor projects across constituencies
* Analyze project expenditure and timeline variations
* Identify potential anomalies
* Review anomaly reasons and risk levels
* Take monitoring actions such as issuing notices or recommending fund-related actions
* Review project monitoring information

### 5. Administrator

Administrators can:

* Manage the overall system
* Access project information
* Monitor system activities
* Review anomaly information
* Access audit records
* Manage administrative actions

---

## 🔍 Key Features

### 🔐 Role-Based Authentication

Users log in according to their assigned role. Access to dashboards and operations is controlled based on permissions.

### 📊 Role-Based Dashboards

Each user receives a dashboard containing features relevant to their responsibilities.

### 💰 Budget & Expenditure Monitoring

The system compares:

* Estimated Budget
* Actual Expenditure

This helps identify projects where expenditure differs significantly from the planned amount.

### ⏱️ Timeline Monitoring

Project timelines are monitored using:

* Planned Timeline
* Actual Timeline

This helps identify projects with significant delays.

### 🚨 Anomaly Detection

The system evaluates project cost and timeline variations and identifies projects that may require additional monitoring.

The system can provide:

* Anomaly status
* Anomaly reason
* Risk level

### 📝 Citizen Defect Reporting

Citizens can submit reports regarding defects or issues observed in development projects.

### 📋 Audit Logging

Important system actions are recorded in audit logs to improve accountability and traceability.

### 📄 PDF Reports

Authorized users can generate and download project monitoring reports in PDF format according to their permissions.

---

## 🧠 Monitoring & Risk Analysis

MPLAD INSIGHT uses project information such as expenditure and timelines to support monitoring.

For example:

```text
Estimated Budget  →  Actual Expenditure
Planned Timeline  →  Actual Timeline
                         ↓
                 Monitoring Analysis
                         ↓
                Anomaly / Risk Result
```

The system categorizes project risk into:

* **Normal**
* **Moderate**
* **High**

The result is intended to support monitoring and human review rather than automatically making final administrative decisions.

---

## 🏗️ System Architecture

```text
                    MPLAD INSIGHT
                          │
                    User Login
                          │
                 Role-Based Access
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
     Citizen              MP          Project Officer
        │                 │                 │
        └─────────────────┼─────────────────┘
                          │
                Monitoring Officer
                          │
                    Administrator
                          │
                    Project Database
                          │
             ┌────────────┴────────────┐
             │                         │
      Monitoring Analysis         Audit Logs
             │
       Anomaly / Risk
             │
       Reports & Actions
```

---

## 🗄️ Database

The system uses **SQLite** as the database.

Major data entities include:

* Users
* Projects
* Citizen Reports
* Audit Logs

### Project Information

Project records can contain information such as:

* Project title
* Category
* Constituency
* Estimated budget
* Actual expenditure
* Planned timeline
* Actual timeline
* Project status
* Anomaly flag
* Anomaly reason
* Social category
* Domain
* Allocation category

---

## 🛠️ Technology Stack

| Component               | Technology          |
| ----------------------- | ------------------- |
| Frontend / UI           | Streamlit           |
| Programming Language    | Python              |
| Database                | SQLite              |
| Data Processing         | Python              |
| Monitoring Logic        | Rule-based Analysis |
| Reporting               | PDF Generation      |
| Development Environment | Visual Studio Code  |
| Version Control         | Git & GitHub        |

---

## 📁 Project Structure

```text
MPLAD-INSIGHT-Monitoring-System/
│
├── app.py
├── login.py
├── register.py
├── permissions.py
├── ml_engine.py
├── database.py
│
├── pages/
│   ├── home.py
│   ├── dashboard.py
│   └── profile.py
│
├── data/
│
├── reports/
│
├── mplad.db
│
├── requirements.txt
│
└── README.md
```

> The exact folder structure may vary depending on the latest project version.

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/MPLAD-INSIGHT-Monitoring-System.git
```

### 2. Open the Project

```bash
cd MPLAD-INSIGHT-Monitoring-System
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

For Windows:

```bash
venv\Scripts\activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the Application

```bash
streamlit run app.py
```

The application will open in the browser.

---

## 🔄 Application Workflow

```text
User Registration
       ↓
     Login
       ↓
Role Identification
       ↓
Role-Based Dashboard
       ↓
Project Monitoring
       ↓
Budget & Timeline Analysis
       ↓
Anomaly / Risk Identification
       ↓
Human Review & Monitoring Action
       ↓
Audit Logging
       ↓
Report Generation
```

---

## 🔒 Security & Access Control

The system implements role-based permissions so that users can access only the operations relevant to their assigned role.

Examples:

* Citizens receive public/project-related access.
* Project Officers manage project information.
* MPs can monitor projects relevant to their constituency.
* Monitoring Officers can perform monitoring and anomaly-related activities.
* Administrators have broader system-level access.

Passwords are stored using hashing rather than plain-text storage.

---

## 🌍 Real-World Use

MPLAD INSIGHT can support stakeholders involved in development-project monitoring by providing a centralized view of:

* Project progress
* Fund utilization
* Timeline performance
* Potential anomalies
* Citizen-reported issues
* Monitoring activities
* Project reports

The system can be extended to integrate with official government data sources and workflows for real-world deployment.

---

## 📈 Future Scope

Possible future enhancements include:

* Integration with official MPLADS data sources
* GIS/map-based project visualization
* Mobile application for field monitoring
* Photo/video-based project verification
* Automated notifications
* Advanced anomaly detection
* Integration with government authentication systems
* Real-time project progress updates
* Field officer inspection support
* Advanced analytics and visualization

---

## 👨‍💻 Team Project

**MPLAD INSIGHT – Monitoring System** is developed as a **group project** to demonstrate a role-based approach to development-project monitoring, transparency, and accountability.

### Team Members

Add your team members here:

```text
1. Your Name – Role / Contribution
2. Team Member 2 – Role / Contribution
3. Team Member 3 – Role / Contribution
4. Team Member 4 – Role / Contribution
```

---

## 📜 Disclaimer

MPLAD INSIGHT is an academic/project implementation developed for demonstrating the concept of role-based development-project monitoring.

It is not an official Government of India MPLADS application and should not be considered a replacement for official government systems or procedures.

---

## ⭐ Project Objective

> **To provide a centralized, role-based monitoring platform that improves visibility into development projects, supports early identification of potential irregularities, and promotes transparency and accountability through structured project information, monitoring, citizen reporting, and audit tracking.**
