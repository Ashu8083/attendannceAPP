from kombu import uuid

from datetime import datetime, time, timedelta, timezone

from sqlalchemy import true

from app.core.config import get_settings
from app.enums.role_enums import UserRole
from jose import jwt, ExpiredSignatureError, JWTError

## responsibility of JWT handler
# * create JWT
# * decode JWT
# * verify expiration
# * verify signature
settings = get_settings()

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 5
REFRESH_TOKEN_EXPIRE_DAYS = 7

expire_time = (datetime.now(timezone.utc) + timedelta(minutes=15)).time()
refresh_token_expiration_time = datetime.now() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)


def create_access_token(user_id,user_role) -> str:# life spam will 1 week generate new token on the use of the access token
    playload = {
        "user_id" : user_id,
        "user_role" : user_role,
        "expire_time" : expire_time,
        "token_type" : "access"
    }

    return jwt.encode(
        playload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
def create_refresh_token (user_id,user_role) :# life spam will 5 min (for revoke , revoke the user directly )
    playload = {
        "user_id": user_id,
        "user_role": user_role,
        "expire_time": refresh_token_expiration_time,
        "token_type": "access"
    }
    return refresh_token_expiration_time , jwt.encode(
        playload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


    return
def decode_token(token):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return payload
    except ExpiredSignatureError:
        raise Exception("Token has expired")
    except JWTError:
        raise Exception("Invalid token")

    return True

def verify_refresh_token (refresh_token):  # store in the db as token or in the device table
    return
def verify_access_token(access_token): # depends on the expiration and user details for validate
    return








