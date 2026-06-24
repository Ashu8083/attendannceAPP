from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.repo.user_repo import UserRepo
from app.repo.organisation_repo import OrganisationRepo
from app.repo.user_repo import UserRepo
from app.service.organisation_service import OrganisationService
from app.service.user_service import UserService

def get_organaistion_service(
    db: Session = Depends(get_db)
):
    repo = OrganisationRepo(db)
    return OrganisationService(repo)

def get_user_service(
        db: Session = Depends(get_db)
):
    repo = UserRepo(db)
    return UserService(repo)


