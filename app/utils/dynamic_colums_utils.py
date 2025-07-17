from typing import Any

from app.schema.employee_schema import EmployeeSerializer


class TransformerDynamicColumn(object):
    def __init__(self) -> None:
        self.all_fields = list(EmployeeSerializer.model_fields.keys())

    def get_dynamic_columns(self, company):
        # circular import issue workaround
        from app.utils.filter_helper import DynamicColumnFilterHelper
        
        if not company:
            return self.all_fields

        dynamic_columns = DynamicColumnFilterHelper().get_dynamic_column(company)
        if dynamic_columns and dynamic_columns.fields:
            dynamic_columns_cfg = dynamic_columns.fields.split(",")
        else:
            dynamic_columns_cfg = self.all_fields

        return dynamic_columns_cfg

    def __call__(self, items, company) -> Any:
        dynamic_columns = self.get_dynamic_columns(company)
        default_fields = {"status", "first_name", "last_name"}
        existing = set(self.all_fields)
        allowed = set(dynamic_columns)
        for item in items:
            for field_name in existing - allowed - default_fields:
                item.pop(field_name)
        return items