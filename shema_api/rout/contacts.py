"""Module providing a function printing python version."""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session
from shema_api.mod.models import Contact_mod, User_mod
from shema_api.app.schema import ContactResponse, ContactCreate, ContactUpdate
from shema_api.data.base import get_db
from shema_api.fun.dependencies import get_current_user
from shema_api.fun.crud import get_upcoming_birthdays_mod

router = APIRouter()


@router.get("/contacts", response_model=List[ContactResponse], tags=["contacts"])
def get_contacts(
    db: Session = Depends(get_db), current_user: User_mod = Depends(get_current_user)
):
    """Function get_contacts printing python version."""
    return db.query(Contact_mod).filter(Contact_mod.owner_id == current_user.id).all()


@router.post(
    "/contacts/create",
    response_model=ContactResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["contacts"],
    dependencies=[Depends(RateLimiter(times=5, seconds=60))],
)
def create_contact(
    contact: ContactCreate,
    db: Session = Depends(get_db),
    current_user: User_mod = Depends(get_current_user),
):
    """Function create_contact printing python version."""
    db_contact = Contact_mod(**contact.dict(), owner_id=current_user.id)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


@router.get(
    "/contacts/search_id/{contact_id}",
    response_model=ContactResponse,
    tags=["contacts"],
)
def get_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User_mod = Depends(get_current_user),
):
    """Function get_contact printing python version."""
    contact = (
        db.query(Contact_mod)
        .filter(Contact_mod.id == contact_id, Contact_mod.owner_id == current_user.id)
        .first()
    )
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@router.put(
    "/contacts/update/{contact_id}", response_model=ContactResponse, tags=["contacts"]
)
def update_contact(
    contact_id: int,
    contact: ContactUpdate,
    db: Session = Depends(get_db),
    current_user: User_mod = Depends(get_current_user),
):
    """Function update_contact printing python version."""
    db_contact = (
        db.query(Contact_mod)
        .filter(Contact_mod.id == contact_id, Contact_mod.owner_id == current_user.id)
        .first()
    )
    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    for key, value in contact.dict(exclude_unset=True).items():
        setattr(db_contact, key, value)
    db.commit()
    db.refresh(db_contact)
    return db_contact


@router.delete(
    "/contacts/delete/{contact_id}", response_model=ContactResponse, tags=["contacts"]
)
def delete_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User_mod = Depends(get_current_user),
):
    """Function delete_contact printing python version."""
    db_contact = (
        db.query(Contact_mod)
        .filter(Contact_mod.id == contact_id, Contact_mod.owner_id == current_user.id)
        .first()
    )
    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    db.delete(db_contact)
    db.commit()
    return db_contact


@router.get(
    "/contacts/search-first-last-email/{contact_id}",
    response_model=List[ContactResponse],
    tags=["contacts"],
)
def search_contacts(
    first_name: Optional[str] = Query(None, max_length=50),
    last_name: Optional[str] = Query(None, max_length=50),
    email: Optional[str] = Query(None, max_length=100),
    db: Session = Depends(get_db),
    current_user: User_mod = Depends(get_current_user),
):
    """Function search_contacts printing python version."""
    query = db.query(Contact_mod).filter(Contact_mod.owner_id == current_user.id)

    if first_name:
        query = query.filter(Contact_mod.first_name.ilike(f"%{first_name}%"))
    if last_name:
        query = query.filter(Contact_mod.last_name.ilike(f"%{last_name}%"))
    if email:
        query = query.filter(Contact_mod.email.ilike(f"%{email}%"))

    results = query.all()
    return results


@router.get(
    "/contacts/birthday-upcoming/{contact_id}",
    response_model=List[ContactResponse],
    tags=["contacts"],
)
def get_upcoming_birthdays(
    days: int = Query(
        7, ge=1, le=365, description="Number of days for upcoming birthdays"
    ),
    db: Session = Depends(get_db),
    current_user: User_mod = Depends(get_current_user),
):
    """Function get_upcoming_birthdays printing python version."""
    contacts = get_upcoming_birthdays_mod(db, days, current_user.id)
    if not contacts:
        raise HTTPException(
            status_code=404, detail="No contacts found with upcoming birthdays"
        )
    return contacts
