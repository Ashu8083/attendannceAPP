"""
Master Seeder Script for Runamarga HRMS Attendance App.

Seeds default records for all database models:
- Permissions (System & Organisation level)
- System Roles (SYSTEM_ADMIN, SYSTEM_MANAGER, SYSTEM_ACCOUNTANT) & Role Permissions
- Default System Admin User (prompts for email or accepts --email CLI argument) & UserRole assignment
- Organisation & Subscription
- Branch, Shift, OrganisationCalendar, OrganisationWorkSchedule, Holidays
- Organisation Roles (ORGANISATION_ADMIN, HR_MANAGER, MANAGER, EMPLOYEE) & Role Permissions
- Default Organisation Admin User & Employee, EmployeeRoles assignment
- Department, Team, EmployeeDetails, EmployeeDocuments, EmployeeFaceModel
- LeaveRequest, Attendance, AttendanceEvidence, AttendanceLog
- UserDeviceDetails, TempOtpStorage, Token
"""

import sys
import uuid
import argparse
from datetime import date, time, datetime, timedelta

from sqlalchemy.orm import Session

# Database and models
from app.db.database import SessionLocal, Base, engine
from app.models import (
    Permission,
    SystemRoles,
    SystemRolePermissions,
    OrganisationRoles,
    OrganisationLevelRolePermissions,
    User,
    UserRole,
    Organisation,
    Subscription,
    Branch,
    Shift,
    OrganisationCalendar,
    OrganisationWorkSchedule,
    Holidays,
    Employee,
    EmployeeRoles,
    DepartmentModel,
    Team,
    EmployeeDetails,
    EmployeeDocuments,
    EmployeeFaceModel,
    LeaveRequest,
    Attendance,
    AttendanceEvidence,
    AttendanceLog,
    UserDeviceDetails,
    TempOtpStorage,
    Token,
)

# Enums
from app.enums.permission_scop import PermissionScopEnumUpdate
from app.enums.scops import AccountType
from app.enums.user_status_enums import UserStatus
from app.enums.organissation_status_enums import OrganizationStatus
from app.enums.subcription_type import (
    SubscriptionTypeORG,
    SubscriptionStatusORG,
    SubscriptionDuratioORG,
)
from app.enums.employee_status import EmployeeStatus
from app.enums.work_mode import WorkMode
from app.enums.departement_status import DepartmentStatusEnum
from app.enums.calender_enums import HolidayType, HolidayStatus
from app.enums.leave_status import LeaveStatus
from app.enums.attandance_status import AttendanceStatus, TypeAttendance


# ============================================================
# SEED DEFINITIONS
# ============================================================

SYSTEM_PERMISSIONS = [
    {"name": "system.all", "description": "Full access to all system-level administration", "scope": PermissionScopEnumUpdate.SYSTEM},
    {"name": "organisation.create", "description": "Create new organisations", "scope": PermissionScopEnumUpdate.SYSTEM},
    {"name": "organisation.view", "description": "View all organisations", "scope": PermissionScopEnumUpdate.SYSTEM},
    {"name": "organisation.update", "description": "Update organisation details", "scope": PermissionScopEnumUpdate.SYSTEM},
    {"name": "organisation.delete", "description": "Delete organisations", "scope": PermissionScopEnumUpdate.SYSTEM},
    {"name": "admin.manager", "description": "Manage organisation administrator accounts", "scope": PermissionScopEnumUpdate.SYSTEM},
    {"name": "system_role.create", "description": "Create system-level roles", "scope": PermissionScopEnumUpdate.SYSTEM},
    {"name": "system_role.view", "description": "View system-level roles", "scope": PermissionScopEnumUpdate.SYSTEM},
    {"name": "system_role.delete", "description": "Delete system-level roles", "scope": PermissionScopEnumUpdate.SYSTEM},
    {"name": "system_role.permission.assign", "description": "Assign permissions to system roles", "scope": PermissionScopEnumUpdate.SYSTEM},
    {"name": "system_role.permission.view", "description": "View system role permissions", "scope": PermissionScopEnumUpdate.SYSTEM},
    {"name": "permission.create", "description": "Create new system permissions", "scope": PermissionScopEnumUpdate.SYSTEM},
    {"name": "permission.view", "description": "View system permissions", "scope": PermissionScopEnumUpdate.SYSTEM},
    {"name": "subscription.manage", "description": "Manage organisation subscriptions", "scope": PermissionScopEnumUpdate.SYSTEM},
]

ORGANISATION_PERMISSIONS = [
    {"name": "organisation.admin", "description": "Full organisation level administration", "scope": PermissionScopEnumUpdate.ORGANIZATION},
    {"name": "employee.create", "description": "Create employee records", "scope": PermissionScopEnumUpdate.ORGANIZATION},
    {"name": "employee.view", "description": "View employee records", "scope": PermissionScopEnumUpdate.ORGANIZATION},
    {"name": "employee.update", "description": "Update employee details", "scope": PermissionScopEnumUpdate.ORGANIZATION},
    {"name": "employee.delete", "description": "Delete employee records", "scope": PermissionScopEnumUpdate.ORGANIZATION},
    {"name": "department.create", "description": "Create new departments", "scope": PermissionScopEnumUpdate.ORGANIZATION},
    {"name": "department.view", "description": "View department information", "scope": PermissionScopEnumUpdate.ORGANIZATION},
    {"name": "department.update", "description": "Update department details", "scope": PermissionScopEnumUpdate.ORGANIZATION},
    {"name": "department", "description": "General department management access", "scope": PermissionScopEnumUpdate.ORGANIZATION},
    {"name": "attendance.view", "description": "View attendance records", "scope": PermissionScopEnumUpdate.ORGANIZATION},
    {"name": "attendance.update", "description": "Update attendance records", "scope": PermissionScopEnumUpdate.ORGANIZATION},
    {"name": "attendance.punch", "description": "Punch self attendance in/out", "scope": PermissionScopEnumUpdate.ORGANIZATION},
    {"name": "leave.request.view", "description": "View leave request status", "scope": PermissionScopEnumUpdate.ORGANIZATION},
    {"name": "leave.self.request", "description": "Apply for self leave", "scope": PermissionScopEnumUpdate.ORGANIZATION},
    {"name": "leave.view", "description": "View organisation leave requests", "scope": PermissionScopEnumUpdate.ORGANIZATION},
    {"name": "leave.approve", "description": "Approve employee leave requests", "scope": PermissionScopEnumUpdate.ORGANIZATION},
    {"name": "leave.reject", "description": "Reject employee leave requests", "scope": PermissionScopEnumUpdate.ORGANIZATION},
    {"name": "leave.update", "description": "Update leave request details", "scope": PermissionScopEnumUpdate.ORGANIZATION},
    {"name": "role.manager", "description": "Manage organisation roles", "scope": PermissionScopEnumUpdate.ORGANIZATION},
    {"name": "role.view", "description": "View organisation roles", "scope": PermissionScopEnumUpdate.ORGANIZATION},
    {"name": "shift.manage", "description": "Manage shifts and work schedules", "scope": PermissionScopEnumUpdate.ORGANIZATION},
    {"name": "branch.manage", "description": "Manage organisation branches", "scope": PermissionScopEnumUpdate.ORGANIZATION},
]


# ============================================================
# MAIN SEEDER FUNCTION
# ============================================================

def seed_database(db: Session, sys_admin_email: str):
    """
    Executes full database seeding for all models.
    """
    print("=" * 60)
    print("Starting HRMS Database Master Seeder")
    print(f"System Admin Email: {sys_admin_email}")
    print("=" * 60)

    # ------------------------------------------------------------
    # 1. Seed Permissions
    # ------------------------------------------------------------
    print("\n[1/10] Seeding Permissions...")
    permission_map = {}
    all_perm_defs = SYSTEM_PERMISSIONS + ORGANISATION_PERMISSIONS

    for perm_data in all_perm_defs:
        perm = db.query(Permission).filter(Permission.name == perm_data["name"]).first()
        if not perm:
            perm = Permission(
                id=uuid.uuid4(),
                name=perm_data["name"],
                description=perm_data["description"],
                scope=perm_data["scope"],
                assignable=True,
            )
            db.add(perm)
            db.flush()
            print(f"  + Added Permission: {perm.name} ({perm.scope.value})")
        else:
            print(f"  . Found Permission: {perm.name}")
        permission_map[perm.name] = perm

    # ------------------------------------------------------------
    # 2. Seed System Roles & Permissions
    # ------------------------------------------------------------
    print("\n[2/10] Seeding System Roles & Role Permissions...")
    sys_roles_def = [
        {
            "role_name": "SYSTEM_ADMIN",
            "description": "Full access to system level administration",
            "perm_names": [p["name"] for p in SYSTEM_PERMISSIONS],
        },
        {
            "role_name": "SYSTEM_MANAGER",
            "description": "System level management of organisations and system users",
            "perm_names": [
                "organisation.create", "organisation.view", "organisation.update",
                "admin.manager", "system_role.view", "permission.view"
            ],
        },
        {
            "role_name": "SYSTEM_ACCOUNTANT",
            "description": "System level financial and subscription management",
            "perm_names": ["organisation.view", "subscription.manage"],
        },
    ]

    sys_role_map = {}
    for r_def in sys_roles_def:
        role = db.query(SystemRoles).filter(SystemRoles.role_name == r_def["role_name"]).first()
        if not role:
            role = SystemRoles(
                id=uuid.uuid4(),
                role_name=r_def["role_name"],
                description=r_def["description"],
            )
            db.add(role)
            db.flush()
            print(f"  + Added SystemRole: {role.role_name}")
        else:
            print(f"  . Found SystemRole: {role.role_name}")

        sys_role_map[role.role_name] = role

        # Map System Role Permissions
        for perm_name in r_def["perm_names"]:
            p_obj = permission_map.get(perm_name)
            if p_obj:
                srp = db.query(SystemRolePermissions).filter(
                    SystemRolePermissions.system_roles_id == role.id,
                    SystemRolePermissions.permission_id == p_obj.id,
                ).first()
                if not srp:
                    srp = SystemRolePermissions(
                        system_roles_id=role.id,
                        permission_id=p_obj.id,
                    )
                    db.add(srp)
                    print(f"    -> Mapped Permission '{perm_name}' to SystemRole '{role.role_name}'")

    # ------------------------------------------------------------
    # 3. Seed Default System Admin User & UserRole
    # ------------------------------------------------------------
    print("\n[3/10] Seeding System Admin User...")
    sys_admin_user = db.query(User).filter(User.email == sys_admin_email).first()
    if not sys_admin_user:
        sys_admin_user = User(
            id=uuid.uuid4(),
            full_name="System Super Admin",
            email=sys_admin_email,
            password_hash="pbkdf2:sha256:default_admin_hash",  # Default placeholder hash
            account_type=AccountType.SYSTEM,
            status=UserStatus.ACTIVE,
        )
        db.add(sys_admin_user)
        db.flush()
        print(f"  + Added System Admin User: {sys_admin_user.email}")
    else:
        print(f"  . Found System Admin User: {sys_admin_user.email}")

    # Assign SYSTEM_ADMIN role to System Admin User
    admin_sys_role = sys_role_map["SYSTEM_ADMIN"]
    user_role_entry = db.query(UserRole).filter(
        UserRole.user_id == sys_admin_user.id,
        UserRole.system_roles_id == admin_sys_role.id,
    ).first()
    if not user_role_entry:
        user_role_entry = UserRole(
            id=uuid.uuid4(),
            user_id=sys_admin_user.id,
            system_roles_id=admin_sys_role.id,
        )
        db.add(user_role_entry)
        print(f"  -> Assigned SYSTEM_ADMIN role to user {sys_admin_user.email}")

    # ------------------------------------------------------------
    # 4. Seed Organisation, Subscription, Branch, Shift, Calendar, Schedule, Holidays
    # ------------------------------------------------------------
    print("\n[4/10] Seeding Default Organisation & Structural Entities...")
    org_code = "ORG001"
    org_email = "admin@defaultorg.com"

    org = db.query(Organisation).filter(Organisation.organisation_code == org_code).first()
    if not org:
        org = Organisation(
            id=uuid.uuid4(),
            name="Default Organisation",
            organisation_code=org_code,
            organisation_email=org_email,
            status=OrganizationStatus.ACTIVE,
            address="123 Main Headquarters St",
            phone_number="+1234567890",
            latitude=28.6139,
            longitude=77.2090,
            allowed_radius=100,
            number_of_employee=1,
        )
        db.add(org)
        db.flush()
        print(f"  + Added Organisation: {org.name} ({org.organisation_code})")
    else:
        print(f"  . Found Organisation: {org.name}")

    # Subscription
    sub = db.query(Subscription).filter(Subscription.organisation_id == org.id).first()
    if not sub:
        sub = Subscription(
            id=uuid.uuid4(),
            subscription_type=SubscriptionTypeORG.PREMIMUM,
            organisation_id=org.id,
            starting_date=datetime.utcnow(),
            ending_date=datetime.utcnow() + timedelta(days=365),
            subscription_duration=SubscriptionDuratioORG.YEARLY,
            subscription_status=SubscriptionStatusORG.ACTIVE,
        )
        db.add(sub)
        print(f"  + Added Subscription: {sub.subscription_type.value} for {org.name}")
    else:
        print(f"  . Found Subscription for {org.name}")

    # Branch
    branch = db.query(Branch).filter(
        Branch.organisation_id == org.id,
        Branch.branch_name == "Main HQ Branch"
    ).first()
    if not branch:
        branch = Branch(
            id=uuid.uuid4(),
            branch_name="Main HQ Branch",
            organisation_id=org.id,
            address="123 Main Headquarters St",
            city="Metropolis",
            state="State",
            zip_code="100001",
            latitude=28.6139,
            longitude=77.2090,
            geofencing=100,
            grace_period=15,
            total_number_of_paid_leaves=12,
            is_verified=True,
            status=OrganizationStatus.ACTIVE,
        )
        db.add(branch)
        db.flush()
        print(f"  + Added Branch: {branch.branch_name}")
    else:
        print(f"  . Found Branch: {branch.branch_name}")

    # Shift
    shift = db.query(Shift).filter(
        Shift.organisation_id == org.id,
        Shift.name == "Morning Shift"
    ).first()
    if not shift:
        shift = Shift(
            name="Morning Shift",
            organisation_id=org.id,
            branch_id=branch.id,
            start_time=time(9, 0),
            end_time=time(17, 0),
            grace_minutes=15,
            break_time_minutes=60,
            break_type="LUNCH",
        )
        db.add(shift)
        db.flush()
        print(f"  + Added Shift: {shift.name}")
    else:
        print(f"  . Found Shift: {shift.name}")

    # Organisation Calendar
    cal = db.query(OrganisationCalendar).filter(
        OrganisationCalendar.organisation_id == org.id,
        OrganisationCalendar.name == "FY 2026-2027 Calendar"
    ).first()
    if not cal:
        cal = OrganisationCalendar(
            id=uuid.uuid4(),
            organisation_id=org.id,
            organisation_branch_id=branch.id,
            name="FY 2026-2027 Calendar",
            finance_year_start=date(2026, 4, 1),
            finance_year_end=date(2027, 3, 31),
            status="ACTIVE",
        )
        db.add(cal)
        db.flush()
        print(f"  + Added OrganisationCalendar: {cal.name}")
    else:
        print(f"  . Found OrganisationCalendar: {cal.name}")

    # Organisation Work Schedule (Mon-Fri)
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    for day in days_of_week:
        is_working = day not in ["Saturday", "Sunday"]
        ws = db.query(OrganisationWorkSchedule).filter(
            OrganisationWorkSchedule.calendar_id == cal.id,
            OrganisationWorkSchedule.day_of_week == day
        ).first()
        if not ws:
            ws = OrganisationWorkSchedule(
                id=uuid.uuid4(),
                calendar_id=cal.id,
                day_of_week=day,
                is_working_day=is_working,
            )
            db.add(ws)
            print(f"    -> Added WorkSchedule: {day} (Working={is_working})")

    # Holidays
    holiday = db.query(Holidays).filter(
        Holidays.organisation_calender_id == cal.id,
        Holidays.name == "Christmas Day"
    ).first()
    if not holiday:
        holiday = Holidays(
            id=uuid.uuid4(),
            organisation_calender_id=cal.id,
            holidays_date=date(2026, 12, 25),
            name="Christmas Day",
            description="Public Holiday",
            type_of_holiday=HolidayType.NATIONAL,
            status=HolidayStatus.ACTIVE,
        )
        db.add(holiday)
        print(f"  + Added Holiday: {holiday.name}")

    # ------------------------------------------------------------
    # 5. Seed Organisation Roles & Role Permissions
    # ------------------------------------------------------------
    print("\n[5/10] Seeding Organisation Roles & Role Permissions...")
    org_roles_def = [
        {
            "role_name": "ORGANISATION_ADMIN",
            "description": "Full administrative access to organisation resources",
            "perm_names": [p["name"] for p in ORGANISATION_PERMISSIONS],
        },
        {
            "role_name": "HR_MANAGER",
            "description": "HR management role for employees, leaves, attendance, and departments",
            "perm_names": [
                "employee.create", "employee.view", "employee.update", "employee.delete",
                "department.create", "department.view", "department.update", "department",
                "attendance.view", "attendance.update",
                "leave.view", "leave.approve", "leave.reject", "leave.update",
                "shift.manage", "branch.manage",
            ],
        },
        {
            "role_name": "MANAGER",
            "description": "Team lead/manager role for viewing team attendance and approving leaves",
            "perm_names": [
                "employee.view", "department.view",
                "attendance.view",
                "leave.view", "leave.approve", "leave.reject",
            ],
        },
        {
            "role_name": "EMPLOYEE",
            "description": "Standard employee role for self-service attendance and leave requests",
            "perm_names": [
                "attendance.punch", "leave.self.request", "leave.request.view", "employee.view"
            ],
        },
    ]

    org_role_map = {}
    for r_def in org_roles_def:
        org_role = db.query(OrganisationRoles).filter(
            OrganisationRoles.organisation_id == org.id,
            OrganisationRoles.role_name == r_def["role_name"]
        ).first()

        if not org_role:
            org_role = OrganisationRoles(
                id=uuid.uuid4(),
                role_name=r_def["role_name"],
                description=r_def["description"],
                organisation_id=org.id,
                branch_id=branch.id,
            )
            db.add(org_role)
            db.flush()
            print(f"  + Added OrganisationRole: {org_role.role_name}")
        else:
            print(f"  . Found OrganisationRole: {org_role.role_name}")

        org_role_map[org_role.role_name] = org_role

        # Map Organisation Role Permissions
        for perm_name in r_def["perm_names"]:
            p_obj = permission_map.get(perm_name)
            if p_obj:
                orp = db.query(OrganisationLevelRolePermissions).filter(
                    OrganisationLevelRolePermissions.organisation_role_id == org_role.id,
                    OrganisationLevelRolePermissions.permission_id == p_obj.id
                ).first()
                if not orp:
                    orp = OrganisationLevelRolePermissions(
                        organisation_role_id=org_role.id,
                        permission_id=p_obj.id,
                    )
                    db.add(orp)
                    print(f"    -> Mapped Permission '{perm_name}' to OrganisationRole '{org_role.role_name}'")

    # ------------------------------------------------------------
    # 6. Seed Organisation Admin User & Employee Record
    # ------------------------------------------------------------
    print("\n[6/10] Seeding Organisation Admin User & Employee...")
    org_admin_email = "admin@defaultorg.com"
    org_admin_user = db.query(User).filter(User.email == org_admin_email).first()
    if not org_admin_user:
        org_admin_user = User(
            id=uuid.uuid4(),
            organisation_id=org.id,
            full_name="Default Org Admin",
            email=org_admin_email,
            password_hash="pbkdf2:sha256:default_org_admin_hash",
            account_type=AccountType.ORGANISATION,
            status=UserStatus.ACTIVE,
        )
        db.add(org_admin_user)
        db.flush()
        print(f"  + Added Organisation Admin User: {org_admin_user.email}")
    else:
        print(f"  . Found Organisation Admin User: {org_admin_user.email}")

    # Employee record for Org Admin User
    employee = db.query(Employee).filter(
        Employee.organisation_id == org.id,
        Employee.employee_code == "EMP001"
    ).first()

    if not employee:
        employee = Employee(
            id=uuid.uuid4(),
            user_id=org_admin_user.id,
            organisation_id=org.id,
            employee_code="EMP001",
            department="Management",
            designation="Organisation Administrator",
            organisation_branch=branch.id,
            employee_status=EmployeeStatus.ACTIVE,
            shift_id=shift.id,
            join_date=date(2026, 1, 1),
            work_mode=WorkMode.WFO,
        )
        db.add(employee)
        db.flush()
        print(f"  + Added Employee: {employee.employee_code} ({employee.designation})")
    else:
        print(f"  . Found Employee: {employee.employee_code}")

    # Employee Role Assignment
    org_admin_role = org_role_map["ORGANISATION_ADMIN"]
    emp_role_entry = db.query(EmployeeRoles).filter(
        EmployeeRoles.employee_id == employee.id,
        EmployeeRoles.organisation_roles_id == org_admin_role.id
    ).first()

    if not emp_role_entry:
        emp_role_entry = EmployeeRoles(
            id=uuid.uuid4(),
            employee_id=employee.id,
            organisation_roles_id=org_admin_role.id,
        )
        db.add(emp_role_entry)
        print(f"  -> Assigned ORGANISATION_ADMIN role to Employee {employee.employee_code}")

    # ------------------------------------------------------------
    # 7. Seed Department & Team
    # ------------------------------------------------------------
    print("\n[7/10] Seeding Department & Team...")
    dept = db.query(DepartmentModel).filter(
        DepartmentModel.organisation_id == org.id,
        DepartmentModel.name == "Management"
    ).first()

    if not dept:
        dept = DepartmentModel(
            name="Management",
            department_head=employee.id,
            organisation_id=org.id,
            branch_id=branch.id,
            department_status=DepartmentStatusEnum.ACTIVATE,
        )
        db.add(dept)
        db.flush()
        print(f"  + Added Department: {dept.name}")
    else:
        print(f"  . Found Department: {dept.name}")

    team = db.query(Team).filter(
        Team.department_id == dept.id,
        Team.name == "Leadership Team"
    ).first()

    if not team:
        team = Team(
            id=uuid.uuid4(),
            department_id=dept.id,
            name="Leadership Team",
            team_head=employee.id,
            description="Executive Leadership Team",
            is_activated=True,
        )
        db.add(team)
        db.flush()
        print(f"  + Added Team: {team.name}")
    else:
        print(f"  . Found Team: {team.name}")

    # ------------------------------------------------------------
    # 8. Seed Employee Profile Data (Details, Documents, Face)
    # ------------------------------------------------------------
    print("\n[8/10] Seeding Employee Profile Data...")
    emp_details = db.query(EmployeeDetails).filter(EmployeeDetails.employee_id == employee.id).first()
    if not emp_details:
        emp_details = EmployeeDetails(
            id=uuid.uuid4(),
            employee_id=employee.id,
            employee_profile_image="uploads/employees/EMP001/profile.jpg",
            full_name="Default Org Admin",
            dob=date(1990, 1, 1),
            gender="MALE",
            marital_status="SINGLE",
            address="123 Main St",
            city="Metropolis",
            state="State",
        )
        db.add(emp_details)
        print(f"  + Added EmployeeDetails for {employee.employee_code}")
    else:
        print(f"  . Found EmployeeDetails for {employee.employee_code}")

    emp_docs = db.query(EmployeeDocuments).filter(EmployeeDocuments.employee_id == employee.id).first()
    if not emp_docs:
        emp_docs = EmployeeDocuments(
            id=uuid.uuid4(),
            employee_id=employee.id,
            photo_url="uploads/employees/EMP001/photo.jpg",
            aadhaar_document_url="uploads/employees/EMP001/aadhaar.pdf",
            pan_document_url="uploads/employees/EMP001/pan.pdf",
            resume_url="uploads/employees/EMP001/resume.pdf",
        )
        db.add(emp_docs)
        print(f"  + Added EmployeeDocuments for {employee.employee_code}")
    else:
        print(f"  . Found EmployeeDocuments for {employee.employee_code}")

    emp_face = db.query(EmployeeFaceModel).filter(EmployeeFaceModel.employee_id == employee.id).first()
    if not emp_face:
        emp_face = EmployeeFaceModel(
            id=uuid.uuid4(),
            employee_id=employee.id,
            embedding=[0.05] * 128,  # Sample dummy 128D embedding array
        )
        db.add(emp_face)
        print(f"  + Added EmployeeFaceModel for {employee.employee_code}")
    else:
        print(f"  . Found EmployeeFaceModel for {employee.employee_code}")

    # ------------------------------------------------------------
    # 9. Seed Security & Session Data (UserDeviceDetails, TempOtpStorage, Token)
    # ------------------------------------------------------------
    print("\n[9/10] Seeding User Device, OTP & Token Data...")
    device_id = uuid.uuid4()
    device = db.query(UserDeviceDetails).filter(UserDeviceDetails.user_id == sys_admin_user.id).first()
    if not device:
        device = UserDeviceDetails(
            id=device_id,
            user_id=sys_admin_user.id,
            device_type="WEB",
            device_unique_id=uuid.uuid4(),
            firebase_fcm_token="sample_fcm_token_super_admin",
            last_login=datetime.utcnow(),
            is_login=True,
        )
        db.add(device)
        db.flush()
        print(f"  + Added UserDeviceDetails for {sys_admin_user.email}")
    else:
        print(f"  . Found UserDeviceDetails for {sys_admin_user.email}")

    otp_entry = db.query(TempOtpStorage).filter(TempOtpStorage.user_id == sys_admin_user.id).first()
    if not otp_entry:
        otp_entry = TempOtpStorage(
            id=uuid.uuid4(),
            user_id=sys_admin_user.id,
            otp="123456",
            date=datetime.utcnow(),
            expire_time=time(23, 59),
            is_expired=False,
        )
        db.add(otp_entry)
        print(f"  + Added TempOtpStorage for {sys_admin_user.email}")

    token_entry = db.query(Token).filter(Token.user_id == sys_admin_user.id).first()
    if not token_entry:
        token_entry = Token(
            id=uuid.uuid4(),
            user_id=sys_admin_user.id,
            device_id=device.id,
            refresh_token="sample_refresh_token_string",
            is_revoked=False,
            expires_at=datetime.utcnow() + timedelta(days=7),
        )
        db.add(token_entry)
        print(f"  + Added Token for {sys_admin_user.email}")

    # ------------------------------------------------------------
    # 10. Seed Operational Data (Leave, Attendance, Logs)
    # ------------------------------------------------------------
    print("\n[10/10] Seeding Attendance & Leave Records...")
    leave_req = db.query(LeaveRequest).filter(
        LeaveRequest.employee_id == employee.id,
        LeaveRequest.reason == "Initial System Test Leave"
    ).first()

    if not leave_req:
        leave_req = LeaveRequest(
            id=uuid.uuid4(),
            employee_id=employee.id,
            organization_id=org.id,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=1),
            status=LeaveStatus.APPROVED,
            reason="Initial System Test Leave",
            approved_by=sys_admin_user.id,
            approved_at=datetime.utcnow(),
        )
        db.add(leave_req)
        print(f"  + Added LeaveRequest for {employee.employee_code}")
    else:
        print(f"  . Found LeaveRequest for {employee.employee_code}")

    today_date = date.today()
    att_rec = db.query(Attendance).filter(
        Attendance.employee_id == employee.id,
        Attendance.attendance_date == today_date
    ).first()

    if not att_rec:
        att_rec = Attendance(
            id=uuid.uuid4(),
            organisation_id=org.id,
            employee_id=employee.id,
            branches=branch.id,
            attendance_date=today_date,
            is_punchin=True,
            punchin_time=time(9, 0),
            is_punchout=True,
            punchout_time=time(17, 0),
            status=AttendanceStatus.PRESENT,
            work_mode=WorkMode.WFO,
        )
        db.add(att_rec)
        db.flush()
        print(f"  + Added Attendance Record for {employee.employee_code} on {today_date}")

        # Attendance Evidence
        ev_in = AttendanceEvidence(
            id=uuid.uuid4(),
            attendance_record_id=att_rec.id,
            face_match_score=0.96,
            type=TypeAttendance.CHECKIN,
            face_profile_url="organisations/001/attendance/checkin.jpg",
        )
        ev_out = AttendanceEvidence(
            id=uuid.uuid4(),
            attendance_record_id=att_rec.id,
            face_match_score=0.97,
            type=TypeAttendance.CHECKOUT,
            face_profile_url="organisations/001/attendance/checkout.jpg",
        )
        db.add(ev_in)
        db.add(ev_out)
        print("    -> Added CHECKIN & CHECKOUT AttendanceEvidence records")
    else:
        print(f"  . Found Attendance Record for {employee.employee_code}")

    att_log = db.query(AttendanceLog).filter(
        AttendanceLog.attendance_records_id == att_rec.id
    ).first()

    if not att_log:
        att_log = AttendanceLog(
            id=uuid.uuid4(),
            oranisation_id=org.id,
            attendance_records_id=att_rec.id,
            device_id=device.id,
            log="Punch-in log test record",
            is_success=True,
        )
        db.add(att_log)
        print(f"  + Added AttendanceLog for {employee.employee_code}")

    # ------------------------------------------------------------
    # Commit Transaction
    # ------------------------------------------------------------
    db.commit()
    print("\n" + "=" * 60)
    print("SUCCESS: Database master seeding completed successfully!")
    print(f"System Admin Email Configured : {sys_admin_user.email}")
    print(f"Default Organisation Code     : {org.organisation_code}")
    print(f"Default Employee Code         : {employee.employee_code}")
    print("=" * 60)


# ============================================================
# CLI ENTRY POINT
# ============================================================

def get_admin_email_from_user(cli_email: str | None = None) -> str:
    """
    Retrieves system admin email via argument, interactive prompt, or default fallback.
    """
    if cli_email and cli_email.strip():
        return cli_email.strip()

    default_email = "admin@system.com"
    if sys.stdin.isatty():
        try:
            user_input = input(f"Enter System Admin email address [default: {default_email}]: ").strip()
            if user_input:
                return user_input
        except (KeyboardInterrupt, EOFError):
            print("\nUsing default admin email.")

    return default_email


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seed initial model data for HRMS Attendance App.")
    parser.add_argument(
        "--email", "-e",
        type=str,
        help="Email address for default System Admin user (e.g. admin@system.com)",
    )

    args = parser.parse_args()
    admin_email = get_admin_email_from_user(args.email)

    db_session = SessionLocal()
    try:
        seed_database(db=db_session, sys_admin_email=admin_email)
    except Exception as err:
        db_session.rollback()
        print(f"\n❌ Error during database seeding: {err}", file=sys.stderr)
        raise
    finally:
        db_session.close()
