"""empty message

Revision ID: 04e4d20f1200
Revises: c78580acd81a
Create Date: 2018-12-29 21:53:12.200161

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '04e4d20f1200'
down_revision = 'c78580acd81a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('about_me', sa.Text(), nullable=True))
    op.add_column('user', sa.Column('last_seen', sa.DateTime(), nullable=True))
    op.add_column('user', sa.Column('location', sa.String(length=64), nullable=True))
    op.add_column('user', sa.Column('member_since', sa.DateTime(), nullable=True))
    op.add_column('user', sa.Column('name', sa.String(length=64), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'name')
    op.drop_column('user', 'member_since')
    op.drop_column('user', 'location')
    op.drop_column('user', 'last_seen')
    op.drop_column('user', 'about_me')
    # ### end Alembic commands ###