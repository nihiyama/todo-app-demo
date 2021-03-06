"""init

Revision ID: da3cbce8a795
Revises: 
Create Date: 2022-01-10 21:51:53.659983+09:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'da3cbce8a795'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('todo_boards',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sa.String(length=32), nullable=False),
    sa.Column('title', sa.String(length=256), nullable=True),
    sa.Column('detail', sa.Text(), nullable=True),
    sa.Column('list_order', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_todo_boards_id'), 'todo_boards', ['id'], unique=False)
    op.create_index(op.f('ix_todo_boards_uuid'), 'todo_boards', ['uuid'], unique=True)
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sa.String(length=32), nullable=False),
    sa.Column('email_address', sa.String(length=256), nullable=False),
    sa.Column('user_name', sa.String(length=256), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.Column('is_superuser', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('hashed_password')
    )
    op.create_index(op.f('ix_users_email_address'), 'users', ['email_address'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_user_name'), 'users', ['user_name'], unique=False)
    op.create_index(op.f('ix_users_uuid'), 'users', ['uuid'], unique=True)
    op.create_table('todo_lists',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('todo_board_id', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(length=256), nullable=True),
    sa.Column('detail', sa.Text(), nullable=True),
    sa.Column('card_order', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['todo_board_id'], ['todo_boards.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_todo_lists_id'), 'todo_lists', ['id'], unique=False)
    op.create_index(op.f('ix_todo_lists_todo_board_id'), 'todo_lists', ['todo_board_id'], unique=False)
    op.create_table('user_todo_board_association',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('todo_board_id', sa.Integer(), nullable=False),
    sa.Column('is_owner', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['todo_board_id'], ['todo_boards.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'todo_board_id')
    )
    op.create_table('todo_cards',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('todo_list_id', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(length=256), nullable=True),
    sa.Column('detail', sa.Text(), nullable=True),
    sa.Column('start_date', sa.Date(), nullable=True),
    sa.Column('end_date', sa.Date(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['todo_list_id'], ['todo_lists.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_todo_cards_id'), 'todo_cards', ['id'], unique=False)
    op.create_index(op.f('ix_todo_cards_todo_list_id'), 'todo_cards', ['todo_list_id'], unique=False)
    op.create_table('user_todo_card_map',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('todo_card_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['todo_card_id'], ['todo_cards.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_todo_card_map')
    op.drop_index(op.f('ix_todo_cards_todo_list_id'), table_name='todo_cards')
    op.drop_index(op.f('ix_todo_cards_id'), table_name='todo_cards')
    op.drop_table('todo_cards')
    op.drop_table('user_todo_board_association')
    op.drop_index(op.f('ix_todo_lists_todo_board_id'), table_name='todo_lists')
    op.drop_index(op.f('ix_todo_lists_id'), table_name='todo_lists')
    op.drop_table('todo_lists')
    op.drop_index(op.f('ix_users_uuid'), table_name='users')
    op.drop_index(op.f('ix_users_user_name'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email_address'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_todo_boards_uuid'), table_name='todo_boards')
    op.drop_index(op.f('ix_todo_boards_id'), table_name='todo_boards')
    op.drop_table('todo_boards')
    # ### end Alembic commands ###
