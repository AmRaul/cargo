"""
Script to create initial data for testing the Cargo Logistics system.
Run this after running migrations: alembic upgrade head
"""
import sys
import uuid
from datetime import date, datetime, timedelta

from sqlalchemy.orm import Session

# Add parent directory to path to import app modules
sys.path.insert(0, ".")

from app.core.database import SessionLocal
from app.models.supplier import Supplier
from app.models.client import Client
from app.models.rate import Rate
from app.models.shipment import Shipment, ShipmentStatusEnum
from app.models.expense import Expense, ExpenseTypeEnum


def create_initial_data():
    db: Session = SessionLocal()

    try:
        print("Creating initial data...")

        # Create Suppliers
        supplier1 = Supplier(
            id=uuid.uuid4(),
            name="Shanghai Trading Co",
            country="China",
            city="Shanghai",
            contact_person="Li Wei",
            contact_info="Phone: +86-21-1234-5678, Email: li.wei@shanghai-trading.cn",
            notes="Main supplier for perfumes and cosmetics"
        )

        supplier2 = Supplier(
            id=uuid.uuid4(),
            name="Guangzhou Logistics",
            country="China",
            city="Guangzhou",
            contact_person="Wang Ming",
            contact_info="Phone: +86-20-9876-5432, Email: wang@guangzhou-log.cn",
            notes="Electronics and textiles"
        )

        db.add_all([supplier1, supplier2])
        db.commit()
        print(f"✓ Created {2} suppliers")

        # Create Clients
        client1 = Client(
            id=uuid.uuid4(),
            name="Ivan Petrov",
            company_name="Petrov Trading LLC",
            contact_person="Ivan Petrov",
            contact_info="Phone: +7-495-123-4567, Email: ivan@petrov-trading.ru",
            notes="Regular client, pays on time"
        )

        client2 = Client(
            id=uuid.uuid4(),
            name="Anna Sidorova",
            company_name="Sidorova Import",
            contact_person="Anna Sidorova",
            contact_info="Phone: +7-812-765-4321, Email: anna@sidorova-import.ru",
            notes="Large volumes, needs special rates"
        )

        db.add_all([client1, client2])
        db.commit()
        print(f"✓ Created {2} clients")

        # Create Rates
        rate1 = Rate(
            id=uuid.uuid4(),
            cargo_type="perfumes",
            supplier_id=supplier1.id,
            client_id=client1.id,
            buy_rate=1.78,
            sell_rate=2.10,
            currency="USD",
            unit="kg",
            valid_from=date(2024, 1, 1),
            valid_to=date(2024, 12, 31)
        )

        rate2 = Rate(
            id=uuid.uuid4(),
            cargo_type="electronics",
            supplier_id=supplier2.id,
            client_id=client2.id,
            buy_rate=1.50,
            sell_rate=1.95,
            currency="USD",
            unit="kg",
            valid_from=date(2024, 1, 1),
            valid_to=date(2024, 12, 31)
        )

        rate3 = Rate(
            id=uuid.uuid4(),
            cargo_type="textiles",
            supplier_id=supplier2.id,
            client_id=None,  # General rate
            buy_rate=0.80,
            sell_rate=1.20,
            currency="USD",
            unit="kg",
            valid_from=date(2024, 1, 1),
            valid_to=date(2024, 12, 31)
        )

        db.add_all([rate1, rate2, rate3])
        db.commit()
        print(f"✓ Created {3} rates")

        # Create Shipments
        shipment1 = Shipment(
            id=uuid.uuid4(),
            shipment_code="CN-RU-001",
            supplier_id=supplier1.id,
            client_id=client1.id,
            rate_id=rate1.id,
            cargo_type="perfumes",
            quantity=500.0,  # 500 kg
            departure_date=date(2024, 11, 15),
            arrival_date=date(2024, 12, 10),
            status=ShipmentStatusEnum.DELIVERED
        )

        shipment2 = Shipment(
            id=uuid.uuid4(),
            shipment_code="CN-RU-002",
            supplier_id=supplier2.id,
            client_id=client2.id,
            rate_id=rate2.id,
            cargo_type="electronics",
            quantity=1200.0,  # 1200 kg
            departure_date=date(2024, 12, 1),
            arrival_date=date(2024, 12, 25),
            status=ShipmentStatusEnum.IN_TRANSIT
        )

        shipment3 = Shipment(
            id=uuid.uuid4(),
            shipment_code="CN-RU-003",
            supplier_id=supplier2.id,
            client_id=client1.id,
            rate_id=rate3.id,
            cargo_type="textiles",
            quantity=800.0,  # 800 kg
            departure_date=date(2024, 12, 20),
            arrival_date=None,
            status=ShipmentStatusEnum.PLANNED
        )

        db.add_all([shipment1, shipment2, shipment3])
        db.commit()
        print(f"✓ Created {3} shipments")

        # Create Expenses
        expense1 = Expense(
            id=uuid.uuid4(),
            shipment_id=shipment1.id,
            expense_type=ExpenseTypeEnum.CUSTOMS,
            amount=150.0,
            currency="USD",
            comment="Customs clearance in Russia",
            expense_date=date(2024, 12, 11)
        )

        expense2 = Expense(
            id=uuid.uuid4(),
            shipment_id=shipment1.id,
            expense_type=ExpenseTypeEnum.DELIVERY,
            amount=80.0,
            currency="USD",
            comment="Delivery to Moscow",
            expense_date=date(2024, 12, 12)
        )

        expense3 = Expense(
            id=uuid.uuid4(),
            shipment_id=shipment2.id,
            expense_type=ExpenseTypeEnum.WAREHOUSE,
            amount=200.0,
            currency="USD",
            comment="Warehouse storage (10 days)",
            expense_date=date(2024, 12, 5)
        )

        expense4 = Expense(
            id=uuid.uuid4(),
            shipment_id=shipment2.id,
            expense_type=ExpenseTypeEnum.AGENT_FEE,
            amount=120.0,
            currency="USD",
            comment="Agent fee in Shanghai",
            expense_date=date(2024, 12, 2)
        )

        db.add_all([expense1, expense2, expense3, expense4])
        db.commit()
        print(f"✓ Created {4} expenses")

        print("\n✅ Initial data created successfully!")
        print("\nSummary:")
        print(f"  - Suppliers: 2")
        print(f"  - Clients: 2")
        print(f"  - Rates: 3")
        print(f"  - Shipments: 3")
        print(f"  - Expenses: 4")
        print("\nYou can now:")
        print("  1. Start the server: uvicorn app.main:app --reload")
        print("  2. Access admin panel: http://localhost:8000/admin")
        print("  3. Access API docs: http://localhost:8000/docs")

    except Exception as e:
        print(f"❌ Error creating initial data: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    create_initial_data()
