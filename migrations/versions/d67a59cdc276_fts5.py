"""fts5

Revision ID: d67a59cdc276
Revises: 8b2cb65c8247
Create Date: 2024-05-04 04:15:06.161688

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd67a59cdc276'
down_revision = '8b2cb65c8247'
branch_labels = None
depends_on = None


def upgrade():
    
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('title', sa.String(length=50), nullable=False))
        batch_op.alter_column('body',
               existing_type=sa.VARCHAR(length=140),
               type_=sa.String(length=500),
               existing_nullable=False)

    
    op.execute(
        """
        CREATE VIRTUAL TABLE IF NOT EXISTS post_search USING fts5(
            post_id,
            title,
            body
        );
        """

    )
    op.execute(
        """
        CREATE TRIGGER post_after_insert AFTER INSERT ON Post
        BEGIN
            INSERT INTO post_search(post_id,title,body)
            VALUES (new.id,new.title,new.body);
        END;
        """
    )
    op.execute(
        """
        CREATE TRIGGER post_after_update AFTER UPDATE ON Post
        BEGIN
            UPDATE post_search
            SET body = new.body,title = new.title
            WHERE post_id = new.id;
        END;
        """
    )

    op.execute(
        """
        CREATE TRIGGER post_after_delete AFTER DELETE ON Post
            BEGIN
                DELETE FROM post_search WHERE post_id = new.id;
            END;
        """
    )


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("DROP TABLE IF EXISTS post_search")
    # ### end Alembic commands ###
