# RUNAMARGA HRMS APPLICATION

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.138.0-009688.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-336791.svg)](https://www.postgresql.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-red.svg)](https://www.sqlalchemy.org/)
[![Docker](https://img.shields.io/badge/Docker-Supported-blue.svg)](https://www.docker.com/)

**RUNAMARGA HRMS** is a production-grade, Software-as-a-Service (SaaS) Multi-Tenant Human Resource Management System backend built with Python and FastAPI. It provides comprehensive APIs to streamline employee lifecycle management, attendance tracking with geofencing, leave workflows, role-based access control (RBAC), subscription management, and email notifications.

---

## 🌟 Key Features

* **Multi-Tenant Architecture**: Supports multiple organizations with isolated tenant data, custom departments, shifts, and subscription plans.
* **Authentication & Authorization**: Secure JWT-based authentication with refresh tokens, OTP email verification, and password hashing (`bcrypt`/`passlib`).
* **Granular Role-Based Access Control (RBAC)**: Flexible role and permission management supporting System Admins, Organization Admins, and Organization Employees/Users.
* **Attendance Management**: Check-in and check-out tracking, geofencing location calculations, attendance logs, and manager approval workflows.
* **Leave Management**: Complete leave request application lifecycle (Submit, Approve, Reject, Status tracking).
* **Employee & Department Management**: Employee onboarding, department assignment, shift scheduling, and device registration tracking.
* **Email Notification System**: Asynchronous SMTP notification service using `fastapi-mail` for welcome messages, OTPs, and leave status updates.
* **Database Migrations**: Version-controlled database schema migrations managed by **Alembic**.
* **Containerized Setup**: Ready-to-use Docker and Docker Compose environment with integrated Redis caching.

---

## 🛠️ Technology Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Framework** | [FastAPI](https://fastapi.tiangolo.com/) | High-performance asynchronous web framework |
| **Language** | [Python 3.11](https://www.python.org/) | Core programming language |
| **Database** | [PostgreSQL](https://www.postgresql.org/) | Relational database for persistent storage |
| **ORM** | [SQLAlchemy 2.0](https://www.sqlalchemy.org/) | Database ORM and relational mapping |
| **Migrations** | [Alembic](https://alembic.sqlalchemy.org/) | Schema migration management |
| **Caching / Storage** | [Redis](https://redis.io/) | In-memory cache & temporary session/OTP storage |
| **Task Queue** | [Celery](https://docs.celeryq.dev/) | Asynchronous background task execution |
| **Security** | PyJWT / Passlib / Bcrypt | JWT verification, hashing, and token handling |
| **Email Service** | FastAPI-Mail / SMTP | Async email generation & templating |
| **Containerization** | Docker & Docker Compose | Container orchestration for development & production |
| **Testing** | [Pytest](https://docs.pytest.org/) | Unit and integration test suite |

---

## 🏗️ Project Architecture & File Structure

The project follows a **Layered Architecture** adhering to the **Repository Pattern** and **Dependency Injection** principles. This ensures clear separation of concerns (API routes -> Services -> Repositories -> Models/DB).

```
attendannceAPP/
├── .env                      # Local environment variable configuration
├── .gitignore                # Git untracked files configuration
├── Dockerfile                # Docker image build instructions for FastAPI app
├── compose.yaml              # Docker Compose configuration for Web & Redis services
├── alembic.ini               # Alembic database migration configuration
├── main.py                   # Application entrypoint (FastAPI initialization, middleware, routes, exception handlers)
├── requirements.txt          # Python project dependencies
├── README.md                 # Project documentation
│
├── app/                      # Application core source code
│   ├── api/                  # API Controllers / Routes layer
│   │   ├── __init__.py                           # Central router aggregator (`all_router`)
│   │   ├── auth_api.py                           # User login, registration, OTP verification & refresh tokens
│   │   ├── testemailrouter.py                    # Utility endpoint for testing email sending
│   │   ├── organisation_admin_api/               # Routes for Organization Admins
│   │   │   ├── attendance_relate_api.py          # Admin attendance overview & adjustments
│   │   │   ├── department_api.py                 # Department CRUD operations
│   │   │   ├── employee_api.py                   # Employee management & onboarding
│   │   │   ├── leave_request_api.py              # Leave request approval/rejection workflows
│   │   │   ├── organisation_role_management.py   # Org role & permission management
│   │   │   └── shift_api.py                      # Work shift creation & assignments
│   │   │
│   │   ├── organisation_user_api/                # Routes for Employees / End Users
│   │   │   ├── attendance_api.py                 # Self check-in, check-out, and attendance history
│   │   │   ├── employee_self_api.py              # Employee self-profile retrieval & updates
│   │   │   └── leave_related_api.py              # Apply for leave & view personal leave status
│   │   │
│   │   ├── role_permission_apis/                 # Dynamic role-permission mapping endpoints
│   │   │   └── role_permission_api.py
│   │   │
│   │   └── system_admin_api/                     # Platform-wide System Admin routes
│   │       ├── employee_API.py                   # System employee management
│   │       ├── organigastion_api.py              # Organization tenant registration & management
│   │       ├── organisation_admin_manager.py     # Organization admin user assignment
│   │       ├── subscription_manager_api.py       # Plan & subscription administration
│   │       ├── system_role_permission_api.py     # System role definitions & permissions
│   │       └── user_api.py                       # Global user management
│   │
│   ├── auth/                 # Credentials checking, token inspection, and auth helpers
│   ├── core/                 # Global configuration (`config.py`), logging setup, OTP generator, request contexts
│   ├── db/                   # Database engine setup (`database.py`), SQLAlchemy Base, Unit of Work (`UnitOfWork.py`)
│   ├── dependancy/           # FastAPI dependency providers (service injection, permission check dependencies)
│   ├── email/                # Email utilities (`fastapi-mail` client, HTML templates, background email sender)
│   ├── enums/                # System Enumerations (Employee Status, Attendance Status, Leave Status, Roles, Gender, etc.)
│   ├── exceptions/           # Custom application exceptions and FastAPI global exception handlers
│   ├── helperFunction/       # Utility helpers (Geofencing distance calculations, date/time formatters)
│   ├── middleware/           # Middleware definitions (`AuthMiddleware` for inspecting JWT request headers)
│   ├── models/               # SQLAlchemy ORM Models / Database Schemas
│   │   ├── attendance_record_model.py            # Attendance check-in/out records
│   │   ├── department_model.py                   # Department definitions
│   │   ├── employee_models.py                    # Employee profiles & metadata
│   │   ├── leave_record_model.py                 # Leave requests & status records
│   │   ├── organisation_role.py                  # Roles within an organization
│   │   ├── organisations.py                      # Tenant Organization details
│   │   ├── subcription_model.py                  # Organization subscription plans
│   │   ├── user_models.py                        # System User accounts
│   │   └── ...                                   # Role, Permission, Device & OTP storage models
│   │
│   ├── redis_config/         # Redis connection client setup (`redis.py`)
│   ├── repo/                 # Data Access Repositories (Database query execution layer)
│   ├── schemas/              # Pydantic Schemas for API payload validation & response serialization
│   ├── security/             # Password hashing (`passlib`/`bcrypt`) & JWT token generation/decoding
│   ├── service/              # Business Logic Services (Auth, Attendance, Leave, Employee, Department services)
│   └── test/                 # Pytest automated test scripts & test suite
│
└── migrations/               # Database Schema Migrations (Alembic)
    ├── env.py                # Alembic migration environment script
    ├── script.py.mako        # Migration script template
    └── versions/             # Individual database migration revision scripts
```

---

## ⚙️ Configuration & Environment Variables

Create a `.env` file in the project root directory (you can base it on `.env.example` or the template below):

```env
# ==================================
# Database Configuration (PostgreSQL)
# ==================================
DATABASE_URL=postgresql://postgres:root@localhost:5432/attendance_db

# Alternative for Docker deployment:
# DATABASE_URL=postgresql://postgres:root@host.docker.internal:5432/attendance_db

DB_HOST=localhost
DB_PORT=5432
DB_NAME=attendance_db
DB_USER=postgres
DB_PASSWORD=root

# ==================================
# JWT Security Configuration
# ==================================
SECRET_KEY=your_super_secret_jwt_key_here

# ==================================
# Email Configuration (SMTP)
# ==================================
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_smtp_app_password
MAIL_FROM=your_email@gmail.com
MAIL_FROM_NAME=HRMS Attendance
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=465
MAIL_STARTTLS=False
MAIL_SSL_TLS=True
USE_CREDENTIALS=True
VALIDATE_CERTS=True

# ==================================
# Redis Configuration
# ==================================
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
```

---

## 🚀 How to Start the Application

### Option 1: Local Development Setup

#### 1. Prerequisites
Ensure you have the following installed on your machine:
* **Python 3.11+**
* **PostgreSQL** (running locally on port `5432` with a database named `attendance_db`)
* **Redis** (running locally on port `6379`)

#### 2. Clone & Navigate to Project Directory
```bash
cd attendannceAPP
```

#### 3. Create & Activate Virtual Environment

* **macOS / Linux**:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

* **Windows (Command Prompt)**:
  ```cmd
  python -m venv venv
  venv\Scripts\activate
  ```

* **Windows (PowerShell)**:
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```

#### 4. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 5. Run Database Migrations (Alembic)
Ensure PostgreSQL is running and your `.env` database parameters are correct, then run:
```bash
alembic upgrade head
```

#### 6. Start the FastAPI Development Server
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
The server will start at **`http://localhost:8000`**.

---

### Option 2: Running with Docker & Docker Compose

If you prefer containerized deployment with Docker:

#### 1. Prerequisites
* **Docker Engine** & **Docker Compose** installed.

#### 2. Start Services
Run the following command in the project root directory:
```bash
docker compose up --build
```

This will build the FastAPI application container (`web`) and launch a Redis cache container (`redis`).

To run containers in background (detached mode):
```bash
docker compose up -d
```

To stop the containers:
```bash
docker compose down
```

---

## 📖 API Documentation & Swagger UI

Once the application is running, you can access interactive documentation directly in your browser:

* **Swagger UI (Interactive Docs)**: [http://localhost:8000/docs](http://localhost:8000/docs)
* **ReDoc (Alternative Docs)**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Summary of Primary Endpoints

| Group | Method | Path | Description |
| :--- | :--- | :--- | :--- |
| **General** | `GET` | `/` | Health check endpoint |
| **Auth** | `POST` | `/auth/login` | User authentication & JWT token generation |
| **Auth** | `POST` | `/auth/verify-otp` | Verify OTP code |
| **Attendance** | `POST` | `/attendance/check-in` | Employee check-in with location verification |
| **Attendance** | `POST` | `/attendance/check-out` | Employee check-out |
| **Leave** | `POST` | `/leave/apply` | Apply for leave |
| **Leave** | `GET` | `/leave/my-requests` | Retrieve personal leave requests |
| **Admin** | `GET` | `/org-admin/employees` | Retrieve employee roster |
| **Admin** | `POST` | `/org-admin/department` | Create new department |
| **System Admin** | `POST` | `/system-admin/organisation` | Register new tenant organisation |

---

## 🧪 Running Automated Tests

Tests are located in the `app/test/` directory.

To execute the test suite using **Pytest**:
```bash
pytest
```

To run tests with detailed output:
```bash
pytest -v
```

---

## 📄 License & Maintainers

Developed as part of the **RUNAMARGA HRMS Ecosystem**.
For questions or support, contact the system administrator or development team.