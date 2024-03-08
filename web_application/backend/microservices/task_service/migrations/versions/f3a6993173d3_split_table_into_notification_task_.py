"""split table into notification_task, complete_task, task

Revision ID: f3a6993173d3
Revises: 3227658ec714
Create Date: 2024-03-08 13:12:41.447586

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'f3a6993173d3'
down_revision: Union[str, None] = '3227658ec714'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('complete_task',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('task_id', sa.Integer(), nullable=False),
                    sa.Column('complete_at', sa.DateTime(), nullable=True),
                    sa.Column('planned_complete_at', sa.DateTime(), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('task_id')
                    )
    op.create_table('notification_task',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('task_id', sa.Integer(), nullable=False),
                    sa.Column('send_notification_at', sa.DateTime(), nullable=False),
                    sa.Column('duration_send_notification_at', sa.Time(), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('task_id')
                    )
    op.alter_column('task', 'description',
                    existing_type=sa.VARCHAR(length=255),
                    type_=sa.String(length=512),
                    nullable=True)
    op.alter_column('task', 'created_at',
                    existing_type=postgresql.TIMESTAMP(),
                    nullable=False)
    op.drop_column('task', 'is_complete')
    op.drop_column('task', 'send_notification_at')
    op.drop_column('task', 'duration_repeat_send_notification_at')
    op.drop_column('task', 'complete_at')
    op.drop_column('task', 'planned_complete_at')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('planned_complete_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.add_column('task', sa.Column('complete_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.add_column('task', sa.Column('duration_repeat_send_notification_at', postgresql.TIME(), autoincrement=False,
                                    nullable=True))
    op.add_column('task', sa.Column('send_notification_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.add_column('task', sa.Column('is_complete', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.alter_column('task', 'created_at',
                    existing_type=postgresql.TIMESTAMP(),
                    nullable=True)
    op.alter_column('task', 'description',
                    existing_type=sa.String(length=512),
                    type_=sa.VARCHAR(length=255),
                    nullable=False)
    op.drop_table('notification_task')
    op.drop_table('complete_task')
    # ### end Alembic commands ###
