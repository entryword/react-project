"""empty message

Revision ID: f642e899ac2b
Revises: f97fe6bfeec6
Create Date: 2019-03-31 08:47:36.254888

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'f642e899ac2b'
down_revision = 'f97fe6bfeec6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('slide',
    sa.Column('sn', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(length=128), nullable=False),
    sa.Column('title', sa.String(length=128), nullable=False),
    sa.Column('url', sa.String(length=1024), nullable=False),
    sa.PrimaryKeyConstraint('sn')
    )
    op.create_table('event_slide',
    sa.Column('event_info_sn', sa.Integer(), nullable=False),
    sa.Column('slide_sn', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['event_info_sn'], ['event_info.sn'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['slide_sn'], ['slide.sn'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('event_info_sn', 'slide_sn')
    )
    op.alter_column('event_apply', 'apply',
               existing_type=mysql.LONGTEXT(charset='utf8mb4', collation='utf8mb4_bin'),
               type_=sa.JSON(),
               existing_nullable=True)
    op.alter_column('event_apply', 'limit',
               existing_type=mysql.LONGTEXT(charset='utf8mb4', collation='utf8mb4_bin'),
               type_=sa.JSON(),
               existing_nullable=True)
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
    op.alter_column('event_apply', 'limit',
               existing_type=sa.JSON(),
               type_=mysql.LONGTEXT(charset='utf8mb4', collation='utf8mb4_bin'),
               existing_nullable=True)
    op.alter_column('event_apply', 'apply',
               existing_type=sa.JSON(),
               type_=mysql.LONGTEXT(charset='utf8mb4', collation='utf8mb4_bin'),
               existing_nullable=True)
    op.drop_table('event_slide')
    op.drop_table('slide')
    # ### end Alembic commands ###
