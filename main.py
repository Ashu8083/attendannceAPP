from fastapi import FastAPI

#from app.core
from app.db.database import engine
from app.db.database import Base
from app.models.organisations import Organisation
from app.models.attendance_record_model import Attendance
from app.models.user_models import User
from app.models.employee_models import Employee
from app.models.subcription_model import Subscription
from app.models.leave_record_model import LeaveRequest
app = FastAPI()

@app.get("/")
def home():
    return{"message" : "FastAPI server"}

Base.metadata.create_all(
    bind = engine
)