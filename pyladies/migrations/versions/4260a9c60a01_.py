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
    sa.Column('event_info_id', sa.Integer(), nullable=False),
    sa.Column('slide_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['event_info_id'], ['event_info.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['slide_id'], ['slide_resource.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('event_info_id', 'slide_id')
    )

    # ## copy data to join table ##
    op.execute(text("""
      INSERT INTO event_slide (event_info_id, slide_id)
        SELECT
          event_info.event_info_id, slide.id
        FROM
          (SELECT id, url FROM slide_resource GROUP BY url) AS slide
        LEFT JOIN
          (SELECT event_info_id, url FROM slide_resource) AS event_info
        ON slide.url = event_info.url
      """))

    op.drop_constraint('slide_resource_ibfk_1', 'slide_resource', type_='foreignkey')
    op.drop_column('slide_resource', 'event_info_id')

    ## Remove duplicate data in slide_resource ##
    op.execute(text("""
      CREATE TABLE temp (id int);
      """))
    op.execute(text("""
      INSERT INTO temp
          SELECT id FROM slide_resource GROUP BY url;
      """))
    op.execute(text("""
      DELETE FROM slide_resource WHERE id NOT IN (SELECT id FROM temp);
      """))
    op.drop_table('temp')


def downgrade():
    ## Restore duplicate data in slide_resource ##
    op.execute(text("""
      CREATE TABLE temp LIKE slide_resource;
      """))
    op.add_column('temp', sa.Column('event_info_id', sa.Integer(), nullable=False))
    op.execute(text("""
      INSERT INTO temp (event_info_id, type, title, url)
        SELECT
          mapping_info.event_info_id, slide_info.type, slide_info.title, slide_info.url
        FROM
          (SELECT event_info_id, slide_id FROM event_slide) AS mapping_info
        LEFT JOIN
          (SELECT * FROM slide_resource) AS slide_info
        ON mapping_info.slide_id = slide_info.id
      """))
    op.execute(text("""
      DELETE FROM slide_resource;
      """))
    op.add_column('slide_resource', sa.Column('event_info_id', sa.Integer(), nullable=False))
    op.execute(text("""
      INSERT INTO slide_resource
        SELECT * FROM temp;
      """))
    op.drop_table('temp')

    op.create_foreign_key(
      "slide_resource_ibfk_1",
      "slide_resource",
      "event_info",
      ["event_info_id"],
      ["id"],
      ondelete="CASCADE")
    op.drop_table('event_slide')
