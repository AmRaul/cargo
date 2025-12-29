from sqladmin import ModelView, BaseView, expose
from starlette.requests import Request
from starlette.responses import Response
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy import select
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
        Client.client_number,
        Client.name,
        Client.company_name,
        Client.contact_person,
        Client.created_at
    ]

    column_searchable_list = [Client.client_number, Client.name, Client.company_name]
    column_sortable_list = [Client.client_number, Client.name, Client.company_name, Client.created_at]

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
        "client_number": "Номер",
        "name": "Имя",
        "company_name": "Компания",
        "contact_person": "Контакт",
        "contact_info": "Контактная информация",
        "notes": "Примечания",
        "created_at": "Создан",
        "updated_at": "Обновлен"
    }


class RateAdmin(ModelView, model=Rate):
    name = "Тариф"
    name_plural = "Тарифы"
    icon = "fa-solid fa-dollar-sign"

    column_list = [
        Rate.cargo_type,
        Rate.supplier_id,
        Rate.client_id,
        Rate.buy_rate,
        Rate.sell_rate,
        Rate.currency,
        Rate.unit,
        "margin",
        "margin_percent",
        Rate.valid_from,
        Rate.valid_to
    ]

    column_searchable_list = [Rate.cargo_type, Rate.currency, Rate.unit]
    column_sortable_list = [Rate.cargo_type, Rate.buy_rate, Rate.sell_rate, Rate.created_at]

    column_filters = [Rate.cargo_type, Rate.supplier_id, Rate.client_id, Rate.currency]

    column_details_exclude_list = [Rate.id]

    form_columns = [
        Rate.cargo_type,
        Rate.supplier,
        Rate.client,
        Rate.buy_rate,
        Rate.sell_rate,
        Rate.currency,
        Rate.unit,
        Rate.valid_from,
        Rate.valid_to
    ]

    form_ajax_refs = {
        "supplier": {
            "fields": ("name", "country"),
            "order_by": "name",
        },
        "client": {
            "fields": ("client_number", "name"),
            "order_by": "client_number",
        }
    }

    column_labels = {
        "id": "ID",
        "cargo_type": "Тип груза",
        "supplier": "Поставщик",
        "supplier_id": "Поставщик",
        "client": "Клиент",
        "client_id": "Клиент",
        "buy_rate": "Закупка",
        "sell_rate": "Продажа",
        "margin": "Маржа ($)",
        "margin_percent": "Маржа (%)",
        "currency": "Валюта",
        "unit": "Ед. изм.",
        "valid_from": "Действует с",
        "valid_to": "Действует до",
        "created_at": "Дата создания",
        "updated_at": "Дата обновления"
    }

    def _safe_supplier_name(model, attr):
        """Safely get supplier name with error handling"""
        try:
            return getattr(model.supplier, 'name', '—') if hasattr(model, 'supplier') and model.supplier else "—"
        except Exception:
            return "—"

    def _safe_client_number(model, attr):
        """Safely get client number with error handling"""
        try:
            return getattr(model.client, 'client_number', 'Базовый тариф') if hasattr(model, 'client') and model.client else "Базовый тариф"
        except Exception:
            return "Базовый тариф"

    column_formatters = {
        Rate.supplier_id: _safe_supplier_name,
        Rate.client_id: _safe_client_number,
        "margin": lambda m, a: f"${(m.sell_rate - m.buy_rate):.2f}" if m.sell_rate and m.buy_rate else "—",
        "margin_percent": lambda m, a: f"{((m.sell_rate - m.buy_rate) / m.buy_rate * 100):.1f}%" if m.sell_rate and m.buy_rate and m.buy_rate > 0 else "—"
    }

    def scaffold_list_query(self):
        """Override to eagerly load relationships"""
        stmt = select(self.model).options(
            selectinload(Rate.supplier),
            selectinload(Rate.client)
        )
        return stmt


class ShipmentAdmin(ModelView, model=Shipment):
    name = "Поставка"
    name_plural = "Поставки"
    icon = "fa-solid fa-truck"

    column_list = [
        Shipment.shipment_code,
        Shipment.client_id,
        Shipment.supplier_id,
        Shipment.cargo_type,
        Shipment.quantity,
        "revenue",
        "total_expenses",
        "profit",
        "margin_percent",
        Shipment.status,
        Shipment.departure_date,
        Shipment.arrival_date
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

    column_filters = [Shipment.client_id, Shipment.supplier_id, Shipment.status, Shipment.cargo_type]

    column_details_exclude_list = [Shipment.id]

    form_columns = [
        Shipment.shipment_code,
        Shipment.supplier,
        Shipment.client,
        Shipment.rate,
        Shipment.cargo_type,
        Shipment.quantity,
        Shipment.departure_date,
        Shipment.arrival_date,
        Shipment.status
    ]

    form_ajax_refs = {
        "supplier": {
            "fields": ("name", "country"),
            "order_by": "name",
        },
        "client": {
            "fields": ("client_number", "name"),
            "order_by": "client_number",
        },
        "rate": {
            "fields": ("cargo_type",),
            "order_by": "cargo_type",
        }
    }

    form_choices = {
        "status": [
            ("planned", "Запланирована"),
            ("in_transit", "В пути"),
            ("delivered", "Доставлена")
        ]
    }

    column_labels = {
        "id": "ID",
        "shipment_code": "Код",
        "supplier": "Поставщик",
        "supplier_id": "Поставщик",
        "client": "Клиент",
        "client_id": "Клиент",
        "rate": "Тариф",
        "rate_id": "Тариф",
        "cargo_type": "Груз",
        "quantity": "Кол-во",
        "revenue": "Выручка",
        "total_expenses": "Расходы",
        "profit": "Прибыль",
        "margin_percent": "Маржа %",
        "status": "Статус",
        "departure_date": "Отправка",
        "arrival_date": "Прибытие",
        "created_at": "Создано",
        "updated_at": "Обновлено"
    }

    def _get_finance_data(self, model):
        """Helper to get finance data for a shipment"""
        from app.services.finance import calculate_shipment_finance
        from app.core.database import SessionLocal

        db = SessionLocal()
        try:
            return calculate_shipment_finance(model.id, db)
        except Exception:
            return {
                "revenue": 0,
                "cost_of_goods": 0,
                "total_expenses": 0,
                "profit": 0,
                "margin_percent": 0
            }
        finally:
            db.close()

    def _safe_shipment_supplier(model, attr):
        """Safely get supplier name with error handling"""
        try:
            return getattr(model.supplier, 'name', '—') if hasattr(model, 'supplier') and model.supplier else "—"
        except Exception:
            return "—"

    def _safe_shipment_client(model, attr):
        """Safely get client number with error handling"""
        try:
            return getattr(model.client, 'client_number', '—') if hasattr(model, 'client') and model.client else "—"
        except Exception:
            return "—"

    column_formatters = {
        Shipment.supplier_id: _safe_shipment_supplier,
        Shipment.client_id: _safe_shipment_client,
        "revenue": lambda m, a: f"${ShipmentAdmin._get_finance_data(None, m)['revenue']:.0f}",
        "total_expenses": lambda m, a: f"${ShipmentAdmin._get_finance_data(None, m)['total_expenses']:.0f}",
        "profit": lambda m, a: f"${ShipmentAdmin._get_finance_data(None, m)['profit']:.0f}",
        "margin_percent": lambda m, a: f"{ShipmentAdmin._get_finance_data(None, m)['margin_percent']:.1f}%"
    }

    column_type_formatters = {
        "status": lambda m, a: {
            "planned": "Запланирована",
            "in_transit": "В пути",
            "delivered": "Доставлена"
        }.get(m.status.value, m.status.value) if hasattr(m, 'status') and m.status else ""
    }

    def scaffold_list_query(self):
        """Override to eagerly load relationships"""
        stmt = select(self.model).options(
            selectinload(Shipment.supplier),
            selectinload(Shipment.client),
            selectinload(Shipment.rate)
        )
        return stmt


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
        Expense.shipment,
        Expense.expense_type,
        Expense.amount,
        Expense.currency,
        Expense.comment,
        Expense.expense_date
    ]

    form_ajax_refs = {
        "shipment": {
            "fields": ("shipment_code", "cargo_type"),
            "order_by": "shipment_code",
        }
    }

    form_choices = {
        "expense_type": [
            ("customs", "Таможня"),
            ("delivery", "Доставка"),
            ("agent_fee", "Агентский сбор"),
            ("warehouse", "Склад")
        ]
    }

    column_labels = {
        "id": "ID",
        "shipment": "Поставка",
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


class DashboardView(BaseView):
    name = "Дашборд"
    icon = "fa-solid fa-chart-line"

    @expose("/dashboard", methods=["GET"])
    async def dashboard_page(self, request: Request) -> Response:
        """Dashboard with statistics"""
        from app.api.dashboard import get_dashboard_stats
        from app.core.database import SessionLocal

        db = SessionLocal()
        try:
            stats = get_dashboard_stats(db)
        finally:
            db.close()

        # Generate HTML
        html = f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Dashboard - Cargo Logistics</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
                background: #f5f5f5;
                padding: 20px;
            }}
            .container {{
                max-width: 1400px;
                margin: 0 auto;
            }}
            .header {{
                background: white;
                padding: 30px;
                border-radius: 10px;
                margin-bottom: 20px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            .header h1 {{
                color: #333;
                font-size: 32px;
                margin-bottom: 5px;
            }}
            .header p {{
                color: #666;
                font-size: 14px;
            }}
            .stats-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin-bottom: 20px;
            }}
            .stat-card {{
                background: white;
                padding: 25px;
                border-radius: 10px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            .stat-card .label {{
                color: #666;
                font-size: 14px;
                margin-bottom: 10px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }}
            .stat-card .value {{
                font-size: 36px;
                font-weight: bold;
                color: #3b82f6;
                margin-bottom: 5px;
            }}
            .stat-card .subtext {{
                color: #999;
                font-size: 12px;
            }}
            .stat-card.positive .value {{
                color: #10b981;
            }}
            .stat-card.negative .value {{
                color: #ef4444;
            }}
            .section {{
                background: white;
                border-radius: 10px;
                padding: 30px;
                margin-bottom: 20px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            .section h2 {{
                color: #333;
                font-size: 24px;
                margin-bottom: 20px;
                padding-bottom: 15px;
                border-bottom: 2px solid #f0f0f0;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
            }}
            th {{
                background: #f8f9fa;
                padding: 15px;
                text-align: left;
                font-weight: 600;
                color: #333;
                border-bottom: 2px solid #e9ecef;
                font-size: 14px;
            }}
            td {{
                padding: 15px;
                border-bottom: 1px solid #e9ecef;
                color: #555;
            }}
            tr:hover {{
                background: #f8f9ff;
            }}
            .positive {{
                color: #10b981;
                font-weight: 600;
            }}
            .negative {{
                color: #ef4444;
                font-weight: 600;
            }}
            .badge {{
                display: inline-block;
                padding: 4px 12px;
                border-radius: 20px;
                font-size: 12px;
                font-weight: 600;
            }}
            .badge-success {{
                background: #d1fae5;
                color: #065f46;
            }}
            .badge-warning {{
                background: #fef3c7;
                color: #92400e;
            }}
            .badge-danger {{
                background: #fee2e2;
                color: #991b1b;
            }}
            .back-link {{
                display: inline-block;
                margin-bottom: 20px;
                padding: 10px 20px;
                background: #3b82f6;
                color: white;
                text-decoration: none;
                border-radius: 8px;
                font-weight: 500;
                transition: background 0.2s;
            }}
            .back-link:hover {{
                background: #2563eb;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <a href="/admin" class="back-link">← Вернуться в админку</a>

            <div class="header">
                <h1>📊 Dashboard</h1>
                <p>Общая статистика и финансовые показатели</p>
            </div>

            <!-- Общая статистика -->
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="label">Всего клиентов</div>
                    <div class="value">{stats['overview']['total_clients']}</div>
                    <div class="subtext">Активных клиентов в системе</div>
                </div>

                <div class="stat-card">
                    <div class="label">Всего поставок</div>
                    <div class="value">{stats['overview']['total_shipments']}</div>
                    <div class="subtext">Доставлено: {stats['overview']['delivered_count']}, В пути: {stats['overview']['in_transit_count']}</div>
                </div>

                <div class="stat-card {'positive' if stats['finance']['total_profit'] > 0 else 'negative'}">
                    <div class="label">Общая прибыль</div>
                    <div class="value">${stats['finance']['total_profit']:,.0f}</div>
                    <div class="subtext">Средняя маржа: {stats['finance']['avg_margin']:.1f}%</div>
                </div>

                <div class="stat-card">
                    <div class="label">Общая выручка</div>
                    <div class="value">${stats['finance']['total_revenue']:,.0f}</div>
                    <div class="subtext">Расходы: ${stats['finance']['total_expenses']:,.0f}</div>
                </div>
            </div>

            <!-- Детальная финансовая статистика -->
            <div class="section">
                <h2>💰 Финансовые показатели</h2>
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="label">Выручка</div>
                        <div class="value" style="color: #3b82f6;">${stats['finance']['total_revenue']:,.2f}</div>
                    </div>
                    <div class="stat-card">
                        <div class="label">Себестоимость</div>
                        <div class="value" style="color: #f59e0b;">${stats['finance']['total_cost']:,.2f}</div>
                    </div>
                    <div class="stat-card">
                        <div class="label">Расходы</div>
                        <div class="value" style="color: #ef4444;">${stats['finance']['total_expenses']:,.2f}</div>
                    </div>
                    <div class="stat-card {'positive' if stats['finance']['total_profit'] > 0 else 'negative'}">
                        <div class="label">Чистая прибыль</div>
                        <div class="value">${stats['finance']['total_profit']:,.2f}</div>
                        <div class="subtext">Маржа: {stats['finance']['avg_margin']:.1f}%</div>
                    </div>
                </div>
            </div>

            <!-- Статистика по клиентам -->
            <div class="section">
                <h2>👥 Статистика по клиентам</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Клиент</th>
                            <th>Имя / Компания</th>
                            <th>Поставок</th>
                            <th>Объем (кг)</th>
                            <th>Выручка</th>
                            <th>Прибыль</th>
                            <th>Маржа %</th>
                            <th>Статус</th>
                        </tr>
                    </thead>
                    <tbody>
    """

        for client in stats['clients']:
            profit_class = 'positive' if client['profit'] > 0 else 'negative'

            if client['margin_percent'] > 30:
                status_badge = 'badge-success'
                status_text = 'Отлично'
            elif client['margin_percent'] > 15:
                status_badge = 'badge-warning'
                status_text = 'Хорошо'
            else:
                status_badge = 'badge-danger'
                status_text = 'Низкая маржа'

            html += f"""
                        <tr>
                            <td><strong>{client['client_number']}</strong></td>
                            <td>
                                <strong>{client['name']}</strong><br>
                                <small style="color: #999;">{client['company']}</small>
                            </td>
                            <td>{client['shipments_count']}</td>
                            <td>{client['volume']:.0f} кг</td>
                            <td>${client['revenue']:,.0f}</td>
                            <td class="{profit_class}">${client['profit']:,.0f}</td>
                            <td class="{profit_class}">{client['margin_percent']:.1f}%</td>
                            <td><span class="badge {status_badge}">{status_text}</span></td>
                        </tr>
        """

        if not stats['clients']:
            html += """
                        <tr>
                            <td colspan="8" style="text-align: center; padding: 40px; color: #999;">
                                Нет данных по клиентам
                            </td>
                        </tr>
        """

        html += """
                    </tbody>
                </table>
            </div>

            <!-- Статистика по статусам поставок -->
            <div class="section">
                <h2>🚚 Статус поставок</h2>
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="label">Запланировано</div>
                        <div class="value" style="color: #3b82f6;">{}</div>
                        <div class="subtext">Ожидают отправки</div>
                    </div>
                    <div class="stat-card">
                        <div class="label">В пути</div>
                        <div class="value" style="color: #f59e0b;">{}</div>
                        <div class="subtext">Находятся в доставке</div>
                    </div>
                    <div class="stat-card">
                        <div class="label">Доставлено</div>
                        <div class="value" style="color: #10b981;">{}</div>
                        <div class="subtext">Успешно завершено</div>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """.format(
            stats['overview']['planned_count'],
            stats['overview']['in_transit_count'],
            stats['overview']['delivered_count']
        )

        return Response(content=html, media_type="text/html")

