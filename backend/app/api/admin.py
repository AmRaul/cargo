from fastapi import APIRouter, Depends, Request, HTTPException, Header
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.config import settings
from app.models.order import Order, OrderStatusEnum
import base64

router = APIRouter(prefix="/admin", tags=["admin"])


def check_auth(authorization: str = Header(None)):
    """Проверка Basic Auth для админки"""
    if not authorization:
        return False

    try:
        scheme, credentials = authorization.split()
        if scheme.lower() != 'basic':
            return False

        decoded = base64.b64decode(credentials).decode('utf-8')
        username, password = decoded.split(':')

        return username == "admin" and password == settings.ADMIN_PASSWORD
    except:
        return False


@router.get("/", response_class=HTMLResponse)
def admin_dashboard(authorization: str = Header(None), db: Session = Depends(get_db)):
    """Простая админ панель для просмотра заявок"""

    # Проверка авторизации
    if not check_auth(authorization):
        return HTMLResponse(
            content="",
            status_code=401,
            headers={"WWW-Authenticate": "Basic realm=\"Admin Panel\""}
        )

    orders = db.query(Order).order_by(Order.created_at.desc()).all()

    # Генерация HTML
    html = """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Админ панель - Cargo Express</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }
            .container {
                max-width: 1400px;
                margin: 0 auto;
            }
            .header {
                background: white;
                padding: 30px;
                border-radius: 15px;
                margin-bottom: 20px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            }
            .header h1 {
                color: #667eea;
                font-size: 32px;
                margin-bottom: 10px;
            }
            .stats {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
                margin-bottom: 20px;
            }
            .stat-card {
                background: white;
                padding: 20px;
                border-radius: 15px;
                text-align: center;
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            }
            .stat-card .number {
                font-size: 36px;
                font-weight: bold;
                color: #667eea;
                margin-bottom: 5px;
            }
            .stat-card .label {
                color: #666;
                font-size: 14px;
            }
            .orders-container {
                background: white;
                border-radius: 15px;
                padding: 30px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                overflow-x: auto;
            }
            .orders-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 20px;
            }
            .orders-header h2 {
                color: #333;
                font-size: 24px;
            }
            .refresh-btn {
                background: #667eea;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 8px;
                cursor: pointer;
                font-size: 14px;
                font-weight: 600;
                transition: all 0.3s;
            }
            .refresh-btn:hover {
                background: #5568d3;
                transform: translateY(-2px);
            }
            table {
                width: 100%;
                border-collapse: collapse;
                min-width: 1000px;
            }
            th {
                background: #f8f9fa;
                padding: 15px;
                text-align: left;
                font-weight: 600;
                color: #333;
                border-bottom: 2px solid #e9ecef;
                position: sticky;
                top: 0;
            }
            td {
                padding: 15px;
                border-bottom: 1px solid #e9ecef;
                color: #555;
            }
            tr:hover {
                background: #f8f9ff;
            }
            .status-badge {
                display: inline-block;
                padding: 6px 12px;
                border-radius: 20px;
                font-size: 12px;
                font-weight: 600;
                text-transform: uppercase;
            }
            .status-new { background: #e3f2fd; color: #1976d2; }
            .status-in_progress { background: #fff3e0; color: #f57c00; }
            .status-completed { background: #e8f5e9; color: #388e3c; }
            .status-cancelled { background: #ffebee; color: #d32f2f; }
            .route-badge {
                display: inline-block;
                padding: 6px 12px;
                border-radius: 8px;
                font-size: 12px;
                font-weight: 600;
                background: #f0f0f0;
                color: #333;
            }
            .no-orders {
                text-align: center;
                padding: 60px 20px;
                color: #999;
            }
            .no-orders .icon {
                font-size: 64px;
                margin-bottom: 20px;
            }
            .action-btn {
                background: #667eea;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 6px;
                cursor: pointer;
                font-size: 12px;
                margin-right: 5px;
                transition: all 0.2s;
            }
            .action-btn:hover {
                background: #5568d3;
            }
            .delete-btn {
                background: #ef5350;
            }
            .delete-btn:hover {
                background: #d32f2f;
            }
            .email-link {
                color: #667eea;
                text-decoration: none;
            }
            .email-link:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📦 Админ панель Cargo Express</h1>
                <p style="color: #666; margin-top: 5px;">Управление заявками на грузоперевозки</p>
            </div>

            <div class="stats">
    """

    # Подсчет статистики
    total = len(orders)
    new_count = sum(1 for o in orders if o.status == OrderStatusEnum.NEW)
    in_progress = sum(1 for o in orders if o.status == OrderStatusEnum.IN_PROGRESS)
    completed = sum(1 for o in orders if o.status == OrderStatusEnum.COMPLETED)

    html += f"""
                <div class="stat-card">
                    <div class="number">{total}</div>
                    <div class="label">Всего заявок</div>
                </div>
                <div class="stat-card">
                    <div class="number">{new_count}</div>
                    <div class="label">Новые</div>
                </div>
                <div class="stat-card">
                    <div class="number">{in_progress}</div>
                    <div class="label">В работе</div>
                </div>
                <div class="stat-card">
                    <div class="number">{completed}</div>
                    <div class="label">Завершено</div>
                </div>
            </div>

            <div class="orders-container">
                <div class="orders-header">
                    <h2>Список заявок</h2>
                    <button class="refresh-btn" onclick="location.reload()">🔄 Обновить</button>
                </div>
    """

    if not orders:
        html += """
                <div class="no-orders">
                    <div class="icon">📭</div>
                    <h3>Заявок пока нет</h3>
                    <p>Новые заявки появятся здесь автоматически</p>
                </div>
        """
    else:
        html += """
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Дата</th>
                            <th>Клиент</th>
                            <th>Контакты</th>
                            <th>Маршрут</th>
                            <th>Груз</th>
                            <th>Вес/Объем</th>
                            <th>Статус</th>
                            <th>Действия</th>
                        </tr>
                    </thead>
                    <tbody>
        """

        for order in orders:
            status_class = f"status-{order.status.value}"
            status_text = {
                'new': 'Новая',
                'in_progress': 'В работе',
                'completed': 'Завершена',
                'cancelled': 'Отменена'
            }.get(order.status.value, order.status.value)

            route_text = {
                'uae_to_rf': '🇦🇪 ОАЭ → РФ',
                'turkey_to_rf': '🇹🇷 Турция → РФ'
            }.get(order.route.value, order.route.value)

            created = order.created_at.strftime('%d.%m.%Y %H:%M') if order.created_at else '-'

            weight_vol = []
            if order.cargo_weight:
                weight_vol.append(f"{order.cargo_weight} кг")
            if order.cargo_volume:
                weight_vol.append(f"{order.cargo_volume} м³")
            weight_vol_text = " / ".join(weight_vol) if weight_vol else "-"

            html += f"""
                        <tr>
                            <td><strong>#{order.id}</strong></td>
                            <td>{created}</td>
                            <td>
                                <strong>{order.client_name}</strong>
                                {f'<br><small>{order.company_name}</small>' if order.company_name else ''}
                            </td>
                            <td>
                                📞 {order.client_phone}<br>
                                {f'<a href="mailto:{order.client_email}" class="email-link">✉️ {order.client_email}</a>' if order.client_email else ''}
                            </td>
                            <td><span class="route-badge">{route_text}</span></td>
                            <td>{order.cargo_type}</td>
                            <td>{weight_vol_text}</td>
                            <td><span class="status-badge {status_class}">{status_text}</span></td>
                            <td>
                                <button class="action-btn" onclick="viewDetails({order.id})">👁️ Детали</button>
                            </td>
                        </tr>
            """

        html += """
                    </tbody>
                </table>
        """

    html += """
            </div>
        </div>

        <script>
            function viewDetails(orderId) {
                window.open('/api/v1/orders/' + orderId, '_blank');
            }

            // Автообновление каждые 30 секунд
            setTimeout(() => location.reload(), 30000);
        </script>
    </body>
    </html>
    """

    return html
