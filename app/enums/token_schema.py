from datetime import datetime
from uuid import UUID

from  pydantic import  BaseModel

class TokenSchema(BaseModel):

        user_id :UUID
        device_id :UUID | None
        refresh_token :str
        expires_at : datetime
