from sqladmin import ModelView
from app.models.supplier import Supplier
from app.models.client import Client
from app.models.rate import Rate
from app.models.shipment import Shipment
from app.models.expense import Expense


class SupplierAdmin(ModelView, model=Supplier):
    name = "Supplier"
    name_plural = "Suppliers"
    icon = "fa-solid fa-warehouse"

    column_list = [
        Supplier.id,
        Supplier.name,
        Supplier.country,
        Supplier.city,
        Supplier.contact_person,
        Supplier.created_at
    ]

    column_searchable_list = [Supplier.name, Supplier.country, Supplier.city]
    column_sortable_list = [Supplier.name, Supplier.country, Supplier.created_at]

    column_details_exclude_list = [Supplier.id]

    form_columns = [
        Supplier.name,
        Supplier.country,
        Supplier.city,
        Supplier.contact_person,
        Supplier.contact_info,
        Supplier.notes
    ]


class ClientAdmin(ModelView, model=Client):
    name = "Client"
    name_plural = "Clients"
    icon = "fa-solid fa-users"

    column_list = [
        Client.id,
        Client.name,
        Client.company_name,
        Client.contact_person,
        Client.created_at
    ]

    column_searchable_list = [Client.name, Client.company_name]
    column_sortable_list = [Client.name, Client.company_name, Client.created_at]

    column_details_exclude_list = [Client.id]

    form_columns = [
        Client.name,
        Client.company_name,
        Client.contact_person,
        Client.contact_info,
        Client.notes
    ]


class RateAdmin(ModelView, model=Rate):
    name = "Rate"
    name_plural = "Rates"
    icon = "fa-solid fa-dollar-sign"

    column_list = [
        Rate.id,
        Rate.cargo_type,
        Rate.supplier_id,
        Rate.client_id,
        Rate.buy_rate,
        Rate.sell_rate,
        Rate.currency,
        Rate.unit,
        Rate.valid_from,
        Rate.valid_to
    ]

    column_searchable_list = [Rate.cargo_type, Rate.currency, Rate.unit]
    column_sortable_list = [Rate.cargo_type, Rate.buy_rate, Rate.sell_rate, Rate.created_at]

    column_details_exclude_list = [Rate.id]

    form_columns = [
        Rate.cargo_type,
        Rate.supplier_id,
        Rate.client_id,
        Rate.buy_rate,
        Rate.sell_rate,
        Rate.currency,
        Rate.unit,
        Rate.valid_from,
        Rate.valid_to
    ]


class ShipmentAdmin(ModelView, model=Shipment):
    name = "Shipment"
    name_plural = "Shipments"
    icon = "fa-solid fa-truck"

    column_list = [
        Shipment.id,
        Shipment.shipment_code,
        Shipment.supplier_id,
        Shipment.client_id,
        Shipment.cargo_type,
        Shipment.quantity,
        Shipment.status,
        Shipment.departure_date,
        Shipment.arrival_date,
        Shipment.created_at
    ]

    column_searchable_list = [Shipment.shipment_code, Shipment.cargo_type]
    column_sortable_list = [
        Shipment.shipment_code,
        Shipment.quantity,
        Shipment.status,
        Shipment.departure_date,
        Shipment.created_at
    ]

    column_default_sort = [(Shipment.created_at, True)]  # Sort by created_at descending

    column_details_exclude_list = [Shipment.id]

    form_columns = [
        Shipment.shipment_code,
        Shipment.supplier_id,
        Shipment.client_id,
        Shipment.rate_id,
        Shipment.cargo_type,
        Shipment.quantity,
        Shipment.departure_date,
        Shipment.arrival_date,
        Shipment.status
    ]

    # TODO: Add computed columns for finance (revenue, cost, profit, margin)
    # This requires custom column formatters


class ExpenseAdmin(ModelView, model=Expense):
    name = "Expense"
    name_plural = "Expenses"
    icon = "fa-solid fa-money-bill"

    column_list = [
        Expense.id,
        Expense.shipment_id,
        Expense.expense_type,
        Expense.amount,
        Expense.currency,
        Expense.expense_date,
        Expense.comment
    ]

    column_searchable_list = [Expense.comment]
    column_sortable_list = [
        Expense.expense_type,
        Expense.amount,
        Expense.expense_date,
        Expense.created_at
    ]

    column_default_sort = [(Expense.expense_date, True)]

    column_details_exclude_list = [Expense.id]

    form_columns = [
        Expense.shipment_id,
        Expense.expense_type,
        Expense.amount,
        Expense.currency,
        Expense.comment,
        Expense.expense_date
    ]
