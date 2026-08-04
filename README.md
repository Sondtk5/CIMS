# Continual Improvement Management System (CIMS) v1.0

[![Standard Compliance](https://img.shields.io/badge/Standards-ISO%209001%3A2015%20Clause%2010.3%20%7C%20IATF%2016949-blue.svg)](#)
[![Stack](https://img.shields.io/badge/Stack-FastAPI%20%7C%20React%20%7C%20Material--UI%20%7C%20ECharts-green.svg)](#)
[![Deployment](https://img.shields.io/badge/Deployment-Docker%20Compose-orange.svg)](#)

---

## 📌 Project Overview

**Continual Improvement Management System (CIMS)** is an enterprise web platform developed for the **TPM Department** to centrally manage, track, evaluate, and audit all Continuous Improvement (CI) projects. Designed in compliance with **ISO 9001:2015 Clause 10.3**, **IATF 16949**, **CAPA**, **PDCA**, and **DMAIC** standards, CIMS replaces manual Excel tracking with real-time KPI calculations, full audit traceability, horizontal deployment (Yokoten) tracking, and executive dashboards.

Target GitHub Repository: `https://github.com/Sondtk5/CIMS`

---

## ✨ Core Features

1. **Continual Improvement Master Dashboard**:
   - 9 Top KPI cards (Total CI, Complete, Running, Pending, On-time Rate, Effectiveness Rate, Avg Closing Time, Cost Saving, Horizontal Deployment).
   - Real-time KPI Performance table with status indicators (`Good`, `Close`, `Warning`).
   - Project Status Donut Chart & Project Category Donut Chart.
   - Monthly KPI Trend Line/Bar Chart (Jan–Dec).
   - 10-column CI Project Record table with interactive row pop-up editor.
   - Process Flow Diagram (PDCA & DMAIC stages).

2. **Interactive CI Project Workspace Pop-up Modal**:
   - Click any `CI No.` or **Edit** button to open the full interactive workspace modal.
   - **Tab 1: General Info & Request Form** (replicating `CI REQUEST FORM / CI 요청서`).
   - **Tab 2: DMAIC Project Report** (replicating `CI PROJECT REPORT / CI 프로젝트 보고서`).
   - **Tab 3: Root Cause Analysis** (interactive 5-Why tree and 4M1E Fishbone diagram).
   - **Tab 4: Verification & Cost Savings** (Before, Target, After metrics & QA PASS/FAIL verification).
   - **Tab 5: TPM Review & Approval**.
   - **Print Feature**: Dedicated **"Print Request Form"** and **"Print DMAIC Report"** buttons formatted for clean paper or PDF export.

3. **Admin Settings (KPI Target Configuration)**:
   - Configurable KPI target thresholds (e.g. On-Time Completion Rate Target $\ge 95\%$, Effectiveness Rate Target $\ge 90\%$, Avg Closing Time $< 60$ Days, Cost Saving Target $\ge \$50,000$, Yokoten Target $\ge 3$).
   - Dynamically updates dashboard thresholds and status evaluations across the entire system.

4. **ISO 9001 / IATF Immutable Audit Trail**:
   - Tracks all project additions, edits, deletions, QA verifications, and admin target adjustments with timestamp, user, role, old value, new value, and reason.

5. **Full Database Persistence**:
   - SQLite database backend retaining all changes permanently across restarts.

---

## 🚀 Single-Command Docker Desktop Launch

Run the system locally using Docker Desktop with a single command:

```bash
docker-compose up -d
```

- **Frontend Application**: `http://localhost:80`
- **FastAPI REST API & Swagger Docs**: `http://localhost:8000/docs`

---

## 🔑 Pre-Configured User Accounts & Roles

| Role | Username | Password | Access Rights |
| :--- | :--- | :--- | :--- |
| **Administrator** | `admin` | `password123` | Full Access (All CRUD, Admin Settings, Audit Trail) |
| **TPM Manager** | `manager` | `password123` | Create / Edit / Delete CI Projects & Approvals |
| **Engineer** | `engineer` | `password123` | Create / Edit own CI Projects & 5-Why / Actions |
| **QA Inspector** | `qa` | `password123` | Verify Effectiveness & PASS / FAIL status |
| **Management** | `management` | `password123` | Executive Dashboard & Reports Only |
| **Auditor** | `auditor` | `password123` | Read Only Audit Trail & Reports |

---

## 🛠️ GitHub Repository Push Instructions

To push this codebase to your GitHub repository (`https://github.com/Sondtk5/CIMS`):

```bash
# 1. Initialize git inside cims folder
git init

# 2. Add all project files
git add .

# 3. Commit initial release
git commit -m "feat: initial release of Continual Improvement Management System (CIMS) v1.0"

# 4. Set main branch & add remote
git branch -M main
git remote add origin https://github.com/Sondtk5/CIMS.git

# 5. Push code to GitHub
git push -u origin main
```

---

## 📂 Project Structure

```
cims/
├── docker-compose.yml          # Multi-container setup
├── README.md                   # System documentation & setup guide
├── .gitignore
├── backend/
│   ├── Dockerfile              # Python 3.11 slim backend image
│   ├── requirements.txt        # FastAPI, SQLAlchemy, PyJWT dependencies
│   └── app/
│       ├── main.py             # FastAPI entrypoint
│       ├── database.py         # SQLAlchemy connection
│       ├── seed.py             # Pre-populated demo projects & targets
│       ├── models/             # User, CIProject, KPITarget, CIAudit
│       ├── schemas/            # Pydantic schemas
│       ├── routers/            # Auth, Projects, Dashboard, Settings, Audit
│       └── services/           # KPI calculator engine & audit logger
└── frontend/
    ├── Dockerfile              # Multi-stage Nginx build image
    ├── nginx.conf              # Reverse proxy & static routing
    ├── package.json            # React, MUI v5, ECharts, Axios
    └── src/
        ├── App.jsx             # Main Router & Theme Provider
        ├── theme.js            # MUI Light/Dark mode styling
        ├── components/
        │   ├── Navbar.jsx      # Top Bar with UTI Logo & User Menu
        │   ├── Sidebar.jsx     # Navigation menu
        │   ├── CIEditModal.jsx # Pop-up modal for editing CI Projects
        │   ├── CIRequestFormPrintView.jsx # Printable Image 1 template
        │   └── CIReportPrintView.jsx      # Printable Image 2 template
        ├── pages/
        │   ├── MasterDashboard.jsx # Exact 8-section layout (Image 3)
        │   ├── ProjectRegister.jsx # List view with search/filter/sort
        │   ├── AdminSettings.jsx   # Admin KPI Target configuration
        │   ├── Reports.jsx         # Departmental summary reports
        │   ├── AuditLogs.jsx       # ISO/IATF Audit Trail
        │   └── Login.jsx           # JWT Login page with role buttons
        └── services/
            └── api.js          # Axios API client
```
