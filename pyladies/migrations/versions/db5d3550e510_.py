"""empty message

Revision ID: db5d3550e510
Revises: 39ad6fa5fbf0
Create Date: 2018-11-18 07:09:42.010689

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'db5d3550e510'
down_revision = '39ad6fa5fbf0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('link', 'url',
               existing_type=mysql.VARCHAR(length=128),
               type_=sa.String(length=1024),
               existing_nullable=False)
    op.alter_column('slide_resource', 'url',
               existing_type=mysql.VARCHAR(length=128),
               type_=sa.String(length=1024),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('slide_resource', 'url',
               existing_type=sa.String(length=1024),
               type_=mysql.VARCHAR(length=128),
               existing_nullable=False)
    op.alter_column('link', 'url',
               existing_type=sa.String(length=1024),
               type_=mysql.VARCHAR(length=128),
               existing_nullable=False)
    # ### end Alembic commands ###
