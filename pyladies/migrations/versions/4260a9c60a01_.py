"""empty message

Revision ID: 4260a9c60a01
Revises: 6f56606cf4ac
Create Date: 2019-03-31 13:00:14.627197

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision = '4260a9c60a01'
down_revision = '6f56606cf4ac'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('event_slide',
    sa.Column('event_info_sn', sa.Integer(), nullable=False),
    sa.Column('slide_sn', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['event_info_sn'], ['event_info.sn'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['slide_sn'], ['slide_resource.sn'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('event_info_sn', 'slide_sn')
    )
    ## copy data to join table ##
    op.execute(text("""
      INSERT INTO event_slide (event_info_sn, slide_sn) 
      SELECT event_info_sn, sn FROM slide_resource
      """))
    op.drop_constraint('slide_resource_ibfk_1', 'slide_resource', type_='foreignkey')
    op.drop_column('slide_resource', 'event_info_sn')


def downgrade():
    op.add_column('slide_resource', sa.Column('event_info_sn', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False))
    op.execute(text("""
      INSERT INTO slide_resource (event_info_sn) 
      SELECT event_info_sn FROM event_slide
      WHERE event_slide.slide_sn = slide_resource.sn
      """))
    op.create_foreign_key('slide_resource_ibfk_1', 'slide_resource', 'event_info', ['event_info_sn'], ['sn'], ondelete='CASCADE')
    op.drop_table('event_slide')
