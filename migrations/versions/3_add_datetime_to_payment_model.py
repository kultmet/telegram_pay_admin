"""add datetime to payment model

Revision ID: f51640d87d67
Revises: 53d1606bdd80
Create Date: 2023-06-09 22:16:33.276101

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f51640d87d67'
down_revision = '53d1606bdd80'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('payment', sa.Column('timestamp', sa.DateTime(timezone=False), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('payment', 'timestamp')
    # ### end Alembic commands ###
