"""add_index

Revision ID: 2b4a2ad10bfe
Revises: 9a88c2b81d82
Create Date: 2024-04-11 15:43:11.534823

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2b4a2ad10bfe'
down_revision: Union[str, None] = '9a88c2b81d82'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('idx_complete_at', 'complete_task', ['complete_at'], unique=False)
    op.create_index('idx_for_complete_task', 'complete_task', ['id'], unique=False)
    op.create_index('idx_planned_complete_at', 'complete_task', ['planned_complete_at'], unique=False)
    op.create_foreign_key(None, 'complete_task', 'task', ['task_id'], ['id'], ondelete='CASCADE')
    op.create_index('idx_for_notification_task', 'notification_task', ['id'], unique=False)
    op.create_index('idx_send_notification_at', 'notification_task', ['send_notification_at'], unique=False)
    op.create_foreign_key(None, 'notification_task', 'task', ['task_id'], ['id'], ondelete='CASCADE')
    op.create_index('idx_create_by', 'task', ['create_by'], unique=False)
    op.create_index('idx_for_task', 'task', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('idx_for_task', table_name='task')
    op.drop_index('idx_create_by', table_name='task')
    op.drop_constraint(None, 'notification_task', type_='foreignkey')
    op.drop_index('idx_send_notification_at', table_name='notification_task')
    op.drop_index('idx_for_notification_task', table_name='notification_task')
    op.drop_constraint(None, 'complete_task', type_='foreignkey')
    op.drop_index('idx_planned_complete_at', table_name='complete_task')
    op.drop_index('idx_for_complete_task', table_name='complete_task')
    op.drop_index('idx_complete_at', table_name='complete_task')
    # ### end Alembic commands ###
