"""empty message

Revision ID: f97fe6bfeec6
Revises: db5d3550e510
Create Date: 2019-02-15 17:38:56.867993

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'f97fe6bfeec6'
down_revision = 'db5d3550e510'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('event_apply',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('event_basic_id', sa.Integer(), nullable=False),
    sa.Column('apply', sa.JSON(), nullable=True),
    sa.Column('start_time', sa.String(length=128), nullable=True),
    sa.Column('end_time', sa.String(length=128), nullable=True),
    sa.Column('limit', sa.JSON(), nullable=True),
    sa.Column('limit_desc', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['event_basic_id'], ['event_basic.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('event_basic_id')
    )
    op.alter_column('speaker', 'major_related',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Boolean(),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('speaker', 'major_related',
               existing_type=sa.Boolean(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=False)
    op.drop_table('event_apply')
    # ### end Alembic commands ###
