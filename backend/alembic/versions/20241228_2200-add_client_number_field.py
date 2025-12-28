"""Add client_number field

Revision ID: add_client_number
Revises: initial_cargo_schema
Create Date: 2024-12-28 22:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'add_client_number'
down_revision: Union[str, None] = 'initial_cargo_schema'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add client_number column (temporarily nullable to populate existing records)
    op.add_column('clients', sa.Column('client_number', sa.String(20), nullable=True))

    # Generate client numbers for existing clients
    connection = op.get_bind()
    result = connection.execute(sa.text("SELECT id FROM clients ORDER BY created_at"))
    clients = result.fetchall()

    for idx, client in enumerate(clients, start=1):
        client_number = f"CL-{idx:04d}"
        connection.execute(
            sa.text("UPDATE clients SET client_number = :client_number WHERE id = :client_id"),
            {"client_number": client_number, "client_id": client[0]}
        )

    # Now make it non-nullable and add unique constraint
    op.alter_column('clients', 'client_number', nullable=False)
    op.create_unique_constraint('uq_clients_client_number', 'clients', ['client_number'])
    op.create_index('ix_clients_client_number', 'clients', ['client_number'])


def downgrade() -> None:
    op.drop_index('ix_clients_client_number', table_name='clients')
    op.drop_constraint('uq_clients_client_number', 'clients', type_='unique')
    op.drop_column('clients', 'client_number')
