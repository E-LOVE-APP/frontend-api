"""uc-16-add-user-interaction-model

Revision ID: 67577aefe0a2
Revises: 5983095292a3
Create Date: 2024-11-04 23:00:38.585468

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '67577aefe0a2'
down_revision: Union[str, None] = '5983095292a3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_interaction',
    sa.Column('user_id', sa.String(length=36), nullable=False),
    sa.Column('target_user_id', sa.String(length=36), nullable=False),
    sa.Column('interaction_type', sa.String(length=10), nullable=False),
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['target_user_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_interaction')
    # ### end Alembic commands ###
