import uuid
from sqlalchemy.orm import Session
from datetime import datetime, date ,timedelta,time

from app.repo.department_repo import DepartmentRepo
from app.models.temp_otp_storage import TempOtpStorage
from app.schemas.otp_schema import OTPSchema


class AuthRepo :
    def __init__(self,db: Session):
        self.db  = db


    def get_otp(self ,user_id : uuid.UUID ):
        otp =  self.db.query(TempOtpStorage).filter(TempOtpStorage.user_id == user_id,
            TempOtpStorage.is_expired.is_(False),
            TempOtpStorage.expire_time > datetime.now().time()
        ).first()
        try:
            self.db.delete(otp)
            self.db.commit()
        except Exception as e:
            raise e
        return otp

    def create_otp(self,user_id : uuid.UUID ,otp :str):
        expire_time = (datetime.now() + timedelta(minutes=5)).time()

        temp_otp = TempOtpStorage(
            otp = otp,
            date= date.today(),
            expire_time = expire_time,
            user_id = user_id,
            is_expired = False
        )
        try:
            self.db.add(temp_otp)
            self.db.commit()
            self.db.refresh(temp_otp)
        except Exception as e:
            self.db.rollback()
            raise e
        return temp_otp

    def get_otp_by_email(self,email :str) :
        return  self.db.query(TempOtpStorage).filter(TempOtpStorage.user_email == email).first()




