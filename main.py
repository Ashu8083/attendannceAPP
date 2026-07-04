from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

#from app.core
from app.db.database import engine
from app.db.database import Base
from app.middleware.middleware import AuthMiddleware
from app.models.organisations import Organisation
from app.models.attendance_record_model import Attendance
from app.models.user_models import User
from app.models.employee_models import Employee
from app.models.subcription_model import Subscription
from app.models.leave_record_model import LeaveRequest
from app.api import all_router
app = FastAPI()




app.add_middleware(
    CORSMiddleware,
    #allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(AuthMiddleware)
@app.get("/")
def home():
    return{"message" : "FastAPI server"}

for router in all_router:
    app.include_router(router)

Base.metadata.create_all(
    bind = engine
)