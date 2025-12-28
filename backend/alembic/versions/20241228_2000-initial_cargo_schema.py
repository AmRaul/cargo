"""Initial cargo schema

Revision ID: initial_cargo_schema
Revises:
Create Date: 2024-12-28 20:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'initial_cargo_schema'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create suppliers table
    op.create_table(
        'suppliers',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('country', sa.String(100), nullable=True),
        sa.Column('city', sa.String(100), nullable=True),
        sa.Column('contact_person', sa.String(255), nullable=True),
        sa.Column('contact_info', sa.Text, nullable=True),
        sa.Column('notes', sa.Text, nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.func.now()),
    )
    op.create_index('ix_suppliers_id', 'suppliers', ['id'])

    # Create clients table
    op.create_table(
        'clients',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('company_name', sa.String(255), nullable=True),
        sa.Column('contact_person', sa.String(255), nullable=True),
        sa.Column('contact_info', sa.Text, nullable=True),
        sa.Column('notes', sa.Text, nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.func.now()),
    )
    op.create_index('ix_clients_id', 'clients', ['id'])

    # Create rates table
    op.create_table(
        'rates',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('cargo_type', sa.String(255), nullable=False),
        sa.Column('supplier_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('client_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('buy_rate', sa.Float, nullable=False),
        sa.Column('sell_rate', sa.Float, nullable=False),
        sa.Column('currency', sa.String(10), nullable=False, server_default='USD'),
        sa.Column('unit', sa.String(20), nullable=False),
        sa.Column('valid_from', sa.Date, nullable=True),
        sa.Column('valid_to', sa.Date, nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.func.now()),
        sa.ForeignKeyConstraint(['supplier_id'], ['suppliers.id']),
        sa.ForeignKeyConstraint(['client_id'], ['clients.id']),
    )
    op.create_index('ix_rates_id', 'rates', ['id'])

    # Create shipments table
    op.create_table(
        'shipments',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('shipment_code', sa.String(100), nullable=False, unique=True),
        sa.Column('supplier_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('client_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('rate_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('cargo_type', sa.String(255), nullable=False),
        sa.Column('quantity', sa.Float, nullable=False),
        sa.Column('departure_date', sa.Date, nullable=True),
        sa.Column('arrival_date', sa.Date, nullable=True),
        sa.Column('status', sa.Enum('planned', 'in_transit', 'delivered', name='shipmentstatusenum'), server_default='planned'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.func.now()),
        sa.ForeignKeyConstraint(['supplier_id'], ['suppliers.id']),
        sa.ForeignKeyConstraint(['client_id'], ['clients.id']),
        sa.ForeignKeyConstraint(['rate_id'], ['rates.id']),
    )
    op.create_index('ix_shipments_id', 'shipments', ['id'])
    op.create_index('ix_shipments_shipment_code', 'shipments', ['shipment_code'])

    # Create expenses table
    op.create_table(
        'expenses',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('shipment_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('expense_type', sa.Enum('customs', 'delivery', 'agent_fee', 'warehouse', name='expensetypeenum'), nullable=False),
        sa.Column('amount', sa.Float, nullable=False),
        sa.Column('currency', sa.String(10), nullable=False, server_default='USD'),
        sa.Column('comment', sa.Text, nullable=True),
        sa.Column('expense_date', sa.Date, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['shipment_id'], ['shipments.id'], ondelete='CASCADE'),
    )
    op.create_index('ix_expenses_id', 'expenses', ['id'])


def downgrade() -> None:
    op.drop_index('ix_expenses_id', table_name='expenses')
    op.drop_table('expenses')
    op.execute('DROP TYPE expensetypeenum')

    op.drop_index('ix_shipments_shipment_code', table_name='shipments')
    op.drop_index('ix_shipments_id', table_name='shipments')
    op.drop_table('shipments')
    op.execute('DROP TYPE shipmentstatusenum')

    op.drop_index('ix_rates_id', table_name='rates')
    op.drop_table('rates')

    op.drop_index('ix_clients_id', table_name='clients')
    op.drop_table('clients')

    op.drop_index('ix_suppliers_id', table_name='suppliers')
    op.drop_table('suppliers')
