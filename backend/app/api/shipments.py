from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from app.core.database import get_db
from app.models.shipment import Shipment
from app.schemas.shipment import ShipmentCreate, ShipmentResponse, ShipmentUpdate, ShipmentWithFinance
from app.services.finance import calculate_shipment_with_finance

router = APIRouter(prefix="/shipments", tags=["shipments"])


@router.post("/", response_model=ShipmentResponse, status_code=status.HTTP_201_CREATED)
def create_shipment(shipment: ShipmentCreate, db: Session = Depends(get_db)):
    """Create a new shipment"""
    # Check if shipment_code already exists
    existing = db.query(Shipment).filter(Shipment.shipment_code == shipment.shipment_code).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Shipment code '{shipment.shipment_code}' already exists"
        )

    db_shipment = Shipment(**shipment.model_dump())
    db.add(db_shipment)
    db.commit()
    db.refresh(db_shipment)
    return db_shipment


@router.get("/", response_model=List[ShipmentResponse])
def get_shipments(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all shipments"""
    shipments = db.query(Shipment).offset(skip).limit(limit).all()
    return shipments


@router.get("/{shipment_id}", response_model=ShipmentResponse)
def get_shipment(shipment_id: UUID, db: Session = Depends(get_db)):
    """Get shipment by ID"""
    shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
    if not shipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment not found"
        )
    return shipment


@router.get("/{shipment_id}/finance", response_model=ShipmentWithFinance)
def get_shipment_finance(shipment_id: UUID, db: Session = Depends(get_db)):
    """Get shipment with financial calculations"""
    shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
    if not shipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment not found"
        )

    return calculate_shipment_with_finance(shipment, db)


@router.patch("/{shipment_id}", response_model=ShipmentResponse)
def update_shipment(
    shipment_id: UUID,
    shipment_update: ShipmentUpdate,
    db: Session = Depends(get_db)
):
    """Update shipment"""
    db_shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
    if not db_shipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment not found"
        )

    update_data = shipment_update.model_dump(exclude_unset=True)

    # Check if shipment_code is being changed and if it already exists
    if "shipment_code" in update_data:
        existing = db.query(Shipment).filter(
            Shipment.shipment_code == update_data["shipment_code"],
            Shipment.id != shipment_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Shipment code '{update_data['shipment_code']}' already exists"
            )

    for field, value in update_data.items():
        setattr(db_shipment, field, value)

    db.commit()
    db.refresh(db_shipment)
    return db_shipment


@router.delete("/{shipment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_shipment(shipment_id: UUID, db: Session = Depends(get_db)):
    """Delete shipment"""
    db_shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
    if not db_shipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment not found"
        )

    db.delete(db_shipment)
    db.commit()
    return None
