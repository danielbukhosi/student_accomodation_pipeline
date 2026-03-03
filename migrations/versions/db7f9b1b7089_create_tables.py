"""create tables

Revision ID: db7f9b1b7089
Revises: 
Create Date: 2026-01-27 23:28:00.128818

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'db7f9b1b7089'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
           """
                CREATE TABLE rooms(
                room_id INT PRIMARY KEY,
                name TEXT NOT NULL,
                inserted_at TIMESTAMP DEFAULT NOW()
                );
            """
     )
    op.execute(
                 """
            CREATE TABLE students(
            student_id INT PRIMARY KEY,
            name TEXT NOT NULL, 
            room_id INT references rooms(room_id),
            birthday DATE,
            sex TEXT NOT NULL,
            inserted_at TIMESTAMP DEFAULT NOW()
            );
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP TABLE students;")
    op.execute("DROP TABLE rooms;")
