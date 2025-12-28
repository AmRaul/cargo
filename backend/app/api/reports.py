from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from datetime import date
from uuid import UUID
from app.core.database import get_db
from app.models.shipment import Shipment
from app.models.expense import Expense
from app.models.rate import Rate
from app.services.finance import calculate_shipment_finance

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/summary")
def get_summary_report(
    date_from: Optional[date] = Query(None, description="Start date (inclusive)"),
    date_to: Optional[date] = Query(None, description="End date (inclusive)"),
    db: Session = Depends(get_db)
):
    """
    Get financial summary report for a period.
    Returns: total revenue, total profit, average margin
    """
    query = db.query(Shipment)

    # Filter by date range if provided
    if date_from:
        query = query.filter(Shipment.created_at >= date_from)
    if date_to:
        query = query.filter(Shipment.created_at <= date_to)

    shipments = query.all()

    total_revenue = 0.0
    total_cost = 0.0
    total_expenses = 0.0
    total_profit = 0.0

    shipment_count = len(shipments)

    for shipment in shipments:
        try:
            finance = calculate_shipment_finance(shipment.id, db)
            total_revenue += finance["revenue"]
            total_cost += finance["cost_of_goods"]
            total_expenses += finance["total_expenses"]
            total_profit += finance["profit"]
        except Exception:
            continue

    avg_margin = (total_profit / total_revenue * 100) if total_revenue > 0 else 0.0

    return {
        "period": {
            "from": date_from.isoformat() if date_from else None,
            "to": date_to.isoformat() if date_to else None
        },
        "shipments_count": shipment_count,
        "total_revenue": round(total_revenue, 2),
        "total_cost_of_goods": round(total_cost, 2),
        "total_expenses": round(total_expenses, 2),
        "total_profit": round(total_profit, 2),
        "average_margin_percent": round(avg_margin, 2)
    }


@router.get("/by-client/{client_id}")
def get_client_report(
    client_id: UUID,
    date_from: Optional[date] = Query(None, description="Start date (inclusive)"),
    date_to: Optional[date] = Query(None, description="End date (inclusive)"),
    db: Session = Depends(get_db)
):
    """
    Get report by client: total volume, profit, etc.
    """
    query = db.query(Shipment).filter(Shipment.client_id == client_id)

    # Filter by date range if provided
    if date_from:
        query = query.filter(Shipment.created_at >= date_from)
    if date_to:
        query = query.filter(Shipment.created_at <= date_to)

    shipments = query.all()

    total_volume = sum(shipment.quantity for shipment in shipments)
    total_revenue = 0.0
    total_profit = 0.0

    for shipment in shipments:
        try:
            finance = calculate_shipment_finance(shipment.id, db)
            total_revenue += finance["revenue"]
            total_profit += finance["profit"]
        except Exception:
            continue

    avg_margin = (total_profit / total_revenue * 100) if total_revenue > 0 else 0.0

    return {
        "client_id": str(client_id),
        "period": {
            "from": date_from.isoformat() if date_from else None,
            "to": date_to.isoformat() if date_to else None
        },
        "shipments_count": len(shipments),
        "total_volume": round(total_volume, 2),
        "total_revenue": round(total_revenue, 2),
        "total_profit": round(total_profit, 2),
        "average_margin_percent": round(avg_margin, 2)
    }


@router.get("/by-supplier/{supplier_id}")
def get_supplier_report(
    supplier_id: UUID,
    date_from: Optional[date] = Query(None, description="Start date (inclusive)"),
    date_to: Optional[date] = Query(None, description="End date (inclusive)"),
    db: Session = Depends(get_db)
):
    """
    Get report by supplier: total volume, cost, etc.
    """
    query = db.query(Shipment).filter(Shipment.supplier_id == supplier_id)

    # Filter by date range if provided
    if date_from:
        query = query.filter(Shipment.created_at >= date_from)
    if date_to:
        query = query.filter(Shipment.created_at <= date_to)

    shipments = query.all()

    total_volume = sum(shipment.quantity for shipment in shipments)
    total_cost = 0.0
    total_revenue = 0.0

    for shipment in shipments:
        try:
            finance = calculate_shipment_finance(shipment.id, db)
            total_cost += finance["cost_of_goods"]
            total_revenue += finance["revenue"]
        except Exception:
            continue

    return {
        "supplier_id": str(supplier_id),
        "period": {
            "from": date_from.isoformat() if date_from else None,
            "to": date_to.isoformat() if date_to else None
        },
        "shipments_count": len(shipments),
        "total_volume": round(total_volume, 2),
        "total_cost_of_goods": round(total_cost, 2),
        "total_revenue": round(total_revenue, 2)
    }
