"""new rows for dates

Revision ID: 0ddebca14b78
Revises: 2a6cf68bff88
Create Date: 2020-09-16 13:09:33.524122

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0ddebca14b78'
down_revision = '2a6cf68bff88'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cars', sa.Column('last_cleaning', sa.DateTime(), nullable=True))
    op.add_column('cars', sa.Column('last_repairing', sa.DateTime(), nullable=True))
    op.drop_column('cars', 'date_of_last_inspection')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cars', sa.Column('date_of_last_inspection', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.drop_column('cars', 'last_repairing')
    op.drop_column('cars', 'last_cleaning')
    # ### end Alembic commands ###