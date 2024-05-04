"""add title fields in post model 

Revision ID: df53aa9d99e7
Revises: d67a59cdc276
Create Date: 2024-05-05 00:33:43.143171

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'df53aa9d99e7'
down_revision = 'd67a59cdc276'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('title', sa.String(length=50), nullable=False))
        batch_op.alter_column('body',
               existing_type=sa.VARCHAR(length=140),
               type_=sa.String(length=500),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.alter_column('body',
               existing_type=sa.String(length=500),
               type_=sa.VARCHAR(length=140),
               existing_nullable=False)
        batch_op.drop_column('title')

    op.create_table('post_search_idx',
    sa.Column('segid', sa.NullType(), nullable=False),
    sa.Column('term', sa.NullType(), nullable=False),
    sa.Column('pgno', sa.NullType(), nullable=True),
    sa.PrimaryKeyConstraint('segid', 'term')
    )
    op.create_table('post_search_data',
    sa.Column('id', sa.INTEGER(), nullable=True),
    sa.Column('block', sa.BLOB(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('post_search',
    sa.Column('post_id', sa.NullType(), nullable=True),
    sa.Column('body', sa.NullType(), nullable=True)
    )
    op.create_table('post_search_docsize',
    sa.Column('id', sa.INTEGER(), nullable=True),
    sa.Column('sz', sa.BLOB(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('post_search_content',
    sa.Column('id', sa.INTEGER(), nullable=True),
    sa.Column('c0', sa.NullType(), nullable=True),
    sa.Column('c1', sa.NullType(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('post_search_config',
    sa.Column('k', sa.NullType(), nullable=False),
    sa.Column('v', sa.NullType(), nullable=True),
    sa.PrimaryKeyConstraint('k')
    )
    op.drop_table('search')
    # ### end Alembic commands ###
