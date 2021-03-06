"""empty message

Revision ID: b1984cd2e6ab
Revises: 65bd75fa4d4a
Create Date: 2021-05-19 20:28:04.005586

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

import app

# revision identifiers, used by Alembic.
revision = 'b1984cd2e6ab'
down_revision = '65bd75fa4d4a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('member',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=64), nullable=False),
        sa.Column('mail', sa.String(length=128), nullable=False),
        sa.Column('is_student', sa.Boolean(), nullable=True),
        sa.Column('title', sa.String(length=64), nullable=True),
        sa.Column('fields', app.sqldb.models.IntegerArrayType(length=128), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_member_mail'), 'member', ['mail'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_member_mail'), table_name='member')
    op.drop_table('member')
    # ### end Alembic commands ###
