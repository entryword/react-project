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
        SELECT 
          event_info.event_info_sn, slide.sn
        FROM 
          (SELECT sn, url FROM slide_resource GROUP BY url) AS slide 
        LEFT JOIN 
          (SELECT event_info_sn, url FROM slide_resource) AS event_info 
        ON slide.url = event_info.url
      """))

    op.drop_column('slide_resource', 'event_info_sn')

    ## Remove duplicate data in slide_resource ##
    op.execute(text("""
      SET FOREIGN_KEY_CHECKS = 0;
      """))
    op.execute(text("""
      CREATE TABLE temp LIKE slide_resource;
      """))
    op.execute(text("""
      INSERT INTO temp
          SELECT * FROM slide_resource GROUP BY url;
      """))
    op.drop_table('slide_resource')
    op.rename_table('temp', 'slide_resource')
    op.execute(text("""
      SET FOREIGN_KEY_CHECKS = 1;
      """))

def downgrade():
    op.add_column('slide_resource', sa.Column('event_info_sn', sa.Integer(), nullable=False))
    op.execute(text("""
      UPDATE slide_resource 
      SET event_info_sn =(
        SELECT event_slide.event_info_sn FROM event_slide
        WHERE slide_resource.sn = event_slide.slide_sn)  
      """))
    op.drop_table('event_slide')
