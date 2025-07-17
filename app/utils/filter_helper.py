from app.db.connection import Session
from app.schema.employee_schema import ListEmployeeQueryParams
from app.db.models import Employee, DynamicColumn
from sqlalchemy import and_, desc


class DBconnection:
    def __init__(self):
        self.db = Session()


class EmployeeFilterHelper(DBconnection):
    def filter_employees(self, params: ListEmployeeQueryParams):
        conditions = []

        if params.company:
            conditions.append(Employee.company.has(name=params.company))

        if params.location:
            conditions.append(Employee.location.has(name=params.location))

        if params.department:
            conditions.append(Employee.department.has(name=params.department))

        if params.position:
            conditions.append(Employee.position.has(name=params.position))

        if params.status:
            conditions.append(Employee.status.in_(params.status))

        query = self.db.query(Employee).filter(and_(True, *conditions)).order_by(desc("id"))
        return query


class DynamicColumnFilterHelper(DBconnection):
    def get_dynamic_column(self, company):
        return self.db.query(DynamicColumn).filter(DynamicColumn.company.has(name=company)).first()