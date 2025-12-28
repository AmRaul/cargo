from sqladmin import ModelView
from app.models.supplier import Supplier
from app.models.client import Client
from app.models.rate import Rate
from app.models.shipment import Shipment
from app.models.expense import Expense


class SupplierAdmin(ModelView, model=Supplier):
    name = "Поставщик"
    name_plural = "Поставщики"
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

    column_labels = {
        "id": "ID",
        "name": "Название",
        "country": "Страна",
        "city": "Город",
        "contact_person": "Контактное лицо",
        "contact_info": "Контактная информация",
        "notes": "Примечания",
        "created_at": "Дата создания",
        "updated_at": "Дата обновления"
    }


class ClientAdmin(ModelView, model=Client):
    name = "Клиент"
    name_plural = "Клиенты"
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

    column_labels = {
        "id": "ID",
        "name": "Имя",
        "company_name": "Название компании",
        "contact_person": "Контактное лицо",
        "contact_info": "Контактная информация",
        "notes": "Примечания",
        "created_at": "Дата создания",
        "updated_at": "Дата обновления"
    }


class RateAdmin(ModelView, model=Rate):
    name = "Тариф"
    name_plural = "Тарифы"
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

    column_labels = {
        "id": "ID",
        "cargo_type": "Тип груза",
        "supplier_id": "Поставщик",
        "client_id": "Клиент",
        "buy_rate": "Ставка закупки",
        "sell_rate": "Ставка продажи",
        "currency": "Валюта",
        "unit": "Единица измерения",
        "valid_from": "Действует с",
        "valid_to": "Действует до",
        "created_at": "Дата создания",
        "updated_at": "Дата обновления"
    }


class ShipmentAdmin(ModelView, model=Shipment):
    name = "Поставка"
    name_plural = "Поставки"
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

    column_labels = {
        "id": "ID",
        "shipment_code": "Код поставки",
        "supplier_id": "Поставщик",
        "client_id": "Клиент",
        "rate_id": "Тариф",
        "cargo_type": "Тип груза",
        "quantity": "Количество",
        "status": "Статус",
        "departure_date": "Дата отправки",
        "arrival_date": "Дата прибытия",
        "created_at": "Дата создания",
        "updated_at": "Дата обновления"
    }

    column_type_formatters = {
        "status": lambda m, a: {
            "planned": "Запланирована",
            "in_transit": "В пути",
            "delivered": "Доставлена"
        }.get(m.status.value, m.status.value) if hasattr(m, 'status') and m.status else ""
    }

    # TODO: Add computed columns for finance (revenue, cost, profit, margin)
    # This requires custom column formatters


class ExpenseAdmin(ModelView, model=Expense):
    name = "Расход"
    name_plural = "Расходы"
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

    column_labels = {
        "id": "ID",
        "shipment_id": "Поставка",
        "expense_type": "Тип расхода",
        "amount": "Сумма",
        "currency": "Валюта",
        "comment": "Комментарий",
        "expense_date": "Дата расхода",
        "created_at": "Дата создания"
    }

    column_type_formatters = {
        "expense_type": lambda m, a: {
            "customs": "Таможня",
            "delivery": "Доставка",
            "agent_fee": "Агентский сбор",
            "warehouse": "Склад"
        }.get(m.expense_type.value, m.expense_type.value) if hasattr(m, 'expense_type') and m.expense_type else ""
    }
