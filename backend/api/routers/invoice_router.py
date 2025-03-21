from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from backend.database import get_db
from backend.models import Invoice, Booking
from backend.schemas import InvoiceCreate, InvoiceResponse, InvoiceUpdate
from backend.auth import get_current_user

router = APIRouter(prefix="/invoices", tags=["Invoices"])


@router.post("/", response_model=InvoiceResponse,
             status_code=status.HTTP_201_CREATED)
def create_invoice(
    invoice_data: InvoiceCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),  # adjust type if needed
):
    # Check if the referenced booking exists
    booking = db.query(Booking).filter
    (Booking.id == invoice_data.booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    new_invoice = Invoice(
        booking_id=invoice_data.booking_id,
        amount_due=invoice_data.amount_due,
        status=invoice_data.status,  # will use default if not provided
    )
    db.add(new_invoice)
    db.commit()
    db.refresh(new_invoice)
    return new_invoice


@router.get("/", response_model=List[InvoiceResponse])
def list_invoices(db: Session = Depends(get_db)):
    invoices = db.query(Invoice).all()
    return invoices


@router.get("/{invoice_id}", response_model=InvoiceResponse)
def get_invoice(invoice_id: int, db: Session = Depends(get_db)):
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice


@router.put("/{invoice_id}", response_model=InvoiceResponse)
def update_invoice(
    invoice_id: int,
    invoice_data: InvoiceUpdate,
    db: Session = Depends(get_db)
):
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()

    if invoice is None:
        raise HTTPException(status_code=404, detail="Invoice not found")
    else:
        if invoice_data.status is not None:
            invoice.status = invoice_data.status   # type: ignore

        if invoice_data.amount_due is not None:
            invoice.amount_due = invoice_data.amount_due  # type: ignore

        db.commit()
        db.refresh(invoice)
        return invoice


@router.delete("/{invoice_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_invoice(invoice_id: int, db: Session = Depends(get_db)):
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    db.delete(invoice)
    db.commit()
    return {"detail": "Invoice deleted"}
