"""Add relationships

Revision ID: 6f3eb160a860
Revises: 9734d10f834f
Create Date: 2025-07-11 16:24:54.798818

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '6f3eb160a860'
down_revision = '9734d10f834f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.drop_table('comment')
    op.drop_table('post')
    with op.batch_alter_table('comments', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('comments_author_id_fkey'), type_='foreignkey')
        batch_op.drop_constraint(batch_op.f('comments_post_id_fkey'), type_='foreignkey')
        batch_op.create_foreign_key(None, 'posts', ['post_id'], ['id'])
        batch_op.create_foreign_key(None, 'users', ['author_id'], ['id'])

    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('posts_author_id_fkey'), type_='foreignkey')
        batch_op.create_foreign_key(None, 'users', ['author_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key(batch_op.f('posts_author_id_fkey'), 'users', ['author_id'], ['id'], ondelete='CASCADE')

    with op.batch_alter_table('comments', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key(batch_op.f('comments_post_id_fkey'), 'posts', ['post_id'], ['id'], ondelete='CASCADE')
        batch_op.create_foreign_key(batch_op.f('comments_author_id_fkey'), 'users', ['author_id'], ['id'], ondelete='CASCADE')

    op.create_table('post',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('post_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('title', sa.VARCHAR(length=150), autoincrement=False, nullable=False),
    sa.Column('content', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('author_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], name='post_author_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='post_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('comment',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('content', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('post_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('author_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], name=op.f('comment_author_id_fkey')),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], name=op.f('comment_post_id_fkey')),
    sa.PrimaryKeyConstraint('id', name=op.f('comment_pkey'))
    )
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('username', sa.VARCHAR(length=80), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.Column('password', sa.VARCHAR(length=200), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('user_pkey')),
    sa.UniqueConstraint('email', name=op.f('user_email_key'), postgresql_include=[], postgresql_nulls_not_distinct=False),
    sa.UniqueConstraint('username', name=op.f('user_username_key'), postgresql_include=[], postgresql_nulls_not_distinct=False)
    )
    # ### end Alembic commands ###
