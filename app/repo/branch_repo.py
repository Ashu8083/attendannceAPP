from app.models import Branch

class BranchRepo:
    def __init__(self,db_session):
        self.db_session = db_session

    def create_branch(self,branch:Branch ):
        pass