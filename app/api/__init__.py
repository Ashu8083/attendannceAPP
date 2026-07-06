from .organigastion_api import organisation_router
from app.api.user_api import user_router
from app.api.employee_api import employee_router
from app.api.attendance_api import  attendance_router
from app.api.role_permission_api import permission_router
from app.api.department_api import department_router
from app.api.auth_api import auth_router

all_router = [
    organisation_router,
    user_router,
    employee_router,
    attendance_router,
    permission_router,
    department_router,
    auth_router,

]


