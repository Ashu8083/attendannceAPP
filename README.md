## RUNAMARGA HRMS APPLICATION

RUNAMARGA HRMS is a production-grade Software-as-a-Service (SaaS) Human Resource Management System designed to streamline employee management, attendance tracking, leave management, and payroll operations.

The application is built using Python, FastAPI, PostgreSQL, and Docker, following a scalable layered architecture to support enterprise-level deployment.

Key Features

* Employee management with secure authentication and authorization.
* Attendance management with AI-powered face verification for secure check-in and check-out.
* Leave management workflow with approval process.
* Payslip generation and payroll management.
* Email notification system for welcome emails, OTP verification, and other system notifications.
* JWT-based authentication with refresh token support.
* Role-Based Access Control (RBAC) for secure, permission-based access.
* RESTful APIs designed for scalability and maintainability.
* Containerized deployment using Docker for consistent development and production environments.

Technology Stack

* Backend: Python, FastAPI
* Database: PostgreSQL
* ORM: SQLAlchemy
* Database Migration: Alembic
* Authentication: JWT, Refresh Tokens, OTP Verification
* Email Service: SMTP-based Email Notifications
* AI/ML: Face Verification Model for Attendance
* Containerization: Docker


Local Development Setup

1. Create a Python Virtual Environment

Before running the project locally, create and activate a Python virtual environment.

Install virtualenv (Optional)

If venv is not available on your system, install virtualenv:

pip install virtualenv

Note: Python 3 includes the built-in venv module, so installing virtualenv is usually not required.

⸻

2. Create a Virtual Environment

Run the following command from the project directory:

python -m venv <venv_name>

Example:

python -m venv venv

⸻

3. Activate the Virtual Environment

Windows (Command Prompt)

<venv_name>\Scripts\activate

Windows (PowerShell)

<venv_name>\Scripts\Activate.ps1

macOS / Linux

source <venv_name>/bin/activate

After activation, your terminal prompt should display the virtual environment name:

(venv) user@machine project-folder %

⸻

Install Project Dependencies

All required Python packages are listed in the requirements.txt file located in the project’s root directory.

Install the dependencies using:

pip install -r requirements.txt

⸻

Verify Installation

To confirm that all packages have been installed successfully:

pip list

⸻

Deactivate the Virtual Environment

When you’re finished working, deactivate the virtual environment by running:

deactivate



# ==========================
# Database Configuration
# ==========================

DATABASE_URL=postgresql://<username>:<password>@<host>:<port>/<database_name>

# Example (Local PostgreSQL)
# DATABASE_URL=postgresql://postgres:root@host.docker.internal:5432/attendance_db

# Secret Key
SECRET_KEY=your_secret_key_here

# ==========================
# Email Configuration
# ==========================

MAIL_USERNAME=example@gmail.com
MAIL_PASSWORD=your_app_password

MAIL_FROM=example@gmail.com
MAIL_FROM_NAME=HRMS Attendance

MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587

MAIL_STARTTLS=True
MAIL_SSL_TLS=False

USE_CREDENTIALS=True
VALIDATE_CERTS=True

# ==========================
# PostgreSQL Configuration
# ==========================

DB_HOST=host.docker.internal
DB_PORT=5432
DB_NAME=attendance_db
DB_USER=postgres
DB_PASSWORD=root

# ==========================
# Redis Configuration
# ==========================

REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0




# for unit test use pytest 