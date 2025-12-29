"""
Скрипт для создания тестовых данных

Запуск:
cd backend
python -m scripts.seed_test_data
"""

from datetime import date, datetime, timedelta
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.supplier import Supplier
from app.models.client import Client
from app.models.rate import Rate
from app.models.shipment import Shipment
from app.models.expense import Expense


def clear_all_data(db: Session):
    """Удалить все тестовые данные"""
    print("🗑️  Очистка существующих данных...")
    db.query(Expense).delete()
    db.query(Shipment).delete()
    db.query(Rate).delete()
    db.query(Client).delete()
    db.query(Supplier).delete()
    db.commit()
    print("✅ Данные очищены")


def create_suppliers(db: Session):
    """Создать поставщиков"""
    print("\n📦 Создание поставщиков...")

    suppliers = [
        Supplier(
            name="Guangzhou Trading Co",
            country="China",
            city="Guangzhou",
            contact_person="Wang Li",
            contact_info="Email: wang@gtc.cn\nPhone: +86 20 1234 5678",
            notes="Основной поставщик из Китая. Работаем 3 года."
        ),
        Supplier(
            name="Istanbul Logistics",
            country="Turkey",
            city="Istanbul",
            contact_person="Mehmet Yılmaz",
            contact_info="Email: mehmet@istlog.tr\nPhone: +90 212 555 0123",
            notes="Турецкий партнер. Быстрая доставка."
        ),
        Supplier(
            name="Shenzhen Factory Direct",
            country="China",
            city="Shenzhen",
            contact_person="Chen Wei",
            contact_info="Email: chen@szfd.com\nPhone: +86 755 8888 9999",
            notes="Прямой завод. Низкие цены на электронику."
        )
    ]

    for supplier in suppliers:
        db.add(supplier)

    db.commit()

    for supplier in suppliers:
        db.refresh(supplier)

    print(f"✅ Создано поставщиков: {len(suppliers)}")
    return suppliers


def create_clients(db: Session):
    """Создать клиентов"""
    print("\n👥 Создание клиентов...")

    clients = [
        Client(
            client_number="CL-0001",
            name="Иван Петров",
            company_name="ИП Петров И.И.",
            contact_person="Иван Петров",
            contact_info="Телефон: +7 903 123-45-67\nEmail: ivanov@mail.ru",
            notes="VIP клиент. Работаем 2 года. Высокая маржа."
        ),
        Client(
            client_number="CL-0002",
            name="Мария Сидорова",
            company_name="ООО Импорт Плюс",
            contact_person="Мария Сидорова",
            contact_info="Телефон: +7 905 987-65-43\nEmail: sidorova@import.ru",
            notes="Большие объемы, низкая маржа"
        ),
        Client(
            client_number="CL-0003",
            name="Алексей Смирнов",
            company_name="Смирнов Трейд",
            contact_person="Алексей Смирнов",
            contact_info="Телефон: +7 916 555-11-22\nEmail: smirnov@trade.ru",
            notes="Новый клиент. Тестовый период."
        ),
        Client(
            client_number="CL-0004",
            name="Елена Козлова",
            company_name="ООО Парфюм Опт",
            contact_person="Елена Козлова",
            contact_info="Телефон: +7 926 777-88-99\nEmail: kozlova@parfum.ru",
            notes="Специализируется на духах и косметике"
        )
    ]

    for client in clients:
        db.add(client)

    db.commit()

    for client in clients:
        db.refresh(client)

    print(f"✅ Создано клиентов: {len(clients)}")
    return clients


def create_rates(db: Session, suppliers, clients):
    """Создать тарифы"""
    print("\n💰 Создание тарифов...")

    guangzhou = suppliers[0]
    istanbul = suppliers[1]
    shenzhen = suppliers[2]

    petrov = clients[0]
    sidorova = clients[1]
    smirnov = clients[2]
    kozlova = clients[3]

    rates = [
        # Духи из Китая
        Rate(
            cargo_type="Духи",
            supplier_id=guangzhou.id,
            client_id=petrov.id,
            buy_rate=1.78,
            sell_rate=2.50,  # Маржа 0.72
            currency="USD",
            unit="kg",
            valid_from=date(2024, 1, 1),
            valid_to=date(2024, 12, 31)
        ),
        Rate(
            cargo_type="Духи",
            supplier_id=guangzhou.id,
            client_id=kozlova.id,
            buy_rate=1.78,
            sell_rate=2.10,  # Маржа 0.32 (низкая)
            currency="USD",
            unit="kg",
            valid_from=date(2024, 1, 1),
            valid_to=date(2024, 12, 31)
        ),

        # Одежда из Китая
        Rate(
            cargo_type="Одежда",
            supplier_id=guangzhou.id,
            client_id=sidorova.id,
            buy_rate=2.00,
            sell_rate=2.80,  # Маржа 0.80
            currency="USD",
            unit="kg",
            valid_from=date(2024, 1, 1),
            valid_to=date(2024, 12, 31)
        ),

        # Электроника из Shenzhen
        Rate(
            cargo_type="Электроника",
            supplier_id=shenzhen.id,
            client_id=smirnov.id,
            buy_rate=3.50,
            sell_rate=5.00,  # Маржа 1.50 (высокая)
            currency="USD",
            unit="kg",
            valid_from=date(2024, 1, 1),
            valid_to=date(2024, 12, 31)
        ),

        # Текстиль из Турции
        Rate(
            cargo_type="Текстиль",
            supplier_id=istanbul.id,
            client_id=sidorova.id,
            buy_rate=1.50,
            sell_rate=2.20,  # Маржа 0.70
            currency="USD",
            unit="kg",
            valid_from=date(2024, 1, 1),
            valid_to=date(2024, 12, 31)
        ),

        # Косметика из Китая
        Rate(
            cargo_type="Косметика",
            supplier_id=guangzhou.id,
            client_id=kozlova.id,
            buy_rate=2.20,
            sell_rate=3.00,  # Маржа 0.80
            currency="USD",
            unit="kg",
            valid_from=date(2024, 1, 1),
            valid_to=date(2024, 12, 31)
        )
    ]

    for rate in rates:
        db.add(rate)

    db.commit()

    for rate in rates:
        db.refresh(rate)

    print(f"✅ Создано тарифов: {len(rates)}")
    return rates


def create_shipments(db: Session, rates):
    """Создать поставки"""
    print("\n🚚 Создание поставок...")

    today = date.today()

    shipments = [
        # Поставка 1: Духи Петрову (прибыльная, доставлена)
        Shipment(
            shipment_code="CN-RU-001",
            supplier_id=rates[0].supplier_id,
            client_id=rates[0].client_id,
            rate_id=rates[0].id,
            cargo_type="Духи",
            quantity=150.0,  # 150 кг
            departure_date=today - timedelta(days=20),
            arrival_date=today - timedelta(days=5),
            status="delivered"
        ),

        # Поставка 2: Духи Козловой (низкая маржа, в пути)
        Shipment(
            shipment_code="CN-RU-002",
            supplier_id=rates[1].supplier_id,
            client_id=rates[1].client_id,
            rate_id=rates[1].id,
            cargo_type="Духи",
            quantity=200.0,  # 200 кг
            departure_date=today - timedelta(days=10),
            arrival_date=today + timedelta(days=5),
            status="in_transit"
        ),

        # Поставка 3: Одежда Сидоровой (большой объем, доставлена)
        Shipment(
            shipment_code="CN-RU-003",
            supplier_id=rates[2].supplier_id,
            client_id=rates[2].client_id,
            rate_id=rates[2].id,
            cargo_type="Одежда",
            quantity=500.0,  # 500 кг
            departure_date=today - timedelta(days=30),
            arrival_date=today - timedelta(days=10),
            status="delivered"
        ),

        # Поставка 4: Электроника Смирнову (высокая маржа, запланирована)
        Shipment(
            shipment_code="CN-RU-004",
            supplier_id=rates[3].supplier_id,
            client_id=rates[3].client_id,
            rate_id=rates[3].id,
            cargo_type="Электроника",
            quantity=80.0,  # 80 кг
            departure_date=today + timedelta(days=5),
            arrival_date=today + timedelta(days=20),
            status="planned"
        ),

        # Поставка 5: Текстиль из Турции (в пути)
        Shipment(
            shipment_code="TR-RU-001",
            supplier_id=rates[4].supplier_id,
            client_id=rates[4].client_id,
            rate_id=rates[4].id,
            cargo_type="Текстиль",
            quantity=300.0,  # 300 кг
            departure_date=today - timedelta(days=7),
            arrival_date=today + timedelta(days=3),
            status="in_transit"
        ),

        # Поставка 6: Косметика Козловой (доставлена)
        Shipment(
            shipment_code="CN-RU-005",
            supplier_id=rates[5].supplier_id,
            client_id=rates[5].client_id,
            rate_id=rates[5].id,
            cargo_type="Косметика",
            quantity=120.0,  # 120 кг
            departure_date=today - timedelta(days=25),
            arrival_date=today - timedelta(days=8),
            status="delivered"
        ),

        # Поставка 7: Еще одежда Сидоровой (запланирована)
        Shipment(
            shipment_code="CN-RU-006",
            supplier_id=rates[2].supplier_id,
            client_id=rates[2].client_id,
            rate_id=rates[2].id,
            cargo_type="Одежда",
            quantity=450.0,  # 450 кг
            departure_date=today + timedelta(days=10),
            arrival_date=today + timedelta(days=25),
            status="planned"
        )
    ]

    for shipment in shipments:
        db.add(shipment)

    db.commit()

    for shipment in shipments:
        db.refresh(shipment)

    print(f"✅ Создано поставок: {len(shipments)}")
    return shipments


def create_expenses(db: Session, shipments):
    """Создать расходы"""
    print("\n💸 Создание расходов...")

    expenses = []

    # Расходы для CN-RU-001 (Духи Петрову)
    expenses.extend([
        Expense(
            shipment_id=shipments[0].id,
            expense_type="customs",
            amount=120.0,
            currency="USD",
            comment="Таможенное оформление",
            expense_date=shipments[0].arrival_date
        ),
        Expense(
            shipment_id=shipments[0].id,
            expense_type="warehouse",
            amount=30.0,
            currency="USD",
            comment="Хранение на складе 2 дня",
            expense_date=shipments[0].arrival_date + timedelta(days=1)
        ),
        Expense(
            shipment_id=shipments[0].id,
            expense_type="agent_fee",
            amount=50.0,
            currency="USD",
            comment="Агентское вознаграждение",
            expense_date=shipments[0].arrival_date
        )
    ])

    # Расходы для CN-RU-002 (Духи Козловой)
    expenses.extend([
        Expense(
            shipment_id=shipments[1].id,
            expense_type="customs",
            amount=180.0,
            currency="USD",
            comment="Таможня (больший объем)",
            expense_date=date.today()
        )
    ])

    # Расходы для CN-RU-003 (Одежда Сидоровой - большой объем)
    expenses.extend([
        Expense(
            shipment_id=shipments[2].id,
            expense_type="customs",
            amount=350.0,
            currency="USD",
            comment="Таможенное оформление",
            expense_date=shipments[2].arrival_date
        ),
        Expense(
            shipment_id=shipments[2].id,
            expense_type="warehouse",
            amount=100.0,
            currency="USD",
            comment="Хранение 5 дней",
            expense_date=shipments[2].arrival_date + timedelta(days=2)
        ),
        Expense(
            shipment_id=shipments[2].id,
            expense_type="delivery",
            amount=80.0,
            currency="USD",
            comment="Доставка до клиента",
            expense_date=shipments[2].arrival_date + timedelta(days=5)
        ),
        Expense(
            shipment_id=shipments[2].id,
            expense_type="agent_fee",
            amount=70.0,
            currency="USD",
            comment="Комиссия агента",
            expense_date=shipments[2].arrival_date
        )
    ])

    # Расходы для TR-RU-001 (Текстиль)
    expenses.extend([
        Expense(
            shipment_id=shipments[4].id,
            expense_type="customs",
            amount=200.0,
            currency="USD",
            comment="Таможня Турция",
            expense_date=date.today()
        ),
        Expense(
            shipment_id=shipments[4].id,
            expense_type="agent_fee",
            amount=60.0,
            currency="USD",
            comment="Турецкий агент",
            expense_date=date.today() - timedelta(days=3)
        )
    ])

    # Расходы для CN-RU-005 (Косметика)
    expenses.extend([
        Expense(
            shipment_id=shipments[5].id,
            expense_type="customs",
            amount=90.0,
            currency="USD",
            comment="Таможня",
            expense_date=shipments[5].arrival_date
        ),
        Expense(
            shipment_id=shipments[5].id,
            expense_type="warehouse",
            amount=25.0,
            currency="USD",
            comment="Склад",
            expense_date=shipments[5].arrival_date + timedelta(days=1)
        )
    ])

    for expense in expenses:
        db.add(expense)

    db.commit()

    print(f"✅ Создано расходов: {len(expenses)}")
    return expenses


def print_summary(db: Session):
    """Вывести статистику"""
    print("\n" + "="*60)
    print("📊 СТАТИСТИКА СОЗДАННЫХ ДАННЫХ")
    print("="*60)

    suppliers_count = db.query(Supplier).count()
    clients_count = db.query(Client).count()
    rates_count = db.query(Rate).count()
    shipments_count = db.query(Shipment).count()
    expenses_count = db.query(Expense).count()

    print(f"\n📦 Поставщики: {suppliers_count}")
    print(f"👥 Клиенты: {clients_count}")
    print(f"💰 Тарифы: {rates_count}")
    print(f"🚚 Поставки: {shipments_count}")
    print(f"💸 Расходы: {expenses_count}")

    # Статистика по поставкам
    delivered = db.query(Shipment).filter(Shipment.status == "delivered").count()
    in_transit = db.query(Shipment).filter(Shipment.status == "in_transit").count()
    planned = db.query(Shipment).filter(Shipment.status == "planned").count()

    print(f"\n📊 Статусы поставок:")
    print(f"   ✅ Доставлено: {delivered}")
    print(f"   🚛 В пути: {in_transit}")
    print(f"   📅 Запланировано: {planned}")

    print("\n" + "="*60)
    print("✅ Все данные успешно созданы!")
    print("="*60)
    print("\n🌐 Откройте админку: http://localhost:8000/admin")
    print("   Логин: admin")
    print("   Пароль: из ADMIN_PASSWORD в .env")
    print("\n")


def main():
    """Основная функция"""
    print("="*60)
    print("🚀 СОЗДАНИЕ ТЕСТОВЫХ ДАННЫХ")
    print("="*60)

    db = SessionLocal()

    try:
        # Очистка
        clear_all_data(db)

        # Создание данных
        suppliers = create_suppliers(db)
        clients = create_clients(db)
        rates = create_rates(db, suppliers, clients)
        shipments = create_shipments(db, rates)
        expenses = create_expenses(db, shipments)

        # Статистика
        print_summary(db)

    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
