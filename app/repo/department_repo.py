
from sqlalchemy.orm  import Session

from app.schemas import
from app.models.department_model import DepartmentModel

class DepartmentRepo:
    def __init__(self,db : Session):
        self.db = db



    def create_departments(self):
        return
    def get_all_depertment (self):
        return
    def department_id (self):
        return
    def get_department(self):
        return
    def remove_department_(self):
        return
    def suspend_department(self):
        return
    def soft_delete_department(self):
        return
    def update_department(self):
        return