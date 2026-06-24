from fastapi import APIRouter

from .organigastion_api import organisation_router
from app.api.user_api import user_router

all_router = [
    organisation_router,
    user_router
]


