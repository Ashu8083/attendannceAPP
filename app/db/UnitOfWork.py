from sqlalchemy.orm import session

class UnitOfWork:

    def __init__(self,db):
        self.db = db

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):

        if exc_type:
            self.db.rollback()
        else:
            self.db.commit()