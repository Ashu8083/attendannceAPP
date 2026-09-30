from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session
from app.models import Branch
from schemas.branch_schema import UpdateBranch, SearchFilters
from test.unit_test.conftest import db_session


class BranchRepo:

    def __init__(self,db_session :Session):
        self.db_session = db_session

    def create_branch(self,branch:Branch ):

        self.db_session.add(branch)
        self.db_session.commit()
        self.db_session.refresh(branch)
        return branch

    def update_branch(self,
                      branch : Branch ,
                      branch_update : UpdateBranch
                      ):

        for field, value in branch_update.model_dump(exclude_unset=True).items():
            setattr(branch, field, value)

        self.db_session.add(branch)
        self.db_session.commit()
        self.db_session.refresh(branch)
        return branch

    def get_branch_by_filter(self,
                             branch : SearchFilters ):

        query = self.db_session.query(Branch)

        if branch.organisation_id:
            query = query.filter(Branch.organisation_id == branch.organisation_id)
        if branch.branch_name:
            query = query.filter(Branch.branch_name == branch.branch_name)
        if branch.status:
            query = query.filter(Branch.status == branch.status)

        return query.all

    def get_branch_by_id(self,
                         id : UUID ):
        query = self.db_session.query(Branch).filter(Branch.id == id)
        return query.first()







