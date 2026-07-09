from app.api.system_admin_api.organigastion_api import organisation_router
from app.api.system_admin_api.user_api import user_router
from app.api.organisation_admin_api.employee_api import employee_router
from app.api.organisation_user_api.attendance_api import  attendance_router
from app.api.organisation_user_api.employee_self_api import employee_self_router
from app.api.role_permission_apis.role_permission_api import permission_router
from app.api.organisation_admin_api.department_api import department_router
from app.api.auth_api import auth_router
from app.api.organisation_admin_api.attendance_relate_api import attendance_manager
from app.api.organisation_user_api.leave_related_api import leave_request_router

all_router = [
    organisation_router,
    user_router,
    employee_router,
    attendance_router,
    permission_router,
    department_router,
    auth_router,
    attendance_manager,
    employee_self_router,
    leave_request_router,
]


