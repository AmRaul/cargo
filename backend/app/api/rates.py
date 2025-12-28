from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from app.core.database import get_db
from app.models.rate import Rate
from app.schemas.rate import RateCreate, RateResponse, RateUpdate

router = APIRouter(prefix="/rates", tags=["rates"])


@router.post("/", response_model=RateResponse, status_code=status.HTTP_201_CREATED)
def create_rate(rate: RateCreate, db: Session = Depends(get_db)):
    """Create a new rate"""
    db_rate = Rate(**rate.model_dump())
    db.add(db_rate)
    db.commit()
    db.refresh(db_rate)
    return db_rate


@router.get("/", response_model=List[RateResponse])
def get_rates(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all rates"""
    rates = db.query(Rate).offset(skip).limit(limit).all()
    return rates


@router.get("/{rate_id}", response_model=RateResponse)
def get_rate(rate_id: UUID, db: Session = Depends(get_db)):
    """Get rate by ID"""
    rate = db.query(Rate).filter(Rate.id == rate_id).first()
    if not rate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rate not found"
        )
    return rate


@router.patch("/{rate_id}", response_model=RateResponse)
def update_rate(
    rate_id: UUID,
    rate_update: RateUpdate,
    db: Session = Depends(get_db)
):
    """Update rate"""
    db_rate = db.query(Rate).filter(Rate.id == rate_id).first()
    if not db_rate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rate not found"
        )

    update_data = rate_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_rate, field, value)

    db.commit()
    db.refresh(db_rate)
    return db_rate


@router.delete("/{rate_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_rate(rate_id: UUID, db: Session = Depends(get_db)):
    """Delete rate"""
    db_rate = db.query(Rate).filter(Rate.id == rate_id).first()
    if not db_rate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rate not found"
        )

    db.delete(db_rate)
    db.commit()
    return None
