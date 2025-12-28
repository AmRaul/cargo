from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.shipment import Shipment
from app.models.expense import Expense
from app.models.rate import Rate
from typing import Dict
from uuid import UUID


def calculate_shipment_finance(shipment_id: UUID, db: Session) -> Dict[str, float]:
    """
    Calculate financial metrics for a shipment.

    Returns:
        dict with keys: revenue, cost_of_goods, total_expenses, profit, margin_percent
    """
    # Get shipment with rate
    shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()

    if not shipment:
        raise ValueError(f"Shipment {shipment_id} not found")

    # Get rate
    rate = db.query(Rate).filter(Rate.id == shipment.rate_id).first()

    if not rate:
        raise ValueError(f"Rate {shipment.rate_id} not found")

    # Calculate revenue = quantity × sell_rate
    revenue = shipment.quantity * rate.sell_rate

    # Calculate cost of goods = quantity × buy_rate
    cost_of_goods = shipment.quantity * rate.buy_rate

    # Calculate total expenses
    total_expenses_result = db.query(func.sum(Expense.amount))\
        .filter(Expense.shipment_id == shipment_id)\
        .scalar()

    total_expenses = total_expenses_result if total_expenses_result else 0.0

    # Calculate profit = revenue - cost_of_goods - total_expenses
    profit = revenue - cost_of_goods - total_expenses

    # Calculate margin % = (profit / revenue) × 100
    margin_percent = (profit / revenue * 100) if revenue > 0 else 0.0

    return {
        "revenue": round(revenue, 2),
        "cost_of_goods": round(cost_of_goods, 2),
        "total_expenses": round(total_expenses, 2),
        "profit": round(profit, 2),
        "margin_percent": round(margin_percent, 2)
    }


def calculate_shipment_with_finance(shipment: Shipment, db: Session) -> Dict:
    """
    Return shipment data with financial calculations.

    Args:
        shipment: Shipment model instance
        db: Database session

    Returns:
        dict with shipment data and financial metrics
    """
    finance = calculate_shipment_finance(shipment.id, db)

    return {
        "id": shipment.id,
        "shipment_code": shipment.shipment_code,
        "supplier_id": shipment.supplier_id,
        "client_id": shipment.client_id,
        "rate_id": shipment.rate_id,
        "cargo_type": shipment.cargo_type,
        "quantity": shipment.quantity,
        "departure_date": shipment.departure_date,
        "arrival_date": shipment.arrival_date,
        "status": shipment.status,
        "created_at": shipment.created_at,
        "updated_at": shipment.updated_at,
        **finance
    }
