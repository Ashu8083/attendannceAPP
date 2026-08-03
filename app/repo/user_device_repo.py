from uuid import UUID
import uuid
from datetime import datetime,date

from dns import update
from sqlalchemy import select

from app.models.token import Token
from app.models.userdevice_details import UserDeviceDetails
from sqlalchemy.orm import Session
from app.schemas.userdevice_schema import UserDeviceCreate,UserDeviceResponse,UserDeviceUpdate

class UserDeviceDetailRepo:
    def __init__(self,db :Session):
        self.db = db
    
    def create_user_device(self,user_id :uuid.UUID ,userdevice : UserDeviceCreate):

        user_device = UserDeviceDetails(
                                        user_id = user_id,
                                        device_unique_id = userdevice.device_unique_id,
                                        device_type = userdevice.device_type,
                                        firebase_fcm_token = userdevice.firebaseFCM_token,
                                        last_login = datetime.now(),
                                        is_login = True
                                         )
        self.db.add(user_device)
        self.db.flush()
        return user_device
    
    def update_on_user_logout(self,user_id,user_device_id,userdeviceupdate : UserDeviceUpdate):

        user_device = self.db.query(UserDeviceDetails).filter(UserDeviceDetails.user_id == user_id,
                                                              UserDeviceDetails.device_unique_id == user_device_id).first()
        
        if not user_device: 
            raise ValueError("Device Record not Found")
        user_device.firebaseFCM_token = None
        user_device.is_login = False
        user_device.logout_time = datetime.now()
        try:
            self.db.commit()
            self.db.refresh(user_device)
        except Exception :
            self.db.rollback()
            raise ValueError("Internal error")

        return user_device
    
    def update_on_userdevice(self,user_id,user_device_id,userdeviceupdate : UserDeviceUpdate):

        user_device = self.db.query(UserDeviceDetails).filter(UserDeviceDetails.user_id == user_id,
                                                              UserDeviceDetails.device_unique_id == user_device_id).first()
        
        if not user_device: 
            raise ValueError("Device Record not Found")
        

        for feild,value in userdeviceupdate.model_dump().items():
            setattr(user_device, feild, value)
        
        try:
            self.db.commit()
            self.db.refresh(user_device)
        except Exception :
            self.db.rollback()
            raise ValueError("Internal error")
        return user_device
    
    # def delete_user_device():
    #     return
    def user_fcm_token(self):
        return

    def user_refresh_token(self,user_id : uuid.UUID , refresh_token : str):
        user_device = self.db.query(UserDeviceDetails).filter(UserDeviceDetails.user_id == user_id,).first()

        refresh_token = user_device.token.refresh_token

        return refresh_token

    def get_by_fcm_token(
        self,
        fcm_token: str
    ) -> UserDeviceDetails | None:
        stmt = select(UserDeviceDetails).where(
            UserDeviceDetails.firebase_fcm_token == fcm_token
        )
        return self.db.scalar(stmt)
    
    def get_active_device(
        self,
        user_id: UUID,
        device_unique_id: str
    ) -> UserDeviceDetails | None:
        stmt = select(UserDeviceDetails).where(
            UserDeviceDetails.user_id == user_id,
            UserDeviceDetails.device_unique_id == device_unique_id,
            UserDeviceDetails.is_login.is_(True)
        )
        return self.db.scalar(stmt)
    

    def delete(self, device: UserDeviceDetails) -> None:
        self.db.delete(device)

    
    def logout_device(
        self,
        device_id: UUID,
        logout_time
    ) -> None:
        stmt = (
            update(UserDeviceDetails)
            .where(UserDeviceDetails.id == device_id)
            .values(
                is_login=False,
                logout_time=logout_time
            )
        )
        self.db.execute(stmt)

    
    def logout_all_devices(self, user_id: UUID, logout_time) -> None:
        stmt = (
            update(UserDeviceDetails)
            .where(UserDeviceDetails.user_id == user_id)
            .values(
                is_login=False,
                logout_time=logout_time
            )
        )
        self.db.execute(stmt)

