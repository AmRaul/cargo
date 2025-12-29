from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date, datetime, timedelta
from typing import List, Dict
from uuid import UUID

from app.core.database import get_db
from app.models.client import Client
from app.models.supplier import Supplier
from app.models.shipment import Shipment
from app.models.expense import Expense
from app.models.rate import Rate
from app.services.finance import calculate_shipment_finance

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


def get_dashboard_stats(db: Session) -> Dict:
    """Get overall dashboard statistics"""

    # Общая статистика
    total_clients = db.query(Client).count()
    total_suppliers = db.query(Supplier).count()
    total_shipments = db.query(Shipment).count()

    # Статистика по поставкам
    delivered_count = db.query(Shipment).filter(Shipment.status == "delivered").count()
    in_transit_count = db.query(Shipment).filter(Shipment.status == "in_transit").count()
    planned_count = db.query(Shipment).filter(Shipment.status == "planned").count()

    # Финансовая статистика
    all_shipments = db.query(Shipment).all()

    total_revenue = 0
    total_cost = 0
    total_expenses = 0
    total_profit = 0

    for shipment in all_shipments:
        try:
            finance = calculate_shipment_finance(shipment.id, db)
            total_revenue += finance["revenue"]
            total_cost += finance["cost_of_goods"]
            total_expenses += finance["total_expenses"]
            total_profit += finance["profit"]
        except Exception:
            continue

    avg_margin = (total_profit / total_revenue * 100) if total_revenue > 0 else 0

    # Статистика по клиентам
    clients_stats = []
    clients = db.query(Client).all()

    for client in clients:
        client_shipments = db.query(Shipment).filter(Shipment.client_id == client.id).all()

        if not client_shipments:
            continue

        client_revenue = 0
        client_profit = 0
        client_volume = 0

        for shipment in client_shipments:
            try:
                finance = calculate_shipment_finance(shipment.id, db)
                client_revenue += finance["revenue"]
                client_profit += finance["profit"]
                client_volume += shipment.quantity
            except Exception:
                continue

        client_margin = (client_profit / client_revenue * 100) if client_revenue > 0 else 0

        clients_stats.append({
            "client_number": client.client_number,
            "name": client.name,
            "company": client.company_name or "—",
            "shipments_count": len(client_shipments),
            "volume": client_volume,
            "revenue": client_revenue,
            "profit": client_profit,
            "margin_percent": client_margin
        })

    # Сортировка клиентов по прибыли
    clients_stats.sort(key=lambda x: x["profit"], reverse=True)

    return {
        "overview": {
            "total_clients": total_clients,
            "total_suppliers": total_suppliers,
            "total_shipments": total_shipments,
            "delivered_count": delivered_count,
            "in_transit_count": in_transit_count,
            "planned_count": planned_count
        },
        "finance": {
            "total_revenue": total_revenue,
            "total_cost": total_cost,
            "total_expenses": total_expenses,
            "total_profit": total_profit,
            "avg_margin": avg_margin
        },
        "clients": clients_stats
    }


@router.get("/", response_class=HTMLResponse)
def dashboard_page(db: Session = Depends(get_db)):
    """Dashboard HTML page"""

    stats = get_dashboard_stats(db)

    # Генерация HTML
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
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }}
            .container {{
                max-width: 1400px;
                margin: 0 auto;
            }}
            .header {{
                background: white;
                padding: 30px;
                border-radius: 15px;
                margin-bottom: 20px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            }}
            .header h1 {{
                color: #667eea;
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
                border-radius: 15px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
                transition: transform 0.2s;
            }}
            .stat-card:hover {{
                transform: translateY(-5px);
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
                color: #667eea;
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
                border-radius: 15px;
                padding: 30px;
                margin-bottom: 20px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
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
                margin-bottom: 15px;
                color: white;
                text-decoration: none;
                padding: 10px 20px;
                background: rgba(255,255,255,0.2);
                border-radius: 8px;
                transition: all 0.2s;
            }}
            .back-link:hover {{
                background: rgba(255,255,255,0.3);
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
                        <div class="value" style="color: #667eea;">${stats['finance']['total_revenue']:,.2f}</div>
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

    return html


@router.get("/stats")
def dashboard_stats_api(db: Session = Depends(get_db)):
    """Get dashboard statistics as JSON"""
    return get_dashboard_stats(db)
