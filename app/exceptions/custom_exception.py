from app.exceptions.exception import AppException
from app.models import Employee
from app.core.logging_config import logger
from app.schemas import organisation_schema


class OraganisationNotFound(AppException):
    def __init__(self,organisation_code : str | None):
        message =( f"Oraganisation Not Found with {organisation_code}"
                   if  organisation_code
                   else "Oraganisation Not Found"
                   )

        super().__init__(
            message= message,
            status_code= 404,
            error_code= "ORGANISATION_NOT_FOUND"
        )


class OrganisationAlreadyExists(AppException):
    def __init__(self,organisation_code : str | None):
        messsage =( f"Organisation Already Exists with {organisation_code}"
                    if organisation_code
                    else "Organisation Already Exists"
                    )
        super().__init__(
            message= messsage,
            status_code= 409,
            error_code= "ORGANISATION_ALREADY_EXIST"
        )

class UserNotFound(AppException):
    def __init__(self, user_identi : str | None = None):
        message = (
            f"User with email '{user_identi}' not found"
            if user_identi
            else "User not found"
        )

        super().__init__(
            message=message,
            status_code=404,
            error_code="USER_NOT_FOUND"
        )
class EmailAlreadyExists(AppException):
    def __init__(self):
        super().__init__(
            message= "User with this Email Already Exist",
            status_code=409,
            error_code="EMAIL_ALREADY_EXISTS"
        )



# Employee Related Exception

class EmployeeNotFound(AppException):
    def __init__(self):
        super().__init__(
            message= "Employee Not Found with employeeCode",
            status_code=404,
            error_code="EMPLOYEE_NOT_FOUND"
        )

class EmployeeAlreadyExists(AppException):
    def __init__(self):
        super().__init__(
            message= "Employee Already Exists",
            status_code= 409,
            error_code = "EMPLOYEE_ALREADY_EXISTS"
        )

class EmployeeIsInactive(AppException):
    def __init__(self):
        super().__init__(
            message= "Employee Inactivate",
            status_code= 409,
            error_code = "EMPLOYEE_IS_INACTIVE"
        )




#Attendance Related Exception

class AttendanceNotFound(AppException):
    def __init__(self):
        super().__init__(
            message="",
            status_code=404,
            error_code="ATTENDANCE_NOT_FOUND",
        )

class TodayAttendanceAlreadyTaken(AppException):
    def __init__(self):
        super().__init__(
            message= "Your Attendance Already Taken",
            status_code=409,
            error_code= "ATTENDANCE_ALREDY_TAKEN"
        )
class AttendanceRecordNotFound(AppException):
    def __init__(self):
        super().__init__(
            message= "Attendance Record not Found",
            status_code= 404,
            error_code= "NOT_ATTENDANCE_RECORD_NOT_FOUND"
        )

class AlreadyPunchIN(AppException):
    def __init__(self):
        super().__init__(
            message= "Employee Already PunchIn",
            status_code= 409,
            error_code= "ALREADY_PUNCH_IN"
        )
class AlreadyPunchOut(AppException):
    def __init__(self):
        super().__init__(
            message= " Employee Already PunchOut",
            status_code= 409,
            error_code= "ALREADY_PUNCH_OUT"
        )
class NotPunchIn(AppException):
    def __init__(self):
        super().__init__(
            message= "Employee Punch IN Not Found",
            status_code= 404,
            error_code= "NOT_PUNCH_IN"
        )


#Location Error

class EmployeeNotInOfficePermises(AppException):
    def __init__(self):
        super().__init__(
        )



class OtpInValid(AppException):
    def __init__(self):
        super().__init__(
            message= "Invalid OTP or expired",
            status_code= 401,
            error_code= "OTP_INVALID"
        )

class TokenInValid(AppException):
    def __init__(self):
        super().__init__(
            message= "Invalid Token ",
            status_code= 403
        )
class AccessTokenExpired(AppException):
    def __init__(self):
        super().__init__(
            message= "token expired or not found",
            status_code= 403,
        )
class MissingToken(AppException):
    def __init__(self):
        super().__init__(
            message= "Token missing  ",
            status_code= 401,
            error_code= "MISSING_BARRER_TOKEN"
        )
class MissingAuthorizationHeader(AppException):
    def __init__(self):
        super().__init__(
            message= "Missing Authorization header",
            status_code= 401,
            error_code="MISSING_AUTHORIZATION_HEADER"
        )


class PermissionDenied(AppException):
    def __init__(self):
        super().__init__(
            message= "permission denied",
            status_code= 403,
            error_code= "Forbidden"

        )
class PermissionAlreadyExist(AppException):
    def __init__(self):
        super().__init__(
            message="Permission Aleardy Exist",
            status_code= 409,
            error_code="PERMISSION_NOT_FOUND"
        )

class RoleAlreadyExist(AppException):
    def __init__():
        super().__init__(
            message="Role Aleardy Exist",
            status_code= 409,
            error_code="DUPLICATE_RECORD"
        )

class RoleNotFound(AppException):
    def __init__(self,role_name: str | None = None):
        if not role_name:
            super().__init__(
                message=f"Role Not Found",
                status_code=404,
                error_code="ROLE_NOT_FOUND"
            )
        super().__init__(
            message=f"Role Not Found with {role_name}",
            status_code= 404,
            error_code="ROLE_NOT_FOUND"
        )
class PermissionNotFound(AppException):
    def __init__(self,permission_name :str):
        super().__init__(
            message=f"Permission Not Found with {permission_name}",
            status_code= 404,
            error_code="DULICATE_RECORD"
        )
class RolePermissionNotFound():
    def __init__(self):
        super().__init__(
            message=f"Role  Not Found with ",
            status_code= 404,
            error_code="ROLE_NOT_FOUND"

        )


class FaceDetectionNotFound(AppException):
    def __init__(self):
        super().__init__(
            message= "FaceNotDetect",
            status_code= 404,
            error_code= "FACE_NOT_DETECT"
        )


class FaceNotFound(AppException):
    def __init__(self):
        super().__init__(
            message= "Employee Face not Found",
            status_code= 404,
            error_code= "NOT_FOUND"
        )
class FaceDoseNotMatch(AppException):
    def __init__(self):
        super().__init__(
            message= "face not match ",
            status_code = 404,
            error_code = "NOT_FOUND"
        )
