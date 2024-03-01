"""empty message

Revision ID: 6398383441e2
Revises: ebd8567f4b14
Create Date: 2024-03-01 12:58:40.577410

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6398383441e2'
down_revision = 'ebd8567f4b14'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('password_hash', sa.String(length=254), nullable=False),
    sa.Column('creation_date', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###