import uuid

from datetime import datetime, time, timedelta, timezone

from cryptography.fernet import InvalidToken
from sqlalchemy import true

from app.core.config import get_settings
from app.enums.role_enums import UserRole
from jose import jwt, ExpiredSignatureError, JWTError

from app.exceptions.custom_exception import AccessTokenExpired

## responsibility of JWT handler
# * create JWT
# * decode JWT
# * verify expiration
# * verify signature
settings = get_settings()

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7


def create_access_token(user_id,user_role,organisation_id,employee_id :uuid.UUID | None) -> str:# life spam will 1 week generate new token on the use of the access token

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    playload = {
        "user_id": str(user_id),
        "system_role" : user_role,
        "organisation_id": str(organisation_id),
        "employee_id": str(employee_id) if employee_id else None,
        "token_type" : "access",
        "exp": expire,
    }

    return jwt.encode(
        playload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
def create_refresh_token (user_id,user_role,organisation_id) :# life spam will 5 min (for revoke , revoke the user directly )
    expire = datetime.now(timezone.utc) + timedelta(
        days=REFRESH_TOKEN_EXPIRE_DAYS
    )
    refresh_token_expiration_time = datetime.now(timezone.utc) + timedelta()

    playload = {
        "user_id": str(user_id),
        "organisation_id": str(organisation_id),
        "system_role" : user_role,
        "token_type": "refresh",
        "exp": expire,
    }
    return refresh_token_expiration_time , jwt.encode(
        playload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

def decode_token(token):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return payload
    # except ExpiredSignatureError:
    #     raise Exception("Token has expired")
    # except JWTError:
    #     raise Exception("Invalid token")
    except ExpiredSignatureError:
        raise AccessTokenExpired()
    except JWTError:
        raise InvalidToken()

    return True

def verify_refresh_token (refresh_token):  # store in the db as token or in the device table
    return
def verify_access_token(access_token): # depends on the expiration and user details for validate
    return








