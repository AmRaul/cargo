from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from app.core.database import get_db
from app.models.expense import Expense
from app.schemas.expense import ExpenseCreate, ExpenseResponse, ExpenseUpdate

router = APIRouter(prefix="/expenses", tags=["expenses"])


@router.post("/", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    """Create a new expense"""
    db_expense = Expense(**expense.model_dump())
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense


@router.get("/", response_model=List[ExpenseResponse])
def get_expenses(
    skip: int = 0,
    limit: int = 100,
    shipment_id: UUID = None,
    db: Session = Depends(get_db)
):
    """Get all expenses, optionally filtered by shipment_id"""
    query = db.query(Expense)

    if shipment_id:
        query = query.filter(Expense.shipment_id == shipment_id)

    expenses = query.offset(skip).limit(limit).all()
    return expenses


@router.get("/{expense_id}", response_model=ExpenseResponse)
def get_expense(expense_id: UUID, db: Session = Depends(get_db)):
    """Get expense by ID"""
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )
    return expense


@router.patch("/{expense_id}", response_model=ExpenseResponse)
def update_expense(
    expense_id: UUID,
    expense_update: ExpenseUpdate,
    db: Session = Depends(get_db)
):
    """Update expense"""
    db_expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not db_expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )

    update_data = expense_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_expense, field, value)

    db.commit()
    db.refresh(db_expense)
    return db_expense


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(expense_id: UUID, db: Session = Depends(get_db)):
    """Delete expense"""
    db_expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not db_expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )

    db.delete(db_expense)
    db.commit()
    return None
