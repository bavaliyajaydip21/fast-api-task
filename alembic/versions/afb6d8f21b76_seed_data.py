"""seed_data

Revision ID: afb6d8f21b76
Revises: 48e12f3c689c
Create Date: 2025-07-17 17:23:33.945194

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'afb6d8f21b76'
down_revision: Union[str, Sequence[str], None] = '48e12f3c689c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# this data is generated using help of AI
def upgrade():
    # raw SQL insert statements
    op.execute("INSERT INTO company (id, name) VALUES (1, 'Acme Corp')")
    op.execute("INSERT INTO location (id, name) VALUES (1, 'New York'), (2, 'San Francisco')")
    op.execute("INSERT INTO department (id, name, company_id) VALUES (1, 'Engineering', 1)")
    op.execute("INSERT INTO position (id, name) VALUES (1, 'Backend Engineer')")
    op.execute("""
        INSERT INTO employee (
            id, first_name, last_name, contact_info, status,
            department_id, position_id, location_id, company_id
        )
        VALUES (
            1, 'John', 'Doe', 'john.doe@example.com', 'active',
            1, 1, 1, 1
        )
    """)
 
def downgrade():
    op.execute("DELETE FROM employee WHERE id = 1")
    op.execute("DELETE FROM department WHERE id = 1")
    op.execute("DELETE FROM position WHERE id = 1")
    op.execute("DELETE FROM location WHERE id IN (1, 2)")
    op.execute("DELETE FROM company WHERE id = 1")
 