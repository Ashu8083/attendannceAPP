from contextlib import asynccontextmanager

from fastapi import FastAPI
from redis import RedisError
from starlette.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.db.database import engine, Base
from app.middleware.middleware import AuthMiddleware
from app.api import all_router

from app.exceptions.exception_handaler import *

# Import models so SQLAlchemy registers them
from app.models.organisations import Organisation
from app.models.attendance_record_model import Attendance
from app.models.user_models import User
from app.models.employee_models import Employee
from app.models.subcription_model import Subscription
from app.models.leave_record_model import LeaveRequest

from app.core.logging_config import logger
from app.redis_config.redis import redis_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting HRMS Backend...")

    try:
        logger.info("Verifying PostgreSQL connection...")

        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        logger.info("PostgreSQL connection verified successfully.")

        # Development only
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables initialized.")

    except SQLAlchemyError:
        logger.exception("Failed to connect to PostgreSQL.")
        raise

    yield

    # try :
    #     logger.info("Verifying Redis connection...")
    #     await redis_client.ping()
    #     logger.info("Redis connection verified successfully.")
    # except RedisError as error:
    #     logger.exception("Failed to connect to Redis.")
    # yield
    # await redis_client.close()

    logger.info("Shutting down HRMS Backend...")


app = FastAPI(
    title="HRMS API",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(AuthMiddleware)
app.add_exception_handler(AppException, app_exception_handler)

app.add_exception_handler(RequestValidationError, validation_exception_handler)

app.add_exception_handler(HTTPException, http_exception_handler)

app.add_exception_handler(Exception, generic_exception_handler)


@app.get("/")
def home():
    return {"message": "FastAPI Server"}


for router in all_router:
    app.include_router(router)