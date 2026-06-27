import uuid
from datetime import datetime,date
from app.models.userdevice_details import UserDeviceDetails
from sqlalchemy.orm import Session
from app.schemas.userdevice_schema import UserDeviceCreate,UserDeviceResponse,UserDeviceUpdate

class UserDeviceDetailRepo:
    def __init__(self,db :Session):
        self.db = db
    
    def create_user_device(self,user_id :uuid ,userdevice : UserDeviceCreate):
        user_device = self.db.query(UserDeviceDetails).filter(UserDeviceDetails.user_id == user_id,
                                                UserDeviceDetails.device_unique_id == userdevice.device_unique_id).first()
        
        if  user_device:
            raise ValueError("User Device Record alread Exist")
        
        user_device = UserDeviceDetails(
                                        user_id = user_id,
                                        device_unique_id = userdevice.device_unique_id,
                                        device_type = userdevice.device_type,
                                        firebaseFCM_token = userdevice.firebaseFCM_token,
                                        refresh_token_id = userdevice.refresh_token_id,
                                        last_login = date.now(),
                                        is_login = True
                                         )
        self.db.add(user_device)
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
    
    def delete_user_device():
        return